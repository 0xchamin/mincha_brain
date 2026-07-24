# Brain - a compounding learning kit (agent-driven)

> **Brain** turns the things you learn from - **YouTube videos, blog posts, research papers, and
> code repositories** - into durable, cited, *compounding* knowledge. Paste a URL; the agent
> ingests it, understands it (the meaningful **visuals** for media - slides, diagrams, figures; or
> **traces the code** for a repo), keeps only what the other leg corroborates, distills a learning
> document, and files durable claims into a growing brain. Code sources are for **learning from** a
> repo, not building on it.

This is a **convention, not an application**. There is nothing to build or run as a service. The
GitHub Copilot CLI agent *is* the engine - driven by `AGENTS.md` + `personas/`. **Inspired by
`starter-kit`** (the starter kit agent starter kit): same three ideas (layered lazy context,
close-the-loop compounding, ground-every-claim), re-pointed from "ship code" to "learn deeply and
remember forever."

> **No agent Skills to install (by design).** The ingest flow lives in `AGENTS.md` + personas, the
> one contract every harness reads - so there are no per-harness Skill files to maintain. Packaging
> the mechanical pre-filter pipeline as a Skill is deliberate **future work**, revisited only after
> the flow is battle-tested. See [`prd.md` §10](prd.md).

> **Full design + rationale:** [`prd.md`](prd.md). **Read that first** if you want the *why*.
> **New here?** [`how_to_use_this.md`](how_to_use_this.md) is the complete end-to-end walkthrough
> (clone -> setup -> launch agent -> paste a URL -> learn -> ask).

---

## 60-second mental model

You feed sources **one at a time**. Each lives in its own `sources/<id>/` folder and walks the
same flow. Durable, corroborated claims are **promoted up** to `brain/`, so your *next* source
starts richer than this one.

```
paste URL -> capture -> understand -> distill -> compound -> ask
(video/       (transcript/  (agent VIEWs  (LEARNING.md  (brain/topics/  (known: from source
 blog/paper)   text +        visuals +     text + few    merge & cite)    unknown: synth report)
               figures)      corroborate)  visuals)
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
├── README.md           # this file
├── AGENTS.md           # behavioral contract + the paste-a-URL ingest rule (single source of truth)
├── link-agents.sh      # macOS/Linux: symlink CLAUDE.md + copilot-instructions.md -> AGENTS.md
├── link-agents.ps1     # Windows: same, once per clone (git-ignored links)
├── requirements.txt    # pip packages for the .venv (yt-dlp, faster-whisper, imagehash, pillow)
├── personas/           # role overlays: curator, code-explorer, synthesizer, fact-checker, mentor, architect
├── sources/            # ONE folder per ingested source
│   └── _TEMPLATE/      #   copy this to start a new source (media: raw/; code: MAP.md + repo/)
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

Launch Copilot CLI inside this folder and use prompts like:

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

**Where packaging does belong (later):** only the mechanical ingest **pipeline** (`yt-dlp → ffmpeg
→ imagehash`) could ship as a small `pip` package the agent calls from `.venv` - separate from the
convention. A zero-install `npx create-brain` scaffolder is possible if you ever want *multiple*
brains, but "Use this template" already covers that. See [`prd.md` §10](prd.md).

---

## Start here

1. Read [`how_to_use_this.md`](how_to_use_this.md) - the complete end-to-end walkthrough.
2. Read [`prd.md`](prd.md) for the design and rationale.
3. Set up the `.venv` (above).
4. Paste a YouTube / blog / paper / GitHub-repo URL and let the agent ingest it.
5. After a few sources, watch `brain/topics/` and the root `INDEX.md` get richer - that is the
   compounding.
