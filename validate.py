#!/usr/bin/env python3
"""
validate.py - the type checker for a prose contract.

Brain is a convention, not an application: the pipeline, the corroboration gate and the
file schema all live as English in AGENTS.md, and the agent is the runtime. That works,
but prose has no compiler - nothing catches a stale INDEX row, an uncited frame, or a
log entry filed out of order. This script is that missing gate.

It enforces only what AGENTS.md already requires. If a check here and AGENTS.md ever
disagree, AGENTS.md wins and this file is the bug.

Usage:
    python3 validate.py            # report, exit 1 on any error
    python3 validate.py --strict   # warnings are errors too

Stdlib only, on purpose: CI must not need a venv to check a folder of Markdown.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SOURCE_STATUSES = {
    "capture", "understand", "researched", "distill",
    "awaiting-promotion", "compounded", "blocked", "partial",
}
TOPIC_STATUSES = {"seed", "emerging", "established"}
VISUAL_LEG_PREFIXES = ("analysed", "skipped", "n/a")


@dataclass
class Finding:
    level: str      # "error" | "warn"
    path: Path
    line: int       # 0 = whole file
    message: str

    def __str__(self) -> str:
        loc = f"{self.path.relative_to(ROOT)}"
        if self.line:
            loc += f":{self.line}"
        return f"  {loc}: {self.message}"


findings: list[Finding] = []


def err(path: Path, line: int, message: str) -> None:
    findings.append(Finding("error", path, line, message))


def warn(path: Path, line: int, message: str) -> None:
    findings.append(Finding("warn", path, line, message))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def source_dirs() -> list[Path]:
    return sorted(
        d for d in (ROOT / "sources").iterdir()
        if d.is_dir() and d.name != "_TEMPLATE"
    )


def topic_files() -> list[Path]:
    return sorted((ROOT / "brain" / "topics").glob("*.md"))


def markdown_files() -> list[Path]:
    """All Markdown in the kit, excluding symlinks.

    CLAUDE.md and .github/copilot-instructions.md are git-ignored symlinks to AGENTS.md
    (one canonical contract, see AGENTS.md Appendix). Following them would double-report
    every finding, and would falsely flag AGENTS.md's root-relative links as broken when
    resolved from .github/.

    BUILD.md is excluded for the same reason one level up: it is a *generated bundle*
    (tools/make_build_doc.py) that embeds those files verbatim, so checking it re-checks
    content already checked at its source, and reports false positives because embedded
    relative links resolve from the wrong directory - personas/README.md's `](architect.md)`
    would resolve to <root>/architect.md. Regenerate it rather than lint it; the generator
    fails loudly if a source file is missing, and `--check` catches staleness.

    staging/ and site/ are excluded for a third reason: they are git-ignored and hold material
    the kit has not adopted. AGENTS.md is explicit that "material becomes part of the kit when
    it is filed, not when it is copied in" - so linting the inbox inverts that rule and turns
    the build red for the crime of having received something. This was not theoretical: six
    staged research modules produced 1,485 style errors on 2026-08-03, not one of them about a
    kit file. site/ is generated, disposable output, checked at its source like BUILD.md.
    raw/ and repo/ are the same class one level down, inside a source.
    """
    skip = {".git", ".venv", "__pycache__", "node_modules",
            "raw", "repo", "staging", "site"}
    return sorted(
        p for p in ROOT.rglob("*.md")
        if not any(part in skip for part in p.parts)
        and not p.is_symlink()
        and p != ROOT / "BUILD.md"
    )


def field(text: str, name: str) -> str | None:
    """Pull `| Field | value |` out of a SOURCE.md-style table."""
    m = re.search(rf"^\|\s*{re.escape(name)}\s*\|(.+?)\|\s*$", text, re.M)
    return m.group(1).strip() if m else None


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check_index_integrity() -> None:
    """AGENTS.md: every source folder <-> exactly one INDEX row; same for topics.

    A source on disk but not in INDEX.md is unfindable - the failure this rule exists
    to prevent.
    """
    index = ROOT / "INDEX.md"
    if not index.exists():
        err(index, 0, "INDEX.md is missing - it is the brain's entry point")
        return
    text = read(index)

    # Count table ROWS, not raw occurrences: one row legitimately mentions a path twice,
    # once as link text and once as the href.
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("|")]

    for d in source_dirs():
        n = sum(1 for ln in rows if re.search(rf"sources/{re.escape(d.name)}\b", ln))
        if n == 0:
            err(index, 0, f"source '{d.name}' has no INDEX row (unfindable)")
        elif n > 1:
            warn(index, 0, f"source '{d.name}' appears in {n} rows - expected exactly one")

    for t in topic_files():
        n = sum(1 for ln in rows if re.search(rf"brain/topics/{re.escape(t.name)}\b", ln))
        if n == 0:
            err(index, 0, f"topic '{t.name}' has no INDEX row (unfindable)")
        elif n > 1:
            warn(index, 0, f"topic '{t.name}' appears in {n} rows - expected exactly one")

    # And the reverse: INDEX must not point at folders that no longer exist.
    for m in re.finditer(r"sources/([0-9]{6}_[a-z0-9-]+)", text):
        if not (ROOT / "sources" / m.group(1)).is_dir():
            err(index, text[:m.start()].count("\n") + 1,
                f"INDEX row points to missing source folder '{m.group(1)}'")


def check_source_metadata() -> None:
    """Every SOURCE.md carries a legal Status, a Visual leg, and an Owner."""
    for d in source_dirs():
        sf = d / "SOURCE.md"
        if not sf.exists():
            err(d, 0, "missing SOURCE.md")
            continue
        text = read(sf)

        status = field(text, "Status")
        if status is None:
            err(sf, 0, "no Status field")
        else:
            first = status.split("(")[0].strip().split()[0] if status.split() else ""
            if first not in SOURCE_STATUSES:
                err(sf, 0, f"Status '{status}' is not one of {sorted(SOURCE_STATUSES)}")

        vleg = field(text, "Visual leg")
        if vleg is None:
            warn(sf, 0, "no 'Visual leg' field (ADR-0003) - was the visual leg analysed or skipped?")
        elif not vleg.lower().startswith(VISUAL_LEG_PREFIXES):
            err(sf, 0, f"Visual leg '{vleg}' must start with one of {VISUAL_LEG_PREFIXES}")

        if not field(text, "Owner"):
            warn(sf, 0, "no Owner field")

        # Topics named here must exist as topic notes.
        topics = field(text, "Topics") or ""
        for raw in (t.strip() for t in topics.split(",")):
            if not raw or raw.lower() in {"n/a", "-", ""}:
                continue
            slug = raw.lower().replace(" ", "-")
            if not (ROOT / "brain" / "topics" / f"{slug}.md").exists():
                err(sf, 0, f"Topics names '{raw}' but brain/topics/{slug}.md does not exist")


def check_frames_are_cited() -> None:
    """AGENTS.md: a kept frame must be cited by its own source's LEARNING.md.

    Signal, not archive - and the bar is *taught*, not merely *gated*. This check used to
    accept a citation from nodes.md or a topic note, and the 2026-08-02 retrofit programme
    found **16 frames across four sources** that were extracted, deduped, viewed, gated and
    kept, and that no reader ever saw, because the prose never used them - among them an
    opening hook, two core evidence slides, and the frame memory.md calls the best single
    visual on its topic. A frame only a nodes.md row cites is an archive entry.

    Cheap to check and it caught a class no human noticed across eleven sources.
    """
    for d in source_dirs():
        vis = d / "visuals"
        learning = d / "LEARNING.md"
        if not vis.is_dir() or not learning.exists():
            continue
        text = read(learning)
        for img in sorted(vis.glob("*.jpg")) + sorted(vis.glob("*.png")):
            if img.name not in text:
                err(img, 0, f"frame is not cited in {d.name}/LEARNING.md - teach it or prune it")


def check_topic_notes() -> None:
    """Topic notes declare a legal Status and list their feeding sources."""
    for t in topic_files():
        text = read(t)
        m = re.search(r"^\*\*Status:\*\*\s*(\S+)", text, re.M)
        if not m:
            err(t, 0, "no '**Status:**' line (seed / emerging / established)")
        else:
            status = m.group(1).strip("*` ").lower()
            if status not in TOPIC_STATUSES:
                err(t, 0, f"Status '{status}' is not one of {sorted(TOPIC_STATUSES)}")
        if "Sources feeding this topic" not in text:
            warn(t, 0, "no 'Sources feeding this topic' section")


def check_log_chronology() -> None:
    """log.md is append-only and chronological.

    KNOWN LIMITATION, stated so nobody trusts this further than it goes: entries sharing
    a date are indistinguishable to this check, so it cannot catch a same-day entry filed
    in the wrong order - which is the mistake that actually happened twice while building
    the kit (every entry was 2026-07-25). Catching that would need per-entry timestamps,
    which are not worth the ceremony. Order within a day stays a human responsibility.
    """
    log = ROOT / "brain" / "log.md"
    if not log.exists():
        err(log, 0, "brain/log.md is missing")
        return
    prev, prev_line = None, 0
    for i, line in enumerate(read(log).splitlines(), 1):
        m = re.match(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|", line)
        if not m:
            continue
        date = m.group(1)
        if prev and date < prev:
            err(log, i, f"date {date} is earlier than {prev} on line {prev_line} - log must be chronological")
        prev, prev_line = date, i


def check_claims() -> None:
    """Every claim carries a citation, and claim numbers are unique and sequential."""
    claims = ROOT / "brain" / "claims.md"
    if not claims.exists():
        err(claims, 0, "brain/claims.md is missing")
        return
    seen: list[int] = []
    for i, line in enumerate(read(claims).splitlines(), 1):
        m = re.match(r"^\|\s*(\d+)\s*\|(.+)$", line)
        if not m:
            continue
        num = int(m.group(1))
        cells = [c.strip() for c in m.group(2).split("|")]
        seen.append(num)
        # cells: claim, topic, sources, confidence, (trailing)
        if len(cells) < 4:
            err(claims, i, f"claim {num} has too few columns")
            continue
        if not cells[2] or cells[2] in {"-", "n/a"}:
            err(claims, i, f"claim {num} has no citation - AGENTS.md forbids uncited claims")
        topic = cells[1].strip()
        if topic and not (ROOT / "brain" / "topics" / f"{topic}.md").exists():
            err(claims, i, f"claim {num} names topic '{topic}' with no matching note")
    if seen != sorted(set(seen)):
        err(claims, 0, f"claim numbers are not unique+ascending: {seen}")
    if seen and seen != list(range(1, len(seen) + 1)):
        warn(claims, 0, "claim numbers are not a gapless 1..N sequence")


CLAIM_REF = re.compile(r"\bclaims?\s+(\d+(?:\s*[-,]\s*\d+)*)", re.I)


def _cited_numbers(blob: str) -> list[int]:
    """'48-55' -> [48, 55] (endpoints only); '11, 14, 17' -> [11, 14, 17].

    Interior members of a range are not checked: dreaming may drop a claim, leaving a
    legal gap inside an otherwise valid span.
    """
    out: list[int] = []
    for part in (p.strip() for p in blob.split(",")):
        if not part:
            continue
        if "-" in part:
            lo, _, hi = part.partition("-")
            out += [int(lo), int(hi)]
        else:
            out.append(int(part))
    return out


def check_claim_references() -> None:
    """Prose citing 'claim N' must name a claim that exists.

    Claim numbers are quoted all over the brain - AGENTS.md, topic notes, ADRs, log.md,
    LEARNING.md, context notes. Every one of those is a *copy* of a fact that lives in
    brain/claims.md, and copies drift. check_claims() verifies the table; this verifies
    everything pointing at it. It is the same idea as check_local_links(), for a cross-link
    that happens to be written as a number instead of a path.

    Catches: a typo, a reference past the end of the table, and a claim dropped by a
    dreaming pass that left danglers behind.

    KNOWN LIMITATION, and it is the important one: this cannot catch a reference to a claim
    that EXISTS but says something else. That is exactly the bug that prompted the check -
    AGENTS.md cited claim 33 for "the generator and the evaluator are separate processes"
    when 33 is about ablation and the right claim was 34. Claim 33 existed, so this check
    would have passed it. Deciding whether a cited claim actually supports the sentence
    citing it is a reading judgement, and judgement stays with the fact-checker; a validator
    that scored it would be laundering taste as a green check.
    """
    claims_file = ROOT / "brain" / "claims.md"
    if not claims_file.exists():
        return  # check_claims already reported this
    known = {
        int(m.group(1))
        for m in re.finditer(r"^\|\s*\**(\d+)\**\s*\|", read(claims_file), re.M)
    }
    if not known:
        return
    ceiling = max(known)

    for md in markdown_files():
        for i, line in enumerate(read(md).splitlines(), 1):
            for m in CLAIM_REF.finditer(line):
                for n in _cited_numbers(m.group(1)):
                    if n not in known:
                        err(md, i, f"cites claim {n}, which does not exist "
                                   f"(brain/claims.md holds 1..{ceiling})")


def check_foundations() -> None:
    """AGENTS.md: every foundation declares that it is supplied background, uncited.

    The whole value of `brain/` is that a claim carries a citation and a gate verdict.
    `foundations/` holds material that has neither and never will, so the one thing that
    keeps it from corrupting the brain is that **its status is declared rather than
    assumed** - a reader meeting the file must be told before they read it.

    Cheap to check, and it is the only rule this layer has that a machine can enforce.
    Whether a file really is a fundamental rather than a smuggled claim stays a judgement.
    """
    d = ROOT / "foundations"
    if not d.is_dir():
        return
    for f in sorted(d.glob("*.md")):
        if f.name == "README.md":
            continue
        if "uncited by construction" not in read(f):
            err(f, 0, "foundation is missing its status header - it must declare itself "
                      "supplied background, uncited by construction (see foundations/README.md)")


def check_adrs() -> None:
    """ADRs are numbered uniquely and carry Status + Date."""
    adr_dir = ROOT / "brain" / "decisions"
    if not adr_dir.is_dir():
        return
    numbers: dict[str, Path] = {}
    for f in sorted(adr_dir.glob("*.md")):
        m = re.match(r"^(\d{4})-[a-z0-9-]+\.md$", f.name)
        if not m:
            err(f, 0, "ADR filename must be NNNN-kebab-slug.md")
            continue
        if m.group(1) in numbers and m.group(1) != "0000":
            err(f, 0, f"duplicate ADR number {m.group(1)} (also {numbers[m.group(1)].name})")
        numbers[m.group(1)] = f
        if f.name.startswith("0000"):
            continue
        text = read(f)
        if not re.search(r"^\|\s*Status\s*\|", text, re.M):
            err(f, 0, "ADR has no Status row")
        if not re.search(r"^\|\s*Date\s*\|", text, re.M):
            err(f, 0, "ADR has no Date row")


def check_local_links() -> None:
    """Relative Markdown links must resolve - cross-links are the brain's connective tissue."""
    link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for md in markdown_files():
        for i, line in enumerate(read(md).splitlines(), 1):
            for target in link_re.findall(line):
                t = target.strip()
                if t.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                if "<" in t or ">" in t:
                    continue  # template placeholder, e.g. visuals/<file>.jpg
                t = t.split("#")[0].strip()
                if not t:
                    continue
                resolved = (md.parent / t).resolve()
                if not resolved.exists():
                    err(md, i, f"broken relative link -> {target}")


def check_mermaid() -> None:
    """Mermaid fences are balanced and declare a diagram type."""
    types = ("flowchart", "graph", "sequenceDiagram", "classDiagram", "stateDiagram",
             "erDiagram", "journey", "gantt", "pie", "mindmap", "timeline")
    for md in markdown_files():
        lines = read(md).splitlines()
        open_at = None
        for i, line in enumerate(lines, 1):
            s = line.strip()
            if open_at is None and s.startswith("```mermaid"):
                open_at = i
                nxt = next((l.strip() for l in lines[i:] if l.strip()), "")
                if not nxt.startswith(types):
                    err(md, i, f"mermaid block does not start with a diagram type (got '{nxt[:30]}')")
            elif open_at is not None and s == "```":
                open_at = None
        if open_at is not None:
            err(md, open_at, "unclosed ```mermaid fence")


def check_diagram_walkthroughs() -> None:
    """AGENTS.md: every diagram in teaching material carries a walkthrough.

    Scoped to knowledge OUTPUTS - LEARNING.md, topic notes, reports, and the templates that
    model them. Not prd.md or how_to_use_this.md, where a diagram illustrates surrounding
    prose rather than teaching on its own.

    This checks only that an explanation EXISTS and has some substance. Whether it teaches
    judgement or merely narrates the arrows is a judgement call, and judgement stays in
    AGENTS.md - a validator that scored explanation quality would be laundering taste as a
    green check.
    """
    MIN_CHARS = 150
    LOOKAHEAD = 14

    targets: list[Path] = []
    targets += sorted((ROOT / "sources").glob("*/LEARNING.md"))
    targets += sorted((ROOT / "sources").glob("*/MAP.md"))
    targets += topic_files()
    targets += sorted((ROOT / "reports").glob("*.md"))

    for md in targets:
        lines = read(md).splitlines()
        i = 0
        while i < len(lines):
            if not lines[i].strip().startswith("```mermaid"):
                i += 1
                continue
            close = next((j for j in range(i + 1, len(lines))
                          if lines[j].strip() == "```"), None)
            if close is None:
                break  # unclosed fence - check_mermaid reports it
            prose = 0
            for k in range(close + 1, min(close + 1 + LOOKAHEAD, len(lines))):
                s = lines[k].strip()
                if s.startswith("#") or s.startswith("```"):
                    break  # next section or next diagram - the walkthrough is missing
                if s.startswith("<!--") or s.startswith("-->"):
                    continue
                prose += len(s)
            if prose < MIN_CHARS:
                err(md, i + 1,
                    f"diagram has no walkthrough ({prose} chars of prose follow it, need >= {MIN_CHARS}) "
                    f"- AGENTS.md requires orientation, crux, why-this-shape, provenance")
            i = close + 1


# Non-ASCII that earns its place, all already load-bearing somewhere in the kit:
# section signs in citations, the two callout markers, box-drawing for directory trees,
# arrows and comparison operators in prose and tables.
ALLOWED_NON_ASCII = set(
    "§💡⚠️"          # citations, the two callout markers (+ variation selector)
    "─│├└┌┐┘┤┬┴┼"        # box drawing, for directory trees
    "→←↔⇔↑↓"              # arrows
    "≤≥≠±×÷"              # comparison and arithmetic
    "²³·…"                # superscripts, middot, ellipsis
    "⭐"                   # used in a couple of tables
    # Diacritics in researchers' names and paper titles. Added 2026-08-04, when the reading
    # list first had to cite Christopher Re and the Darwin Godel Machine and could spell
    # neither. A brain whose entire purpose is accurate citation must not silently ASCII-fold
    # an author's name, so the alternative - dropping the accents - was the worse defect.
    # Deliberately a fixed list of Latin-1 letters, not a category test: a stray CJK glyph is
    # still the thing this check exists to catch.
    "áàâäãåéèêëíìîïóòôöõúùûüñçßøæœÁÀÂÄÃÅÉÈÊËÍÌÎÏÓÒÔÖÕÚÙÛÜÑÇØÆŒ"
    # Latin Extended-A, added 2026-08-05 for Slavic, Baltic and Turkish surnames - the first
    # was Mislav Balunovic (AgentDojo). Same reasoning as the Latin-1 block above: a citation
    # index must not ASCII-fold an author's name. Still a fixed list, not a category test.
    "ćčďěğıłńňřśšťůźżžĆČĎĚĞİŁŃŇŘŚŠŤŮŹŻŽāēīōūąęįųĀĒĪŌŪĄĘĮŲ"
)


def check_style() -> None:
    """AGENTS.md: never use the em dash - and no unexpected non-ASCII generally.

    The em dash rule is explicit in AGENTS.md. The wider check exists because an agent
    writing 5,000-word notes will occasionally emit a stray character from another script:
    a CJK glyph appeared mid-rewrite on 2026-08-02 and was caught only because someone
    thought to look. Smart quotes and non-breaking spaces are the more common version and
    are equally invisible in review.

    The allowlist is deliberately explicit rather than a category test - every character in
    it is one the kit actually uses, so adding to it is a decision rather than a default.
    """
    for md in markdown_files():
        for i, line in enumerate(read(md).splitlines(), 1):
            if "—" in line:
                err(md, i, "em dash (U+2014) - AGENTS.md requires a plain dash '-'")
            for ch in line:
                if ord(ch) > 127 and ch not in ALLOWED_NON_ASCII and not _is_emoji(ch):
                    err(md, i, f"unexpected non-ASCII {ch!r} (U+{ord(ch):04X}) - "
                               f"if intended, add it to ALLOWED_NON_ASCII")


def _is_emoji(ch: str) -> bool:
    """Emoji are legal (favicons, section markers); other scripts are the thing being caught."""
    return ord(ch) >= 0x1F000


def check_stage_specs() -> None:
    """Every stages/*.md must be routed to from AGENTS.md (ADR-0027).

    This is the failure a split introduces and a long file cannot have: a spec
    that exists, is correct, and that nothing points at - so no agent ever loads
    it. Cheap to check, and the only genuinely new risk the extraction created.
    """
    d = ROOT / "stages"
    if not d.is_dir():
        return
    agents = read(ROOT / "AGENTS.md")
    readme = read(d / "README.md") if (d / "README.md").exists() else ""
    for f in sorted(d.glob("*.md")):
        if f.name == "README.md":
            continue
        if f"stages/{f.name}" not in agents:
            err(ROOT / "AGENTS.md", 0,
                f"stage spec 'stages/{f.name}' is not linked from AGENTS.md - "
                f"an unrouted spec is a spec no agent loads")
        if f"]({f.name})" not in readme:
            warn(d / "README.md", 0, f"stages/README.md does not list {f.name}")


CHECKS = [
    ("INDEX integrity", check_index_integrity),
    ("source metadata", check_source_metadata),
    ("frames are cited", check_frames_are_cited),
    ("topic notes", check_topic_notes),
    ("log chronology", check_log_chronology),
    ("claims", check_claims),
    ("claim references", check_claim_references),
    ("foundations", check_foundations),
    ("ADRs", check_adrs),
    ("local links", check_local_links),
    ("mermaid", check_mermaid),
    ("diagram walkthroughs", check_diagram_walkthroughs),
    ("style", check_style),
    ("stage specs", check_stage_specs),
]


def coverage_report() -> list[str]:
    """Counts, not judgements - the two coverage facts nothing else surfaces.

    This is deliberately NOT a check and can never fail the run. Whether 4 of 26
    sources verified is acceptable, or whether a dream pass is overdue, are
    judgement calls that belong to the human and to `AGENTS.md` - encoding a
    threshold here would launder judgement as a green check (ADR-0004). What the
    validator can honestly do is make an invisible number visible at the one
    moment somebody is already looking at the brain's health.
    """
    lines: list[str] = []

    srcs = source_dirs()
    verified = [d for d in srcs if (d / "verify.md").exists()]
    lines.append(f"  /verify coverage: {len(verified)}/{len(srcs)} sources have a verify.md")

    # Presentation narrative: mandatory for sources ingested from 260815 onward
    # (ADR-0026). Reported, never enforced - whether an older note earns one is
    # judgement, and retrofitting 26 notes on day one is how debt is created.
    PRESENT_FROM = "260815"
    scoped = [d for d in srcs if d.name[:6] >= PRESENT_FROM]
    have = [d for d in scoped
            if (d / "LEARNING.md").exists()
            and "## Presentation narrative" in read(d / "LEARNING.md")]
    older = len(srcs) - len(scoped)
    lines.append(
        f"  presentation narrative: {len(have)}/{len(scoped)} in-scope sources "
        f"(from {PRESENT_FROM}); {older} older source(s) exempt, retrofit on demand"
    )

    dreams = sorted(
        p for p in (ROOT / "brain" / "dreams").glob("[0-9][0-9][0-9][0-9]-*.md")
    )
    if not dreams:
        lines.append("  dream passes: none recorded")
        return lines

    last = dreams[-1]
    stem = last.stem.split("-", 1)[1] if "-" in last.stem else ""
    since = [d for d in srcs if d.name[:6] > stem] if len(stem) == 6 else []
    lines.append(
        f"  last dream pass: {last.name} ({len(dreams)} total); "
        f"{len(since)} source(s) ingested since"
    )
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate the Brain kit's conventions.")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--no-coverage", action="store_true",
                    help="suppress the informational coverage report")
    args = ap.parse_args()

    for name, fn in CHECKS:
        try:
            fn()
        except Exception as exc:  # a broken check must not masquerade as a clean brain
            err(ROOT, 0, f"check '{name}' crashed: {exc!r}")

    errors = [f for f in findings if f.level == "error"]
    warns = [f for f in findings if f.level == "warn"]

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for f in errors:
            print(f)
    if warns:
        print(f"\nWARNINGS ({len(warns)}):")
        for f in warns:
            print(f)

    n_src, n_topic = len(source_dirs()), len(topic_files())
    if not errors and not warns:
        print(f"OK - {n_src} sources, {n_topic} topics, {len(CHECKS)} checks, nothing to report.")
    else:
        print(f"\n{n_src} sources, {n_topic} topics, {len(CHECKS)} checks: "
              f"{len(errors)} error(s), {len(warns)} warning(s).")

    if not args.no_coverage:
        print("\nCoverage (informational - never fails the run):")
        for line in coverage_report():
            print(line)

    return 1 if errors or (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
