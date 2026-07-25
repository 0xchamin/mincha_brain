# MinCha Brain - a compounding learning kit (agent-driven)

> *A persistent, compounding brain - the human curates and asks, the agent synthesizes and cites,
> and every source becomes context for the next.*

> **MinCha Brain** (**Brain** for short) turns the things you learn from - **YouTube videos, blog
> posts, research papers, and code repositories** - into durable, cited, *compounding* knowledge.
> Paste a URL; the agent
> ingests it, understands it (the meaningful **visuals** for media - slides, diagrams, figures; or
> **traces the code** for a repo), keeps only what the other leg corroborates, distills a learning
> document, and files durable claims into a growing brain. Code sources are for **learning from** a
> repo, not building on it.

This is a **convention, not an application**. There is nothing to build or run as a service. Your
coding agent *is* the engine - Claude Code, Copilot CLI, Codex, Cursor, whichever you already use -
driven by `AGENTS.md` + `personas/`, the one contract they all read. It rests on three ideas -
layered lazy context, close-the-loop compounding, and ground-every-claim - re-pointed from "ship
code" to "learn deeply and remember forever."

> **No agent Skills to install (by design).** The ingest flow lives in `AGENTS.md` + personas, the
> one contract every harness reads - so there are no per-harness Skill files to maintain. See
> [`prd.md` §10](prd.md).
>
> **Two scripts, though - and only two.** "Convention, not application" means no *app*, not no code.
> [`tools/ingest.py`](tools/ingest.py) freezes the mechanical steps (transcript de-duplication, the
> static-video probe, frame extraction, contact sheets) and [`validate.py`](validate.py) type-checks
> the contract itself. Both draw the same line: **form is code, judgement is prose.** See
> [`prd.md` §4.1](prd.md).

> **Full design + rationale:** [`prd.md`](prd.md). **Read that first** if you want the *why*.
> **New here?** [`how_to_use_this.md`](how_to_use_this.md) is the complete end-to-end walkthrough
> (clone -> setup -> launch agent -> paste a URL -> learn -> ask).

---

## 60-second mental model

You feed sources **one at a time**. Each lives in its own `sources/<id>/` folder and walks the
same flow. Durable, corroborated claims are **promoted up** to `brain/`, so your *next* source
starts richer than this one.

```
paste URL -> capture -> understand -> [deep research] -> distill -> compound -> ask
(video/       (transcript/  (agent VIEWs   (OPT-IN only:   (LEARNING.md  (brain/topics/  (known: from source
 blog/paper/   text +        visuals +      external        text + few    merge & cite     unknown: synth
 code repo)    figures /     corroborate    evidence ->     visuals)      + validate.py)   report)
               git clone)    / trace code)  context/)
```

Two kinds of files:
- **Config (your taste):** `AGENTS.md`, `personas/` - how the agent behaves.
- **Knowledge (facts):** `brain/` (compounds across sources) and each `sources/<id>/` (one
  source's living record).

---

## Layout

```text
brain/
├── INDEX.md            # ⭐ ASK HERE: annotated catalog of every source + topic ("when to read")
├── prd.md              # the design + rationale (read first)
├── how_to_use_this.md  # the end-to-end walkthrough (clone -> setup -> paste a URL -> ask)
├── README.md           # this file
├── LICENSE             # MIT
├── AGENTS.md           # behavioral contract + the paste-a-URL ingest rule (single source of truth)
├── validate.py         # type checker for the contract - run before every git diff (stdlib only)
├── tools/ingest.py     # frozen mechanical steps: transcript / probe / frames / sheet
├── .github/workflows/  # CI: runs validate.py on every push and PR
├── link-agents.sh      # macOS/Linux: symlink CLAUDE.md + copilot-instructions.md -> AGENTS.md
├── link-agents.ps1     # Windows: same, once per clone (git-ignored links)
├── requirements.txt    # pip packages for the .venv (yt-dlp, faster-whisper, imagehash, pillow)
├── personas/           # role overlays: curator, code-explorer, synthesizer, fact-checker, mentor, architect
├── sources/            # ONE folder per ingested source
│   └── _TEMPLATE/      #   copy this to start a new source (media: raw/; code: MAP.md + repo/)
│                       #   also: visuals/ (curated frames), context/ (deep-research notes)
├── brain/              # THE COMPOUNDING VAULT (content; the whole-brain index is root INDEX.md)
│   ├── topics/         #   living topic notes: agents, mcp, skills, rag, agent-security, inferencing
│   ├── glossary.md     #   💡 terms defined once, reused
│   ├── claims.md       #   cross-source corroborated claims (cited)
│   ├── decisions/      #   ADRs for durable structural decisions
│   └── log.md          #   append-only chronological ingest log
└── reports/            # generated Markdown/HTML study material
```

> **To ask a question of the brain, start at the root [`INDEX.md`](INDEX.md).** It is the annotated
> entry point and is auto-maintained as sources are ingested and the loop is closed.

---

## Get the kit

Brain is a **template repo you clone once and live in** - a personal, git-tracked knowledge vault,
not a package you install per project.

- **GitHub:** click **"Use this template"**, or `gh repo create <you>/brain --template <owner>/brain --private --clone`
- **Or just clone:** `git clone <repo-url> brain`

Then `git push` as you go - your `brain/` compounding *is* the git history, so pushing backs up
your knowledge.

> **No `pip install brain` / `npx brain` (by design).** See ["Why not a package"](#why-not-a-package)
> below - in short, the agent reads `AGENTS.md` from the repo root, and this is a living vault you
> edit in place, so a package would only hide the files and fight in-place edits.

---

## One-time setup

The kit is cross-platform (it is just Markdown + a Python venv + system `ffmpeg`). Pick your OS.

**macOS (personal laptop):**

```bash
cd ~/projects/brain            # wherever you cloned it
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt        # yt-dlp, faster-whisper, imagehash, pillow
brew install ffmpeg                     # system ffmpeg (Homebrew)
```

> No Homebrew? Install it once: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`, then `brew install ffmpeg`.

**Windows:**

```powershell
cd C:\DEVBOX\projects\brain
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt        # yt-dlp, faster-whisper, imagehash, pillow
winget install Gyan.FFmpeg             # system ffmpeg (or scoop/choco)
```

The agent calls `yt-dlp` / `ffmpeg` from the activated env when it ingests a video. Re-activate
the venv each new shell (`source .venv/bin/activate` on macOS, `.\.venv\Scripts\Activate.ps1` on
Windows).

> **Optional but recommended: the [GitHub CLI](https://cli.github.com) (`gh`).** For code sources it
> records the license, pins the commit SHA, and fetches the README so the agent can *orient before
> cloning*. Absent, the agent falls back to plain `git clone` + `web_fetch`. Never a blocker.
>
> **`validate.py` needs none of this** - stdlib only, no venv, no `ffmpeg`. `python3 validate.py`
> works in a fresh clone.

### Optional: point other agents at the same rules

`AGENTS.md` is the **single contract** for every harness. Copilot CLI, Codex, and Cursor read it
natively - nothing to do. Claude Code (`CLAUDE.md`) and GitHub Copilot in the IDE / coding agent
(`.github/copilot-instructions.md`) expect a different filename, so run the linker **once per
clone** to create git-ignored symlinks back to `AGENTS.md`:

```bash
./link-agents.sh          # macOS / Linux
```
```powershell
.\link-agents.ps1         # Windows (needs Developer Mode for symlinks; falls back to a 1-line pointer)
```

You never maintain a second copy - the links just point at `AGENTS.md`. See the per-harness map in
[`AGENTS.md`](AGENTS.md) (Appendix).

---

## How to drive it

Launch your agent inside this folder (`claude`, `copilot`, `codex`, ...) and use prompts like:

- **Ingest media:** paste a video / blog / paper URL, or *"ingest this: <url>"* -> the agent runs
  the full flow (`AGENTS.md` "paste-a-URL trigger").
- **Ingest code:** paste a **GitHub repo URL**, or *"learn this repo: <url>"* -> the agent clones
  it, writes a `MAP.md` orientation, and traces the key concepts (code-explorer persona). It
  learns *from* the repo; it does not build on it.
- **Learn one:** *"walk me through what this video (or repo) taught, mentor-style."*
- **Ask a known source:** *"in that MCP talk, what were the tool-poisoning mitigations?"*
- **Ask across the brain:** *"what do I know about agent memory poisoning?"* -> synthesized,
  cited report with the best visuals across sources.
- **Build material:** *"make me an HTML primer on Agents + MCP from everything I've ingested."*
- **Compound:** *"promote durable claims from this source into the topic notes."*

Two switches worth knowing, because both change what the brain is allowed to claim:

- **Deep research (opt-in, never automatic):** say *"deep research"* with the URL, or on an
  already-ingested source. The agent tests **specific gated claims** against outside sources,
  weighs them by tier (T1 spec/paper ... T5 aggregator) under an **independence rule**, and files a
  permanent note in `sources/<id>/context/`. This is the only way a claim earns real confidence -
  the corroboration gate alone buys internal consistency, not truth.
- **Skip the visuals:** say *"transcript only"* / *"don't analyze video"* for a podcast or webcam
  interview where the picture never changes. Otherwise the agent runs a **free static probe** and
  auto-degrades if the video yields `<= 3` distinct frames. Either way the cost is recorded, not
  hidden: with one leg, **every node from that source is `single-leg` (needs-check) by
  construction** - a transcript agreeing with itself is not two legs.

```bash
python3 validate.py     # type-checks the whole brain; no venv needed. Exit 1 = the pass isn't done.
```

The agent runs this itself before showing you a `git diff`, and CI runs it on every push. You can
run it any time to check the vault has not drifted.

---

## The one idea that makes it work

Every source has an **evidence leg** and a **claim leg** that must agree. For **media** it is a
**visual** (frame / figure) ↔ the **surrounding text**; for **code** it is the **code**
(`path:line`) ↔ its **docs / README / comments**. The agent keeps a claim **only when the two legs
corroborate** - the **corroboration gate**. That agreement is what separates a trustworthy brain
from a pile of screenshots (or copy-pasted code). For code, a docs↔code **divergence** is itself a
prized finding. See [`prd.md` §6](prd.md).

---

## Why not a package

Brain is intentionally **not** `pip`/`npm` installable. It's a **template repo you clone and edit
in place**, because:

- **The agent reads `AGENTS.md` from the repo root.** Codex, Cursor, and Copilot discover the
  contract by walking the working tree. A package would bury those files in `site-packages` /
  `node_modules` where the agent can't see them - you'd need an installer whose only job is to
  scaffold back the clone you already have.
- **It's a personal vault, not a per-project dependency.** One long-lived clone accumulates your
  `sources/` and `brain/`. `pip install` into each project is the wrong model and would fragment
  the brain.
- **Editing-in-place + git is the feature.** Your compounding `brain/` *is* the git history. A
  package makes the canonical files read-only and upgrades would overwrite your edits.

**Where packaging does belong (later):** only the mechanical ingest steps (`yt-dlp → ffmpeg →
imagehash`), which now live in-tree as [`tools/ingest.py`](tools/ingest.py) - and being *in the
working tree* is the point, since that is what lets the agent read and adapt them. Package it only
if it ever grows a release cadence of its own. A zero-install `npx create-brain` scaffolder is
possible if you ever want *multiple* brains, but "Use this template" already covers that. See
[`prd.md` §10](prd.md).

---

## Start here

1. Read [`how_to_use_this.md`](how_to_use_this.md) - the complete end-to-end walkthrough.
2. Read [`prd.md`](prd.md) for the design and rationale.
3. Set up the `.venv` (above).
4. Paste a YouTube / blog / paper / GitHub-repo URL and let the agent ingest it.
5. After a few sources, watch `brain/topics/` and the root `INDEX.md` get richer - that is the
   compounding.

---

## Acknowledgements

MinCha Brain stands on the shoulders of two pieces of work whose ideas it directly builds on:

- **Andrej Karpathy - [*LLM Wiki: A Pattern for Personal Knowledge Bases*](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).**
  The idea of a **persistent, compounding wiki** that sits between you and your raw sources - the
  LLM *ingests* a source and synthesizes it into interlinked notes (rather than re-retrieving raw
  docs each query), while the human curates and asks. Brain's `brain/` vault, the ingest ->
  compound flow, and the `INDEX.md` integrity checks are this pattern applied to multimodal sources.
- **Eugene Yan - [*How to Work and Compound with AI*](https://eugeneyan.com/writing/working-with-ai/).**
  The principle that **every finished artifact becomes context for the next session** - via layered
  lazy context, **annotated indexes**, taste encoded as configuration, and a verification-first
  loop. Brain's annotated root `INDEX.md`, `AGENTS.md` + `personas/` as taste-config, and the
  corroboration gate come straight from this thinking.

Any mistakes or over-reaches in adapting these ideas are mine, not theirs.

---

## License

Released under the **MIT License** - see [`LICENSE`](LICENSE). In short: use, modify, and
redistribute freely, with attribution and no warranty. Your ingested `sources/` and compounded
`brain/` are *your* content; the MIT license covers the kit (the convention, `AGENTS.md`,
`personas/`, templates), not the third-party material you learn from - respect each source's own
license and terms.
