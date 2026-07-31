# AGENTS.md - Brain (agent-driven compounding learning kit)

Behavioral contract for any agent harness (Copilot CLI, Claude Code, Cursor, ...) working in
this kit. Read this first, then the relevant `sources/<id>/` and `brain/`. Brain turns things
you learn from - **YouTube videos, blog posts, research papers, and code repositories** - into
durable, cited, compounding knowledge.

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
| Repo clones | `sources/<id>/repo/` (git-ignored) | clone-per-source, snapshot pinned by commit SHA in `SOURCE.md` |
| Kit scripts | `tools/ingest.py` (mechanical toolbox), `validate.py` (contract type checker) | the only two frozen scripts; everything else is assembled per source |

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
     dedup -> **~5-10 candidate frames** -> you `view` each and extract its crux. **Use
     [`tools/ingest.py`](tools/ingest.py) for the mechanical steps** (`transcript`, `probe`,
     `frames`, `sheet`) rather than re-deriving them - see "The mechanical toolbox" below. The
     visual leg is **on by default but skippable** - see "The visual leg".
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
5. **Deep research (optional - only when the user asks).** If the user says **"deep research"**
   alongside the URL (or invokes the harness's research command), run an external-evidence pass
   **after the gate and before distilling** - see "Deep research on request" below. **Never
   automatic:** most sources do not earn it, and it is slow and token-heavy.
6. **Distill** (adopt **curator**): write `LEARNING.md` - the distilled, transferable concept the
   source taught, + 3-8 curated visuals/diagrams, every claim cited.
7. **Compound (automatic by default).** As soon as the gate yields eligible nodes, **promote them
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
   - **Run `python3 validate.py` before you show the `git diff`.** It is the type checker for this
     contract (see "Validating the contract" below) and it is **not optional** - a compound pass
     that leaves the validator failing is not finished.

> **Pre-filter before you look, never eyeball hundreds.** For video, `ffmpeg` scene-detect +
> `imagehash` dedup MUST reduce candidates to a handful *before* you `view` them (viewing is
> token-heavy). For code, **orient then trace** - use the module map + code-intel tools to reach
> the relevant lines; never attempt to read a whole large repo.

> **Prune uncited frames after distilling (signal, not archive).** `visuals/` keeps **only frames a
> knowledge node or the report actually cites** - not every extracted/deduped candidate. As the last
> step of the distill/compound pass, grep each `visuals/*.jpg` name across `nodes.md`, `LEARNING.md`,
> and `brain/topics/*.md`; **delete the zero-hit frames** and update the `SOURCE.md` frame count. Raw
> video/captions stay git-ignored in `raw/` and are discardable.

> **The shell steps are reference, not a fixed script.** This kit is a convention: the `yt-dlp` /
> `ffmpeg` / `imagehash` / `pdftotext` commands named here and in `prd.md` §5 are the *approach* you
> assemble for the source at hand and your OS - not a checked-in pipeline. Keep frame filenames
> timestamped (`frame_<seconds>.jpg`) so citations can deep-link.

## The mechanical toolbox (`tools/ingest.py`)

> **Why this exists.** "Generate code on the fly" is right when variation is a *feature* - mid-ingest
> you may abandon phash dedup and switch to transcript-anchored extraction, and a rigid script would
> fight you. It is wrong when variation is a *bug*. VTT parsing has no reason to differ between
> videos, and **ADR-0003's `<= 3 distinct frames` threshold is meaningless if every agent computes
> "distinct" with a different scene threshold or hash distance.** Generate what should vary; freeze
> what should not.

**A toolbox, not a pipeline.** Independent subcommands you compose per source. There is deliberately
no `--url do-everything` entrypoint - "the shell steps are reference, not a fixed script" still
holds, and assembly stays your job.

| Command | Does | Needs |
|---|---|---|
| `python3 tools/ingest.py transcript <in.vtt> <out.txt>` | de-duplicates YouTube's rolling captions into timestamped blocks (`[MM:SS t=NNN] ...`) so `&t=` citations land right | **stdlib only** |
| `python3 tools/ingest.py probe <video.mp4>` | **the ADR-0003 static-video probe** - scene-detect + phash -> `STATIC` / `RICH` + the exact `SOURCE.md` line to record. On `STATIC` it also writes a **9-frame confirmation sheet** to `view` first (ADR-0006) - the verdict is advisory | ffmpeg + `.venv` |
| `python3 tools/ingest.py frames <video.mp4> --at 233,290 --out DIR` | extracts frames at given seconds (`--crop` for the slide area) | ffmpeg |
| `python3 tools/ingest.py sheet DIR --out STEM` | tiles frames into contact sheets - **triage 17 candidates in 1-2 `view` calls instead of 17** | ffmpeg |

**Run `probe` before deciding the visual leg.** Do not eyeball it, and do not re-derive the
threshold: a verdict computed with different constants is not comparable to any previous source's.

> **What must never move into this file: judgement.** Reading a slide, gating a claim, deciding which
> frames earn their place, calling a docs-vs-code divergence - those stay here and in `personas/`.
> The toolbox crops images; it does not decide what they mean. Same line `validate.py` draws:
> **form is code, judgement is prose.**

> **Still assemble per source.** `yt-dlp` invocations stay ad hoc (format selection genuinely varies).
> If a step needs to differ for the source at hand, differ - then if you write the same thing a third
> time, add it to the toolbox rather than to your scratch directory.

## Validating the contract (`validate.py`)

> **Why this exists.** This kit is a **convention, not an application** - the pipeline, the gate and
> the schema are prose, and the agent is the runtime. That is the design's strength and its one
> structural weakness: **prose has no compiler.** Nothing catches a stale `INDEX.md` row, an uncited
> frame that survived the prune, a claim promoted without a citation, or a broken cross-link. Those
> do not fail loudly; they accumulate. `validate.py` is the missing gate.

**Run `python3 validate.py` before showing the `git diff` at the end of any compound, research or
close-the-loop pass.** Stdlib only - no venv needed. CI runs it on every push and PR
(`.github/workflows/validate.yml`). Exit code 1 means the pass is not finished.

What it enforces (all of it already required above): INDEX integrity both ways; legal `SOURCE.md`
Status / Visual leg, and Topics that name real notes; every kept frame cited somewhere; legal topic
Status; `log.md` chronology; every claim carrying a citation and naming a real topic; unique ADR
numbers with Status + Date; resolving relative links; balanced mermaid fences; no em dashes.

> **The validator is subordinate to this file.** If a check and `AGENTS.md` disagree, `AGENTS.md`
> wins and the check is the bug. It enforces the contract; it does not define it.

> **What it cannot do.** It checks *form*, never *judgement*. It cannot tell you whether a claim is
> corroborated, whether a frame earns its place, whether a topic should split, or whether an
> external source is genuinely independent. Those stay with the fact-checker and architect personas.
> It also cannot catch a `log.md` entry misordered *within a single day* - the ordering that has
> actually gone wrong in practice. A green validator means the shape is right, not that the thinking
> is.

## The visual leg (on by default, skippable)

> **Why this switch exists.** Extracting and `view`ing frames is the most token-expensive step in a
> media ingest. On a slide-heavy talk it is the whole point - the slides *are* the second leg. On a
> podcast, a webcam interview, or a fireside chat, the picture never changes and every token spent
> looking at it buys nothing.

**Default: analyse the visual leg.** Three ways it is skipped, in priority order:

1. **The user opts out.** "don't analyze video", "skip the frames", "transcript only", or similar,
   at any point before distilling. Explicit instruction always wins - skip even the probe.
2. **The static-video probe says there is nothing to see, *and you confirmed it*.** Run
   **`python3 tools/ingest.py probe <video>`** - scene-detect + `imagehash` dedup, the *first* step
   of the pipeline anyway, costing **no tokens**. It prints `STATIC` / `RICH` and the exact
   `SOURCE.md` line to record. If the whole video yields **<= 3 distinct frames** it reports
   `STATIC`. (The threshold is a heuristic - for calibration, `260725_12-factor-agents` gave 19
   distinct.) **Use the tool, not a hand-rolled equivalent:** its scene threshold and hash distance
   are fixed constants, and a verdict computed with different ones is not comparable across sources.

   > ⚠️ **`STATIC` is advisory, never dispositive** ([ADR-0006](brain/decisions/0006-static-probe-is-advisory.md)).
   > **Scene detection measures whole-frame delta**, so a **templated slide deck** - fixed background,
   > logo, speaker inset, track footer, with the slide body a minority of the pixels - reads as static
   > while every slide changes. This has happened twice
   > (`260726_dont-ship-skills-without-evals`: `candidates=3` on ~20 dense slides;
   > `260725_12-factor-agents` at the dedup stage). On `STATIC` the tool now writes a
   > **9-frame confirmation sheet** spread across the runtime and prints its path: **`view` it before
   > honouring the verdict.** Differing slides mean **override** - extract transcript-anchored frames
   > and record the override in `SOURCE.md`.
   >
   > **Why the extra call is worth it:** the two errors are not symmetric. A false `RICH` wastes one
   > `view`. A false `STATIC` destroys the source's second leg and cannot be cheaply undone, because
   > the degrade rule below forbids retro-marking nodes `corroborated`. Only after the sheet agrees do
   > you **auto-degrade to transcript-only and say so in one line.** Do not `view` full-resolution
   > webcam stills to re-confirm what the sheet already settled.
3. **Capture fails** - no video stream, download blocked. Note it and proceed.

> **Never skip the probe to save time.** It is the cheapest signal available and it is what makes the
> default safe. Skipping frames is a *judgement*; skipping the probe is *guessing*. And **never
> honour a `STATIC` without the confirmation sheet** - that is guessing one level up.

### The cost of skipping, which is never silent

Dropping the visual leg means **every node from that source is `single-leg` by construction** - the
source can no longer produce an internally `corroborated` claim, because there is only one leg to
corroborate with. That is acceptable, often correct, and must be **recorded, not discovered**:

- Set `SOURCE.md` **Visual leg** to `skipped (user)` / `skipped (static probe: N distinct frames)` /
  `analysed (N frames kept)`.
- Gate every node `single-leg`, confidence `needs-check`. Do **not** mark anything `corroborated` on
  transcript agreement alone - a transcript agreeing with itself is not two legs.
- Say so in one line when it happens, so the human can override.

> **Deep research is the natural complement.** A transcript-only source has one leg; the way back to
> two is **external** evidence, not a harder look at the video. If a skipped-visual source matters,
> reach for "deep research" on its nodes.

### Applies to the other media types too

Same rule, same recording: a blog post with only decorative images, or a paper whose figures are
unreadable at source resolution, degrades to text-only with the same `single-leg` consequence. Code
sources are unaffected - their visual leg is *generated* from the code, and generating a diagram is
cheap.

## Deep research on request (external evidence)

> **Why this exists.** The corroboration gate buys *internal* consistency - a slide agrees with the
> narration, code agrees with its docs. That is not truth (see Global rules). Real confidence rises
> only with **external** corroboration. Deep research is the mechanism: it reaches outside the source
> to test what the source claims, and to attach the intellectual context that makes a claim land -
> the prior work, the competing framing, the name the field already has for this thing.

**Trigger (never automatic).** The user says **"deep research"** with the URL, or asks for it on an
already-ingested source, or invokes the harness's research command. Adopt **fact-checker +
synthesizer** (+ **mentor** when the goal is teaching a concept).

**Target the nodes, not the subject.** Open-ended "research <topic>" returns adjacent reading and
makes you a summarizer. Research **specific gated claims by node ID** from `nodes.md`, prioritising:
`single-leg` nodes, anything marked `needs-check`, recorded divergences, and the `LEARNING.md` open
questions. Each finding resolves to one of four verdicts:

| Verdict | Meaning | Effect |
|---|---|---|
| `supports` | An **independent** source agrees | Node confidence may rise; cite the external source in `brain/claims.md` |
| `contradicts` | A credible source disagrees | **A finding, not a failure** - record both, flag the conflict |
| `refines` | Broadly agrees but bounds/qualifies the claim | Rewrite the claim with the qualifier |
| `no-evidence` | Nothing credible found either way | **Also informative** - the claim is one practitioner's experience; say so |

**Read the brain before you read the web.** `grep` the root `INDEX.md`, `brain/topics/*.md` and
`brain/claims.md` first - a prior source may already answer this, and the link between them is worth
more than a fresh fetch.

### Source credibility tiers (record the tier with every citation)

| Tier | What | How to weigh it |
|---|---|---|
| **T1** | Peer-reviewed papers, official specs/standards, official API/product docs | Strongest for *how something works*. |
| **T2** | First-party engineering writing (Anthropic, OpenAI, DeepMind, Cursor, ...) and official repos | Authoritative **about their own system**; **positioned** on the wider field. Flag when a vendor is cited on a topic they sell. |
| **T3** | Preprints (arXiv) | Good for recency and for the field's vocabulary; **not peer-reviewed** - always label as preprint, never treat as settled. |
| **T4** | Practitioner experience: conference talks, engineering blogs, respected individual writers | Same evidential class as most sources in this brain - experience reports, rarely measured. |
| **T5** | Aggregators and directories (Pulse MCP, awesome-lists, doc hubs) | Use for **discovery**; cite the primary source they point to, not them. |

> **The independence rule (hard).** External evidence only counts as corroboration when it is
> **independent** of the original source - not the same author, organisation, or commercial interest.
> A talk's companion repo, a vendor blog restating the vendor's own conference talk, or a paper by
> the same lab is **the same leg wearing a different hat**. Record it, but never let it raise
> confidence. When independence is unclear, say so.

### Calibration: aim one level above the source

The reader already knows the fundamentals of LLMs and agents. **Do not write 101 explainers.** The
target is the concept *one level above* the source - the frame that makes its claim feel inevitable
rather than arbitrary.

> **Take the cross-domain hop.** The most valuable framing is often the established name in an older
> discipline - cognitive science, distributed systems, PL theory, control theory, information
> science. (Example: agent skill design is a rediscovery of **procedural memory**.) Searching only AI
> sources will never surface this, so search for it deliberately.

### Budget, output, and honesty

- **Budget (default):** ≤ 8 searches and ≤ 12 fetches per pass. **Stop early** when two independent
  T1-T3 sources agree, or when a pass surfaces nothing new. Record the budget actually used.
- **Never interrupt with clarifying questions.** Make reasonable assumptions, state them explicitly
  in a **Confidence assessment** section at the end of the note. (Pattern borrowed from Copilot
  CLI's `/research`.)
- **Output is a permanent kit file, not a session artifact:**
  `sources/<id>/context/<NN>_<slug>.md`, one note per pass, numbered in order. Copilot CLI writes
  research to a throwaway session directory; this kit does the opposite - **ephemeral output that is
  not captured into a kit file did not happen.**
- **Feed the findings back** in the same pass: update the affected node's confidence in `nodes.md`
  (pointing at the context note), cite external support in `brain/claims.md`, add new terms to
  `brain/glossary.md`, and let `LEARNING.md` cite the context note rather than absorbing it.

> **Keep research out of `LEARNING.md`'s body.** `LEARNING.md` answers exactly one question - *what
> did this source teach?* Blending external findings into it destroys the distinction between "the
> author claims this" and "the field thinks this", which is the whole point of citing. External
> evidence lives in `context/`; durable cross-source synthesis lives in `brain/topics/*.md`.

### Degrade & failure handling (don't fail silently)

| Situation | Do this |
|---|---|
| Video has no captions | Transcribe audio with `faster-whisper`; if that fails, note it and proceed transcript-light. |
| Talking-head video, no useful frames | The static probe catches this: <= 3 distinct frames after dedup -> **`view` the confirmation sheet it writes (ADR-0006)**, then auto-degrade to transcript-only and record `Visual leg: skipped (static probe)`. Nodes are `single-leg` (needs-check), never `corroborated`. |
| **Probe says `STATIC` but the sheet shows changing slides** | A **false STATIC** - a templated deck defeating whole-frame scene detection (ADR-0006). **Override**: extract transcript-anchored frames, record `Visual leg: analysed (N frames kept) - static probe overridden` in `SOURCE.md`, and say why. Do **not** file a bug against the constants; the metric is wrong for this input class, not mis-tuned. |
| User says "don't analyze video" / "transcript only" | Skip frame extraction **and the probe**; record `Visual leg: skipped (user)`; gate every node `single-leg`; say in one line that internal corroboration is now unavailable and deep research is the way back to two legs. |
| Visual leg skipped but the source turns out to matter | Do **not** retro-mark nodes `corroborated`. Either re-run the visual leg and re-gate, or get the second leg externally via deep research. |
| Paywalled / login-required article or paper | Ingest only what you can legitimately access; set `SOURCE.md` Access + Status `blocked` or `partial`; do not bypass. |
| Repo private / huge / has submodules or Git-LFS | Prefer `gh` shallow clone; for huge repos orient from the README + a sparse checkout; never read it all. Non-GitHub git URL: clone by URL, skip `gh`. |
| Repo has no/shallow/stale docs | Code is the primary leg; nodes are `single-leg`; a docs↔code gap is a `divergence` finding, not a drop. |
| License missing/unclear (code) | Record `License: unknown` in `SOURCE.md`; keep the clone git-ignored; do not redistribute source. |
| Symlink not permitted (Windows, no Dev Mode) | `link-agents.ps1` writes a marked one-line pointer instead; the harness still reads `AGENTS.md`. |
| Ingest interrupted | Leave `SOURCE.md` Status at the last safe stage; resume from there next session. **If it stopped at `capture` (nothing gated, `SOURCE.md` still template) - and `ls -la` shows no recent writes, because an unfilled template does not mean no live process - move the folder to git-ignored [`staging/`](staging/README.md) instead of leaving it in `sources/`** - `sources/<id>/` is `validate.py`'s namespace and every folder there is checked as a *finished* source, so a bare capture can only be silenced by faking an INDEX row or deleting the download. **A capture becomes a source when it is distilled, not when it is downloaded.** Move it back when you intend to finish it. |
| Deep research finds nothing credible | Record `no-evidence` in the context note - that the claim rests on one practitioner's experience **is** the finding. Do not pad with weak T4/T5 hits. |
| Deep research finds only non-independent sources | Record them, cite them, but **do not raise confidence** (independence rule). Say plainly that corroboration is still missing. |
| Sources conflict | Keep **both**, cite both with tiers, flag the conflict in the context note and in the topic note's "Open questions / conflicts". Do not silently pick a winner. |
| No web access / search unavailable | Say so, skip the research step, leave `SOURCE.md` Status at `distill`; do not fabricate citations or work from memory. |

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
   | "Deep research" -> external evidence for gated nodes (`context/`) | **fact-checker + synthesizer** | + mentor when the goal is teaching the concept |
   | "Explain / teach me this" | **mentor** | + curator or code-explorer |
   | "What do I know about X?" / build study material | **synthesizer** | + mentor when teaching |
   | Shape the brain: topic taxonomy, split a note | **architect** | - |
3. **Follow the flow** - capture (`raw/` or clone into `repo/`) -> understand (`view` visuals /
   trace code) -> corroborate (`nodes.md`) -> *(optional, on request)* deep research (`context/`)
   -> distill (`LEARNING.md`) -> compound (`brain/`).
4. **Keep documents living** - update them *as you work*, not once at the end.
5. **Ask across the brain (from the repo root)** - known source -> answer from its
   `nodes.md`/`LEARNING.md`; unknown -> read the annotated **root `INDEX.md`** (the entry point),
   `grep` topic notes + sources, then synthesize a cited report into `reports/` (adopt
   **synthesizer**).

## You are probably not the only writer (re-read before you compound)

> **Why this exists.** On 2026-07-31 two agent sessions ingested the memory/dreaming pair
> concurrently. One created `brain/topics/memory.md` and ADR-0007 while the other was mid-capture on
> the source that would merge into it, renamed that source's folder, and briefly moved it to
> `staging/`. Nothing was lost, but only because both noticed. **This is claim 61 happening to this
> repo:** the moment memory has a second writer, it needs versioning, attribution and arbitration.

**Git already supplies the machinery** - commits are attribution, history is versioning, a merge
conflict is the arbitration. There is nothing to build. What is needed is the convention, because
the failure is silent: an agent holding a copy of `claims.md` read forty minutes ago will happily
number its claims from a ceiling that has since moved.

**Source-local files are always safe.** `SOURCE.md`, `nodes.md`, `LEARNING.md`, `MAP.md`,
`visuals/`, `context/` belong to one source and one session. Write them whenever.

**Before touching anything shared, re-read it from disk.** That means `INDEX.md`,
`brain/claims.md`, `brain/glossary.md`, `brain/log.md`, `brain/topics/*.md` and `brain/decisions/`.
Specifically:

- **Take every number from disk, never from context** - the next claim number, the next `S<n>`
  source label, the next ADR number. These are the values most likely to be stale and the ones that
  silently collide.
- **`git log --oneline -10` and `git status`** before the compound step. Commits that landed since
  you started are the fastest signal that a topic note was rewritten under you.
- **A topic note that already exists is a merge target, not a naming collision.** Merge into it and
  update its Status and source count; **never create a second note for the same topic.**
- **If a source folder vanishes mid-ingest, look in `staging/` before re-capturing.** An unfilled
  `SOURCE.md` reads as an abandoned capture to another agent, and moving it there is the correct
  behaviour under the degrade table - it is not a lost folder.
- **A superseded duplicate capture goes to git-ignored `staging/`, never `rm -rf`.** Deleting is the
  human's call.

> **Do not build a locking scheme for this.** Scaffolding encodes an assumption that expires
> (claim 31), and this one has fired once. Re-reading before writing is the whole mitigation.

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
| Understand a source | `context/` notes, `nodes.md`, `MAP.md` | deep research / web + repo investigation (see "Deep research on request" - tiers, independence rule, budget) |
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

## Dreaming on request (the reconciliation pass)

> **Why this exists, and it is the kit taking its own medicine.** Ingest writes to `brain/` **while
> doing something else** - finishing a source. That write is locally optimal and globally
> unexamined: it merges into the topic note in front of it and never asks whether a claim it just
> added contradicts one promoted three sources ago. This is exactly the diagnosis
> [`brain/topics/memory.md`](brain/topics/memory.md) records from S6 and S7 - **memory updated
> in a locally optimal way that is not globally optimal, producing duplication and fragmentation**
> (claim 59, `n10`) - pointed at this repo. `validate.py` does not catch it: it checks **form**, and
> this is **drift**. A green validator means the shape is right, not that the thinking is.

**Dreaming is the global reconciliation pass over `brain/` itself.** Not an ingest, not a research
pass, not lint. It reads across every topic note, `claims.md`, `glossary.md` and `INDEX.md` and asks
one question: **is what this brain believes still coherent with itself?**

**Trigger (never automatic).** The user says **"dream"**, or invokes the harness command. Adopt
**architect + fact-checker** - the architect owns merge/split/status calls, the fact-checker owns
claim verdicts.

> **It must never run as part of an ingest, and this is a design rule, not a preference.** An agent
> finishing a source is holding two objectives - land this source, and keep the brain coherent - and
> it will trade the second against the first silently, because the first is the one with a visible
> finish line (claim 59). Curation gets its own invocation and its own objective, or it gets a token
> effort. **Same reason the generator and the evaluator are separate processes (claim 33).**

### What a pass looks for

| Class | The question | Typical finding |
|---|---|---|
| **Contradiction** | Do two claims disagree? Did a later source overturn an earlier one? | Keep both, cite both, flag the conflict - never silently pick a winner |
| **Duplication / fragmentation** | Is one idea stated in two topic notes, or as two claims? | Merge and de-duplicate; the contract already says *don't stack* |
| **Stale confidence** | Is a claim still `emerging` after a second source corroborated it? Is a `needs-check` now resolved? | Promote or demote the confidence, citing what changed |
| **Stale status** | Is a topic `emerging` on two corroborating sources, or `seed` with one? | Advance it, and record an ADR if the call is a judgement |
| **Orphans** | A claim no topic note references; a topic claim with no `claims.md` row; a source feeding nothing | Wire it up or drop it - an unreferenced claim is invisible |
| **Closed open questions** | Did a later source answer an "Open questions" bullet nobody struck through? | Strike it through with the date and the closing source |
| **Superseded framing** | Was a synthesis section written when the brain knew less? | Rewrite it. **This has already happened once** - `memory.md` kept "this topic has zero measurements" after the charts were recovered, and needed a fix commit |
| **Drift from source** | Does the citation still support the claim as written? | Correct the claim, not the citation |

### How a pass runs

1. **Read the whole brain first.** `INDEX.md`, every `brain/topics/*.md`, `claims.md`, `glossary.md`,
   `brain/decisions/`, and the tail of `log.md`. **Do not sample.** The entire value of being out of
   band is that you can afford to read everything, which is the one thing an ingest cannot.
2. **Collect findings before changing anything**, each naming the files and claim IDs involved.
3. **Write the pass note** to `brain/dreams/<NNNN>-<YYMMDD>.md`, numbered in order. One note per
   pass, permanent. **Ephemeral output not captured into a kit file did not happen.**
4. **Apply the changes** in the same pass - this is a reconciliation, not a report - then run
   `python3 validate.py` and show the `git diff`.
5. **Propose, do not impose.** Anything that changes what the brain *believes* (dropping a claim,
   splitting a topic, reversing a confidence) goes in the note as a **proposal with its reasoning**
   and is applied only if it is a clear defect. **When it is a judgement call, ask.** The human
   adopts; `git revert` is the undo.

> **Findings are the point, including "nothing found".** A pass that surfaces no drift is a real
> result and gets its note - it is evidence the compounding is holding. **Do not manufacture
> findings to justify the pass.**

> **What dreaming must not do:** re-litigate the gate. Whether a node was corroborated is settled in
> the source's `nodes.md` by the fact-checker at ingest time. Dreaming reconciles what was
> **promoted**; it does not re-open source-local judgements, and it never edits a `nodes.md`.

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
- **Every diagram carries a walkthrough (hard rule).** A diagram in a `LEARNING.md`, topic note or
  report is **teaching material**, and a picture dropped in without explanation teaches nobody - the
  reader who already understands it does not need it, and the reader who does not is no better off.
  Write the walkthrough **as a mentor ramping up an engineer**, immediately after the diagram:

  1. **Orientation** (1-2 sentences) - how to read it: direction of flow, what the shapes and colours
     mean. If colour carries meaning, give a legend. Do not make the reader reverse-engineer your
     notation.
  2. **The crux** (one bold sentence) - the single idea this diagram exists to convey. **If you
     cannot name it in one sentence, delete the diagram** - it is decoration.
  3. **Why it is shaped this way** (2-4 sentences) - the design rationale, and what would go wrong
     with a different shape. This is the part that actually teaches: it transfers *judgement*, not
     topology.
  4. **Provenance** - `synthesized from n4, n8` for a diagram you generated, or the normal citation
     if you lifted it. Never let generated material read as sourced evidence.

  > **The anti-pattern: narrating the arrows.** "A calls B, which returns to C" restates what the
  > reader can already see and teaches nothing. Explain what is *not* visible - why the boundary sits
  > there, what the shape rules out, which box is the expensive one, what breaks at scale.
- **Teach as you go.** When a key term surfaces, explain it inline `> 💡 <1-2 sentences>` and
  capture it in `brain/glossary.md` (the **mentor** persona owns deeper teaching).

## Writing & style

- **Commit messages use [Conventional Commits](https://www.conventionalcommits.org):
  `<type>: <subject>`.** Set by this repo's first commit and **binding on agents and contributors
  alike** - do not fall back to a bare descriptive subject. Mapping for this kit:

  | Type | Use for |
  |---|---|
  | `docs:` | ingesting a source, adding a report, promoting claims into `brain/` - the normal compounding pass |
  | `feat:` | a change to the kit contract itself: a new stage, switch, persona, or capability (`AGENTS.md`, `prd.md`, a new command) |
  | `fix:` | correcting a wrong claim, a bad citation, a broken link, a stale `INDEX.md` row |
  | `chore:` | templates, tooling, `.gitignore`, dependencies, housekeeping |
  | `refactor:` | restructuring notes without changing what they claim (e.g. splitting a topic note) |

  Keep the **detailed body** - what was promoted, what was rejected and why. The subject line is for
  scanning; the body is where the reasoning survives.
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
| Claude Code | `CLAUDE.md` (symlink -> `AGENTS.md`) | `/plan` (plan mode), `/review` `/code-review` `/security-review` `/diff` (verify), `/agents` (subagents). **No built-in research** - this kit ships [`.claude/commands/research.md`](.claude/commands/research.md) | `.claude/commands/` |
| Cursor | `AGENTS.md` (native; directory-wide) | Agent / Skills / custom commands | `.cursor/commands/` |

Anything not built in (a `/research` or `/prd` you want everywhere) can be authored as a **custom
command / skill** in that harness's folder above, wrapping the matching step of this contract -
then still **capture its output into the kit file**, per "Leverage your harness's built-in
commands."
