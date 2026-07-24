# AGENTS.md - Brain (agent-driven compounding learning kit)

Behavioral contract for any agent harness (Copilot CLI, Claude Code, Cursor, ...) working in
this kit. Read this first, then the relevant `sources/<id>/` and `brain/`. Brain turns things
you learn from - **YouTube videos, blog posts, research papers, and code repositories** - into
durable, cited, compounding knowledge. **Inspired by `starter-kit`; reuses its philosophy, not its
code.**

> **The agent is the engine.** There is no application. You (the agent) run the pipeline: capture
> the source, `view` visual candidates (your `view` tool *is* the vision model) or trace code
> (grep / code-intel tools), judge corroboration, distill, and file the knowledge. This is a kit
> for **learning from** sources - including repos - **not** for building on top of them. See
> `prd.md` for the full design.

## Repo-specific defaults (this clone)

| Default | Value | Used for |
|---|---|---|
| Owner | `chamin` | pre-fills the `SOURCE.md` Owner row (always this person) |
| Source naming | `YYMMDD_slug` | big-endian date sorts chronologically; `_` divides date/name, `-` between words (e.g. `260724_mcp-security-talk`) |
| Env | `.venv` in this folder | `yt-dlp`, `faster-whisper`, `imagehash`, `pillow` (see `requirements.txt`); `ffmpeg` is a system binary (macOS: `brew install ffmpeg`; Windows: `winget install Gyan.FFmpeg`); `git` for cloning code repos; **`gh` (GitHub CLI) recommended** for code sources (license, commit SHA, orient-before-clone) - optional |
| Seed topics | agents, mcp, skills, rag, agent-security, inferencing | live under `brain/topics/`; **seeds, not a whitelist - the set is open (see "Scope: topics are open")** |
| Repo clones | `sources/<id>/repo/` (git-ignored) | clone-per-source, snapshot pinned by commit SHA in `SOURCE.md` (like starter-kit's `work/`) |

## Scope: topics are open

The goal is to learn **state-of-the-art AI broadly** - agents, MCP, skills, RAG, agent-security,
inferencing, **and new topics as they emerge**. The seed topics are a starting point, **not a
closed list**. When a source teaches a **recognizable, reusable area** the brain does not yet
cover, **capture it as a new topic** (see the compound step) - do not force it into an ill-fitting
existing note. **Domain guardrail:** stay within AI / ML / agentic engineering; if a source is
clearly off-domain, **flag it and ask** rather than silently ingesting. The **architect** persona
owns the create-vs-merge call and keeps the taxonomy from ballooning.

## The paste-a-URL trigger (apply proactively)

When the user pastes a **URL** (or says "ingest this: <url>"), **start the ingest flow without
being asked**:

1. **Classify** the source: YouTube video / blog post / research paper / **code repository**
   (a GitHub / git URL).
2. **Create** `sources/<YYMMDD_slug>/` from `sources/_TEMPLATE/`; fill `SOURCE.md` (url, type,
   title, author, date; for code also **commit SHA + license**) - Owner defaults to `chamin`.
3. **Run the matching ingest flow** (see `prd.md` §5). Summary:
   - **Video:** `yt-dlp` transcript (Whisper fallback) + `ffmpeg` scene-change frames + `imagehash`
     dedup -> **~5-10 candidate frames** -> you `view` each and extract its crux.
   - **Blog:** `web_fetch` the article to `raw/` + download meaningful figures -> `view` each.
   - **Paper:** fetch the PDF, extract text to `raw/` + extract figures/tables -> `view` each.
   - **Code:** `git clone` into `sources/<id>/repo/` (git-ignored) - or `gh repo clone`; use `gh`
     to record the **license** + **pin the commit SHA** in `SOURCE.md`, and to fetch the README
     first (`gh api .../contents/README.md`) to *orient before cloning*. Adopt **code-explorer**:
     **orient** (entry points, module map, "what this repo demonstrates") -> write `MAP.md`;
     then **learn by question** - trace each concept end-to-end with grep / code-intel tools;
     **generate** diagrams (mermaid module/call/sequence) as the visual leg. Do **not** try to
     read the whole repo; orient, then trace on demand.
4. **Run the corroboration gate** (adopt **fact-checker**): keep a claim only when its two legs
   agree - for media, a visual ↔ the surrounding text; **for code, the docs/README/comments ↔
   what the code actually does** (`path:line`). Record `corroborated`/`single-leg`/`divergence`
   items as knowledge nodes in `nodes.md`, each cited (both legs when both exist). A **docs↔code
   divergence** is itself a valuable finding - record it.
5. **Distill** (adopt **curator**): write `LEARNING.md` - the distilled, transferable concept the
   source taught, + 3-8 curated visuals/diagrams, every claim cited.
6. **Compound (automatic by default).** As soon as the gate yields eligible nodes, **promote them
   without waiting to be asked**: merge durable, **transferable** claims (not source-specific
   trivia) into `brain/topics/*.md`, register them in `brain/claims.md`, add/refresh the annotated
   row in the **root `INDEX.md`** (Sources table - a **hard, non-skippable output**), and append a
   dated line to `brain/log.md`. Then **show a one-paragraph
   summary of what was promoted and run `git diff`** so the human can review - `git checkout`/`git
   revert` is the undo, so nothing is silently lost. Set `SOURCE.md` Status to `compounded`. (If you
   cannot finish the pass, set Status `awaiting-promotion` and resume it automatically next session.)
   - **New topic?** If the corroborated claims fit **no** existing topic and name a recognizable,
     reusable area, **create** `brain/topics/<slug>.md` (standard note structure), add a row to the
     **root `INDEX.md`** Topics table (Status **`emerging`** until a *second* source corroborates it),
     and log it. Adopt **architect** for the call. **Don't spawn a topic per source** - park a
     one-off under the nearest topic and promote it to its own note only once it recurs or is
     clearly distinct.
   - **Index integrity (check every compound).** Every `sources/<folder>/` must have **exactly one**
     row in `INDEX.md`'s Sources table, and every `brain/topics/*.md` exactly one Topics row. A
     source or topic on disk but not in `INDEX.md` is unfindable - add the row before finishing.

> **Pre-filter before you look, never eyeball hundreds.** For video, `ffmpeg` scene-detect +
> `imagehash` dedup MUST reduce candidates to a handful *before* you `view` them (viewing is
> token-heavy). For code, **orient then trace** - use the module map + code-intel tools to reach
> the relevant lines; never attempt to read a whole large repo.

> **The shell steps are reference, not a fixed script.** This kit is a convention: the `yt-dlp` /
> `ffmpeg` / `imagehash` / `pdftotext` commands named here and in `prd.md` §5 are the *approach* you
> assemble for the source at hand and your OS - not a checked-in pipeline. Keep frame filenames
> timestamped (`frame_<seconds>.jpg`) so citations can deep-link.

### Degrade & failure handling (don't fail silently)

| Situation | Do this |
|---|---|
| Video has no captions | Transcribe audio with `faster-whisper`; if that fails, note it and proceed transcript-light. |
| Talking-head video, no useful frames | Degrade to transcript-only; nodes are `single-leg` (needs-check), not `corroborated`. |
| Paywalled / login-required article or paper | Ingest only what you can legitimately access; set `SOURCE.md` Access + Status `blocked` or `partial`; do not bypass. |
| Repo private / huge / has submodules or Git-LFS | Prefer `gh` shallow clone; for huge repos orient from the README + a sparse checkout; never read it all. Non-GitHub git URL: clone by URL, skip `gh`. |
| Repo has no/shallow/stale docs | Code is the primary leg; nodes are `single-leg`; a docs↔code gap is a `divergence` finding, not a drop. |
| License missing/unclear (code) | Record `License: unknown` in `SOURCE.md`; keep the clone git-ignored; do not redistribute source. |
| Symlink not permitted (Windows, no Dev Mode) | `link-agents.ps1` writes a marked one-line pointer instead; the harness still reads `AGENTS.md`. |
| Ingest interrupted | Leave `SOURCE.md` Status at the last safe stage; resume from there next session. |

## How to work a source

1. **Orient** - read the source's `SOURCE.md` (for code also `MAP.md`), then the **root `INDEX.md`**
   (a prior source may already cover this), then the relevant `brain/topics/*.md`.
2. **Load a persona (automatically)** from `personas/` - infer the stage from the routing table
   below and adopt the matching persona(s) **without being asked**; announce the switch in one
   line when it changes. Personas **compose** (e.g. `curator + mentor` while distilling *and*
   teaching; `code-explorer + architect` while mapping a repo *and* structuring topics). A
   user-named persona **always overrides**; otherwise adopt from the table without asking - **ask
   only if the stage is genuinely ambiguous**. See `personas/README.md`.

   **Persona routing (auto):**

   | You do / stage | Auto-adopt | Compose with |
   |---|---|---|
   | Paste **media** URL -> capture + `view` + write `LEARNING.md` | **curator** | + fact-checker at the gate |
   | Paste **GitHub** URL -> clone / orient (`MAP.md`) / trace | **code-explorer** | + fact-checker (docs↔code); + architect if mapping topics |
   | Decide keep/drop + enforce citations (the gate) | **fact-checker** | - |
   | "Explain / teach me this" | **mentor** | + curator or code-explorer |
   | "What do I know about X?" / build study material | **synthesizer** | + mentor when teaching |
   | Shape the brain: topic taxonomy, split a note | **architect** | - |
3. **Follow the flow** - capture (`raw/` or clone into `repo/`) -> understand (`view` visuals /
   trace code) -> corroborate (`nodes.md`) -> distill (`LEARNING.md`) -> compound (`brain/`).
4. **Keep documents living** - update them *as you work*, not once at the end.
5. **Ask across the brain (from the repo root)** - known source -> answer from its
   `nodes.md`/`LEARNING.md`; unknown -> read the annotated **root `INDEX.md`** (the entry point),
   `grep` topic notes + sources, then synthesize a cited report into `reports/` (adopt
   **synthesizer**).

## Leverage your harness's built-in commands (then capture into the kit)

You (the agent) are the engine, but your **host harness** (Copilot CLI, Claude Code, Codex,
Cursor, ...) ships its own engines - deep research, planning, code review, security review,
subagents. **Use them at the matching stage, then capture the result into the matching kit file** -
the command output is ephemeral; the kit file is what compounds.

- **Prefer, in order:** the harness's **built-in** command -> a **custom** command/skill you have
  defined -> a **subagent** -> plain **shell + the kit file**. The shell is the floor and works everywhere.
- **Reach for the capability, not the command name.** Names differ per harness and drift often -
  type `/` to discover what yours calls it; the Appendix is a starting map, not gospel.

| Stage | Kit file | Capability to reach for |
|---|---|---|
| Understand a source | `context/` notes, `nodes.md`, `MAP.md` | deep research / web + repo investigation |
| Plan an ingest or repo trace | `MAP.md`, plan note | plan draft + plan critique / rubber-duck |
| Verify a claim or diagram | `nodes.md` | code review, security review, diff review |
| Synthesize across sources | `reports/` | multi-doc synthesis / long-context read |
| Teach a term | `brain/glossary.md`, `LEARNING.md` | quick explainer aside |

> Example: on a **code** source, run your harness's **code-review** / **security-review** command
> over the traced files, then distil its findings into `nodes.md` with `path:line @sha` citations -
> do not leave them in the transcript.

## Close the loop (the compounding)

Compounding is **automatic by default** (see the Compound step): once the gate yields eligible
nodes, promote them in the same pass, then show a summary + `git diff` as the undo. Promote:
- claims -> `brain/topics/<topic>.md` (merge + de-duplicate, don't stack) and `brain/claims.md`
- new terms -> `brain/glossary.md`
- one annotated row -> the **root `INDEX.md`**; one dated line -> `brain/log.md`
- durable structural decisions (topic taxonomy, a topic split) -> record ADR-style in
  `brain/decisions/` (copy `brain/decisions/0000-template.md`) - the **architect** persona owns these.

## Global rules

- **Ground every claim (hard rule).** Every non-trivial statement in a `LEARNING.md`, topic note,
  or report carries a citation: `source@timestamp` (video deep-link `...&t=494s`), `source,
  §/Figure N` (blog/paper), or `path:line @<commit-sha>` (code). No uncited claims. If
  unverified, mark it commentary, not fact.
- **The gate: two legs when you can, one leg at lower confidence when you can't.** Prefer keeping a
  claim only when **both legs agree** - a **visual ↔ surrounding text** (media) or **code ↔ its
  docs/README/comments** (code) - and mark it `corroborated` (confidence OK). When only one leg
  exists (talking-head video with no useful slide; a repo with absent/shallow docs; a figure with
  no caption), you may still keep the claim from its **single primary leg**, but mark it
  `single-leg` (confidence needs-check), never `corroborated`. Reserve high confidence for genuine
  two-leg agreement.
- **"Valid" ≠ true, and "corroborated" ≠ fact-checked.** Two legs agreeing proves only that they are
  **internally consistent** (a slide matches the narration; code matches its docs) - *not* that the
  claim is correct about the world. The human judges truth. Real confidence rises only with
  **external corroboration** (a *second source* agreeing) - note it when it happens (`claims.md`). A
  **docs↔code divergence** is a valuable finding, not a failure - record it with both citations.
- **Signal, not archive.** Keep a few high-value visuals/diagrams per document, not hundreds.
  Promote the **transferable concept**, not source-specific trivia. `brain/` is a signal store,
  not a dump. Discard raw video after processing; keep derived text + selected frames. Cloned
  repos live in git-ignored `repo/` (a snapshot, pinned by commit SHA) - never commit them.
- **Shell-first; spend tokens on judgment.** Do the mechanical work in the shell (`yt-dlp`,
  `ffmpeg`, `imagehash`, `git`, `grep`, code-intel) so it never fills the context window; reserve
  your tokens (and `view`) for what only you can do - reading a visual, judging corroboration,
  distilling. Pre-filter in shell *before* you look. Every harness has a shell - but **commands
  differ by OS** (bash on macOS/Linux vs PowerShell on Windows: `&&` chaining, venv activation, and
  `ffmpeg` quoting all differ), so pick the right dialect or use a Python helper for the non-trivial
  pipeline.
- **Prefer purpose-built CLIs; fall back gracefully (encouraged, not required).** When a mature
  CLI does the job, use it instead of hand-rolling HTTP or parsing: **`gh`** for GitHub sources
  (repo metadata, **license**, default branch, **pin the commit SHA** via
  `gh api repos/{owner}/{repo}/commits/HEAD`, `gh repo clone`, or fetch a single file to *orient
  before cloning*); `git`, `yt-dlp`, `ffmpeg` for the core flow; `pdftotext`/`pandoc` for
  paper/article text. **Check availability first** (`gh --version`); if the tool is absent or a
  harness forbids shell, fall back to the API / `web_fetch`. Only the `requirements.txt` packages
  plus `ffmpeg` + `git` are hard dependencies - everything else is "use if present," never a
  blocker.
- **Living documents.** Re-read at the start of a step; rewrite at the end. A topic note that
  drifted from the sources is a bug - fix it.
- **Flag confidence** on anything non-obvious (OK / needs-check / open-question).
- **Diagrams** use mermaid.live syntax (validate before commit; avoid `<> {} ;` inside sequence
  message text).
- **Teach as you go.** When a key term surfaces, explain it inline `> 💡 <1-2 sentences>` and
  capture it in `brain/glossary.md` (the **mentor** persona owns deeper teaching).

## Writing & style

- Never use the em dash. Use a plain dash `-`.
- Name sources `YYMMDD_slug` (see defaults). Use `_` only as the date/name divider, `-` between
  words.
- Respect source ToS, access, and **license**; ingest only what you can legitimately access.
  Note access limits and (for code) the repo license + commit SHA in `SOURCE.md`. This kit is for
  **learning from** sources, not redistributing them - keep cloned repos git-ignored.
  Personal-use, rate-limited fetching only.

> Inherits nothing external; this is the root contract. Per-source overrides (rare) go in that
> source's `SOURCE.md`.

## Appendix - one contract, every harness (verify; commands drift)

**`AGENTS.md` (this file) is the single source of truth** - never duplicate it into tool-specific
files. Some harnesses read it natively; the two that expect a different filename get a
**git-ignored symlink** created once per clone by `link-agents.sh` (macOS/Linux) or
`link-agents.ps1` (Windows). Commands differ per harness and drift - **type `/` to discover what
yours calls things**; treat this as a starting map.

| Harness | Finds this contract via | Handy built-ins (stage) | Custom commands live in |
|---|---|---|---|
| GitHub Copilot CLI | `AGENTS.md` (native) | `/research` (understand), `/plan` `/rubber-duck` (plan), `/review` `/security-review` (verify), `/pr` | - |
| GitHub Copilot (IDE / coding agent) | `.github/copilot-instructions.md` (symlink -> `AGENTS.md`) | chat, code review, `@workspace` | `.github/prompts/` |
| Codex CLI | `AGENTS.md` (native; also `~/.codex/AGENTS.md`) | `/review` `/diff` (verify), `/compact` | `~/.codex/prompts/` |
| Claude Code | `CLAUDE.md` (symlink -> `AGENTS.md`) | `/plan` (plan mode), `/review` `/code-review` `/security-review` `/diff` (verify), `/agents` (subagents) | `.claude/commands/` |
| Cursor | `AGENTS.md` (native; directory-wide) | Agent / Skills / custom commands | `.cursor/commands/` |

Anything not built in (a `/research` or `/prd` you want everywhere) can be authored as a **custom
command / skill** in that harness's folder above, wrapping the matching step of this contract -
then still **capture its output into the kit file**, per "Leverage your harness's built-in
commands."
