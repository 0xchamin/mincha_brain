#!/usr/bin/env python3
"""Generate BUILD.md - a single self-contained file that rebuilds the kit from scratch.

Why a generator instead of a hand-written document:

    BUILD.md embeds AGENTS.md, validate.py and tools/ingest.py **verbatim**. Those three
    cannot be paraphrased - the contract's precision is the product, and ADR-0005 exists
    precisely because tools/ingest.py's constants must not vary between machines. Retyping
    ~1,300 lines by hand is how silent corruption gets in, so the bundle is built by
    copying bytes, not by writing prose about them.

    It also means BUILD.md can never drift: regenerate it and it is current by construction.

Usage:  python3 tools/make_build_doc.py          # writes ./BUILD.md
        python3 tools/make_build_doc.py --check  # exit 1 if BUILD.md is stale

Stdlib only, like validate.py - a fresh clone must be able to run this before any pip install.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "BUILD.md"

# Six backticks: the source templates contain 3-backtick fences, nothing contains 6.
F = "``````"

LANG = {".md": "markdown", ".py": "python", ".sh": "bash", ".ps1": "powershell",
        ".yml": "yaml", ".txt": "text"}


def lang_for(path: str) -> str:
    return LANG.get(Path(path).suffix, "text")


# --------------------------------------------------------------------------
# What travels verbatim, in the order a reader should meet it.
# --------------------------------------------------------------------------

VERBATIM: list[tuple[str, list[str]]] = [
    ("The contract (read this one yourself)", ["AGENTS.md"]),
    ("Personas", [
        "personas/README.md", "personas/architect.md", "personas/code-explorer.md",
        "personas/curator.md", "personas/fact-checker.md", "personas/mentor.md",
        "personas/synthesizer.md",
    ]),
    ("The two frozen scripts", ["validate.py", "tools/ingest.py"]),
    ("Source template", [
        "sources/_TEMPLATE/SOURCE.md", "sources/_TEMPLATE/nodes.md",
        "sources/_TEMPLATE/LEARNING.md", "sources/_TEMPLATE/MAP.md",
        "sources/_TEMPLATE/raw/README.md", "sources/_TEMPLATE/visuals/README.md",
        "sources/_TEMPLATE/context/README.md",
    ]),
    ("Architecture decision records (the why, minus this brain's content decisions)", [
        "brain/decisions/0000-template.md",
        "brain/decisions/0002-deep-research-stage.md",
        "brain/decisions/0003-optional-visual-leg.md",
        "brain/decisions/0004-validator-as-type-checker.md",
        "brain/decisions/0005-mechanical-toolbox.md",
        "brain/decisions/0006-static-probe-is-advisory.md",
    ]),
    ("Plumbing", [
        "requirements.txt", ".gitignore", ".gitattributes", "link-agents.sh",
        "link-agents.ps1", ".github/workflows/validate.yml",
        ".claude/commands/research.md", "brain/index.md", "LICENSE",
    ]),
]

# --------------------------------------------------------------------------
# What is synthesized fresh: an EMPTY brain, not a copy of this one.
# --------------------------------------------------------------------------

SEED_TOPICS = {
    "agents": ("Agents", "Autonomous LLM agents: the loop, prompt authorship, control flow, "
                         "structured output and tool calls, state and pause/resume, and how much "
                         "of the agent you own versus delegate to a framework."),
    "mcp": ("MCP (Model Context Protocol)", "The Model Context Protocol: servers, tools, "
            "resources, prompts, transport (stdio / HTTP), the client-server handshake, and how "
            "agents consume MCP capabilities."),
    "skills": ("Skills", "Agent skills: what a skill is, how it is defined and packaged, how it "
               "is invoked or auto-triggered, how to evaluate one, and how skills relate to tools "
               "and MCP."),
    "rag": ("RAG", "Retrieval-augmented generation: chunking, embeddings, indexing, retrieval and "
            "reranking, and how retrieval quality is measured."),
    "agent-security": ("Agent security", "Threats and mitigations: prompt injection, tool "
                       "poisoning, exfiltration, sandboxing, and the delegated-authorization "
                       "substrate (scopes, consent, token handling)."),
    "inferencing": ("Inferencing", "LLM serving: KV cache, batching, quantization, speculative "
                    "decoding, and the latency/throughput/cost trade-offs."),
}


def seed_topic(slug: str) -> str:
    title, covers = SEED_TOPICS[slug]
    return f"""# Topic: {title}

**Status:** seed (no source yet -> emerging at 1 source -> established at 2+ corroborating sources)

> Living, cross-source synthesis on {title.lower()}. Many sources feed this note; **merge and
> de-duplicate** as they arrive (architect persona). Every claim cited.

## What this covers

{covers}

## Synthesis

_(empty - populated as sources are ingested.)_

## Key claims

| Claim | Sources (cited) | Confidence |
|---|---|---|
| _(none yet)_ | - | - |

## Key visuals

_(Diagrams/slides across sources, embedded with caption + citation.)_

## Open questions / conflicts

- _(none yet)_

## Sources feeding this topic

- _(none yet)_
"""


def fresh_index() -> str:
    rows = "\n".join(
        f"| {SEED_TOPICS[s][0]} | seed | {SEED_TOPICS[s][1]} | 0 | "
        f"[`brain/topics/{s}.md`](brain/topics/{s}.md) |"
        for s in SEED_TOPICS
    )
    return f"""# Brain - INDEX (ask here)

> **This is the entry point.** To ask a question of the brain - at the repo root - **start here**:
> this catalog tells you which source or topic covers what, so you (or the agent) read the right
> notes instead of every file.
>
> **Auto-maintained.** This file is a **hard output** of ingest, compound, and close-loop - the
> agent rewrites the affected rows every time a source is added, a claim is promoted, or the loop
> is closed. It is **not** hand-curated between those checkpoints.
>
> **Integrity rule (agent must uphold):** every `sources/<folder>/` has **exactly one** row in the
> Sources table below, and every `brain/topics/*.md` has **exactly one** row in the Topics table.
> `validate.py` checks this both ways.
>
> **Annotate every entry** with a one-line summary + "when to read" - a bare list forces a reader
> to open each link to judge relevance; annotating once does that upfront.

## Sources

| Source | Type | Summary | Topics | When to read | Folder |
|---|---|---|---|---|---|
| _(none yet - paste a URL to begin)_ | - | - | - | - | - |

## Topics (living notes)

The compounding synthesis layer - many sources feed each note. See [`brain/topics/`](brain/topics/).

> **Topics are open** - new ones are added as sources introduce a recognizable new area (the
> **architect** persona owns the create-vs-merge call). **Status** advances `seed` (created, no
> source yet) -> `emerging` (one source, needs-check) -> `established` (two or more corroborating
> sources). The six below are seeds, not a whitelist.

| Topic | Status | What it covers | Sources feeding it | Note |
|---|---|---|---|---|
{rows}

## Deeper layers (brain-wide content INDEX points into)

- [`brain/claims.md`](brain/claims.md) - cross-source **corroborated claims** with citations.
- [`brain/glossary.md`](brain/glossary.md) - 💡 **terms** defined once, reused across sources.
- [`brain/log.md`](brain/log.md) - dated **ingest milestones**.
- [`brain/decisions/`](brain/decisions/) - **ADRs** for durable structural decisions.
- [`reports/`](reports/README.md) - **synthesized cross-source study material**.

## Config (taste + workflow)

- [`AGENTS.md`](AGENTS.md) - behavioral contract + the paste-a-URL ingest rule. Read every session.
- [`personas/README.md`](personas/README.md) - role overlays; auto-loaded per the routing table.
"""


SYNTH: dict[str, str] = {
    "INDEX.md": fresh_index(),
    "brain/claims.md": """# Brain - corroborated claims (cross-source)

> Durable, corroborated claims promoted from source `nodes.md` files. Each must be reusable
> across future queries and carry a citation. A claim confirmed by multiple sources is stronger -
> note them all. This is a signal store; task-specific scratch stays in the source folder.

| # | Claim | Topic | Sources (cited) | Confidence |
|---|---|---|---|---|

> When a new source corroborates an existing claim, add its citation to that row rather than
> creating a duplicate. When sources conflict, keep both and flag the conflict.
""",
    "brain/glossary.md": """# Brain - glossary (reusable terms)

> 💡 terms defined once and reused across sources, promoted from source `LEARNING.md` files.
> Keep each to 1-2 sentences. Cite the source where the term was learned.

| Term | 💡 Explanation | First source |
|---|---|---|
""",
    "brain/log.md": """# Brain - chronological log

> Append-only. One dated entry per source ingested or milestone worth remembering.

| Date | Source | Entry |
|---|---|---|
| BOOTSTRAP_DATE | brain (kit) | Kit built from `BUILD.md` (a generated bundle of the reference clone). Empty brain: 6 seed topics, no sources, no claims. |
""",
    "reports/README.md": """# Reports - synthesized cross-source study material

> Written by the **synthesizer** persona when you ask a question the brain can answer from more
> than one source. One file per report, named `YYMMDD_slug.md`. Every claim cited; every diagram
> carries a walkthrough (see `AGENTS.md`).

_(none yet)_
""",
}

TREE = """brain/
brain/topics/
brain/decisions/
sources/
sources/_TEMPLATE/raw/
sources/_TEMPLATE/visuals/
sources/_TEMPLATE/context/
personas/
tools/
reports/
.github/workflows/
.claude/commands/"""


def block(path: str, body: str) -> str:
    if not body.endswith("\n"):
        body += "\n"
    return f"#### `{path}`\n\n{F}{lang_for(path)}\n{body}{F}\n"


def build() -> str:
    today = date.today().isoformat()
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        sha = "unknown"

    p: list[str] = []
    a = p.append

    a(f"""# BUILD.md - build Brain from scratch, from this file alone

> **Generated {today} from commit `{sha}`** by `tools/make_build_doc.py`. Do not hand-edit: edit the
> source files in the reference clone and regenerate, or your copy silently diverges from the kit
> it claims to build.

**Brain is an agent-driven compounding learning kit.** You paste a URL - a YouTube talk, a blog
post, a paper, or a GitHub repo - and the agent captures it, reads the slides or traces the code,
keeps only claims whose two independent legs agree, distills a learning document, and promotes the
durable parts into living topic notes. Every claim carries a citation. Ingest thirty sources and
the thirtieth starts richer than the first.

**There is no application.** The agent is the runtime; the kit is a contract written in Markdown
plus two small frozen scripts. That is why this file can rebuild it.

---

## 1. How to use this file

Hand this file to a coding agent (Claude Code, Copilot CLI, Codex, Cursor) in an empty directory
and say:

> Build the kit described in BUILD.md. Create every file in section 5 with exactly the contents
> given, then run the verification in section 7.

Or do it by hand - it is only file creation. Either way:

- **Sections 5.1 to 5.6 are byte-exact.** Copy them literally. `AGENTS.md`, `validate.py` and
  `tools/ingest.py` in particular must not be paraphrased, reformatted or "improved". The contract's
  precision is the product, and `tools/ingest.py`'s constants are frozen deliberately (ADR-0005) so
  that a verdict computed on one machine means the same thing on another.
- **Section 6 (the empty brain) is a starting state**, not a copy of anyone's knowledge. It ships
  six seed topics and no sources.

---

## 2. What you get

```
you paste a URL
      |
      v
  capture  ->  understand  ->  corroborate  ->  distill  ->  compound
  (shell)      (agent view/    (the gate)       LEARNING.md   brain/topics/
               grep)                                          + claims + INDEX
```

| Stage | What happens | Lands in |
|---|---|---|
| Capture | `yt-dlp` / `web_fetch` / `git clone`; frames sampled and deduped in the shell | `sources/<id>/raw/` |
| Understand | The agent `view`s candidate frames (it *is* the vision model) or traces code | - |
| Corroborate | A claim is kept only when two legs agree: visual vs narration, or code vs docs | `nodes.md` |
| Distill | The transferable concept, 3-8 curated visuals, every claim cited | `LEARNING.md` |
| Compound | Durable claims merged into living topic notes; INDEX and log updated | `brain/` |

---

## 3. Prerequisites

| Need | Why | Check |
|---|---|---|
| **Python 3.9+** | `validate.py` and `tools/ingest.py` (stdlib only) | `python3 -V` |
| **ffmpeg** (with `ffprobe`) | frame sampling, contact sheets, the static probe | `ffmpeg -version` |
| **git** | the kit is a git repo; `git diff` is the undo for every compound pass | `git --version` |
| `gh` (optional) | code sources: license, commit SHA, orient-before-clone | `gh --version` |

**Install ffmpeg**

```bash
brew install ffmpeg                 # macOS
sudo apt install ffmpeg             # Debian / Ubuntu
winget install Gyan.FFmpeg          # Windows (or scoop / choco)
```

> On a managed work laptop where `brew`/`winget` are blocked, a static ffmpeg build unpacked
> anywhere on `PATH` is enough - the kit only ever shells out to `ffmpeg` and `ffprobe`.

**A note on the Python floor:** both scripts use `from __future__ import annotations`, so modern
type syntax is never evaluated at runtime. 3.9 is a safe floor; 3.12 is what the reference clone
runs.

---

## 4. Create the tree

```bash
mkdir -p brain/topics brain/decisions sources/_TEMPLATE/raw sources/_TEMPLATE/visuals \\
         sources/_TEMPLATE/context personas tools reports .github/workflows .claude/commands
git init
```

Directories:

```
{TREE}
```

---

## 5. The files (byte-exact)
""")

    n = 0
    for section, paths in VERBATIM:
        n += 1
        a(f"\n### 5.{n} {section}\n")
        if section.startswith("The contract"):
            a("\n> This is the kit. Everything else supports it. Read it before your first ingest -\n"
              "> not because you must memorise it, but because it is the file your agent obeys, and\n"
              "> you should know what you are agreeing to.\n")
        for rel in paths:
            src = ROOT / rel
            if not src.exists():
                sys.exit(f"missing source file: {rel}")
            a("\n" + block(rel, src.read_text(encoding="utf-8")))

    a(f"""
---

## 6. The empty brain (starting state)

These are **not** copies of the reference brain's knowledge - they are the blank forms. Six seed
topics, no sources, no claims. Your first ingest fills them.

> **Seeds, not a whitelist.** When a source teaches a recognizable, reusable area the brain does not
> cover, create a new topic note (the **architect** persona owns that call). Stay inside AI / ML /
> agentic engineering; flag anything clearly off-domain rather than silently ingesting it.
""")

    a("\n" + block("INDEX.md", SYNTH["INDEX.md"]))
    for slug in SEED_TOPICS:
        a("\n" + block(f"brain/topics/{slug}.md", seed_topic(slug)))
    for rel in ("brain/claims.md", "brain/glossary.md", "brain/log.md", "reports/README.md"):
        body = SYNTH[rel].replace("BOOTSTRAP_DATE", today)
        a("\n" + block(rel, body))

    a(f"""
---

## 7. Install, link, verify

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
chmod +x link-agents.sh && ./link-agents.sh      # Windows: .\\link-agents.ps1
```

> **Do not skip `link-agents`.** It creates the git-ignored pointer files some harnesses expect
> (`CLAUDE.md`, `.github/copilot-instructions.md`) as symlinks to the one canonical `AGENTS.md`.
> Skip it on Claude Code and the agent reads **no contract at all**: no paste-a-URL trigger, no
> personas, no gate. The kit looks like an ordinary folder of Markdown and quietly behaves like one.
> Copilot CLI, Codex and Cursor read `AGENTS.md` natively and do not need it.

**Verify, in this order:**

```bash
python3 validate.py                 # needs no venv - stdlib only
```

Expect: `OK - 0 sources, 6 topics, 11 checks, nothing to report.` **A non-zero exit means the
build is wrong** - most often a file saved with the fenced block markers still in it, or a topic
note whose Status line was reflowed.

```bash
python3 tools/ingest.py --help      # subcommands: transcript, probe, frames, sheet
ffmpeg -version && ffprobe -version
```

Then a live smoke test on any short talk:

```bash
yt-dlp --skip-download --write-auto-subs --sub-lang en --sub-format vtt -o "c.%(ext)s" "<url>"
python3 tools/ingest.py transcript c.en.vtt out.txt
```

Timestamped blocks in `out.txt` means the capture leg works. Delete both files afterwards.

---

## 8. Your first ingest

Launch your agent in the directory and paste a URL. That is the whole interface - the paste-a-URL
rule in `AGENTS.md` does the rest. What should happen:

1. A new `sources/YYMMDD_slug/` from `_TEMPLATE`, `SOURCE.md` filled in.
2. Transcript captured and de-duplicated; the **static probe** run.
3. Frames extracted, triaged as contact sheets, `view`ed - or the visual leg skipped and the cost
   recorded.
4. `nodes.md` written with a gate verdict and **both legs cited** per node.
5. `LEARNING.md` distilled.
6. Claims promoted into `brain/`, `INDEX.md` and `log.md` updated, `validate.py` run, then a summary
   and `git diff` shown for review.

**Commit after each pass.** `git diff` and `git revert` are the undo, which is what makes automatic
compounding safe.

> ⚠️ **The one gotcha worth knowing before it bites you.** The static probe reports `STATIC` when a
> video yields 3 or fewer distinct frames. Scene detection measures **whole-frame** delta, so a
> templated conference deck - fixed background, logo, speaker inset, footer - reads as static while
> every slide changes. `STATIC` is therefore **advisory**: the probe writes a 9-frame confirmation
> sheet, and you `view` it before honouring the verdict (ADR-0006, section 5.5). A false `RICH`
> wastes one `view`; a false `STATIC` destroys the source's second leg irrecoverably.

---

## 9. The daily loop

| You want to | Do this |
|---|---|
| Learn something new | Paste the URL. |
| Go deeper on a claim | Say **"deep research"** with the URL or on an ingested source. Writes an external-evidence note to `sources/<id>/context/`, tiered T1-T5 under a hard independence rule. |
| Be taught a concept | "Explain X" - the **mentor** persona, aimed one level above the source. |
| Ask across everything | Ask from the repo root. The agent reads `INDEX.md`, greps the topic notes, and synthesizes a cited report into `reports/`. |
| Check nothing rotted | `python3 validate.py` |

---

## 10. What this bundle deliberately omits

| Omitted | Why |
|---|---|
| `README.md`, `prd.md`, `how_to_use_this.md` | Their procedural role is this file. The durable design rationale lives in the ADRs (section 5.5), which **are** included. |
| ADR-0001 | A content decision specific to the reference brain (creating a topic from one of its sources), not a kit decision. It also links to a source you will not have. |
| All ingested sources, claims, glossary terms, reports | This is a kit, not someone else's knowledge. Your brain starts empty and earns its content. |

> **Historical references you will see in the contract.** `AGENTS.md` and the ADRs cite source
> folders like `260725_12-factor-agents` as calibration data ("a slide-heavy talk yields 19 distinct
> frames"). Those folders will not exist in your build. The references are deliberate and worth
> keeping: they are the measurements the thresholds were set against, and they are inline code, not
> links, so nothing breaks.

---

## 11. Regenerating this file

```bash
python3 tools/make_build_doc.py            # rewrite BUILD.md from the current tree
python3 tools/make_build_doc.py --check    # exit 1 if stale
```

Run it after any change to the contract, the personas, the scripts or the templates. A hand-edited
BUILD.md is a fork of the kit wearing the kit's name.
""")
    return "".join(p)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if BUILD.md is missing or stale (ignores the generated header)")
    args = ap.parse_args()

    text = build()
    if args.check:
        if not OUT.exists():
            print("BUILD.md missing - run: python3 tools/make_build_doc.py")
            return 1
        def strip_header(s: str) -> str:
            return "\n".join(l for l in s.splitlines() if not l.startswith("> **Generated "))
        if strip_header(OUT.read_text(encoding="utf-8")) != strip_header(text):
            print("BUILD.md is STALE - run: python3 tools/make_build_doc.py")
            return 1
        print("BUILD.md is current.")
        return 0

    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(text.splitlines())} lines, "
          f"{len(text) / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
