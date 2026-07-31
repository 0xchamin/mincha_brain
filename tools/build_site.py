#!/usr/bin/env python3
"""Render the brain into a static, mobile-first reading site (`site/`).

A *renderer*, not a source of truth. Every word it emits comes from a file already
in this repo - `INDEX.md`, `brain/`, `sources/*/LEARNING.md`, `reports/`. It adds
no claims, drops no citations, and is safe to delete: `rm -rf site && python3
tools/build_site.py` reproduces it exactly.

    python3 tools/build_site.py            # -> site/
    python3 tools/build_site.py --serve    # build, then serve on :8000

Needs `markdown` + `pillow` (both in requirements.txt). Mermaid is vendored on
first run into tools/site_assets/vendor/ (git-ignored); without network the
diagrams degrade to their source text and everything else still builds.
"""

from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import shutil
import sys
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ASSETS = REPO / "tools" / "site_assets"
VENDOR = ASSETS / "vendor"
OUT = REPO / "site"

GITHUB_BLOB = "https://github.com/0xchamin/mincha_brain/blob/main/"
MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"}

# ---------------------------------------------------------------- markdown ---

try:
    import markdown as _markdown
except ImportError:  # pragma: no cover - guidance beats a traceback
    sys.exit("missing dependency: pip install markdown  (see requirements.txt)")


def md_to_html(text: str) -> str:
    return _markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "attr_list", "sane_lists", "md_in_html"],
        output_format="html5",
    )


# ------------------------------------------------------------ md utilities ---


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sections(md: str, level: int = 2) -> dict[str, str]:
    """Split markdown on `## ` headings -> {heading_text: body}. Preserves order."""
    marker = "#" * level + " "
    out: dict[str, str] = {}
    current, buf = None, []
    in_fence = False
    for line in md.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith(marker):
            if current is not None:
                out[current] = "\n".join(buf).strip()
            current, buf = line[len(marker):].strip(), []
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf).strip()
    return out


def section(md: str, *names: str) -> str:
    """First matching `## ` section body, matched case-insensitively by prefix."""
    secs = sections(md)
    for want in names:
        for head, body in secs.items():
            if head.lower().startswith(want.lower()):
                return body
    return ""


def split_preamble(md: str) -> tuple[str, str]:
    """Everything between the H1 and the first `## ` heading, and the rest.

    That preamble is written *to the agent* - persona lines, "merge and de-duplicate
    as they arrive", file conventions. On a phone it buries the TL;DR under kit
    boilerplate. It is not all noise though: some notes hide real trust caveats
    there, so it gets collapsed rather than dropped.
    """
    lines = md.splitlines()
    start, in_fence = 0, False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            in_fence = not in_fence
        if line.startswith("# ") and not in_fence:
            start = i + 1
            break
    for j in range(start, len(lines)):
        if lines[j].startswith("```"):
            in_fence = not in_fence
        if lines[j].startswith("## ") and not in_fence:
            return "\n".join(lines[start:j]).strip(), "\n".join(lines[j:])
    return "", md


def title_of(md: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def link_target(cell: str) -> str:
    """`[`brain/topics/agents.md`](brain/topics/agents.md)` -> `brain/topics/agents.md`."""
    m = re.search(r"\]\(([^)]+)\)", cell)
    return m.group(1).strip().strip("`") if m else ""


def facts_table(md: str) -> dict[str, str]:
    """Parse a `| Field | Value |` two-column table into a dict."""
    out: dict[str, str] = {}
    for line in md.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 2 or set(cells[0]) <= set("-: "):
            continue
        if cells[0].lower() in ("field", "term"):
            continue
        out[cells[0]] = cells[1]
    return out


def table_rows(md: str, ncols: int) -> list[list[str]]:
    """Every `|`-delimited body row with exactly `ncols` cells (header + rule dropped)."""
    rows: list[list[str]] = []
    seen_rule = False
    for line in md.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != ncols:
            continue
        if all(set(c) <= set("-: ") and c for c in cells):
            seen_rule = True
            continue
        if not seen_rule:
            continue
        rows.append(cells)
    return rows


def strip_md(text: str) -> str:
    """Markdown -> rough plain text, for search snippets and meta descriptions."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_>#|]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def first_paragraph(md: str) -> str:
    for block in re.split(r"\n\s*\n", md.strip()):
        block = block.strip()
        if block and not block.startswith((">", "|", "#", "!")):
            return block
    return ""


# ---------------------------------------------------------------- the model ---


@dataclass
class Page:
    """One rendered page. `path` is site-relative, e.g. `topics/agents.html`."""

    path: str
    title: str
    kind: str
    body_md: str
    src_dir: Path
    subtitle: str = ""
    meta: list[tuple[str, str]] = field(default_factory=list)
    video: str = ""
    search_text: str = ""


def youtube_id(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})", url or "")
    return m.group(1) if m else ""


def collect() -> tuple[list[Page], list[dict], list[dict], list[dict]]:
    pages: list[Page] = []
    topics: list[dict] = []
    sources: list[dict] = []
    claims: list[dict] = []

    # --- topics -------------------------------------------------------------
    index_md = read(REPO / "INDEX.md")
    # INDEX Topics table: Topic | Status | What it covers | Sources feeding it | Note
    topic_rows = {
        Path(link_target(r[4])).stem: r
        for r in table_rows(section(index_md, "Topics"), 5)
        if link_target(r[4])
    }
    for path in sorted((REPO / "brain" / "topics").glob("*.md")):
        md = read(path)
        slug = path.stem
        status = ""
        m = re.search(r"\*\*Status:\*\*\s*(.+)", md)
        if m:
            status = m.group(1).strip()
        row = topic_rows.get(slug)
        topics.append(
            {
                "slug": slug,
                "title": title_of(md).replace("Topic: ", ""),
                "status": re.sub(r"\s*\(.*", "", status).strip("* "),
                "status_full": status,
                "covers": strip_md(section(md, "What this covers")),
                "nsources": (row[3] if row else "0"),
                "url": f"topics/{slug}.html",
            }
        )
        pages.append(
            Page(
                path=f"topics/{slug}.html",
                title=title_of(md) or slug,
                kind="topic",
                body_md=md,
                src_dir=path.parent,
                subtitle=status,
            )
        )

    # --- sources ------------------------------------------------------------
    index_rows = {
        link_target(r[5]).split("/")[1]: r
        for r in table_rows(section(index_md, "Sources"), 6)
        if link_target(r[5]).startswith("sources/")
    }
    for d in sorted((REPO / "sources").iterdir()):
        learning = d / "LEARNING.md"
        if d.name.startswith("_") or not learning.is_file():
            continue
        md = read(learning)
        facts = facts_table(read(d / "SOURCE.md")) if (d / "SOURCE.md").is_file() else {}
        row = index_rows.get(d.name)
        vid = youtube_id(facts.get("URL", ""))
        sources.append(
            {
                "id": d.name,
                "title": facts.get("Title") or title_of(md).replace("Learning - ", ""),
                "type": facts.get("Type", ""),
                "author": facts.get("Author / channel", ""),
                "published": facts.get("Published", ""),
                "topics": [t.strip() for t in facts.get("Topics", "").split(",") if t.strip()],
                "url": f"sources/{d.name}.html",
                "external": facts.get("URL", ""),
                "tldr": section(md, "TL;DR"),
                "key_claims": section(md, "Key claims"),
                "when": strip_md(row[4]) if row else "",
                "summary": strip_md(row[2]) if row else "",
            }
        )
        pages.append(
            Page(
                path=f"sources/{d.name}.html",
                title=facts.get("Title") or title_of(md),
                kind="source",
                body_md=md,
                src_dir=d,
                subtitle=facts.get("Author / channel", ""),
                meta=[
                    (k, facts[k])
                    for k in ("Type", "Published", "Topics", "Visual leg", "Status")
                    if facts.get(k)
                ],
                video=vid,
            )
        )

    # --- claims -------------------------------------------------------------
    claims_md = read(REPO / "brain" / "claims.md")
    for r in table_rows(claims_md, 5):
        if not r[0].strip("* ").isdigit():
            continue
        conf = strip_md(r[4]).lower()
        claims.append(
            {
                "n": int(r[0].strip("* ")),
                "claim": r[1],
                "topic": strip_md(r[2]),
                "sources": r[3],
                "confidence": conf,
                "tier": (
                    "corroborated"
                    if "corroborated" in conf
                    else "needs-check"
                    if "needs-check" in conf or "open" in conf
                    else "emerging"
                ),
            }
        )

    # --- standalone brain pages --------------------------------------------
    for rel, kind in (
        ("brain/glossary.md", "glossary"),
        ("brain/log.md", "log"),
    ):
        p = REPO / rel
        if p.is_file():
            md = read(p)
            pages.append(
                Page(
                    path=Path(rel).stem + ".html",
                    title=title_of(md) or p.stem,
                    kind=kind,
                    body_md=md,
                    src_dir=p.parent,
                )
            )

    for sub, kind in (("decisions", "decision"), ("dreams", "dream")):
        for p in sorted((REPO / "brain" / sub).glob("*.md")):
            if p.stem in ("0000-template", "README"):
                continue
            md = read(p)
            pages.append(
                Page(
                    path=f"{sub}/{p.stem}.html",
                    title=title_of(md) or p.stem,
                    kind=kind,
                    body_md=md,
                    src_dir=p.parent,
                )
            )

    for p in sorted((REPO / "reports").glob("*.md")):
        if p.stem == "README":
            continue
        md = read(p)
        pages.append(
            Page(
                path=f"reports/{p.stem}.html",
                title=title_of(md) or p.stem,
                kind="report",
                body_md=md,
                src_dir=p.parent,
            )
        )

    return pages, topics, sources, claims


# ------------------------------------------------------------ link rewriting ---


def build_routes(pages: list[Page]) -> dict[str, str]:
    """repo-relative markdown path -> site-relative html path."""
    routes = {
        "INDEX.md": "index.html",
        "brain/index.md": "index.html",
        "brain/claims.md": "claims.html",
    }
    for pg in pages:
        rel = pg.src_dir.relative_to(REPO).as_posix()
        if pg.kind == "source":
            routes[f"{rel}/LEARNING.md"] = pg.path
            routes[rel] = pg.path
            routes[f"{rel}/"] = pg.path
        else:
            stem = Path(pg.path).stem
            routes[f"{rel}/{stem}.md"] = pg.path
    return routes


class Rewriter:
    """Retargets in-repo links: kit pages -> site pages, images -> copied media,
    everything else (nodes.md, SOURCE.md, context/) -> the GitHub blob."""

    def __init__(self, routes: dict[str, str]) -> None:
        self.routes = routes
        self.media: dict[Path, str] = {}

    def _media(self, abs_path: Path) -> str:
        if abs_path not in self.media:
            rel = abs_path.relative_to(REPO)
            dest = "media/" + rel.as_posix().replace("sources/", "").replace("/visuals", "")
            self.media[abs_path] = dest
        return self.media[abs_path]

    def target(self, href: str, src_dir: Path, out_dir: str) -> tuple[str, bool]:
        """-> (new href, is_external)."""
        if re.match(r"^(https?:|mailto:|#|data:)", href):
            return href, href.startswith("http")
        path, _, frag = href.partition("#")
        if not path:
            return href, False
        try:
            abs_path = (src_dir / path).resolve()
            rel = abs_path.relative_to(REPO).as_posix()
        except (ValueError, OSError):
            return href, True

        if abs_path.suffix.lower() in IMAGE_EXT and abs_path.is_file():
            dest = self._media(abs_path)
        elif rel in self.routes:
            dest = self.routes[rel]
        elif rel.rstrip("/") in self.routes:
            dest = self.routes[rel.rstrip("/")]
        else:
            return GITHUB_BLOB + rel + (("#" + frag) if frag else ""), True

        out = posixpath.relpath(dest, out_dir or ".")
        return out + (("#" + frag) if frag else ""), False

    def apply(self, html: str, src_dir: Path, out_path: str) -> str:
        out_dir = posixpath.dirname(out_path)

        def sub(m: re.Match[str]) -> str:
            attr, raw = m.group(1), m.group(2)
            href, external = self.target(raw.replace("&amp;", "&"), src_dir, out_dir)
            href = href.replace("&", "&amp;")
            if attr == "href" and external and href.startswith("http"):
                return f'href="{href}" target="_blank" rel="noopener"'
            if attr == "src":
                return f'src="{href}" loading="lazy" decoding="async"'
            return f'{attr}="{href}"'

        return re.sub(r'(href|src)="([^"]*)"', sub, html)


def copy_media(rewriter: Rewriter) -> int:
    for abs_path, dest in rewriter.media.items():
        target = OUT / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(abs_path, target)
    return len(rewriter.media)


# ------------------------------------------------ post-render html polishing ---

MERMAID_BLOCK = re.compile(
    r'<pre><code class="language-mermaid">(.*?)</code></pre>', re.S
)


def mermaidify(html: str) -> tuple[str, bool]:
    found = bool(MERMAID_BLOCK.search(html))
    html = MERMAID_BLOCK.sub(
        lambda m: f'<pre class="mermaid">{m.group(1)}</pre>', html
    )
    return html, found


TS = re.compile(r"<code>&amp;t=(\d+)s?</code>")
TS_PAIR = re.compile(r"<code>([A-Za-z0-9_-]{11})</code>\s*<code>&amp;t=(\d+)s?</code>")


def linkify_timestamps(html: str, default_video: str) -> str:
    """`&t=616s` citations become tappable YouTube deep links - the single biggest
    quality-of-life win on a phone, where you cannot paste a timestamp by hand."""
    html = TS_PAIR.sub(
        lambda m: f'<a class="ts" href="https://youtu.be/{m.group(1)}?t={m.group(2)}"'
        f' target="_blank" rel="noopener"><code>&amp;t={m.group(2)}s</code></a>',
        html,
    )
    if default_video:
        html = TS.sub(
            lambda m: f'<a class="ts" href="https://youtu.be/{default_video}?t={m.group(1)}"'
            f' target="_blank" rel="noopener"><code>&amp;t={m.group(1)}s</code></a>',
            html,
        )
    return html


def wrap_tables(html: str) -> str:
    """Tables must scroll inside their own box, never the page body."""
    return html.replace("<table>", '<div class="scroll"><table>').replace(
        "</table>", "</table></div>"
    )


def add_heading_ids(html: str) -> tuple[str, list[tuple[int, str, str]]]:
    toc: list[tuple[int, str, str]] = []
    used: set[str] = set()

    def sub(m: re.Match[str]) -> str:
        lvl, inner = int(m.group(1)), m.group(2)
        text = strip_md(re.sub(r"<[^>]+>", "", inner))
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "s"
        n, base = 2, slug
        while slug in used:
            slug, n = f"{base}-{n}", n + 1
        used.add(slug)
        if 2 <= lvl <= 3:
            toc.append((lvl, slug, text))
        return f'<h{lvl} id="{slug}">{inner}<a class="anchor" href="#{slug}">#</a></h{lvl}>'

    html = re.sub(r"<h([1-6])>(.*?)</h\1>", sub, html, flags=re.S)
    return html, toc


def figure_captions(html: str) -> str:
    """`![alt](visuals/x.jpg)` carries the frame's meaning in its alt text - show it."""

    def sub(m: re.Match[str]) -> str:
        tag, alt = m.group(0), m.group(1)
        if not alt.strip():
            return tag
        return f'<figure>{tag}<figcaption>{alt}</figcaption></figure>'

    return re.sub(r'<img alt="([^"]*)"[^>]*>', sub, html)


# ------------------------------------------------------------------ templates ---


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


def shell(
    *,
    path: str,
    title: str,
    body: str,
    description: str = "",
    mermaid: bool = False,
    active: str = "",
) -> str:
    depth = path.count("/")
    base = "../" * depth or "./"
    nav = [
        ("lessons", "index.html", "Lessons", "M4 5h16M4 12h16M4 19h10"),
        ("topics", "topics.html", "Topics", "M4 6h7v7H4zM13 6h7v4h-7zM13 13h7v5h-7zM4 15h7v3H4z"),
        ("sources", "sources.html", "Sources", "M5 4h11l3 3v13H5zM8 9h8M8 13h8M8 17h5"),
        ("claims", "claims.html", "Claims", "M5 12l4 4 10-10"),
        ("search", "search.html", "Search", "M11 4a7 7 0 100 14 7 7 0 000-14zM20 20l-4-4"),
    ]
    tabs = "".join(
        f'<a class="tab{" on" if key == active else ""}" href="{base}{href}">'
        f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{d}"/></svg>'
        f"<span>{label}</span></a>"
        for key, href, label, d in nav
    )
    up = f'<a class="up" href="{base}index.html" aria-label="Home">' if depth else "<span class='up'>"
    up_close = "</a>" if depth else "</span>"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{esc(description[:180])}">
<meta name="theme-color" content="#0f1115" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#fbfbfa" media="(prefers-color-scheme: light)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Brain">
<title>{esc(title)}</title>
<link rel="manifest" href="{base}manifest.webmanifest">
<link rel="icon" href="{base}assets/icon-192.png">
<link rel="apple-touch-icon" href="{base}assets/icon-192.png">
<link rel="stylesheet" href="{base}assets/style.css">
<script>window.SITE_BASE="{base}";window.HAS_MERMAID={str(mermaid).lower()};
(function(){{try{{var t=localStorage.getItem("brain-theme");if(t)document.documentElement.dataset.theme=t;}}catch(e){{}}}})();</script>
</head>
<body>
<header class="bar">
  {up}<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>{up_close}
  <span class="bar-title">{esc(title)}</span>
  <button class="icon" id="theme" aria-label="Toggle theme">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14a8 8 0 01-10-10 8 8 0 1010 10z"/></svg>
  </button>
</header>
<div class="progress"><i></i></div>
<main>{body}</main>
<nav class="tabs">{tabs}</nav>
<script src="{base}assets/app.js" defer></script>
</body>
</html>
"""


def pill(text: str, kind: str = "") -> str:
    cls = re.sub(r"[^a-z0-9]+", "-", (kind or text).lower()).strip("-")
    return f'<span class="pill {cls}">{esc(text)}</span>'


# --------------------------------------------------------------- page builders ---


def render_page(pg: Page, rw: Rewriter) -> tuple[str, str]:
    """-> (html document, plain-text search body)."""
    preamble_md, body_md = split_preamble(pg.body_md)
    html = md_to_html(body_md)
    html = rw.apply(html, pg.src_dir, pg.path)
    html, has_mermaid = mermaidify(html)
    html = linkify_timestamps(html, pg.video)
    html = figure_captions(html)
    html = wrap_tables(html)
    html, toc = add_heading_ids(html)
    # The document's own H1 duplicates the top bar; the bar is always visible.
    html = re.sub(r"<h1[^>]*>.*?</h1>", "", html, count=1, flags=re.S)

    pre_html = ""
    if strip_md(preamble_md):
        inner = linkify_timestamps(
            rw.apply(md_to_html(preamble_md), pg.src_dir, pg.path), pg.video
        )
        pre_html = (
            f'<details class="frontmatter"><summary>About this note</summary>'
            f"{wrap_tables(inner)}</details>"
        )

    head = ""
    if pg.meta:
        head = '<div class="facts">' + "".join(
            f"<div><dt>{esc(k)}</dt><dd>{md_to_html(v)[3:-4]}</dd></div>" for k, v in pg.meta
        ) + "</div>"
        head = rw.apply(head, pg.src_dir, pg.path)

    toc_html = ""
    if len([t for t in toc if t[0] == 2]) >= 3:
        items = "".join(
            f'<a class="l{lvl}" href="#{slug}">{esc(text)}</a>' for lvl, slug, text in toc
        )
        toc_html = f'<details class="toc"><summary>On this page</summary>{items}</details>'

    body = f'<article class="doc"><p class="kicker">{esc(pg.kind)}</p><h1>{esc(pg.title)}</h1>'
    if pg.subtitle:
        body += f'<p class="sub">{md_to_html(pg.subtitle)[3:-4]}</p>'
    body += head + pre_html + toc_html + html + "</article>"
    return (
        shell(
            path=pg.path,
            title=pg.title,
            body=body,
            description=strip_md(pg.body_md)[:180],
            mermaid=has_mermaid,
            active={"topic": "topics", "source": "sources"}.get(pg.kind, ""),
        ),
        # Preamble excluded: it is kit boilerplate and would drown real snippets.
        strip_md(body_md),
    )


def render_home(topics: list[dict], sources: list[dict], claims: list[dict], rw: Rewriter) -> str:
    corr = sum(1 for c in claims if c["tier"] == "corroborated")
    stats = "".join(
        f'<div class="stat"><b>{v}</b><span>{k}</span></div>'
        for k, v in (
            ("sources", len(sources)),
            ("topics", len(topics)),
            ("claims", len(claims)),
            ("corroborated", corr),
        )
    )

    # Meta lessons: the compounding layer.
    tcards = ""
    for t in sorted(topics, key=lambda t: ({"established": 0, "emerging": 1}.get(t["status"], 2), t["title"])):
        n = t["nsources"] or "0"
        tcards += (
            f'<a class="card" href="{t["url"]}"><div class="card-head"><h3>{esc(t["title"])}</h3>'
            f'{pill(t["status"] or "seed")}</div>'
            f'<p>{esc(t["covers"][:210])}{"..." if len(t["covers"]) > 210 else ""}</p>'
            f'<span class="meta">{esc(n)} source{"" if n == "1" else "s"}</span></a>'
        )

    # Source lessons: TL;DR + key claims, lifted verbatim from each LEARNING.md.
    scards = ""
    for s in sources:
        tldr = rw.apply(md_to_html(s["tldr"]), REPO / "sources" / s["id"], "index.html")
        tldr = linkify_timestamps(tldr, youtube_id(s["external"]))
        claims_html = rw.apply(md_to_html(s["key_claims"]), REPO / "sources" / s["id"], "index.html")
        claims_html = linkify_timestamps(claims_html, youtube_id(s["external"]))
        topics_html = "".join(pill(t, "topic-tag") for t in s["topics"])
        scards += f"""<article class="lesson">
  <div class="card-head"><h3><a href="{s["url"]}">{esc(s["title"])}</a></h3>{pill(s["type"] or "note", "type")}</div>
  <p class="byline">{esc(s["author"])}</p>
  <div class="tldr">{tldr}</div>
  <details class="claims"><summary>Key claims</summary>{claims_html}</details>
  <div class="tags">{topics_html}</div>
  <p class="when"><b>When to read:</b> {esc(s["when"])}</p>
  <a class="go" href="{s["url"]}">Read the full note &rarr;</a>
</article>"""

    body = f"""<article class="doc home">
<p class="kicker">compounding notes</p>
<h1>Brain</h1>
<p class="sub">Lessons distilled from every source, and the meta lessons they compound into.</p>
<div class="stats">{stats}</div>

<h2 id="meta">Meta lessons <span class="hint">what the brain believes across sources</span></h2>
<div class="grid">{tcards}</div>

<h2 id="source-lessons">Source lessons <span class="hint">TL;DR + key claims, per source</span></h2>
{scards}
</article>"""
    return shell(
        path="index.html",
        title="Brain",
        body=body,
        description="Lessons from every ingested source, and the topic syntheses they compound into.",
        active="lessons",
    )


def render_topics(topics: list[dict]) -> str:
    rows = ""
    for t in sorted(topics, key=lambda t: ({"established": 0, "emerging": 1}.get(t["status"], 2), t["title"])):
        rows += (
            f'<a class="row" href="{t["url"]}"><div class="row-main"><h3>{esc(t["title"])}</h3>'
            f'<p>{esc(t["covers"][:180])}</p></div>'
            f'<div class="row-side">{pill(t["status"] or "seed")}'
            f'<span class="meta">{esc(t["nsources"] or "0")} src</span></div></a>'
        )
    return shell(
        path="topics.html",
        title="Topics",
        body=f'<article class="doc"><p class="kicker">meta lessons</p><h1>Topics</h1>'
        f'<p class="sub">Living cross-source syntheses. Status advances seed &rarr; emerging &rarr; established.</p>'
        f'<div class="rows">{rows}</div></article>',
        description="Cross-source topic syntheses.",
        active="topics",
    )


def render_sources(sources: list[dict]) -> str:
    rows = ""
    for s in sources:
        rows += (
            f'<a class="row" href="{s["url"]}"><div class="row-main"><h3>{esc(s["title"])}</h3>'
            f'<p>{esc(s["summary"][:200])}</p>'
            f'<span class="meta">{esc(s["author"])}</span></div>'
            f'<div class="row-side">{pill(s["type"] or "note", "type")}</div></a>'
        )
    return shell(
        path="sources.html",
        title="Sources",
        body=f'<article class="doc"><p class="kicker">{len(sources)} ingested</p><h1>Sources</h1>'
        f'<p class="sub">Every source distilled into a cited learning note.</p>'
        f'<div class="rows">{rows}</div></article>',
        description="Every ingested source.",
        active="sources",
    )


def render_claims(claims: list[dict], rw: Rewriter) -> str:
    """A five-column table is unreadable on a phone - render each claim as a card."""
    cards = ""
    for c in claims:
        text = rw.apply(md_to_html(c["claim"]), REPO / "brain", "claims.html")
        srcs = rw.apply(md_to_html(c["sources"]), REPO / "brain", "claims.html")
        srcs = linkify_timestamps(srcs, "")
        cards += (
            f'<article class="claim {c["tier"]}" data-topic="{esc(c["topic"])}" data-tier="{c["tier"]}">'
            f'<div class="claim-head"><span class="n">{c["n"]}</span>'
            f'{pill(c["topic"], "topic-tag")}{pill(c["tier"])}</div>'
            f'<div class="claim-body">{text}</div>'
            f'<details><summary>Sources</summary>{srcs}</details></article>'
        )
    topics = sorted({c["topic"] for c in claims})
    chips = '<button class="chip on" data-filter="*">all</button>' + "".join(
        f'<button class="chip" data-filter="{esc(t)}">{esc(t)}</button>' for t in topics
    )
    return shell(
        path="claims.html",
        title="Claims",
        body=f'<article class="doc"><p class="kicker">{len(claims)} promoted</p><h1>Claims</h1>'
        f'<p class="sub">Durable claims promoted from source notes. Every one carries a citation.</p>'
        f'<div class="chips" id="claim-filter">{chips}</div>{cards}</article>',
        description="Cross-source corroborated claims.",
        active="claims",
    )


def render_search() -> str:
    return shell(
        path="search.html",
        title="Search",
        body='<article class="doc"><h1>Search</h1>'
        '<input id="q" type="search" placeholder="Search lessons, claims, terms..." '
        'autocomplete="off" autocapitalize="none" spellcheck="false">'
        '<p class="sub" id="q-status">Type to search the whole brain. Works offline.</p>'
        '<div id="results" class="rows"></div></article>',
        description="Search the brain.",
        active="search",
    )


# ------------------------------------------------------------------- assets ---


def icon(size: int, dest: Path) -> None:
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (size, size), "#0f1115")
    d = ImageDraw.Draw(img)
    u = size / 16
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(u * 3.6), fill="#0f1115")
    # Three stacked layers narrowing upward: raw -> distilled -> promoted.
    for i, (w, y, col) in enumerate(
        ((10, 10.6, "#3d4a63"), (7.6, 8.0, "#5b7cc4"), (5.2, 5.4, "#e8c37a"))
    ):
        d.rounded_rectangle(
            [u * (8 - w / 2), u * y, u * (8 + w / 2), u * (y + 1.5)],
            radius=int(u * 0.45),
            fill=col,
        )
    d.ellipse([u * 6.4, u * 2.0, u * 9.6, u * 5.2], fill="#e8c37a")
    d.ellipse([u * 7.15, u * 2.75, u * 8.85, u * 4.45], fill="#0f1115")
    img.save(dest, "PNG", optimize=True)


def vendor_mermaid() -> bool:
    VENDOR.mkdir(parents=True, exist_ok=True)
    local = VENDOR / "mermaid.min.js"
    if not local.is_file():
        try:
            print("  fetching mermaid...", end=" ", flush=True)
            with urllib.request.urlopen(MERMAID_URL, timeout=60) as r:  # noqa: S310 - pinned CDN
                local.write_bytes(r.read())
            print("ok")
        except Exception as e:  # noqa: BLE001 - offline builds must still succeed
            print(f"skipped ({e}); diagrams will render as source text")
            return False
    shutil.copy2(local, OUT / "assets" / "mermaid.min.js")
    return True


# --------------------------------------------------------------------- build ---


def build() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)

    pages, topics, sources, claims = collect()
    rw = Rewriter(build_routes(pages))
    search: list[dict] = []

    for pg in pages:
        html, text = render_page(pg, rw)
        dest = OUT / pg.path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        search.append({"t": pg.title, "u": pg.path, "k": pg.kind, "x": text[:6000]})

    (OUT / "index.html").write_text(render_home(topics, sources, claims, rw), encoding="utf-8")
    (OUT / "topics.html").write_text(render_topics(topics), encoding="utf-8")
    (OUT / "sources.html").write_text(render_sources(sources), encoding="utf-8")
    (OUT / "claims.html").write_text(render_claims(claims, rw), encoding="utf-8")
    (OUT / "search.html").write_text(render_search(), encoding="utf-8")

    for c in claims:
        search.append(
            {"t": f"Claim {c['n']}", "u": f"claims.html#c{c['n']}", "k": "claim", "x": strip_md(c["claim"])}
        )
    (OUT / "search.json").write_text(json.dumps(search, separators=(",", ":")), encoding="utf-8")

    n_media = copy_media(rw)
    for name in ("style.css", "app.js"):
        shutil.copy2(ASSETS / name, OUT / "assets" / name)
    icon(192, OUT / "assets" / "icon-192.png")
    icon(512, OUT / "assets" / "icon-512.png")
    has_mermaid = vendor_mermaid()

    (OUT / "manifest.webmanifest").write_text(
        json.dumps(
            {
                "name": "Brain - compounding notes",
                "short_name": "Brain",
                "start_url": "./index.html",
                "scope": "./",
                "display": "standalone",
                "background_color": "#0f1115",
                "theme_color": "#0f1115",
                "icons": [
                    {"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
                    {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    precache = sorted(
        p.relative_to(OUT).as_posix()
        for p in OUT.rglob("*")
        if p.is_file() and p.suffix in {".html", ".css", ".js", ".json", ".webmanifest"}
        and p.name != "mermaid.min.js"
    )
    sw = read(ASSETS / "sw.js")
    revision = str(sum(p.stat().st_mtime_ns for p in OUT.rglob("*") if p.is_file()) % 10**12)
    sw = sw.replace("__PRECACHE__", json.dumps(precache)).replace("__REV__", revision)
    (OUT / "sw.js").write_text(sw, encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    print(
        f"site/ built: {len(pages) + 5} pages, {len(sources)} sources, {len(topics)} topics, "
        f"{len(claims)} claims, {n_media} images, mermaid={'yes' if has_mermaid else 'no'}"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--serve", action="store_true", help="serve site/ on :8000 after building")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    build()
    if args.serve:
        import http.server
        import socketserver

        os.chdir(OUT)
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", args.port), handler) as httpd:
            print(f"serving http://localhost:{args.port}  (ctrl-c to stop)")
            httpd.serve_forever()


if __name__ == "__main__":
    main()
