# BUILD.md - build Brain from scratch, from this file alone

> **Generated 2026-08-02 from commit `9e5f9d6`** by `tools/make_build_doc.py`. Do not hand-edit: edit the
> source files in the reference clone and regenerate, or your copy silently diverges from the kit
> it claims to build.

**Brain is an agent-driven compounding learning kit.** You paste a URL - a YouTube talk, a blog
post, a paper, or a GitHub repo - and the agent captures it, reads the slides or traces the code,
keeps only claims whose two independent legs agree, distills a learning document, and promotes the
durable parts into living topic notes. Every claim carries a citation. Ingest thirty sources and
the thirtieth starts richer than the first.

**There is no application.** The agent is the runtime; the kit is a contract written in Markdown
plus three small frozen scripts. That is why this file can rebuild it.

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
mkdir -p brain/topics brain/decisions sources/_TEMPLATE/raw sources/_TEMPLATE/visuals \
         sources/_TEMPLATE/context personas tools reports .github/workflows .claude/commands
git init
```

Directories:

```
brain/
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
.claude/commands/
```

---

## 5. The files (byte-exact)

### 5.1 The contract (read this one yourself)

> This is the kit. Everything else supports it. Read it before your first ingest -
> not because you must memorise it, but because it is the file your agent obeys, and
> you should know what you are agreeing to.

#### `AGENTS.md`

``````markdown
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
| Kit scripts | `tools/ingest.py` (mechanical toolbox), `validate.py` (contract type checker), `tools/build_site.py` (the mobile reader) | the only three frozen scripts; everything else is assembled per source |

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
6. **Distill** (adopt **curator + mentor**): write `LEARNING.md` - the distilled, transferable concept
   the source taught, + 3-8 curated visuals/diagrams, every claim cited. **Mentor is unconditional at
   this step**, for media and code alike - a `LEARNING.md` is written to be learned from, so the
   teaching voice is the default rather than a mode you switch on.
   - **Voice: an AI architect ramping up a new senior engineer.** Strong reader, no hand-holding on
     engineering, **new to this subject**. Give the mental model and the design rationale, not steps;
     **teach judgement, not topology**; and **earn every claim**, labelling weak evidence where it is
     used rather than in a caveat at the end.
   - **Calibration: enough fundamentals, never 101.** Teach every fundamental *the subject* needs and
     none of the field's. *(Not the same as the deep-research calibration below, which aims one level
     **above** the source - that governs `context/` notes.)*
   - **Order the walkthrough as a ramp, not as the source's running order**: why you should care ->
     the fundamentals in dependency order -> the crux -> the consequences. See
     `sources/_TEMPLATE/LEARNING.md`.
   - **The section skeleton is required, not suggested** - see
     ["Writing a `LEARNING.md`"](#writing-a-learningmd-the-required-shape) below for the ordered
     sections, the **scaffolding rule** that keeps supplied background distinct from source evidence,
     and the three techniques (derive don't list; trace one instance; ask before revealing).
     **Discharging the `💡` asides and the diagram walkthrough is not sufficient** - that has already
     produced a document that met every stated obligation and still taught nobody new.
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
   - **If you touched `AGENTS.md`, `personas/`, `sources/_TEMPLATE/` or a frozen script, run
     `python3 tools/make_build_doc.py` in the same pass.** `BUILD.md` embeds all of them verbatim,
     and the staleness check fires *after* the commit exists - so a miss turns `main` red rather
     than blocking the mistake. This has happened twice.

> **Pre-filter before you look, never eyeball hundreds.** For video, `ffmpeg` scene-detect +
> `imagehash` dedup MUST reduce candidates to a handful *before* you `view` them (viewing is
> token-heavy). For code, **orient then trace** - use the module map + code-intel tools to reach
> the relevant lines; never attempt to read a whole large repo.

> **A kept frame must be taught, not merely gated (signal, not archive).** `visuals/` keeps **only
> frames the source's own `LEARNING.md` cites** - not every extracted/deduped candidate, and **not
> frames cited only in `nodes.md`.** As the last step of the distill/compound pass, grep each
> `visuals/*` name across that source's `LEARNING.md`; **delete the zero-hit frames** and update the
> `SOURCE.md` frame count. Raw video/captions stay git-ignored in `raw/` and are discardable.
>
> **Why the rule tightened (2026-08-02).** It previously accepted a citation from `nodes.md` or a
> topic note, and the retrofit programme found **16 frames across four sources that were extracted,
> deduped, `view`ed, gated and kept - and that no reader ever saw**, because the prose never used
> them. Among them were an opening hook, two core evidence slides, and the frame `memory.md` itself
> calls the best single visual on its topic. **The gate was working; the prose was not spending what
> the gate produced.** A frame that only a `nodes.md` row cites is an archive entry, which is the
> thing this rule exists to prevent. `validate.py` enforces the tightened version.

> **The shell steps are reference, not a fixed script.** This kit is a convention: the `yt-dlp` /
> `ffmpeg` / `imagehash` / `pdftotext` commands named here and in `prd.md` §5 are the *approach* you
> assemble for the source at hand and your OS - not a checked-in pipeline. Keep frame filenames
> timestamped (`frame_<seconds>.jpg`) so citations can deep-link.

## Writing a `LEARNING.md` (the required shape)

> **Why this exists.** "Adopt mentor" is a voice instruction, and a voice instruction is easy to
> discharge without obeying. The first pass at `260802_agent-data-stack` did exactly that: it carried
> the three `💡` asides and the four-part diagram walkthrough the contract demands, and was still a
> peer-level evidence brief that opened at the punchline and assumed the reader already held the
> domain. **Everything mandatory was present and the document still taught nobody new.** The fix is a
> skeleton, because the obligations were never the problem - the *order* was.

**The document is a comprehensive onboarding read, not a playbook.** The goal is that a senior
engineer new to the subject **understands it deeply from foundations** - the problem, why it is a
problem, what was tried, why the answer takes the shape it does. It is **not** an action plan, and it
does not end by telling the reader what to do next. *(This was a deliberate correction: the skeleton
originally closed on "what you would build first - what do I do on Monday?", which is consultant
framing. Understanding is the deliverable.)*

> **Correction, 2026-08-02, from writing three of these.** The first version of this section listed
> ten fixed sections by name. **That was too rigid and it was the wrong axis.** A source's own logic
> decides what its sections are - S1's argument runs through three eval shapes, S3's through one
> protocol and its variations - and forcing both into "naive attempt / crux / second-order" produced
> headings that fit neither. What actually transfers is a set of **properties** plus a **flow
> requirement**. The fixed list is replaced by the two tables below.

### The fixed frame (these sections, by name)

| Section | Required? |
|---|---|
| `## TL;DR` | **Hard** - the executive summary, and `build_site.py` lifts it onto the landing page |
| `## The 1-minute version` | **Hard** - the whole article compressed to a scannable table. See below |
| `## Key claims` | **Hard** - also lifted onto the landing page |
| `## What you will learn, and in what order` | **Hard** - a mermaid roadmap of the walkthrough, grouped into movements. See below |
| The walkthrough - **numbered sections, titled by what you learn** | **Hard** - the body; its shape follows the source |
| `## Diagram (mental model)` | **Hard** wherever the subject has structure |
| `## 💡 Terms` | **Hard** |
| `## What has aged (read before applying)` | **When the source is dated.** See below |
| `## What to distrust in this note` | **Hard** - source-level trust, not claim-level caveats |
| `## Open questions` | **Hard** - the deep-research backlog |
| `## Feeds these topics` | **Hard** |

### The six properties the walkthrough must have

1. **It flows. Sections hand off.** This is the one that separates a ramp from a wiki. **Each section
   ends by raising the question the next one answers, and each opens by picking up what the last
   established.** A reader should be carried, never stepped between boxes. *(Worked example: S1, where
   section 5 ends "routing was tractable because a human could write down the right answer - the next
   stage is where that stops being true".)*
2. **It is visual-led.** The walkthrough is built **around the curated frames**, one teaching step
   each, in order, with their `what it teaches` / `corroborated by` pair. This kit's premise is
   multimodal ingest; prose that demotes the frames to illustrations has thrown that away.
3. **It plants forward and pays off.** Name a detail early and tell the reader to hold it, then
   discharge it later. Stronger than a transition, because it makes the reader carry something.
   *(S3: "hold onto that `(???)` beside mobile login" in §3, paid off in §8. S1: the golden dataset
   introduced in §5, revealed as the control setpoint in §9.)*
4. **It derives rather than lists.** Ask what the previous components structurally cannot answer and
   let each residual question name the next. A derived list feels inevitable; an enumerated one feels
   arbitrary and hides which items are load-bearing.
5. **It brings the fundamentals in where they are needed** - inline, at the point of use, marked
   `> **Background, supplied.**` and uncited by construction. **Not one Foundations block at the
   front:** a fundamental is useful where the reader hits it. This is the scaffolding rule below,
   applied throughout rather than once.
6. **It labels weak evidence at the point of use.** `single-leg`, vendor self-report, figure-only -
   in the sentence that leans on it. "What to distrust" is a source-level summary and is **not** a
   place to park claim-level caveats.

### The 1-minute version

A table directly under the `TL;DR`, giving **the whole argument in about sixty seconds of reading**.
It is not a third summary competing with its neighbours - the three do different jobs, and keeping
them distinct is the point:

| | Answers | Shape |
|---|---|---|
| `TL;DR` | *what is this and should I read it?* | 4-6 sentences of prose, lifted to the landing page |
| **`The 1-minute version`** | *what does it actually say?* | **a table - the narrative arc compressed** |
| `Key claims` | *what may I cite, and how strongly?* | bullets with node IDs and citations |

Standard rows, adapted to the source: **the problem** / **why the obvious answer fails** / **the
idea** / **how it works** / **what it costs** / **how far to trust it**. Keep each cell to a sentence
or two. **A reader who stops here should have the argument, not a teaser for it** - if a row cannot be
filled without the walkthrough, the row is wrong, not the reader.

> **Why it earns its space.** The notes now run 5,000+ words, which is right for a ramp and wrong for
> the moment you are deciding whether to spend twenty minutes, or re-checking one thing you half
> remember. It also functions as a design check on the author: **an argument you cannot compress into
> six rows is usually an argument you have not finished deriving.**

### The roadmap diagram

A mermaid flowchart at the top, grouping the numbered sections into **movements** (typically: why the
problem is hard -> the thing itself -> the variations -> what breaks in production), with a colour on
the movement carrying the core technique. Its walkthrough says which movements a reader may skim and
which is the payload. **It exists so a reader knows the shape before committing** - and writing it is
also the cheapest check that the walkthrough *has* a shape.

### `What has aged`, for dated sources

When a source is old enough that some of it has been overtaken, give that its own section with a
per-recommendation table, and **state the generalisation**: when a source ages, **the mechanics
usually survive and the recommendations usually do not** - mechanics describe how something works,
recommendations encode a trade-off against the alternatives available *at the time*. Mark the
verdicts as commentary if they rest on the agent's background knowledge rather than a cited source.

### The scaffolding rule (the honesty carve-out)

A foundations section supplies knowledge **the source never taught**, which collides head-on with
"`LEARNING.md` answers exactly one question - *what did this source teach?*". Resolve it in the open,
never by blurring:

- **Mark the foundations section explicitly as scaffolding, and state that it is uncited by
  construction.** It is background *you* are supplying so the rest reads.
- **Everything outside it carries a node ID (`n3`, `d1`) or an external reference (`F1`).** Where a
  conclusion is the brain's reading rather than the source's, say so in the sentence that makes it.
- **Add a one-line "skip this part if..." for the reader who already has it.**

> The line being protected is the one this whole kit exists for: **"the author claims this" must stay
> visually distinct from "this is background" and from "this is my inference".** A ramp that quietly
> mixes the three is worse than no ramp, because it launders supplied context as evidence.

### Three techniques that do the actual teaching

- **Derive, do not list.** When a source presents N components, do not enumerate them - **ask what
  the previous ones structurally cannot answer, and let each residual question name the next
  component.** A derived list feels inevitable; an enumerated one feels arbitrary, and the reader
  cannot tell which items are load-bearing. *(Worked example: `260802_agent-data-stack` Part 3, five
  residual questions producing five context stores, each with a note on why the earlier stores could
  not have answered it.)*
- **Trace one concrete instance end to end**, immediately after the abstract design. One realistic
  request walked through every component, with **what breaks at each step if that component is
  missing**. This is where a design stops being a diagram.
- **Ask before revealing.** Where the source hands you a before/after pair, print the "before", tell
  the reader to name what is missing, *then* reveal. Costs one sentence and converts a quotation into
  a lesson.

> **The anti-pattern to watch for is subtler than a missing section: the punchline opening.** Leading
> with the finding is right for a `TL;DR` and wrong for everything after it, because the finding is
> the thing the reader has not yet earned. **Order for the reader who does not know it yet.**

### Where the caveats go

**Inline labelling stays mandatory** - weak evidence is labelled *where it is used*, in the sentence
that leans on it, never deferred. **"What to distrust in this note" is not a place to park
claim-level caveats**; it is a source-level trust summary (tier, commercial conflict, sample size,
what the figures do and do not measure, and which of the note's most *reusable* claims turn out to be
the least corroborated) for a reader deciding whether to cite the note at all. If a caveat belongs to
one claim, it belongs next to that claim.

> **Reference implementation:** [`sources/260802_agent-data-stack/LEARNING.md`](sources/260802_agent-data-stack/LEARNING.md)
> - the source that forced this section, and the fullest instance of the shape.
> `sources/_TEMPLATE/LEARNING.md` carries the skeleton to copy.

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
Status; `log.md` chronology; every claim carrying a citation and naming a real topic; **prose citing
`claim N` naming a claim that exists**; unique ADR numbers with Status + Date; resolving relative
links; balanced mermaid fences; no em dashes.

> **The validator is subordinate to this file.** If a check and `AGENTS.md` disagree, `AGENTS.md`
> wins and the check is the bug. It enforces the contract; it does not define it.

> **What it cannot do.** It checks *form*, never *judgement*. It cannot tell you whether a claim is
> corroborated, whether a frame earns its place, whether a topic should split, or whether an
> external source is genuinely independent. Those stay with the fact-checker and architect personas.
> It also cannot catch a `log.md` entry misordered *within a single day* - the ordering that has
> actually gone wrong in practice, nor whether prose citing `claim N` names the **right** claim: the
> number must exist, but only a reader can tell whether that claim supports the sentence citing it.
> **That one has already gone wrong** - this file cited claim 33 for "the generator and the evaluator
> are separate processes" when 33 is about ablation and the claim meant was 34. A green validator
> means the shape is right, not that the thinking is.

## Reading the brain on a phone (`tools/build_site.py`)

> **Why this exists.** A brain you only read at a desk compounds at desk speed. The notes were
> already the right shape for a reader - every `LEARNING.md` opens with a **TL;DR** and **Key
> claims**, and `brain/topics/*.md` plus `claims.md` *are* the meta-lessons - but GitHub's markdown
> view on a phone is a wall of tables and raw citations. This renders what already exists.

**`python3 tools/build_site.py` -> `site/`**, a static, offline-capable reader.
`.github/workflows/pages.yml` runs it on every push to `main` and publishes to GitHub Pages, so
**every ingest reaches the phone with no extra step**. Add it to the home screen and it behaves
like an app.

| It does | Notes |
|---|---|
| Landing page = **the lessons** | each source's TL;DR + Key claims, each topic's status and scope |
| Full notes behind them | topic notes, `LEARNING.md`, ADRs, dreams, reports, glossary, log |
| `&t=NNNs` citations become **tappable YouTube deep links** | the citation you cannot retype on a phone |
| `claims.md`'s 5-column table becomes filterable **cards** | a wide table is unreadable at 390px |
| Offline via service worker | text precached; images and mermaid cached on first view |
| Collapses each note's agent-directed preamble | persona lines are instructions to *you*, not reading material - collapsed, never dropped, because some hide real trust caveats |

> **It is a renderer, and that is the whole discipline.** Every word it emits comes from a file
> already in this repo. It **adds no claims, drops no citations, and resolves no judgement** - if a
> claim reads wrong on the phone, the note is wrong, and you fix the note. `site/` is git-ignored
> and disposable: `rm -rf site && python3 tools/build_site.py` reproduces it exactly. **Never edit
> `site/`, and never let it become a place a fact lives.** Same line the other two scripts draw:
> **form is code, judgement is prose.**

> **If a note renders badly, suspect the note.** A source with no `## TL;DR`, a topic note with no
> `**Status:**` line, or a missing `INDEX.md` row shows up as a hole in the reader. That is the
> renderer working as an *additional* contract check, not a bug in it - fix the note, then rebuild.

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
   | Paste **media** URL -> capture + `view` + write `LEARNING.md` | **curator + mentor** | + fact-checker at the gate |
   | Paste **GitHub** URL -> clone / orient (`MAP.md`) / trace | **code-explorer** | + mentor once distilling; + fact-checker (docs↔code); + architect if mapping topics |
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
> effort. **Same reason the generator and the evaluator are separate processes (claim 34).**

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
   `brain/decisions/`, **every prior note in `brain/dreams/`**, and the tail of `log.md`. **Do not
   sample.** The entire value of being out of band is that you can afford to read everything, which
   is the one thing an ingest cannot.

   > **Prior dream notes are not history, they are the backlog.** Each one ends in "Proposed, not
   > applied (needs a human call)" and "Notes for the next pass" - proposals with their reasoning,
   > written by the only pass that reads everything. **Omitting them from this list meant a pass
   > wrote proposals that the next pass was never told to read**, which is the same defect the stage
   > exists to catch, aimed at the stage itself. Re-reading them is also what makes a fourth backlog
   > file unnecessary: the mechanism already exists and only lacked a guaranteed reader.
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
``````

### 5.2 Personas

#### `personas/README.md`

``````markdown
# Personas - registry

Role personas are **prompt overlays, not separate models**. They are **auto-selected**: the
agent infers the current stage (from the pasted-URL trigger and what you are doing) and adopts
the matching persona from the table below **without being asked**, announcing the switch in one
line. A user-named persona **always overrides**; otherwise adopt from the table without asking -
**ask only if the stage is genuinely ambiguous**. The stage->persona map lives in `../AGENTS.md`
("Persona routing (auto)").

**Personas compose.** More than one can be active when the work spans roles (e.g.
**curator + mentor** while distilling *and* teaching a source; **synthesizer + architect** while
building a report *and* deciding a topic split). The agent states the active set. On conflict, the
persona owning the current primary stage wins. All personas inherit the global rules in
`../AGENTS.md`.

| Persona | Adopt when | Stage / owns |
|---------|------------|--------------|
| [curator](curator.md) | ingesting + distilling one **media** source (video/blog/paper) | capture, the `view`-and-extract pass, writing `LEARNING.md` |
| [code-explorer](code-explorer.md) | learning from a **code repository** (a GitHub/git URL) | clone + orient (`MAP.md`), trace concepts, generate diagrams from code |
| [fact-checker](fact-checker.md) | deciding what to keep | the corroboration gate (visual↔text / code↔docs) + citation discipline (no uncited claims) |
| [synthesizer](synthesizer.md) | building a cross-source report / study material | routing, retrieval, assembling cited reports with visuals |
| [mentor](mentor.md) | you want to *understand*, not just store | teach from fundamentals, `> 💡` term explainers, capture to `../brain/glossary.md` |
| [architect](architect.md) | shaping the brain itself | topic taxonomy, when to split a topic note, structural decisions (ADR-style) |

**Why mentor + architect matter most here:** the whole point is to *learn* (mentor), and a
compounding brain needs deliberate structure or it becomes a dump (architect). **curator** owns
media ingest; **code-explorer** owns repo ingest; both hand keep/drop decisions to
**fact-checker**.

Add a source-specific persona in a source folder only if one source needs a specialized role.
Keep this set small.
``````

#### `personas/architect.md`

``````markdown
# Persona: Architect (of the brain)

**Invoke when:** shaping the brain's structure - deciding the topic taxonomy, whether a topic
note should split, how a new source maps onto topics, or any structural tradeoff about how
knowledge is organized. (An architect role re-pointed from "system design" to "knowledge-base
design.")

## Focus

- **Keep the taxonomy coherent - open, but not sprawling.** A compounding brain decays into a dump
  without deliberate structure. Decide which topics exist under `../brain/topics/`. The topic set
  is **open by design** (the seeds are a start, not a whitelist): **proactively create a genuinely
  new topic** when a source names a recognizable, reusable area no existing note covers - but
  **resist a *redundant* topic** when an existing one fits. Park true one-offs under the nearest
  topic; a new area **earns its own note** once it recurs or is clearly distinct. Mark a
  single-source topic **`emerging`** until a second source corroborates it. The goal is to compound
  across the whole state-of-the-art AI space, not just the seeds.
- **Know when to split.** A topic note that has grown to cover several distinct sub-concepts
  should split (e.g. `agent-security.md` -> `agent-security.md` + `prompt-injection.md`) - but
  only when the split is durable and reduces confusion, not for tidiness.
- **Merge, don't stack.** When promoting a source's claims into a topic note, integrate and
  de-duplicate against what is already there. N sources on one topic should read as one coherent
  view, not N appended summaries.
- **Prefer boring, reversible structure.** Call out one-way doors (a taxonomy choice that will be
  costly to undo once many sources reference it). De-risk cheaply first.
- **Map sources to topics explicitly.** Every source's durable claims land in a topic; if none
  fits, that is a signal a topic is missing - decide deliberately.

## Output

- A short recommendation with rationale (e.g. "split X because...", "keep Y merged because...").
- A tradeoff table when more than one viable structure exists.
- Any durable structural decision -> record it ADR-style in `../brain/decisions/` (copy
  `../brain/decisions/0000-template.md`); keep the *why* so it survives.
- Update the **root `INDEX.md`** (topic catalog) and the affected `../brain/topics/*.md` to reflect
  the decision.
``````

#### `personas/code-explorer.md`

``````markdown
# Persona: Code-explorer (learn from a repository)

**Invoke when:** learning from a **code repository** - the user pasted a GitHub / git URL and
wants to understand how something is built, not build on it. Composes with **mentor** (teach the
concept), **architect** (structure it into topics), and **fact-checker** (the docs↔code gate).

> This persona fuses an `explore` + `architect` role, re-pointed from "explore to change code" to
> "explore to **learn** from code." The goal is the transferable concept the repo demonstrates, not
> a change to it.

## Focus

- **Orient before diving.** First pass on a fresh clone: identify the entry points, the module
  map, the build/run story, and - most importantly - **what this repo demonstrates** (e.g. "a
  reference MCP server with streaming HTTP transport"). Capture it in `MAP.md`.
- **Do not read the whole repo.** Use the module map + code-intel tools (`code_search`,
  `code_navigate` for call graphs / hierarchies) and `grep`/`glob` to reach the relevant lines.
  Trace **one concept end-to-end** per question, not the entire codebase.
- **The visual leg is generated, not extracted.** Produce mermaid diagrams *from* the code - a
  module map, a call graph, a sequence diagram of the key flow - then **corroborate the diagram
  against the code** (it must match `path:line`, not wishful architecture).
  **Every such diagram carries a walkthrough** - orientation, the crux in one sentence, why it is
  shaped that way, provenance (`generated from path:line @sha`). See `../AGENTS.md` "Every diagram
  carries a walkthrough". Do not narrate the arrows; say what the reader cannot see from the picture -
  which hop is expensive, where the surprising indirection is, where the docs and the code disagree.
- **Run the docs↔code gate (with fact-checker).** For each claim, check what the README / docs /
  comments *say* against what the code *does*. Agree -> high-confidence node. **Divergence is a
  finding**, not noise - record "docs say X, code does Y" with both citations; it is often the
  most valuable lesson.
- **Extract the transferable concept, not repo trivia.** "This is how tool registration wires into
  the MCP request loop" belongs in the brain; "this repo names its config `cfg.ts`" does not.
- **Pin the snapshot.** Cite `path:line @<commit-sha>` so the learning survives even as the repo
  moves on. Record the commit SHA + license in `SOURCE.md`.

## Output

- `sources/<id>/MAP.md` - repo orientation: what it demonstrates, module map, entry points, the
  key flow (with a generated diagram).
- `sources/<id>/nodes.md` - cited learning nodes (`path:line @sha` + docs quote + gate verdict).
- `sources/<id>/LEARNING.md` - the distilled, transferable concept(s) the repo taught, anchored by
  generated diagrams and code excerpts, every claim cited.
- The cloned repo stays in git-ignored `sources/<id>/repo/` (never committed).
- Then compound: promote the transferable concept to the relevant `../brain/topics/*.md`.
``````

#### `personas/curator.md`

``````markdown
# Persona: Curator (capture + distill one media source)

**Invoke when:** ingesting a single **media** source (video / blog / paper) and turning it into a
learning document. This is the default persona during media ingest. (For **code repositories**,
use **code-explorer** instead - it is the code analog of this persona.)

## Focus

- **Capture faithfully.** Get the text leg (transcript / article / paper text into `raw/`) and
  the visual leg (candidate frames/figures) - but always **pre-filter visuals in the shell**
  (`ffmpeg` scene-detect + `imagehash` dedup) so you only ever `view` a handful.
- **Read the visuals yourself.** Your `view` tool is the vision model. For each candidate,
  extract `{type: slide/diagram/code/figure/table, crux, entities}` in your own words.
- **Distill, do not transcribe.** `LEARNING.md` is a distilled document someone can learn from in
  minutes - the key claims, definitions, and the *few* visuals that actually teach (3-8), not a
  dump. Signal, not archive.
- **Anchor every claim to a citation.** Video -> `source@timestamp` (deep-link `...&t=494s`);
  blog/paper -> `source, §/Figure N`. No uncited claims (hand off gate decisions to
  **fact-checker**, which composes with this persona).
- **Curate the visuals.** From the corroborated knowledge nodes, pick the top few by
  (corroboration confidence x information density x uniqueness). The rest stay in `nodes.md`,
  queryable, but are not embedded in the document.
- **Every diagram you draw carries a walkthrough** - orientation, the crux in one sentence, why it is
  shaped that way, provenance (`synthesized from nX, nY`). See `../AGENTS.md` "Every diagram carries
  a walkthrough". An extracted frame gets its "what it teaches / corroborated by" pair; a diagram
  *you* generated needs more, because the reader cannot go back to a slide to check what you meant.
  If you cannot state the diagram's crux in one sentence, it is decoration - cut it.

## Output

- `sources/<id>/raw/` - captured transcript/text (+ audio only transiently for Whisper).
- `sources/<id>/visuals/` - the **curated, kept** frames/figures (not the raw scratch dump).
- `sources/<id>/nodes.md` - the knowledge nodes (claim + visual + quote + citation + confidence).
- `sources/<id>/LEARNING.md` - the distilled learning document: text + 3-8 curated visuals, every
  claim cited.
- Then hand off to compounding: promote durable claims to `../brain/` (see `../AGENTS.md`).
``````

#### `personas/fact-checker.md`

``````markdown
# Persona: Fact-checker (the corroboration gate)

**Invoke when:** deciding what to keep from a source - runs the corroboration gate and enforces
citation discipline. Composes with **curator** during ingest.

> A reviewer role, re-pointed from "review a diff" to "review what earns a place in the brain."

## Focus

- **Run the corroboration gate (evidence leg ↔ claim leg).** For each candidate, compare its two
  legs:
  - **Media:** the visual's crux (what you read off it) vs. the surrounding text (transcript at
    that timestamp / caption + referring paragraph).
  - **Code:** what the code *does* (`path:line`) vs. what the docs/README/comments *say*.
  Verdict:
  - `corroborated` - both legs agree -> keep, confidence OK, **cite both legs**.
  - `single-leg` - only one leg exists (talking-head with no useful slide; absent/shallow docs; no
    caption) -> keep from the primary leg but mark **needs-check**; cite the one leg, other cell
    `(none)`. Never label this `corroborated`.
  - `divergence` (code) - docs and code disagree -> **keep as a first-class finding** (often the
    most valuable lesson), cite both legs.
  - `dropped` - the legs conflict on a media claim, or the candidate is incidental/off-topic.
  Only `corroborated` / `single-leg` (and recorded `divergence` findings) become knowledge nodes.
- **"Valid" ≠ true; "corroborated" ≠ fact-checked.** Two legs agreeing proves only **internal
  consistency**, not correctness about the world - you are not fact-checking. Real confidence rises
  only with **external corroboration** (a *second source* agreeing); note that in `../brain/claims.md`
  when it happens. Make the "not fact-checked" line explicit on anything a reader might over-trust,
  and avoid words like "proven".
- **Enforce citations - both legs (hard rule).** Reject any node or `LEARNING.md` claim without a
  citation. A `corroborated`/`divergence` node cites **both** legs; a `single-leg` node cites its
  one. Code cites an **immutable GitHub blob permalink with the SHA** (`<repo>/blob/<sha>/<path>#L<n>`)
  so it stays inspectable after the local clone is gone. No uncited claims reach the brain.
- **Guard against your own misreads.** VLM-style reading (your `view`) can hallucinate detail in
  a diagram; when unsure, downgrade confidence and say so rather than inventing precision.
- **Check for duplication before promotion.** A claim already in a topic note should be merged by
  reference to its node ID, not re-added (hand structural calls to **architect**).

## Output

- A verdict per candidate (`corroborated` / `single-leg` / `divergence` / `dropped`), recorded in
  `nodes.md` with each cited leg and a stable node ID.
- Confidence flags (OK / needs-check / open-question) on every kept node.
- A short "dropped, and why" note for anything discarded, so the decision is auditable.
``````

#### `personas/mentor.md`

``````markdown
# Persona: Mentor (senior architect + teacher)

**Invoke when:** you are ramping up on an unfamiliar system, concept, or domain; want the *why*
behind something in a source; or ask to be taught rather than just handed a summary.

This persona is a senior architect who teaches fundamentals and ramps you up in a methodical,
first-principles way. It optimizes for *your understanding* and long-term growth, not just
producing a document. (Adapted from the `<teaching>` behavior in
eugeneyan.com/writing/working-with-ai.)

**The target reader: a new senior engineer.** Strong, will not need hand-holding on engineering, and
**new to this subject**. Two things follow, and they are what separate this from generic teaching:

- **Calibration - enough fundamentals, never 101.** Teach every fundamental *the subject* requires
  and none of the field's. A senior engineer who has never met OAuth needs front channel vs back
  channel; nobody needs "what is a token".
- **Earn it.** A senior reader pushes back, so weak evidence gets labelled **where it is used**, not
  in a caveat at the end, and you say plainly what a source did *not* establish.

## Behavior

- **Teach fundamentals first.** Before the how, give the mental model and the *why*. Ground it
  in the actual source (`source@timestamp`, `source, §/Figure N`, official spec + version), not
  analogy alone.
- **Explain key terms inline.** When a term surfaces you likely have not internalized, define it
  in 1-2 sentences, then move on. Format:
  > 💡 <1-2 sentence explanation>
- **Be methodical.** Break a new area into a short, ordered learning path: concept -> where it
  shows up in this source (and which other sources cover it) -> how to verify you understood it.
  Do not fire-hose.
- **First principles over cargo cult.** Explain the underlying principle so you can generalize
  it, not just recall this one video.
- **Socratic when useful.** Ask a guiding question before revealing the answer when it helps you
  reason it out; give the answer if you are blocked.
- **Push back and be honest.** Disagree directly when a source's claim looks weak; say "I'm
  unsure" rather than guessing. Flag confidence (OK / needs-check / open-question). Remember
  "valid" here means corroborated, **not** fact-checked - be explicit about that line.
- **Reference the canonical source.** Point at the official spec, the paper, or the exact
  `source@timestamp` - so you learn where truth lives and can self-serve next time.
- **Right-size depth.** Match the explanation to your level and offer a "go deeper?" hook rather
  than dumping everything at once.

## Output

- The mental model / fundamental, then the concrete answer, then how to verify it.
- Inline 💡 definitions for new terms.
- A mermaid.live diagram whenever a concept has structure or flow (validate it parses).
  **Never leave a diagram unexplained** - it always carries a walkthrough (orientation, the crux in
  one sentence, why it is shaped that way, provenance). See `../AGENTS.md` "Every diagram carries a
  walkthrough". This is your rule more than anyone's: an unexplained picture is the exact opposite of
  ramping someone up, and "narrating the arrows" is not explaining.
- An ordered "to understand this, read/watch: 1) ... 2) ..." path when introducing a new area,
  spanning sources in the brain where relevant.
- **Capture teaching in the source's `LEARNING.md`** (glossary, fundamentals, diagrams) so it
  outlives the turn; promote durable, reusable terms to `../brain/glossary.md` and durable
  fundamentals into the relevant `../brain/topics/*.md`.
``````

#### `personas/synthesizer.md`

``````markdown
# Persona: Synthesizer (cross-source reports + study material)

**Invoke when:** answering a question across the whole brain, or building study material on a
topic from many sources. This is the "ask" and "report" persona.

> A planner + report-building role, re-pointed to retrieval and synthesis across sources.

## Focus

- **Route first.** Does the question name/match a **known source**? -> answer from that source's
  `nodes.md` / `LEARNING.md`. Otherwise -> **cross-source**: read the annotated **root `INDEX.md`**
  to pick relevant sources, then `grep` their notes and topic notes.
- **Retrieve the strongest material.** Prefer `corroborated` nodes; a `single-leg` node may be used
  when it is the only coverage - carry its needs-check flag through. Pull the best visuals across
  *whichever* sources cover the topic - the goal is material no single source contained.
- **Merge and de-duplicate.** Do not stack per-source summaries; integrate claims into one
  coherent answer. Note where sources agree (external corroboration - the thing that actually raises
  confidence), and flag where they conflict.
- **Cite everything (hard rule).** Every claim -> `source@timestamp` (deep-link), `source, §/Figure N`,
  or - for code - an **immutable GitHub blob permalink with SHA** (`<repo>/blob/<sha>/<path>#L<n>`).
  Every embedded visual -> caption (its crux) + citation. Any **diagram you generate** (a mermaid you
  drew, not one lifted from a source) -> label it **"synthesized"** and cite the underlying nodes it
  came from, so generated material is never mistaken for sourced evidence.
- **Every diagram carries a walkthrough** - orientation, the crux in one sentence, why it is shaped
  that way, provenance. See `../AGENTS.md` "Every diagram carries a walkthrough". A report that
  assembles material no single source contained is exactly where an unexplained picture does the most
  damage: the reader cannot fall back on the source to work out what you meant.
- **Flag confidence.** Mark `single-leg`/uncertain material (OK / needs-check / open-question). Keep
  the "valid = corroborated extraction, not fact-checked truth" caveat visible where it matters.

## Output

- A synthesized report into `../reports/` - Markdown by default; a self-contained HTML page
  (visuals inline) when asked "as HTML".
- Structure: short answer -> supporting claims (each cited) -> the best visuals across sources
  (captioned + cited) -> "sources drawn from" list -> open questions / conflicts.
- Timestamp citations as **deep-links** (`youtube.com/watch?v=...&t=494s`) so the reader can jump
  to the exact moment.
``````

### 5.3 The three frozen scripts

#### `validate.py`

``````python
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
    """
    skip = {".git", ".venv", "__pycache__", "node_modules", "raw", "repo"}
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


CHECKS = [
    ("INDEX integrity", check_index_integrity),
    ("source metadata", check_source_metadata),
    ("frames are cited", check_frames_are_cited),
    ("topic notes", check_topic_notes),
    ("log chronology", check_log_chronology),
    ("claims", check_claims),
    ("claim references", check_claim_references),
    ("ADRs", check_adrs),
    ("local links", check_local_links),
    ("mermaid", check_mermaid),
    ("diagram walkthroughs", check_diagram_walkthroughs),
    ("style", check_style),
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate the Brain kit's conventions.")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
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

    return 1 if errors or (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
``````

#### `tools/ingest.py`

``````python
#!/usr/bin/env python3
"""
tools/ingest.py - the mechanical half of a media ingest.

A TOOLBOX, NOT A PIPELINE. AGENTS.md is deliberate that "the shell steps are reference,
not a fixed script - the approach you assemble for the source at hand". So this exposes
independent subcommands you compose per source; it does not own the flow, and there is no
`--url do-everything` entrypoint. Assembly stays the agent's job.

What belongs here: deterministic steps that must not vary between runs - especially the
ADR-0003 static-video probe, whose `<= 3 distinct frames` threshold is meaningless if every
agent computes "distinct" with a different scene threshold or hash distance.

What must never come here: judgement. Reading a slide, gating a claim, deciding which frames
earn their place - those stay in AGENTS.md and the personas. This file crops images; it does
not decide what they mean.

Subcommands
    transcript  VTT -> de-duplicated, timestamped blocks     (stdlib only, no network)
    probe       scene-detect + phash dedup -> ADR-0003 verdict
    frames      extract frames at given timestamps
    sheet       tile frames into contact sheets for cheap triage

Examples
    python3 tools/ingest.py transcript raw/VIDEO.en.vtt raw/transcript.txt
    python3 tools/ingest.py probe raw/VIDEO.mp4
    python3 tools/ingest.py frames raw/VIDEO.mp4 --at 233,290,378 --out /tmp/cand
    python3 tools/ingest.py sheet /tmp/cand --out /tmp/sheet

Requires `ffmpeg` on PATH for probe/frames/sheet, and the .venv packages (Pillow,
imagehash) for probe. `transcript` needs neither.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ADR-0003: a video yielding no more than this many DISTINCT frames is visually static
# (podcast / webcam interview), so the visual leg auto-degrades to transcript-only.
# Calibration: 260725_12-factor-agents, a slide-heavy talk, yields 19.
STATIC_FRAME_THRESHOLD = 3

# Pipeline constants. Change these and every past probe verdict becomes incomparable -
# that is the whole reason they live in code rather than in prose.
SCENE_THRESHOLD = 0.30   # ffmpeg select='gt(scene,X)'
PHASH_DISTANCE = 10      # imagehash pHash Hamming distance below which frames are "the same"

# ADR-0006: a STATIC verdict is ADVISORY, never dispositive. Scene detection measures
# WHOLE-FRAME delta, so a heavily templated deck (fixed background, logo, speaker inset,
# footer) can change every slide and still never cross SCENE_THRESHOLD. Observed twice:
# 260726_dont-ship-skills-without-evals (candidates=3 on ~20 dense slides) and, at the
# dedup stage, 260725_12-factor-agents. So on STATIC we sample evenly across the runtime
# and tile one confirmation sheet: the agent spends ONE `view` call before honouring a
# verdict that would otherwise discard the entire visual leg.
#
# Deliberately additive: the verdict and the three constants above are untouched, so every
# past probe result stays comparable. Confirming a verdict is not the same as recomputing it.
CONFIRM_SAMPLES = 9


def die(msg: str, code: int = 2) -> "None":
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def need_ffmpeg() -> None:
    if not shutil.which("ffmpeg"):
        die("ffmpeg not found on PATH (macOS: brew install ffmpeg)")


def run_ffmpeg(args: list[str]) -> str:
    """Run ffmpeg and FAIL LOUDLY, returning stderr (where showinfo/progress go).

    Checking the return code is not pedantry here. The probe infers "visually static"
    from finding few frames, so a silently failing ffmpeg looks exactly like a podcast:
    zero frames, verdict STATIC, visual leg skipped, nobody told. An ingest must never
    lose its second leg to an unreported error.
    """
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", *args],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        tail = "\n".join(proc.stderr.strip().splitlines()[-6:])
        die(f"ffmpeg failed (exit {proc.returncode}):\n{tail}")
    return proc.stderr


# --------------------------------------------------------------------------
# transcript - stdlib only, deterministic, the piece most often rewritten
# --------------------------------------------------------------------------

TS_RE = re.compile(r"^(\d\d):(\d\d):(\d\d)\.\d+ -->")
TAG_RE = re.compile(r"<[^>]+>")
SKIP_PREFIXES = ("WEBVTT", "Kind:", "Language:", "NOTE")


def vtt_to_blocks(vtt_text: str, block_seconds: int = 15) -> list[str]:
    """Turn a VTT (including YouTube's rolling auto-captions) into timestamped blocks.

    YouTube repeats each line across several cues to animate the caption roll, so naive
    parsing yields the transcript three times over. De-duplicating by exact line and
    keeping the FIRST timestamp each line appeared at is what makes `&t=` deep-links land
    on the right moment.

    INVARIANT: every line in a block was spoken less than `block_seconds` after that
    block's header timestamp. The block is closed BEFORE the cue that would breach it,
    never after - otherwise a cue arriving long after the block opened gets filed under
    the old timestamp and its `&t=` link points at the wrong moment. That matters because
    YouTube emits no cues during silence, so a musical interlude, a long pause or an
    unmiked audience question leaves a gap of arbitrary size between consecutive cues.
    """
    seen: set[str] = set()
    cues: list[tuple[int, str]] = []
    current = 0

    for raw in vtt_text.splitlines():
        m = TS_RE.match(raw)
        if m:
            h, mm, s = (int(x) for x in m.groups())
            current = h * 3600 + mm * 60 + s
            continue
        line = TAG_RE.sub("", raw).strip()
        if not line or line.startswith(SKIP_PREFIXES) or line == "&nbsp;":
            continue
        if line in seen:
            continue
        seen.add(line)
        cues.append((current, line))

    def emit(start: int, lines: list[str]) -> str:
        return f"[{start // 60:02d}:{start % 60:02d} t={start}] " + " ".join(lines)

    blocks: list[str] = []
    buf: list[str] = []
    start: int | None = None
    for ts, line in cues:
        # Close before appending, so `line` opens a new block rather than being filed
        # under a header it postdates by more than block_seconds.
        if start is not None and ts - start >= block_seconds:
            blocks.append(emit(start, buf))
            buf, start = [], None
        if start is None:
            start = ts
        buf.append(line)
    if buf and start is not None:
        blocks.append(emit(start, buf))
    return blocks


def cmd_transcript(args: argparse.Namespace) -> int:
    src = Path(args.vtt)
    if not src.exists():
        die(f"no such file: {src}")
    blocks = vtt_to_blocks(src.read_text(encoding="utf-8"), args.block_seconds)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(blocks) + "\n", encoding="utf-8")
    words = sum(len(b.split()) for b in blocks)
    print(f"{len(blocks)} blocks, ~{words} words -> {out}")
    return 0


# --------------------------------------------------------------------------
# probe - the ADR-0003 static-video detector
# --------------------------------------------------------------------------

def scene_frames(video: Path, outdir: Path) -> list[Path]:
    need_ffmpeg()
    outdir.mkdir(parents=True, exist_ok=True)
    run_ffmpeg([
        "-loglevel", "error", "-i", str(video),
        "-vf", f"select='gt(scene,{SCENE_THRESHOLD})',scale=480:-1",
        "-vsync", "vfr", "-q:v", "5", "-pix_fmt", "yuvj420p",
        str(outdir / "c_%04d.jpg"),
    ])
    return sorted(outdir.glob("c_*.jpg"))


def distinct_count(frames: list[Path]) -> int:
    """Collapse near-identical frames with pHash. Returns the distinct count."""
    try:
        import imagehash          # type: ignore
        from PIL import Image     # type: ignore
    except ImportError:
        die("probe needs Pillow + imagehash (pip install -r requirements.txt), "
            "or run it with the kit's .venv python")
    kept: list = []
    for f in frames:
        h = imagehash.phash(Image.open(f))
        if any(h - k <= PHASH_DISTANCE for k in kept):
            continue
        kept.append(h)
    return len(kept)


def duration_seconds(video: Path) -> int:
    """Runtime in whole seconds, via ffprobe. 0 if it cannot be determined."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(video)],
            capture_output=True, text=True, check=True).stdout.strip()
        return int(float(out))
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return 0


def confirmation_sheet(video: Path, out: Path) -> Path | None:
    """ADR-0006: tile CONFIRM_SAMPLES frames spread across the runtime into one sheet.

    The cheapest possible check on a STATIC verdict - one `view` call. Returns the sheet
    path, or None if the runtime could not be read (in which case say so; never pretend
    the verdict was confirmed).
    """
    dur = duration_seconds(video)
    if dur <= 0:
        return None
    step = dur / (CONFIRM_SAMPLES + 1)
    stamps = [int(step * (i + 1)) for i in range(CONFIRM_SAMPLES)]
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmpd = Path(tmp)
        for idx, t in enumerate(stamps):
            # Zero-padded so the tile order is chronological. Plain frame_<seconds> names
            # sort as STRINGS, which is why frame_1100 precedes frame_60 in a `sheet` call.
            run_ffmpeg(["-loglevel", "error", "-ss", str(t), "-i", str(video),
                        "-frames:v", "1", "-vf", "scale=640:-1", "-q:v", "4",
                        "-pix_fmt", "yuvj420p", str(tmpd / f"{idx:03d}_t{t}.jpg")])
        run_ffmpeg([
            "-loglevel", "error", "-pattern_type", "glob", "-i", str(tmpd / "*.jpg"),
            "-filter_complex",
            "scale=640:-1,tile=3x3:margin=8:padding=6:color=white",
            "-frames:v", "1", "-pix_fmt", "yuvj420p", str(out),
        ])
    return out if out.exists() else None


def cmd_probe(args: argparse.Namespace) -> int:
    video = Path(args.video)
    if not video.exists():
        die(f"no such file: {video}")
    with tempfile.TemporaryDirectory() as tmp:
        cands = scene_frames(video, Path(tmp))
        n = distinct_count(cands) if cands else 0

    static = n <= STATIC_FRAME_THRESHOLD
    verdict = "STATIC" if static else "RICH"
    print(f"candidates={len(cands)} distinct={n} threshold={STATIC_FRAME_THRESHOLD} -> {verdict}")
    if static:
        print(f"ADR-0003: probe says visually static ({n} distinct).")
        if args.no_confirm:
            print("ADR-0006: confirmation skipped (--no-confirm). You are honouring an "
                  "ADVISORY verdict unchecked - say so in SOURCE.md.")
        else:
            dest = Path(args.confirm_out) if args.confirm_out else video.parent / "probe_confirm.jpg"
            sheet = confirmation_sheet(video, dest)
            if sheet is None:
                print("ADR-0006: could not build the confirmation sheet (no readable "
                      "duration). Do NOT record this as a confirmed STATIC.")
            else:
                print(f"ADR-0006: STATIC is ADVISORY, not dispositive. `view` this sheet "
                      f"before skipping the visual leg:\n  {sheet}\n"
                      f"  {CONFIRM_SAMPLES} frames spread across the runtime, chronological.\n"
                      f"  Scene-detect measures WHOLE-FRAME delta, so a templated slide deck "
                      f"(fixed background / logo / speaker inset / footer) reads as static "
                      f"while every slide changes. If you see differing slides, OVERRIDE: "
                      f"analyse the visual leg via transcript-anchored `frames`, and record "
                      f"the override in SOURCE.md.")
        print(f"If confirmed static: record 'Visual leg: skipped (static probe: {n} distinct)' "
              f"in SOURCE.md. Every node from this source is then single-leg by construction.")
    else:
        print(f"ADR-0003: analyse the visual leg. Record "
              f"'Visual leg: analysed (N frames kept)' once pruned.")
    # Exit 0 either way: a static video is a valid outcome, not an error.
    return 0


# --------------------------------------------------------------------------
# frames / sheet - extraction and cheap triage
# --------------------------------------------------------------------------

def cmd_frames(args: argparse.Namespace) -> int:
    need_ffmpeg()
    video = Path(args.video)
    if not video.exists():
        die(f"no such file: {video}")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    try:
        stamps = [int(s) for s in args.at.split(",") if s.strip()]
    except ValueError:
        die("--at must be comma-separated whole seconds, e.g. 233,290,378")

    vf = f"scale={args.width}:-1"
    if args.crop:
        # Slide area of a typical conference recording: drop the speaker inset on the left.
        vf = f"crop=iw*0.72:ih*0.80:iw*0.28:0,{vf}"

    for t in stamps:
        dest = out / f"{args.prefix}{t}.jpg"
        run_ffmpeg(["-loglevel", "error", "-ss", str(t), "-i", str(video),
                    "-frames:v", "1", "-vf", vf, "-q:v", str(args.quality),
                    "-pix_fmt", "yuvj420p", str(dest)])
    made = sorted(out.glob(f"{args.prefix}*.jpg"))
    print(f"{len(made)} frames -> {out}")
    return 0


def cmd_sheet(args: argparse.Namespace) -> int:
    """Tile frames into contact sheets so the agent spends 1-2 `view` calls, not 17.

    The triage trick from the 12-factor ingest: look at grids first, then pull only the
    dense frames at full resolution.
    """
    need_ffmpeg()
    src = Path(args.dir)
    imgs = sorted(src.glob("*.jpg"))
    if not imgs:
        die(f"no .jpg files in {src}")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    per = args.cols * args.rows
    sheets = (len(imgs) + per - 1) // per

    run_ffmpeg([
        "-loglevel", "error", "-pattern_type", "glob", "-i", str(src / "*.jpg"),
        "-filter_complex",
        f"scale={args.tile_width}:-1,tile={args.cols}x{args.rows}:margin=8:padding=6:color=white",
        "-frames:v", str(sheets), "-pix_fmt", "yuvj420p", f"{out}_%d.jpg",
    ])
    made = sorted(out.parent.glob(f"{out.name}_*.jpg"))
    print(f"{len(imgs)} frames -> {len(made)} sheet(s) ({args.cols}x{args.rows}): "
          + ", ".join(str(m) for m in made))
    print("Frames are tiled in filename order, left-to-right, top-to-bottom.")
    return 0


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Mechanical half of a media ingest (a toolbox - compose as needed).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Judgement stays in AGENTS.md. This file crops images; it does not decide "
               "what they mean.",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("transcript", help="VTT -> de-duplicated timestamped blocks")
    p.add_argument("vtt")
    p.add_argument("out")
    p.add_argument("--block-seconds", type=int, default=15)
    p.set_defaults(func=cmd_transcript)

    p = sub.add_parser("probe", help="ADR-0003 static-video probe (+ ADR-0006 confirmation)")
    p.add_argument("video")
    p.add_argument("--confirm-out", default=None,
                   help="where to write the ADR-0006 confirmation sheet "
                        "(default: <video dir>/probe_confirm.jpg)")
    p.add_argument("--no-confirm", action="store_true",
                   help="skip the confirmation sheet on a STATIC verdict. You are then "
                        "honouring an advisory verdict unchecked - record that in SOURCE.md.")
    p.set_defaults(func=cmd_probe)

    p = sub.add_parser("frames", help="extract frames at given timestamps")
    p.add_argument("video")
    p.add_argument("--at", required=True, help="comma-separated seconds, e.g. 233,290")
    p.add_argument("--out", required=True)
    p.add_argument("--prefix", default="frame_")
    p.add_argument("--width", type=int, default=1100)
    p.add_argument("--quality", type=int, default=3)
    p.add_argument("--crop", action="store_true", help="crop to the slide area")
    p.set_defaults(func=cmd_frames)

    p = sub.add_parser("sheet", help="tile frames into contact sheets for triage")
    p.add_argument("dir")
    p.add_argument("--out", required=True, help="output stem, e.g. /tmp/sheet")
    p.add_argument("--cols", type=int, default=3)
    p.add_argument("--rows", type=int, default=3)
    p.add_argument("--tile-width", type=int, default=560)
    p.set_defaults(func=cmd_sheet)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
``````

#### `tools/build_site.py`

``````python
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
``````

### 5.4 Source template

#### `sources/_TEMPLATE/SOURCE.md`

``````markdown
# Source - <TITLE>

> Persona: **curator** (media) / **code-explorer** (code) - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table. The agent fills it on the paste-a-URL trigger
> and keeps it current. Name this folder `YYMMDD_slug` (see `../../AGENTS.md`).

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | video / blog / paper / code |
| URL | <url> |
| Title | <title> |
| Author / channel | <name> |
| Published | <date, if known> |
| Duration / length | <mm:ss for video, page/word count, or repo LOC> |
| Commit SHA | <for code: pin the snapshot, e.g. a1b2c3d> |
| License | <for code: the repo license, e.g. MIT> |
| Ingested | <date> |
| Access | open / paywalled-accessible / limited (note any restriction) |
| Topics | <agents, mcp, skills, rag, agent-security, inferencing, ...> |
| Visual leg | analysed (N frames kept) / skipped (user) / skipped (static probe: N distinct) / n/a (code) |
| Status | capture / understand / researched (optional) / distill / awaiting-promotion / compounded / blocked / partial |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. For **code**: `MAP.md` - repo orientation (what it demonstrates, module map, key flow).
3. `raw/` (media) or `repo/` (code, git-ignored) - the captured ground truth.
4. `nodes.md` - knowledge nodes (corroborated claims + visuals/diagrams + citations).
5. `context/` - **external evidence** from a deep-research pass (empty unless requested).
6. `LEARNING.md` - the distilled learning document.
7. `visuals/` - the curated frames/figures/generated diagrams.

## Ingest notes

- Capture method used (yt-dlp captions / Whisper / web_fetch / PDF / git clone): ...
- Visual pre-filter result (candidates after scene-detect + dedup) / code orientation summary: ...
- Anything notable / limitations: ...

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
``````

#### `sources/_TEMPLATE/nodes.md`

``````markdown
# Knowledge nodes - <TITLE>

> Persona: **fact-checker** - re-adopt when working this file.

> The atomic units of knowledge extracted from this source. Each node has a **stable ID** (`n1`,
> `n2`, ... - never renumber; topic notes reference these), a claim, **both legs each with its own
> citation** (or one leg marked `single-leg`), a gate verdict, and a confidence. Only
> `corroborated`/`single-leg` nodes (and recorded `divergence` findings) feed `LEARNING.md` and get
> promoted to `../../brain/`. The **fact-checker** persona owns the verdicts; see `../../AGENTS.md`
> and `prd.md` §6.

## Nodes

| ID | Claim (crux) | Evidence leg + citation | Corroborating leg + citation | Gate | Confidence |
|---|---|---|---|---|---|
| n1 | <one-line claim> | `visuals/frame_0814.jpg` - slide "..." | narration "..." @ `<url>&t=494s` | corroborated | OK |
| n2 | <claim, talking-head> | narration "..." @ `<url>&t=690s` | (no useful visual) | single-leg | needs-check |
| n3 | <code claim> | `src/server.ts:120` - "..." @ `https://github.com/<owner>/<repo>/blob/<sha>/src/server.ts#L120` | README "tools are registered at startup" @ `<repo-url>/blob/<sha>/README.md#L12` | corroborated | OK |

## Dropped / divergences (audit trail)

| Candidate | Verdict | Note |
|---|---|---|
| `frame_0132` | dropped | text never mentions it; likely incidental slide. |
| `src/auth.ts:44` | divergence | docs say "OAuth required"; code allows anonymous - **finding**, kept. |

> **Citations - cite BOTH legs.** Video -> `<youtube-url>&t=<seconds>s`; blog -> `source, <section
> heading>`; paper -> `source, Figure/Table N, §`; **code -> an immutable GitHub blob permalink
> containing the SHA** (`<repo-url>/blob/<sha>/<path>#L<n>`) so it stays inspectable after the local
> `repo/` clone is gone (fall back to `path:line @<sha>` for non-GitHub). A `single-leg` node cites
> its one leg and leaves the other cell `(none)`.
``````

#### `sources/_TEMPLATE/LEARNING.md`

``````markdown
# Learning - <TITLE>

> Persona: **curator** (media) / **code-explorer** (code) **+ mentor, always**. Re-adopt when working
> this file. Mentor is not conditional here: this document exists to be *learned from*, so the
> teaching voice is the default and not a mode you switch on. Add **fact-checker** at the gate and
> **architect** when mapping which topics this feeds.

> The distilled document you learn from - text anchored by a few curated visuals. Built from the
> corroborated nodes in `nodes.md`. Every claim is cited. Signal, not archive (3-8 visuals, not
> hundreds). See `SOURCE.md` for metadata.

> **Voice: an AI architect ramping up a new senior engineer.** Not a summary of the source, and not
> notes for someone who already sat through it. Your reader is strong, will not need hand-holding on
> engineering, and **has never met this subject** - so give them the mental model and the design
> rationale, not steps. They should finish able to *hold* the subject and argue about it.
>
> Two consequences of that reader being **senior**, and they are what make the voice specific:
> - **Earn every claim.** They will push back, so weak evidence must be labelled where it is used,
>   not buried in a caveat at the end. Say what the source did *not* establish.
> - **Teach judgement, not topology.** They can infer the mechanics; what they cannot infer is why
>   the boundary sits there, which part is expensive, and what breaks at scale.
>
> **Calibration: enough fundamentals, never 101.** Teach every fundamental *the subject itself*
> needs - OAuth's front channel vs back channel, what `tools/list` costs, what a cross-encoder is -
> and none of the field's ("what is a token", "what is an LLM"). If the source assumes knowledge its
> reader will not have, supply it; if the field already assumes it, do not.
> *(Distinct from the deep-research calibration in `AGENTS.md`, which aims one level **above** the
> source. That is for `context/` notes; this is for the source's own subject.)*

## TL;DR

<2-4 sentences: what this source teaches and why it is worth knowing.>

## The 1-minute version

| | |
|---|---|
| **The problem** | <what is actually hard, in one or two sentences> |
| **Why the obvious answer fails** | <the naive approach and the specific way it breaks> |
| **The idea** | <the crux, stated plainly> |
| **How it works** | <the mechanism, compressed> |
| **What it costs** | <the trade the design makes, and what it rules out> |
| **How far to trust it** | <evidence class in one line: measured? third-party? vendor self-report?> |

<!-- The whole argument in ~60 seconds. NOT a teaser - a reader who stops here should have the
     argument. Rows are adaptable to the source; keep each to a sentence or two. If a row cannot be
     filled without the walkthrough, the row is wrong. It is also a design check on you: an argument
     you cannot compress into six rows is usually one you have not finished deriving. -->

## Key claims

- <Claim 1.> `<citation>`
- <Claim 2.> `<citation>`
- <Claim 3.> `<citation>`

## What you will learn, and in what order

```mermaid
flowchart TB
    subgraph A["A. <why the subject is harder than it looks>"]
        S1["1 - <section>"]
    end
    subgraph B["B. <the thing itself, taught once>"]
        S2["2 - <section>"]
    end
    subgraph C["C. <the variations, as deletions from B>"]
        S3["3 - <section>"]
    end
    A --> B --> C

    style B fill:#e8f0fc
```

<!-- A roadmap of the walkthrough, grouped into movements, with a colour on the movement carrying the
     core technique. It exists so the reader knows the shape before committing - and writing it is
     the cheapest check that the walkthrough HAS a shape. Carries a walkthrough like any diagram:
     say which movements may be skimmed and which is the payload. Mark it synthesized. -->

## Walkthrough

<The distilled narrative - the mental model and the crux, in order. Anchor the key moments to
their visuals below. Use `> 💡 <term>` explainers for new concepts (mentor persona).>

<!-- NUMBERED SECTIONS, TITLED BY WHAT YOU LEARN. Their shape follows the SOURCE's own logic - do
     not force every source into one fixed outline. What is required is the six properties, from
     AGENTS.md "Writing a LEARNING.md (the required shape)". In brief:

       1. IT FLOWS. Each section ends by raising the question the next one answers; each opens by
          picking up what the last established. This is the one that separates a ramp from a wiki.
       2. IT IS VISUAL-LED. Built around the curated frames, one teaching step each, in order, with
          their "what it teaches" / "corroborated by" pair.
       3. IT PLANTS FORWARD AND PAYS OFF. Name a detail early, tell the reader to hold it, discharge
          it later.
       4. IT DERIVES RATHER THAN LISTS. Ask what the previous components structurally cannot answer
          and let each residual question name the next.
       5. FUNDAMENTALS GO INLINE WHERE NEEDED, marked "> **Background, supplied.**" and uncited by
          construction. NOT one Foundations block at the front.
       6. WEAK EVIDENCE IS LABELLED AT THE POINT OF USE (single-leg, vendor self-report,
          figure-only), never deferred to the end.

     Order for the reader who does not know it yet: open on why the subject is hard or what it
     costs, teach the thing once and properly, then let the variations become deletions from it.
     The anti-pattern is the PUNCHLINE OPENING - right for a TL;DR, wrong for everything after.

     Worked examples: 260725_closed-loop-evals-multimodal-agent (flow, three eval shapes),
     260725_oauth2-oidc-plain-english (forward planting, "What has aged"),
     260802_agent-data-stack (deriving a design one residual question at a time).

     Delete this comment; keep the properties. -->

### 1. <What the reader learns first - usually why this is harder than it looks, or what it costs>

<The concrete problem a senior engineer will recognise or soon hit. This section is why they keep
reading; it is not optional and it is not a restatement of the TL;DR.>

### <Key visual 1 - what it shows>

![<caption / crux>](visuals/<file>.jpg)

- What it teaches: <crux>. `<citation with &t=...>`
- Corroborated by: "<the text/transcript quote>".

### <Key visual 2 - what it shows>

![<caption / crux>](visuals/<file>.jpg)

- What it teaches: <crux>. `<citation>`

## Diagram (mental model)

```mermaid
flowchart LR
    A[concept] --> B[concept]
```

<!-- Every diagram carries a walkthrough - see AGENTS.md "Every diagram carries a walkthrough".
     Write it as a mentor ramping up an engineer. Delete these four labels, keep the substance. -->

**How to read it:** <direction of flow; what the shapes and colours mean; a legend if colour carries
meaning.>

**The crux: <the one idea this diagram exists to convey - if you cannot say it in one sentence,
delete the diagram.>**

**Why it is shaped this way:** <the design rationale, and what would go wrong with a different shape.
This is the part that teaches judgement rather than topology. Do NOT narrate the arrows - the reader
can see those. Explain what they cannot see: why the boundary sits there, which box is expensive,
what breaks at scale.>

*Synthesized from `n<x>`, `n<y>`.* <or the normal citation if the diagram was lifted from the source.>

## 💡 Terms

| Term | Explanation |
|---|---|
| <term> | <1-2 sentence 💡 definition> |

## What has aged (read before applying)

<ONLY for dated sources. A per-recommendation table: what the source says, its status now, what to
do. State the generalisation: when a source ages the MECHANICS usually survive and the
RECOMMENDATIONS usually do not, because a recommendation encodes a trade-off against the
alternatives available at the time. Mark verdicts as commentary if they rest on background knowledge
rather than a cited source. Delete this section if the source is current.>

## What to distrust in this note

<Source-level trust, NOT claim-level caveats (those stay inline where used): tier and commercial
interest, sample size, what the figures do and do not measure, which of the note's most REUSABLE
claims are the least corroborated, and a line naming the "Background, supplied" blocks as yours and
uncited.>

## Open questions

- <Anything flagged needs-check or open-question, with why. This is the deep-research backlog.>

## Feeds these topics

- `../../brain/topics/<topic>.md` - <which claims were promoted>
``````

#### `sources/_TEMPLATE/MAP.md`

``````markdown
# Map - <REPO NAME>

> Persona: **code-explorer** (+ architect when mapping topics) - re-adopt when working this file.

> **Code sources only.** Repo orientation written by the **code-explorer** persona on a fresh
> clone, before deep tracing. The goal is to learn *what this repo demonstrates* and how to
> navigate it - not to read every line. See `SOURCE.md` for metadata (URL, commit SHA, license).

## What this repo demonstrates

<1-3 sentences: the transferable thing worth learning here, e.g. "a reference MCP server showing
how tool registration wires into a streaming HTTP request loop.">

## How to run / build (learning context only)

<The build/run story in brief - enough to understand the moving parts. We are learning, not
shipping.>

## Module map

| Path | Role |
|---|---|
| `src/<...>` | <what lives here> |
| `<...>` | <...> |

```mermaid
flowchart TD
    A[entry point] --> B[module]
    B --> C[module]
```

> The diagram is **generated from the code** and must match it (`path:line`). It is the code
> source's "visual leg" - corroborate it against the actual structure.

## Entry points

- `path:line @<sha>` - <what happens here>

## Key flow (the one worth tracing)

<Name the single most instructive flow and trace it end-to-end. Each hop cites `path:line @sha`.>

```mermaid
sequenceDiagram
    participant Caller
    participant Module
    Caller->>Module: request
    Module-->>Caller: response
```

<!-- Every diagram carries a walkthrough - see AGENTS.md. Delete these labels, keep the substance. -->

**How to read it:** <direction of flow; what each participant is; a legend if colour or shape carries
meaning.>

**The crux: <the one thing this flow teaches about the repo - if you cannot say it in a sentence,
you have not finished tracing it.>**

**Why it is shaped this way:** <why the code is factored this way, what the boundaries buy, and what
would break if they moved. Do NOT narrate the arrows - explain what the reader cannot see from the
diagram: which hop is expensive, where the surprising indirection is, what the docs claim happens
here versus what the code actually does.>

*Generated from the code at `path:line @<sha>` - a diagram the repo does not contain.*

## Concepts to learn here (queue)

- [ ] <concept 1 - trace it, produce a node>
- [ ] <concept 2>

> Each concept, once traced and corroborated (docs↔code), becomes a node in `nodes.md` and, if
> transferable, is promoted to `../../brain/topics/*.md`.
``````

#### `sources/_TEMPLATE/raw/README.md`

``````markdown
# raw/ - captured source text (ground truth)

Holds the **text leg** of this source, captured verbatim before distillation:

- **Video:** `transcript.vtt` (+ `.json` with timestamps) from yt-dlp captions, or Whisper output.
- **Blog:** `article.md` (clean text from web_fetch).
- **Paper:** `paper.pdf` + `paper.txt` (extracted text).

Everything in `raw/` is **transient local scratch** and git-ignored (except this README) - see
`../../.gitignore`. It is processed then discarded; only derived text worth keeping is promoted into
`SOURCE.md` / `LEARNING.md` / `nodes.md`, and curated frames that survive the corroboration gate
live in `../visuals/`. Nothing here is authoritative once distilled, so it never needs committing.
``````

#### `sources/_TEMPLATE/visuals/README.md`

``````markdown
# visuals/ - curated, kept frames and figures

The **visual leg** of this source, but only the ones that **passed the corroboration gate** and
were curated into the learning document. A handful, not a dump (signal, not archive).

- Video frames: `frame_<seconds>.jpg` (name encodes the timestamp for citation).
- Blog/paper figures: `figure_<n>.png`.

Each file is referenced by a node in `../nodes.md` (with its citation and gate verdict) and, if
selected, embedded in `../LEARNING.md`. Raw pre-curation frame dumps do **not** belong here - they
stay under `../raw/` (all of which is git-ignored except its README).
``````

#### `sources/_TEMPLATE/context/README.md`

``````markdown
# context/ - external evidence (deep research)

> Persona: **fact-checker + synthesizer** (+ **mentor** when teaching).

Notes produced by the **deep research** step - the optional pass that reaches *outside* this source
to test what it claims and to attach the intellectual context around it. See "Deep research on
request" in `../../../AGENTS.md` for the full contract.

**This folder is empty unless the user asked for deep research.** It is never automatic.

## What lives here

One note per research pass, named `<NN>_<slug>.md` (`01_context-window-prior-art.md`), numbered in
order. Each note is **permanent and committed** - unlike a harness's session-scoped research output,
which disappears. Ephemeral output that never reached a kit file did not happen.

## What does *not* live here

- **The source's own claims** - those are `../nodes.md`.
- **The distilled lesson this source taught** - that is `../LEARNING.md`, which answers exactly one
  question: *what did this source teach?* Keep external findings out of its body, or you lose the
  distinction between "the author claims this" and "the field thinks this". `LEARNING.md` may
  **cite** a note here; it must not absorb it.
- **Durable cross-source synthesis** - that belongs in `../../../brain/topics/*.md`.

## Note structure

```markdown
# Research - <question or node cluster>

| Field | Value |
|---|---|
| Pass | 01 |
| Date | YYYY-MM-DD |
| Targets | n4, n8, n9 (node IDs from ../nodes.md) |
| Budget used | 5 searches / 7 fetches (cap: 8 / 12) |

## Findings

| Node | External finding | Verdict | Source (tier, independent?) |
|---|---|---|---|
| n8 | ... | supports / contradicts / refines / no-evidence | <url> (T1, independent) |

## Synthesis
<What this changes about how to read the source - one level above it, no 101 explainers.>

## Cross-domain framing
<The established name in the older discipline, if there is one.>

## Confidence assessment
<Assumptions made without asking, what stayed unresolved, where evidence was thin.>

## Fed back into
- `../nodes.md` - <node confidences updated>
- `../../../brain/claims.md` - <rows added / citations appended>
- `../../../brain/glossary.md` - <terms>
```
``````

### 5.5 Architecture decision records (the why, minus this brain's content decisions)

#### `brain/decisions/0000-template.md`

``````markdown
# ADR 0000: <short decision title>

> Copy this file to `NNNN-slug.md` (next number, kebab-case slug) for each durable structural
> decision about the brain's taxonomy or conventions. Keep the *why* so it survives after the
> context is gone. Owned by the **architect** persona.

| Field | Value |
|---|---|
| Status | proposed / accepted / superseded by ADR-NNNN |
| Date | YYMMDD |
| Deciders | chamin |

## Context

What situation forced a choice? What was ambiguous or in tension? Cite the sources / topic notes
involved (`../topics/<topic>.md`, node IDs, `path:line`).

## Decision

The choice made, stated plainly. If it is a **one-way door** (costly to undo once many sources
reference it), say so explicitly.

## Alternatives considered

- **Option A** - why not.
- **Option B** - why not.

## Consequences

What becomes easier, what becomes harder, and what to revisit later. Note any follow-up edits to
the root `INDEX.md` or the affected `../topics/*.md`.
``````

#### `brain/decisions/0002-deep-research-stage.md`

``````markdown
# ADR 0002: Add an optional deep-research stage (external evidence)

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260725 |
| Deciders | chamin |

## Context

The kit's corroboration gate produces **internal** consistency: a slide agrees with the narration,
code agrees with its docs. `AGENTS.md` has always been explicit that this is *not* truth, and that
real confidence needs a **second source**. Nothing in the kit actually went and got one.

The evidence after two ingests: `brain/claims.md` holds 23 claims, of which exactly **one** (#11) is
cross-source. Both current sources are practitioner conference talks with no measurements. During
the 12-factor ingest the only external artifact fetched - the companion repo README - turned out to
**share an author** with the talk, so it corroborated the framework as stated but not that it works.
That distinction had to be spotted and written by hand, which means it would be missed on a tired
day.

Separately, chamin's stated goal for the kit is first-principles depth: each source should land into
an already-understood conceptual neighbourhood, with the concept *one level above* it attached (his
example: recognising agent skill design as **procedural memory**). Nothing in the flow reached
outward to supply that.

Copilot CLI ships a `/research` command; Claude Code has no built-in equivalent. Its docs were read
before designing this ([GitHub Docs](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/research)).

## Decision

Add **deep research** as an **optional stage between the gate and distillation**, triggered only
when the user says "deep research" (or runs `/research`). Never automatic.

Five design commitments, each chosen against an obvious alternative:

1. **Target gated node IDs, not the subject.** Open-ended topic research yields adjacent reading and
   makes the agent a summarizer; node-targeted research returns a verdict that changes a confidence
   value - `supports` / `contradicts` / `refines` / `no-evidence`.
2. **Tiered sources (T1-T5) plus a hard independence rule.** Same author, organisation or commercial
   interest = the same leg wearing a different hat: record and cite it, but **never** let it raise
   confidence. This encodes the judgement that had to be made manually on the 12-factor repo.
3. **`no-evidence` is a first-class result.** "This rests on one practitioner's experience" is a
   finding worth recording, not a failed search to pad with weak hits.
4. **Output is a permanent kit file** - `sources/<id>/context/<NN>_<slug>.md`. Copilot CLI writes
   research to a throwaway session directory; this kit deliberately inverts that, per its standing
   rule that ephemeral output not captured into a kit file did not happen.
5. **Research stays out of `LEARNING.md`'s body.** That file answers exactly one question - *what did
   this source teach?* Blending external findings in would destroy the distinction between "the
   author claims this" and "the field thinks this", which is what the citation discipline exists to
   preserve. `LEARNING.md` may cite a `context/` note; it must not absorb one.

Borrowed from Copilot CLI's `/research`: the **autonomous stance** (never interrupt with clarifying
questions; state assumptions in a **Confidence assessment** section instead) and writing a full
markdown report to disk rather than answering in the transcript.

## Alternatives considered

- **Automatic research on every ingest** - rejected: slow, token-heavy, and most sources do not earn
  it. Optionality is what keeps the default ingest fast.
- **Research the topic, not the nodes** - rejected: produces a reading list. The whole value is
  moving a specific claim's confidence, which requires a specific claim.
- **Write findings into `LEARNING.md`** (chamin's initial framing) - rejected for the reason in
  decision 5. Discussed and agreed before implementing.
- **A flat "credible sources" whitelist** (Anthropic, OpenAI, DeepMind, arXiv, Cursor, Pulse MCP) -
  rejected as too blunt: a vendor blog is primary on its own system but *positioned* on the field,
  and arXiv is preprint. Flattening them would quietly manufacture false confidence. Kept the named
  sources, but as tiers.
- **Put the contract in `.claude/commands/research.md`** - rejected: `AGENTS.md` is the single
  source of truth for every harness. The command file is a thin wrapper that points at it.

## Consequences

- **Easier:** `claims.md` should stop being a single-source store. Open questions written by hand
  ("no measurement anywhere for the context-limiting claim") become actionable research targets.
- **Harder:** an extra stage to keep honest. The independence rule in particular is easy to
  rationalise around when a source *looks* corroborating.
- **New surface:** `sources/_TEMPLATE/context/` ships with every new source (empty by default), and
  `SOURCE.md` gains a `researched` status.
- **Cost:** capped at 8 searches / 12 fetches per pass, with an early stop on two independent
  agreeing sources.
- **Validated on first run (same day).** The shakedown pass ran against the 12-factor source
  (`sources/260725_12-factor-agents/context/01_context-limits-and-decomposition.md`), spending 5
  searches / 8 fetches of the 8 / 12 budget. It **closed both** flagged open questions - the
  micro-agent claim gained a measurement (+13.1 to +41.5 pp across 10 models) and the context claim
  gained peer-reviewed and 18-model evidence - and produced **two findings absent from the source**:
  a measured boundary (naive memory scaffolds hurt 6 of 10 models) and the Event Sourcing framing.
  Design decisions 1 (node-targeted) and 2 (tiers + independence) both did visible work: the
  Anthropic convergence only counts *because* independence was checked, and a search summary asserted
  the decomposition figures before they could be verified - they were kept only after direct
  confirmation against the paper's full text, which is exactly the failure the contract's
  no-fabrication rule exists to catch.
- **Revisit when:** the first few passes reveal whether node-targeted scope is too narrow. If real
  questions keep spanning sources, add a topic-level mode that writes to `reports/` instead.
``````

#### `brain/decisions/0003-optional-visual-leg.md`

``````markdown
# ADR 0003: Make the visual leg optional (opt-out), with a free static-video probe

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260725 |
| Deciders | chamin |

## Context

Frame extraction and `view`ing are the most token-expensive steps in a media ingest. On a slide-heavy
conference talk that cost is the entire point - the slides *are* the second leg, and the two ingests
so far both depended on them. On a **podcast, webcam interview, or fireside chat the picture never
changes**, so the same spend buys nothing: the agent looks at ten near-identical stills of a person
talking and extracts no crux from any of them.

The kit already handled this as an *accident* - the degrade table said "talking-head video, no useful
frames -> transcript-only, `single-leg`". It had no way to make it a *decision* taken up front,
before the tokens are spent.

Two asymmetries shaped the design:

- **Opposite default from deep research (ADR-0002).** Research is opt-**in** because it is expensive
  and rarely needed. The visual leg is opt-**out** because it is usually the whole reason the source
  is a video rather than an article.
- **The probe is already free.** Scene-detect + `imagehash` dedup is the *first* step of the existing
  pipeline and is pure shell work - no tokens. It therefore doubles as a static-video detector at
  zero marginal cost, which means the default can be made smart rather than merely obedient.

## Decision

**Analyse the visual leg by default. Skip it in three cases**, in priority order:

1. **User opt-out** - "don't analyze video", "transcript only", or similar. Explicit instruction wins
   and skips even the probe.
2. **Static-video probe** - if the whole video yields **<= 3 distinct frames** after scene-detect +
   phash dedup, treat it as visually static, auto-degrade to transcript-only, and say so in one line.
   (Calibration: `260725_12-factor-agents`, a slide-heavy talk, yielded 19 distinct.)
3. **Capture failure** - no video stream or download blocked.

**The consequence is recorded, never discovered.** Dropping the visual leg means every node from that
source is **`single-leg` by construction** - there is no second leg left to corroborate against, and
a transcript agreeing with itself is not two legs. So `SOURCE.md` gains a **Visual leg** field
(`analysed (N frames kept)` / `skipped (user)` / `skipped (static probe: N distinct)` / `n/a (code)`),
every such node is gated `single-leg` / `needs-check`, and the agent states the trade-off in one line
when it happens.

**Deep research is the designated complement.** With the visual leg gone the only route back to two
legs is **external** evidence, not a harder look at the video. The two switches from ADR-0002 and
this one compose deliberately: skip the cheap internal leg, buy an expensive external one *only if
the source turns out to matter*.

The rule generalises to blogs with decorative-only images and papers with unreadable figures. Code
sources are unaffected - their visual leg is *generated* from the code and generating a diagram is
cheap.

## Alternatives considered

- **A pure manual flag, no probe** (the literal request) - rejected as strictly worse: the probe is
  free, already the first pipeline step, and catches the podcast the user forgot to flag. The manual
  switch is kept and takes priority; the probe just makes the default competent.
- **Auto-detect only, no manual switch** - rejected: the user knows "this is a podcast" before any
  shell command runs, and skipping the download entirely is cheaper than probing it. Explicit
  instruction should never be second-guessed by a heuristic.
- **Make it opt-in like deep research** - rejected: it would silently degrade the common case
  (slide-heavy talks), where the visual leg is the source's main value.
- **Let transcript-only nodes count as `corroborated`** when the narration is internally consistent -
  **firmly rejected.** A transcript agreeing with itself is one leg. Allowing this would quietly
  destroy the meaning of `corroborated` across the whole brain, which is the kit's core asset.

## Consequences

- **Easier:** podcasts and interviews become cheap to ingest instead of wasteful, which lowers the
  bar for ingesting them at all.
- **Harder:** a second thing to record honestly. The temptation on a skipped-visual source will be to
  mark a well-argued claim `corroborated`; the contract forbids it.
- **Watch:** the `<= 3 distinct frames` threshold is a heuristic from a sample of one calibration
  point. Revisit after a few podcast ingests - screen-shares and demo-heavy streams are the likely
  false negatives, and a video that *starts* static but shares a screen at minute 40 could be
  mis-classified. If that happens, consider probing in windows rather than over the whole video.
- **Untested.** No podcast or interview has been ingested yet, so neither the switch nor the
  threshold has run in anger.
``````

#### `brain/decisions/0004-validator-as-type-checker.md`

``````markdown
# ADR 0004: Add `validate.py` as the type checker for the prose contract

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260725 |
| Deciders | chamin |

## Context

Brain is a convention, not an application (`prd.md` §0): the pipeline, the corroboration gate and
the file schema live as English in `AGENTS.md`, and the agent is the runtime. The upside is that new
capabilities ship as paragraphs - ADR-0002 and ADR-0003 both added real behaviour without a line of
code. The structural weakness is the mirror of that: **prose has no compiler.** Nothing enforces the
rules but the agent's willingness to follow them, and drift does not fail loudly - it accumulates.

`prd.md` §10 already anticipates **volume** pressure (grep slowing down at a few hundred sources,
answered by a vector index). It does not anticipate **consistency** pressure, which arrives far
earlier. Evidence from a single working day at **two** sources:

- `brain/log.md` was left non-chronological **twice** and hand-corrected both times.
- ADR-0002 nearly stayed marked "untested" after it had been tested.
- The `claims.md` footnote asserting "the only cross-source claim" went stale within one pass.
- INDEX integrity and frame-citation pruning were verified by throwaway shell loops written on the
  spot, then discarded - violating the kit's own rule that ephemeral output not captured into a kit
  file did not happen.

Every one of those is a *form* error a machine can catch.

## Decision

Add **`validate.py` at the repo root**, run before the `git diff` at the end of any compound,
research or close-the-loop pass, and in CI on every push and PR.

Constraints that shaped it:

- **Stdlib only.** CI must not need a venv to check a folder of Markdown. The kit's `requirements.txt`
  exists for the *ingest* pipeline; validation must not inherit it.
- **It enforces the contract, it does not define it.** If a check and `AGENTS.md` disagree,
  `AGENTS.md` wins and the check is the bug. Stated in both files so the precedence never drifts.
- **Form, never judgement.** It cannot decide whether a claim is corroborated, whether a frame earns
  its place, whether a topic should split, or whether a source is genuinely independent. Encoding
  those would be worse than useless - it would launder judgement as a green check. They stay with the
  fact-checker and architect personas.
- **Mutation-tested.** Each of the ten checks was verified against a deliberately corrupted copy of
  the repo. A validator that passes because it is broken is worse than no validator, and the first
  run of that test caught a bad *test* (see Consequences).

## Alternatives considered

- **Do nothing; rely on the agent following `AGENTS.md`** - rejected on the evidence above. The
  contract was violated repeatedly in the same session that wrote it, by an agent that had it in
  context the whole time.
- **A pre-commit hook instead of CI** - rejected as the primary mechanism: hooks are per-clone and
  easy to bypass, and the repo is headed for a public release where contributors' PRs must be
  checked. A hook is a fine optional addition later.
- **Encode judgement too** (score corroboration, flag "weak" claims) - firmly rejected. A green check
  on a judgement call would manufacture false confidence, which is the exact failure mode
  `prd.md`'s confidence semantics were written to prevent.
- **Wait for more sources before building it** - rejected: the failures are already happening, and
  every check written now is one that stops being re-derived ad hoc each session.

## Consequences

- **Easier:** drift fails loudly instead of accumulating. Contributors get the conventions enforced
  automatically rather than by review. Three checks that were being hand-written each session are now
  captured.
- **Harder:** one more thing to keep honest. A check that disagrees with `AGENTS.md` must be fixed,
  not worked around, or the contract quietly becomes whatever the script happens to accept.
- **Known limitation, deliberately accepted:** the `log.md` check compares dates only, so it **cannot**
  catch an entry misordered *within a single day* - which is precisely the mistake that occurred twice.
  Per-entry timestamps would catch it and are not worth the ceremony. Documented in the code and in
  `AGENTS.md` rather than left as a silent gap.
- **Found on the first run:** three genuine defects, all in the validator rather than the repo - two
  false positives from following the git-ignored `AGENTS.md` symlinks, and one from counting raw
  substring matches instead of table rows. Worth recording because it is the expected shape of early
  validator bugs: a checker's first job is to be more correct than the thing it checks.
- **Revisit when:** checks start needing repo state a regex cannot see (e.g. verifying a citation's
  timestamp against a transcript), or if false positives make people add ignore-comments - the point
  at which a validator starts costing more trust than it earns.
``````

#### `brain/decisions/0005-mechanical-toolbox.md`

``````markdown
# ADR 0005: Freeze the mechanical ingest steps as `tools/ingest.py` (a toolbox, not a pipeline)

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260725 |
| Deciders | chamin |

## Context

`prd.md` §10 deferred packaging the mechanical pipeline (`yt-dlp` -> `ffmpeg` -> `imagehash`) with an
explicit revisit trigger: **after ~5-10 real ingests**, "only when the Markdown convention actually
hurts". The brain is at **2** ingests, so on that trigger alone this would be premature.

Two things changed:

1. **ADR-0003 created a deterministic contract rule with no canonical implementation.** The visual-leg
   switch turns on "<= 3 distinct frames after scene-detect + phash dedup". Distinctness depends
   entirely on two constants - the ffmpeg scene threshold and the pHash Hamming distance - and both
   lived only in prose. Two agents would compute different verdicts for the same podcast, and a
   verdict computed with different constants is not comparable to any previous source's. **A
   threshold nobody can reproduce is not a rule.**
2. **The same code kept being written and thrown away.** During the 12-factor ingest, `vtt_clean.py`
   and `dedup.py` were both written into a scratch directory and evaporated with the session -
   violating the kit's own rule that ephemeral output not captured into a kit file did not happen.

The underlying principle, which is what makes this narrow rather than a general push toward scripts:
**generate what should vary, freeze what should not.** On-the-fly code is right when variation is a
feature - mid-ingest the phash dedup was abandoned for transcript-anchored extraction, and a rigid
script would have fought that. It is wrong when variation is a bug: VTT parsing has no reason to
differ between videos, and regenerating it re-rolls the dice on a parser whose output still looks
plausible when subtly wrong.

## Decision

Freeze the deterministic steps as **`tools/ingest.py`**, exposing four independent subcommands:
`transcript` (stdlib only), `probe` (the ADR-0003 verdict), `frames`, `sheet`. `AGENTS.md` instructs
agents to use it, and specifically to run `probe` rather than a hand-rolled equivalent.

Three constraints:

- **A toolbox, not a pipeline.** No `--url do-everything` entrypoint. `AGENTS.md`'s "the shell steps
  are reference, not a fixed script" still holds; assembly stays the agent's job, and `yt-dlp`
  invocations stay ad hoc because format selection genuinely varies.
- **Judgement never moves in.** Reading a slide, gating a claim, deciding which frames earn their
  place - those stay in `AGENTS.md` and `personas/`. The same line `validate.py` draws: **form is
  code, judgement is prose.**
- **Pipeline constants are named module-level values** (`SCENE_THRESHOLD`, `PHASH_DISTANCE`,
  `STATIC_FRAME_THRESHOLD`) with a comment saying that changing them makes every past verdict
  incomparable. That is the entire point of freezing them.

## Alternatives considered

- **Wait for 5-10 ingests, per `prd.md` §10** - overridden narrowly, on reason 1 only. The trigger
  was written before ADR-0003 existed; a contract rule that cannot be reproduced is a stronger
  argument than a usage count.
- **One `ingest.py --url <url>` that runs everything** - rejected: it would own the control flow the
  agent is supposed to own, and would have prevented the mid-ingest strategy switch that produced the
  contact-sheet method in the first place.
- **A `pip` package** (as `prd.md` §10 floats) - rejected for now: it hides the code from the agent
  reading the working tree, for no benefit at this size. A file in `tools/` is inspectable and
  editable in place.
- **Leave it in the harness's scratch directory** - rejected; that is precisely the failure being
  fixed.

## Consequences

- **Easier:** the ADR-0003 verdict is now reproducible across agents and sources. The contact-sheet
  triage (17 candidates -> 1-2 `view` calls) is available rather than being re-invented.
- **Harder:** a second frozen artifact to keep in step with the prose. If `AGENTS.md` and the tool
  disagree, `AGENTS.md` wins and the tool is the bug - same precedence as `validate.py`.
- **Verified, not assumed:**
  - `transcript` reproduces the hand-run output from the 12-factor ingest **byte-for-byte** (modulo a
    trailing newline).
  - `probe` was tested against synthetic static and multi-scene videos: 0 distinct -> `STATIC`,
    5 distinct -> `RICH`.
  - **Testing caught a genuine silent-failure bug:** `run_ffmpeg` originally ignored ffmpeg's return
    code, so *any* ffmpeg error produced zero frames and a `STATIC` verdict - the probe would have
    silently skipped the visual leg on error and never said why. It now fails loudly. This is exactly
    the class of bug prose review cannot catch, and the strongest argument for freezing the step.
  - Two of the test videos were themselves wrong before they were right (a full-range YUV artifact,
    then hue-rotated segments with near-identical luma that ffmpeg's luma-based scene detection
    correctly ignored). Recorded because it is the normal shape of this work: the test is as likely
    to be wrong as the code.
- **Revisit when:** a fifth subcommand is wanted, or when `yt-dlp` invocation stabilises enough to be
  worth wrapping (it is not yet).
``````

#### `brain/decisions/0006-static-probe-is-advisory.md`

``````markdown
# ADR 0006: The static probe's STATIC verdict is advisory, not dispositive

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260726 |
| Deciders | chamin |

## Context

[ADR-0003](0003-optional-visual-leg.md) made the visual leg skippable and gave the decision a free
mechanical signal: scene-detect plus pHash dedup already run as the first shell step, so a video
yielding `<= 3` distinct frames auto-degrades to transcript-only.
[ADR-0005](0005-mechanical-toolbox.md) then froze that computation in `tools/ingest.py probe`,
precisely so that "distinct" would not vary by agent.

Both were right. Neither anticipated the failure mode.

**Scene detection measures whole-frame delta.** A conference recording is usually a composited
stream: a fixed background, a fixed logo, a fixed speaker-at-podium video inset, a fixed track
footer, and a slide body occupying a minority of the pixels. When the slide changes, most of the
frame does not. The delta never crosses `SCENE_THRESHOLD`, and the probe reports a continuously
changing 20-slide deck as visually static.

**Two occurrences, one root cause, at two different stages:**

| Source | Stage that failed | Symptom |
|---|---|---|
| `260725_12-factor-agents` | pHash dedup | Slides sharing a template collapsed into each other; the ingest switched to transcript-anchored extraction. |
| `260726_dont-ship-skills-without-evals` | scene detection | `candidates=3 distinct=3 -> STATIC` on ~20 dense slides. |

The second is the dangerous one, because ADR-0003 makes STATIC **actionable**: honouring it discards
the entire visual leg and gates every node from the source `single-leg` by construction. On that
source it would have destroyed three specific nodes whose numbers **exist only on the slides** - the
skill-length lift curve (`n11`), "rewriting the description alone fixed 5 of 7 failures" (`n13`), and
the 39.2% -> 91.6% case-study table (`n28`).

**Why this is not just a bad constant.** Lowering `SCENE_THRESHOLD` would trade one false verdict
class for another (webcam noise and cross-fades would start reading as RICH), and worse, it would
break the property ADR-0005 exists to protect: **a verdict computed with different constants is not
comparable to any previous source's.** Five sources have already been measured with the current
values. The metric is wrong for this input class, not mis-tuned.

**The asymmetry that decides it.** The two errors do not cost the same. A false RICH wastes one
`view` call on a contact sheet. A false STATIC silently destroys a source's second leg, and the
contract's own degrade rule says that once you skip the visual leg you must **not** retro-mark nodes
`corroborated` - so the loss is not cheaply recoverable. **An asymmetric error deserves an asymmetric
check.**

## Decision

**A `STATIC` verdict is advisory. It must be confirmed by looking before it is honoured.**

`tools/ingest.py probe`, on `STATIC` only, now samples **9 frames spread evenly across the runtime**,
tiles them into one chronological contact sheet, and prints the path with an instruction to `view` it
before skipping the visual leg. Cost: **one `view` call**, on the branch that would otherwise throw
away the entire visual leg. `RICH` is unchanged and costs nothing new.

**The change is deliberately additive.** The verdict, `STATIC_FRAME_THRESHOLD`, `SCENE_THRESHOLD` and
`PHASH_DISTANCE` are untouched, so every past probe result stays comparable and no source needs
re-measuring. **Confirming a verdict is not the same as recomputing it** - that distinction is what
lets this coexist with ADR-0005 rather than eroding it.

Escape hatches, both explicit:

- `--no-confirm` skips the sheet and prints that you are honouring an advisory verdict unchecked,
  which must then be recorded in `SOURCE.md`.
- If the runtime cannot be read, the tool says the sheet could not be built and instructs the agent
  **not** to record a confirmed STATIC. Failure is never silent - the same rule that caught the
  swallowed `ffmpeg` exit code during ADR-0005's shakedown.

A user opt-out ("transcript only") still skips the probe entirely and therefore this too. Explicit
instruction outranks the mechanism, as in ADR-0003.

## Alternatives considered

- **Lower `SCENE_THRESHOLD`** - rejected. Breaks cross-source comparability (ADR-0005's whole point),
  and trades a false-STATIC class for a false-RICH class without fixing the mismatch between a
  whole-frame metric and a partial-frame change.
- **Add `--crop` to `probe`** so it measures only the slide region - rejected as the default. You
  cannot know the crop region without looking first, which is circular, and a per-source crop
  reintroduces exactly the parameter variance ADR-0005 froze. `frames --crop` already exists for use
  *after* you have looked.
- **Make the agent always eyeball a sheet before any probe** - rejected. That is a token cost on
  every ingest to defend against one branch, and it makes the free signal not free.
- **Leave it to the agent's judgement, documented in prose** - rejected, and this is the ADR-0005
  argument restated: the failure already happened twice with the rule in prose. The check belongs at
  the point of action, in the tool's own output, not in a paragraph the agent may or may not recall.
- **Drop the probe entirely** - rejected. It is right for the case it was built for (podcast, webcam
  interview) and costs nothing. The verdict is useful; its authority was too high.

## Consequences

**Easier.** A false STATIC now costs one `view` instead of a source's second leg. The
`260726_dont-ship-skills-without-evals` override becomes the documented default procedure rather than
an ad-hoc save. Agents get the warning where it is actionable - in the tool's output - rather than in
a contract paragraph.

**Harder.** A genuinely static video now costs one `view` call it did not before. That is the price
of the asymmetry and it is small. `probe` also now depends on `ffprobe` for the runtime, which ships
with `ffmpeg` and is already a hard dependency.

**To revisit.** If a third occurrence appears at a stage neither scene detection nor confirmation
covers, the metric itself should be reconsidered - most likely by measuring delta over a
centre-weighted region rather than the whole frame. That *would* be a constants change and would
need its own ADR plus a re-measurement note.

**Follow-ups completed in this pass:** `tools/ingest.py` (implementation + a reproduction test on a
synthetic templated deck: 9 distinct slides, `candidates=0 -> STATIC`, differences plainly visible on
the confirmation sheet); `AGENTS.md` § "The visual leg"; `prd.md` §5.1 and change log; a dated line in
[`../log.md`](../log.md).
``````

### 5.6 Plumbing

#### `requirements.txt`

``````text
# Brain helper packages - install into the local .venv
# macOS:   python3 -m venv .venv ; source .venv/bin/activate ; pip install -r requirements.txt
# Windows: python -m venv .venv  ; .\.venv\Scripts\Activate.ps1 ; pip install -r requirements.txt
# NOTE: ffmpeg is a SYSTEM binary, not a pip package:
#   macOS -> brew install ffmpeg
#   Windows -> winget install Gyan.FFmpeg  (or scoop/choco)

yt-dlp            # fetch YouTube transcripts (auto-captions) and audio
faster-whisper    # ASR fallback when a video has no captions
imagehash         # perceptual-hash dedup of sampled frames
pillow            # image handling for frame/figure processing
requests          # fetch article/paper assets (figures, PDFs)
markdown          # render brain/ + sources/ into the mobile reader (tools/build_site.py)
``````

#### `.gitignore`

``````text
# Local virtual environment
.venv/
__pycache__/
*.pyc

# Raw source material - transient local scratch; processed then discarded.
# Ignore everything under any raw/ folder except its README (which explains the folder).
sources/**/raw/*
!sources/**/raw/README.md

# Cloned code repos - snapshots for learning, never committed
sources/**/repo/

# Captured-but-not-ingested sources (see staging/README.md). A capture becomes a source when it is
# distilled, not when it is downloaded - until then it stays local and out of the contract.
staging/*
!staging/README.md

# Harness pointer symlinks - generated per clone by link-agents.sh / link-agents.ps1
# (AGENTS.md is the single canonical contract; these just point to it. Codex, Cursor and
#  Copilot CLI read AGENTS.md natively and need no link.)
/CLAUDE.md
/.github/copilot-instructions.md

# OS noise
Thumbs.db
.DS_Store


# The mobile reader - a pure render of brain/ + sources/, rebuilt by
# tools/build_site.py and published to GitHub Pages by CI. Never a source of truth.
/site/
tools/site_assets/vendor/
``````

#### `.gitattributes`

``````text
* text=auto eol=lf
``````

#### `link-agents.sh`

``````bash
#!/usr/bin/env bash
# link-agents.sh - macOS / Linux
# One canonical contract (AGENTS.md), symlinked to the pointer paths some harnesses expect.
# Run ONCE per clone. The links are git-ignored, so nothing tool-specific is ever maintained.
#
#   Copilot CLI, Codex, Cursor  -> read AGENTS.md natively (no link needed)
#   Claude Code                 -> CLAUDE.md
#   GitHub Copilot (IDE/agent)  -> .github/copilot-instructions.md
#
# Usage:  ./link-agents.sh
set -euo pipefail
cd "$(dirname "$0")"

ln -sf AGENTS.md CLAUDE.md
mkdir -p .github
ln -sf ../AGENTS.md .github/copilot-instructions.md

echo "Linked -> AGENTS.md:"
echo "  CLAUDE.md                        (Claude Code)"
echo "  .github/copilot-instructions.md  (GitHub Copilot IDE / coding agent)"
echo "Codex, Cursor and Copilot CLI read AGENTS.md natively - no link needed."
``````

#### `link-agents.ps1`

``````powershell
# link-agents.ps1 - Windows (PowerShell)
# One canonical contract (AGENTS.md), symlinked to the pointer paths some harnesses expect.
# Run ONCE per clone. The links are git-ignored, so nothing tool-specific is ever maintained.
#
#   Copilot CLI, Codex, Cursor  -> read AGENTS.md natively (no link needed)
#   Claude Code                 -> CLAUDE.md
#   GitHub Copilot (IDE/agent)  -> .github/copilot-instructions.md
#
# Symlinks on Windows require Developer Mode (Settings > For developers) OR an elevated shell.
# Usage:  .\link-agents.ps1
$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$pointerText = "Read AGENTS.md - it is the single source of truth for every agent harness."

function New-Link($link, $target) {
    if (Test-Path $link) {
        $item = Get-Item $link -Force
        $isSymlink = $item.Attributes -band [IO.FileAttributes]::ReparsePoint
        $isPointer = (-not $isSymlink) -and ((Get-Content $link -Raw -ErrorAction SilentlyContinue).Trim() -eq $pointerText)
        if (-not ($isSymlink -or $isPointer)) {
            Write-Host "  SKIP     $link already exists and is NOT a generated link/pointer - leaving it untouched."
            return
        }
        Remove-Item $link -Force
    }
    try {
        New-Item -ItemType SymbolicLink -Path $link -Target $target -Force | Out-Null
        Write-Host "  symlink  $link -> $target"
    } catch {
        # Fallback when symlinks aren't permitted: a tiny pointer file (still git-ignored).
        # NOTE: this is a POINTER, not a live link - it will not track edits to AGENTS.md.
        # Enable Developer Mode and re-run to get a real symlink.
        $pointerText | Set-Content -Path $link -Encoding utf8
        Write-Host "  POINTER  $link (symlink not permitted; wrote a static one-line pointer - NOT a live link)"
    }
}

New-Link 'CLAUDE.md' 'AGENTS.md'
New-Item -ItemType Directory -Force -Path '.github' | Out-Null
New-Link '.github\copilot-instructions.md' '..\AGENTS.md'

Write-Host "Codex, Cursor and Copilot CLI read AGENTS.md natively - no link needed."
``````

#### `.github/workflows/validate.yml`

``````yaml
name: validate

# The Brain kit is a prose contract - AGENTS.md specifies the pipeline, the corroboration
# gate and the file schema in English, and the agent is the runtime. Prose has no compiler,
# so this workflow is the type checker: it enforces the rules AGENTS.md already states.
# Stdlib only, so there is nothing to install.

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Validate kit conventions
        run: python3 validate.py

      # BUILD.md embeds AGENTS.md, the personas, the templates and both scripts verbatim so the
      # kit can be rebuilt from one file. Nothing stops it going stale except this check, and a
      # BUILD.md that claims to build the current kit but does not is worse than no BUILD.md.
      - name: Check BUILD.md is not stale
        run: python3 tools/make_build_doc.py --check
``````

#### `tools/make_build_doc.py`

``````python
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
        ".yml": "yaml", ".txt": "text", ".css": "css", ".js": "javascript"}


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
    ("The three frozen scripts", ["validate.py", "tools/ingest.py", "tools/build_site.py"]),
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
        # This generator ships with the bundle because the workflow above invokes it
        # (`make_build_doc.py --check`). Omit it and a kit built from BUILD.md alone gets a red
        # CI run on its first push - the bundle would break the very build it describes. It is
        # not one of the frozen scripts (ADR-0005) - it is the bundler, so it lives here
        # in plumbing beside the workflow that calls it.
        "tools/make_build_doc.py",
        # The reader's assets. tools/build_site.py is a frozen script above, but it is inert
        # without these three - AGENTS.md promises a mobile reader, so the bundle must ship one
        # that actually renders.
        "tools/site_assets/style.css", "tools/site_assets/app.js", "tools/site_assets/sw.js",
        ".github/workflows/pages.yml",
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
plus three small frozen scripts. That is why this file can rebuild it.

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
| `README.md`, `prd.md`, `how_to_use_this.md` | Their **procedural** role is this file, so a build from this bundle alone needs none of them. The durable design rationale lives in the ADRs (section 5.5), which **are** included. They are not dead weight, though: the reference repo ships all three, `README.md` is what a newcomer reads first, and `prd.md` carries the risk register and the changelog. Copy them across if you want the full documentation set. |
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
``````

#### `tools/site_assets/style.css`

``````css
/* Brain - mobile reading surface.
   One column, thumb-reachable navigation, legible at arm's length.
   Light and dark are both first-class: the OS decides, the toggle overrides. */

:root {
  --bg: #fbfbfa;
  --bg-soft: #f2f1ee;
  --card: #ffffff;
  --line: #e2e0da;
  --ink: #1b1c1e;
  --ink-2: #55575c;
  --ink-3: #86888e;
  --accent: #2f5fd0;
  --accent-soft: #e8eefc;
  --gold: #9a6b12;
  --gold-soft: #fbf1dc;
  --green: #1d6b45;
  --green-soft: #e2f2e9;
  --amber: #8a5a10;
  --radius: 14px;
  --tabh: 60px;
  color-scheme: light;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f1115;
    --bg-soft: #171a20;
    --card: #171a20;
    --line: #262a33;
    --ink: #e7e8ea;
    --ink-2: #a4a8b2;
    --ink-3: #767b87;
    --accent: #7ea2f0;
    --accent-soft: #1a2438;
    --gold: #e8c37a;
    --gold-soft: #2a2416;
    --green: #6fc99a;
    --green-soft: #12251c;
    --amber: #d7a95e;
    color-scheme: dark;
  }
}

/* The in-page toggle must beat the media query in both directions. */
:root[data-theme="light"] {
  --bg: #fbfbfa; --bg-soft: #f2f1ee; --card: #fff; --line: #e2e0da;
  --ink: #1b1c1e; --ink-2: #55575c; --ink-3: #86888e;
  --accent: #2f5fd0; --accent-soft: #e8eefc;
  --gold: #9a6b12; --gold-soft: #fbf1dc;
  --green: #1d6b45; --green-soft: #e2f2e9; --amber: #8a5a10;
  color-scheme: light;
}
:root[data-theme="dark"] {
  --bg: #0f1115; --bg-soft: #171a20; --card: #171a20; --line: #262a33;
  --ink: #e7e8ea; --ink-2: #a4a8b2; --ink-3: #767b87;
  --accent: #7ea2f0; --accent-soft: #1a2438;
  --gold: #e8c37a; --gold-soft: #2a2416;
  --green: #6fc99a; --green-soft: #12251c; --amber: #d7a95e;
  color-scheme: dark;
}

* { box-sizing: border-box; }

html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; scroll-padding-top: 64px; }

body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font: 17px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, "Helvetica Neue", sans-serif;
  overflow-wrap: break-word;
  padding-bottom: calc(var(--tabh) + env(safe-area-inset-bottom));
  -webkit-font-smoothing: antialiased;
}

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ------------------------------------------------------------- chrome --- */

.bar {
  position: sticky; top: 0; z-index: 20;
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px; padding-top: calc(10px + env(safe-area-inset-top));
  background: color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter: saturate(180%) blur(14px);
  border-bottom: 1px solid var(--line);
}
.bar-title {
  flex: 1; min-width: 0;
  font-size: 15px; font-weight: 600; color: var(--ink-2);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.bar .up { display: flex; color: var(--ink-2); }
.bar .up svg, .icon svg { width: 22px; height: 22px; }
.bar span.up { visibility: hidden; }
.icon {
  background: none; border: 0; padding: 0; color: var(--ink-2);
  display: flex; cursor: pointer;
}
svg { fill: none; stroke: currentColor; stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; }

.progress { position: sticky; top: 0; z-index: 21; height: 2px; }
.progress i { display: block; height: 2px; width: 0; background: var(--accent); transition: width .1s linear; }

.tabs {
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 30;
  display: grid; grid-template-columns: repeat(5, 1fr);
  background: color-mix(in srgb, var(--bg) 92%, transparent);
  backdrop-filter: saturate(180%) blur(14px);
  border-top: 1px solid var(--line);
  padding-bottom: env(safe-area-inset-bottom);
}
.tab {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 3px; height: var(--tabh); font-size: 11px; color: var(--ink-3);
  text-decoration: none;
}
.tab:hover { text-decoration: none; }
.tab svg { width: 21px; height: 21px; }
.tab.on { color: var(--accent); }

/* --------------------------------------------------------------- layout --- */

main { max-width: 760px; margin: 0 auto; padding: 4px 18px 40px; }
.doc { font-size: 17px; }
.kicker {
  margin: 18px 0 2px; font-size: 12px; font-weight: 700;
  letter-spacing: .09em; text-transform: uppercase; color: var(--ink-3);
}
h1 { font-size: 29px; line-height: 1.2; letter-spacing: -.02em; margin: 4px 0 8px; }
h2 { font-size: 22px; line-height: 1.25; letter-spacing: -.01em; margin: 2.1em 0 .5em; }
h3 { font-size: 18.5px; line-height: 1.3; margin: 1.7em 0 .4em; }
h4 { font-size: 16.5px; margin: 1.5em 0 .35em; color: var(--ink-2); }
h2 .hint { display: block; font-size: 13px; font-weight: 400; color: var(--ink-3); letter-spacing: 0; }
.sub { color: var(--ink-2); margin: 0 0 14px; }
p, ul, ol { margin: 0 0 1em; }
li { margin-bottom: .35em; }
hr { border: 0; border-top: 1px solid var(--line); margin: 2em 0; }

.anchor { margin-left: .4em; color: var(--ink-3); opacity: 0; font-weight: 400; }
h2:hover .anchor, h3:hover .anchor { opacity: 1; }

blockquote {
  margin: 1.2em 0; padding: 12px 16px;
  border-left: 3px solid var(--line);
  background: var(--bg-soft); border-radius: 0 10px 10px 0;
  color: var(--ink-2);
}
blockquote p:last-child { margin-bottom: 0; }

code {
  font: 500 .855em/1.5 ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace;
  background: var(--bg-soft); padding: .12em .38em; border-radius: 5px;
  border: 1px solid var(--line);
}
pre {
  background: var(--bg-soft); border: 1px solid var(--line);
  border-radius: var(--radius); padding: 14px; overflow-x: auto;
  font-size: 13.5px; line-height: 1.55;
}
pre code { background: none; border: 0; padding: 0; font-size: inherit; }

a.ts code { background: var(--accent-soft); border-color: transparent; color: var(--accent); }

/* Wide content scrolls in its own box - the page body never does. */
.scroll { overflow-x: auto; margin: 1.2em 0; border: 1px solid var(--line); border-radius: var(--radius); }
table { border-collapse: collapse; width: 100%; font-size: 14.5px; }
th, td { padding: 9px 12px; text-align: left; border-bottom: 1px solid var(--line); vertical-align: top; }
th { background: var(--bg-soft); font-weight: 650; white-space: nowrap; }
tr:last-child td { border-bottom: 0; }

figure { margin: 1.4em 0; }
img { max-width: 100%; height: auto; border-radius: 10px; display: block; border: 1px solid var(--line); }
figcaption { font-size: 13.5px; color: var(--ink-3); margin-top: 7px; line-height: 1.45; }

pre.mermaid { background: transparent; border: 0; padding: 0; text-align: center; }
pre.mermaid svg { max-width: 100%; height: auto; }

details { margin: 1em 0; }
summary {
  cursor: pointer; font-weight: 600; font-size: 15px; color: var(--ink-2);
  padding: 8px 0; list-style: none;
}
summary::-webkit-details-marker { display: none; }
summary::before { content: "▸ "; color: var(--ink-3); }
details[open] > summary::before { content: "▾ "; }

.toc {
  border: 1px solid var(--line); border-radius: var(--radius);
  padding: 2px 14px; background: var(--bg-soft);
}
.toc a { display: block; padding: 5px 0; font-size: 14.5px; color: var(--ink-2); border-top: 1px solid var(--line); }
.toc a.l3 { padding-left: 16px; font-size: 14px; color: var(--ink-3); }
.toc summary { border: 0; }

/* ---------------------------------------------------------------- pills --- */

.pill {
  display: inline-block; font-size: 11.5px; font-weight: 650;
  letter-spacing: .02em; padding: 3px 9px; border-radius: 999px;
  background: var(--bg-soft); color: var(--ink-2); border: 1px solid var(--line);
  white-space: nowrap;
}
.pill.established, .pill.corroborated { background: var(--green-soft); color: var(--green); border-color: transparent; }
.pill.emerging { background: var(--gold-soft); color: var(--gold); border-color: transparent; }
.pill.needs-check { background: var(--gold-soft); color: var(--amber); border-color: transparent; }
.pill.topic-tag { background: var(--accent-soft); color: var(--accent); border-color: transparent; }

/* ----------------------------------------------------------- home cards --- */

.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 18px 0 6px; }
.stat {
  background: var(--card); border: 1px solid var(--line); border-radius: var(--radius);
  padding: 11px 8px; text-align: center;
}
.stat b { display: block; font-size: 21px; letter-spacing: -.02em; }
.stat span { font-size: 10.5px; color: var(--ink-3); text-transform: uppercase; letter-spacing: .05em; }

.grid { display: grid; grid-template-columns: 1fr; gap: 10px; }
@media (min-width: 620px) { .grid { grid-template-columns: 1fr 1fr; } }

.card {
  display: block; background: var(--card); border: 1px solid var(--line);
  border-radius: var(--radius); padding: 14px 16px; color: inherit;
}
.card:hover { text-decoration: none; border-color: var(--accent); }
.card h3 { margin: 0; font-size: 17px; }
.card p { margin: 6px 0 8px; font-size: 14.5px; color: var(--ink-2); line-height: 1.5; }
.card-head { display: flex; align-items: center; gap: 10px; justify-content: space-between; }
.card .meta, .row .meta { font-size: 12.5px; color: var(--ink-3); }

.lesson {
  background: var(--card); border: 1px solid var(--line);
  border-radius: var(--radius); padding: 16px 18px; margin: 12px 0;
}
.lesson h3 { margin: 0; font-size: 18px; line-height: 1.3; }
.lesson h3 a { color: inherit; }
.byline { margin: 4px 0 10px; font-size: 13.5px; color: var(--ink-3); }
.tldr { font-size: 15.5px; color: var(--ink); }
.tldr p:last-child { margin-bottom: 0; }
.lesson .claims { border-top: 1px solid var(--line); margin: 12px 0 0; }
.lesson .claims ul { font-size: 15px; padding-left: 20px; }
.tags { display: flex; flex-wrap: wrap; gap: 6px; margin: 10px 0; }
.when { font-size: 13.5px; color: var(--ink-2); margin: 8px 0; }
.go { display: inline-block; font-size: 14.5px; font-weight: 600; margin-top: 2px; }

/* ------------------------------------------------------------ list rows --- */

.rows { display: flex; flex-direction: column; gap: 8px; }
.row {
  display: flex; gap: 12px; align-items: flex-start; justify-content: space-between;
  background: var(--card); border: 1px solid var(--line);
  border-radius: var(--radius); padding: 13px 15px; color: inherit;
}
.row:hover { text-decoration: none; border-color: var(--accent); }
.row h3 { margin: 0 0 3px; font-size: 16.5px; line-height: 1.3; }
.row p { margin: 0 0 3px; font-size: 14px; color: var(--ink-2); line-height: 1.45; }
.row-side { display: flex; flex-direction: column; align-items: flex-end; gap: 5px; flex-shrink: 0; }
.row-main { min-width: 0; }

/* --------------------------------------------------------------- claims --- */

.chips { display: flex; gap: 7px; overflow-x: auto; padding: 4px 0 12px; margin: 0 -18px; padding-left: 18px; padding-right: 18px; }
.chip {
  flex-shrink: 0; font: inherit; font-size: 13px; font-weight: 600;
  padding: 6px 13px; border-radius: 999px; cursor: pointer;
  background: var(--card); color: var(--ink-2); border: 1px solid var(--line);
}
.chip.on { background: var(--accent); color: #fff; border-color: transparent; }

.claim {
  background: var(--card); border: 1px solid var(--line);
  border-left: 3px solid var(--line);
  border-radius: var(--radius); padding: 13px 15px; margin: 9px 0;
}
.claim.corroborated { border-left-color: var(--green); }
.claim.emerging { border-left-color: var(--gold); }
.claim.needs-check { border-left-color: var(--amber); }
.claim-head { display: flex; align-items: center; gap: 7px; flex-wrap: wrap; margin-bottom: 7px; }
.claim-head .n { font-size: 12.5px; font-weight: 700; color: var(--ink-3); font-variant-numeric: tabular-nums; }
.claim-body { font-size: 15.5px; }
.claim-body p { margin: 0; }
.claim details { margin: 8px 0 0; }
.claim summary { font-size: 13px; padding: 4px 0; }
.claim details p { font-size: 13.5px; margin: 0; color: var(--ink-2); }

/* --------------------------------------------------------------- search --- */

#q {
  width: 100%; font: inherit; font-size: 17px; padding: 12px 14px;
  border: 1px solid var(--line); border-radius: var(--radius);
  background: var(--card); color: var(--ink); margin: 6px 0 10px;
}
#q:focus { outline: 2px solid var(--accent); outline-offset: -1px; border-color: transparent; }
.hit mark { background: var(--gold-soft); color: var(--gold); padding: 0 2px; border-radius: 3px; }

/* --------------------------------------------------------------- facts --- */

.facts {
  display: grid; grid-template-columns: auto 1fr; gap: 5px 14px;
  background: var(--bg-soft); border: 1px solid var(--line);
  border-radius: var(--radius); padding: 12px 15px; margin: 14px 0;
  font-size: 14px;
}
.facts > div { display: contents; }
.facts dt { color: var(--ink-3); white-space: nowrap; }
.facts dd { margin: 0; color: var(--ink-2); }

@media print { .bar, .tabs, .progress { display: none; } body { padding: 0; } }

.frontmatter {
  border: 1px dashed var(--line); border-radius: var(--radius);
  padding: 2px 14px; margin: 12px 0;
}
.frontmatter > summary { color: var(--ink-3); font-size: 13.5px; font-weight: 500; }
.frontmatter blockquote { background: none; border-left-color: var(--line); padding: 4px 12px; margin: .6em 0; }
.frontmatter p, .frontmatter li { font-size: 14px; color: var(--ink-2); }
``````

#### `tools/site_assets/app.js`

``````javascript
/* Brain reader - theme, reading progress, claim filter, offline search, mermaid.
   Everything degrades: with JS off the pages are still complete documents. */

(function () {
  var BASE = window.SITE_BASE || "./";

  /* ---- theme ---------------------------------------------------------- */
  var btn = document.getElementById("theme");
  if (btn) {
    btn.addEventListener("click", function () {
      var cur = document.documentElement.dataset.theme;
      if (!cur) {
        cur = matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      }
      var next = cur === "dark" ? "light" : "dark";
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem("brain-theme", next); } catch (e) {}
    });
  }

  /* ---- reading progress ----------------------------------------------- */
  var bar = document.querySelector(".progress i");
  if (bar) {
    var tick = function () {
      var h = document.documentElement.scrollHeight - innerHeight;
      bar.style.width = (h > 40 ? Math.min(100, (scrollY / h) * 100) : 0) + "%";
    };
    addEventListener("scroll", tick, { passive: true });
    addEventListener("resize", tick);
    tick();
  }

  /* ---- claim filter ---------------------------------------------------- */
  var filter = document.getElementById("claim-filter");
  if (filter) {
    filter.addEventListener("click", function (e) {
      var chip = e.target.closest(".chip");
      if (!chip) return;
      filter.querySelectorAll(".chip").forEach(function (c) { c.classList.remove("on"); });
      chip.classList.add("on");
      var want = chip.dataset.filter;
      document.querySelectorAll(".claim").forEach(function (c) {
        c.hidden = want !== "*" && c.dataset.topic !== want;
      });
    });
  }

  /* ---- search ---------------------------------------------------------- */
  var q = document.getElementById("q");
  if (q) {
    var results = document.getElementById("results");
    var status = document.getElementById("q-status");
    var index = null;

    var load = fetch(BASE + "search.json")
      .then(function (r) { return r.json(); })
      .then(function (d) { index = d; if (q.value) run(); })
      .catch(function () { if (status) status.textContent = "Search index unavailable offline yet - open once online."; });

    var esc = function (s) {
      return s.replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    };

    function snippet(text, term) {
      var i = text.toLowerCase().indexOf(term);
      if (i < 0) return esc(text.slice(0, 150));
      var s = Math.max(0, i - 60);
      return (s ? "..." : "") + esc(text.slice(s, i)) +
        "<mark>" + esc(text.substr(i, term.length)) + "</mark>" +
        esc(text.slice(i + term.length, i + term.length + 110)) + "...";
    }

    function run() {
      var term = q.value.trim().toLowerCase();
      if (!index) return;
      if (term.length < 2) {
        results.innerHTML = "";
        if (status) status.textContent = "Type to search the whole brain. Works offline.";
        return;
      }
      var hits = [];
      for (var i = 0; i < index.length; i++) {
        var e = index[i];
        var t = e.t.toLowerCase().indexOf(term);
        var x = e.x.toLowerCase().indexOf(term);
        if (t < 0 && x < 0) continue;
        hits.push({ e: e, score: (t >= 0 ? 1000 - t : 0) + (x >= 0 ? 100 : 0) });
      }
      hits.sort(function (a, b) { return b.score - a.score; });
      if (status) status.textContent = hits.length + (hits.length === 1 ? " result" : " results");
      results.innerHTML = hits.slice(0, 60).map(function (h) {
        return '<a class="row hit" href="' + BASE + h.e.u + '"><div class="row-main">' +
          "<h3>" + esc(h.e.t) + "</h3><p>" + snippet(h.e.x, term) + "</p></div>" +
          '<div class="row-side"><span class="pill">' + esc(h.e.k) + "</span></div></a>";
      }).join("");
    }

    var timer;
    q.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(run, 90);
    });
    var pre = new URLSearchParams(location.search).get("q");
    if (pre) { q.value = pre; }
    q.focus();
  }

  /* ---- mermaid (lazy: only pages that actually hold a diagram) ---------- */
  if (window.HAS_MERMAID && document.querySelector("pre.mermaid")) {
    var s = document.createElement("script");
    s.src = BASE + "assets/mermaid.min.js";
    s.onload = function () {
      var dark = document.documentElement.dataset.theme
        ? document.documentElement.dataset.theme === "dark"
        : matchMedia("(prefers-color-scheme: dark)").matches;
      window.mermaid.initialize({
        startOnLoad: true,
        securityLevel: "loose",
        theme: dark ? "dark" : "neutral",
        fontFamily: "inherit",
      });
    };
    s.onerror = function () {
      document.querySelectorAll("pre.mermaid").forEach(function (p) {
        p.classList.remove("mermaid");
      });
    };
    document.head.appendChild(s);
  }

  /* ---- offline ---------------------------------------------------------- */
  if ("serviceWorker" in navigator && location.protocol !== "file:") {
    addEventListener("load", function () {
      navigator.serviceWorker.register(BASE + "sw.js", { scope: BASE }).catch(function () {});
    });
  }
})();
``````

#### `tools/site_assets/sw.js`

``````javascript
/* Brain reader - offline cache.
   Text (html/css/js/search index) is precached on install, so the whole brain is
   readable with no network. Images and the 3.4MB mermaid bundle are NOT precached
   - they are cached lazily on first view, which keeps the install cheap on cellular. */

var REV = "__REV__";
var SHELL = "brain-shell-" + REV;
var MEDIA = "brain-media-v1";
var PRECACHE = __PRECACHE__;

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(SHELL).then(function (c) {
      // addAll is all-or-nothing; a single 404 must not sink the whole install.
      return Promise.all(PRECACHE.map(function (u) {
        return c.add(new Request(u, { cache: "reload" })).catch(function () {});
      }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== SHELL && k !== MEDIA) return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;

  var isMedia = /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(req.url) || /mermaid\.min\.js$/.test(req.url);

  if (isMedia) {
    // Cache-first: bytes that never change under the same name.
    e.respondWith(
      caches.match(req).then(function (hit) {
        return hit || fetch(req).then(function (res) {
          var copy = res.clone();
          caches.open(MEDIA).then(function (c) { c.put(req, copy); });
          return res;
        });
      })
    );
    return;
  }

  // Network-first for documents: a rebuilt brain should win when there is signal.
  e.respondWith(
    fetch(req).then(function (res) {
      var copy = res.clone();
      caches.open(SHELL).then(function (c) { c.put(req, copy); });
      return res;
    }).catch(function () {
      return caches.match(req).then(function (hit) {
        return hit || caches.match(new URL("index.html", req.url).pathname);
      });
    })
  );
});
``````

#### `.github/workflows/pages.yml`

``````yaml
name: pages

# Publishes the mobile reader to GitHub Pages on every push to main.
# The site is a pure render of brain/ + sources/ - nothing here is a source of
# truth, so a failed build never costs anything but the deploy.

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

# Let a running deploy finish; queue at most one behind it.
concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install
        run: pip install markdown pillow

      - name: Validate the contract
        run: python3 validate.py

      - name: Build the site
        run: python3 tools/build_site.py

      # One-time repo setup this cannot do for itself:
      #   Settings -> Pages -> Build and deployment -> Source: GitHub Actions
      # Until that is set, this step fails and nothing deploys.
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deploy.outputs.page_url }}
    steps:
      - id: deploy
        uses: actions/deploy-pages@v4
``````

#### `.claude/commands/research.md`

``````markdown
---
description: Deep research on a source's gated claims - external evidence into sources/<id>/context/
argument-hint: <source-id or topic> [| specific question]
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, WebSearch, WebFetch
---

# /research - deep research (external evidence)

**The contract is `AGENTS.md` § "Deep research on request".** Read it now and follow it - this file
is only the Claude Code wrapper for that stage. Do not duplicate the contract here; if the two ever
disagree, `AGENTS.md` wins.

Adopt **fact-checker + synthesizer** (+ **mentor** if the goal is teaching the concept).

## Target

`$ARGUMENTS`

If that names a source folder, research **that source's gated nodes**. If it names a topic or a bare
question, research that - but still land the output in a `context/` note under the most relevant
source, or in `reports/` if it spans several.

## Run it

1. **Orient.** Read the source's `SOURCE.md` and `nodes.md`. Pick the research targets by ID:
   `single-leg` nodes, anything `needs-check`, recorded divergences, and the `LEARNING.md` open
   questions. **Target claims, not the subject** - open-ended topic research makes you a summarizer.
2. **Read the brain before the web.** `grep` the root `INDEX.md`, `brain/topics/*.md` and
   `brain/claims.md`. A prior source may already answer this; that link beats a fresh fetch.
3. **Search and fetch,** favouring T1-T3 (see the tier table in `AGENTS.md`). Deliberately attempt
   the **cross-domain hop** - the established name for this idea in an older discipline. Respect the
   budget: **≤ 8 searches, ≤ 12 fetches**; stop early on two independent agreeing sources, or when a
   pass surfaces nothing new.
4. **Apply the independence rule.** A companion repo, a vendor blog restating that vendor's own
   talk, or same-lab work is *the same leg wearing a different hat*: record it, cite it, but **do not
   raise confidence**.
5. **Write** `sources/<id>/context/<NN>_<slug>.md` using the structure in
   `sources/_TEMPLATE/context/README.md`. Every finding gets a verdict
   (`supports` / `contradicts` / `refines` / `no-evidence`), a tier, and an independence call. End
   with a **Confidence assessment** - never interrupt with clarifying questions; state assumptions
   there instead.
6. **Feed it back in the same pass:** update node confidences in `nodes.md` (pointing at the context
   note), cite external support in `brain/claims.md`, add terms to `brain/glossary.md`, set
   `SOURCE.md` Status, and append to `brain/log.md`. Keep external findings **out of `LEARNING.md`'s
   body** - it may cite the note, never absorb it.
7. **Report back:** one paragraph on what changed - which claims got stronger, which got weaker,
   which found nothing - then `git diff`.

## Calibration

The reader knows LLM and agent fundamentals. **No 101 explainers.** Aim one level above the source:
the frame that makes its claim feel inevitable rather than arbitrary.

## Honesty rules (non-negotiable)

- `no-evidence` is a **result**, not a failure - "this rests on one practitioner's experience" is
  exactly the kind of thing this brain exists to record. Never pad with weak T4/T5 hits.
- `contradicts` is a **finding**. Keep both sides, cite both, flag the conflict.
- If web access is unavailable, say so and stop. **Never fabricate a citation or work from memory.**
``````

#### `brain/index.md`

``````markdown
# Moved -> [`/INDEX.md`](../INDEX.md)

The brain-wide catalog (sources roster + topics roster + pointers) now lives at the **repo root**
as [`INDEX.md`](../INDEX.md), so you can ask questions from the root and the agent finds the right
notes. This stub only exists to redirect old links.

**The content beside this file is unchanged:** [`topics/`](topics/), [`claims.md`](claims.md),
[`glossary.md`](glossary.md), [`log.md`](log.md), [`decisions/`](decisions/). `brain/` still holds
the knowledge; only the whole-brain *index* relocated to the root.
``````

#### `LICENSE`

``````text
MIT License

Copyright (c) 2026 chamin (0xchamin)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
``````

---

## 6. The empty brain (starting state)

These are **not** copies of the reference brain's knowledge - they are the blank forms. Six seed
topics, no sources, no claims. Your first ingest fills them.

> **Seeds, not a whitelist.** When a source teaches a recognizable, reusable area the brain does not
> cover, create a new topic note (the **architect** persona owns that call). Stay inside AI / ML /
> agentic engineering; flag anything clearly off-domain rather than silently ingesting it.

#### `INDEX.md`

``````markdown
# Brain - INDEX (ask here)

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
| Agents | seed | Autonomous LLM agents: the loop, prompt authorship, control flow, structured output and tool calls, state and pause/resume, and how much of the agent you own versus delegate to a framework. | 0 | [`brain/topics/agents.md`](brain/topics/agents.md) |
| MCP (Model Context Protocol) | seed | The Model Context Protocol: servers, tools, resources, prompts, transport (stdio / HTTP), the client-server handshake, and how agents consume MCP capabilities. | 0 | [`brain/topics/mcp.md`](brain/topics/mcp.md) |
| Skills | seed | Agent skills: what a skill is, how it is defined and packaged, how it is invoked or auto-triggered, how to evaluate one, and how skills relate to tools and MCP. | 0 | [`brain/topics/skills.md`](brain/topics/skills.md) |
| RAG | seed | Retrieval-augmented generation: chunking, embeddings, indexing, retrieval and reranking, and how retrieval quality is measured. | 0 | [`brain/topics/rag.md`](brain/topics/rag.md) |
| Agent security | seed | Threats and mitigations: prompt injection, tool poisoning, exfiltration, sandboxing, and the delegated-authorization substrate (scopes, consent, token handling). | 0 | [`brain/topics/agent-security.md`](brain/topics/agent-security.md) |
| Inferencing | seed | LLM serving: KV cache, batching, quantization, speculative decoding, and the latency/throughput/cost trade-offs. | 0 | [`brain/topics/inferencing.md`](brain/topics/inferencing.md) |

## Deeper layers (brain-wide content INDEX points into)

- [`brain/claims.md`](brain/claims.md) - cross-source **corroborated claims** with citations.
- [`brain/glossary.md`](brain/glossary.md) - 💡 **terms** defined once, reused across sources.
- [`brain/log.md`](brain/log.md) - dated **ingest milestones**.
- [`brain/decisions/`](brain/decisions/) - **ADRs** for durable structural decisions.
- [`reports/`](reports/README.md) - **synthesized cross-source study material**.

## Config (taste + workflow)

- [`AGENTS.md`](AGENTS.md) - behavioral contract + the paste-a-URL ingest rule. Read every session.
- [`personas/README.md`](personas/README.md) - role overlays; auto-loaded per the routing table.
``````

#### `brain/topics/agents.md`

``````markdown
# Topic: Agents

**Status:** seed (no source yet -> emerging at 1 source -> established at 2+ corroborating sources)

> Living, cross-source synthesis on agents. Many sources feed this note; **merge and
> de-duplicate** as they arrive (architect persona). Every claim cited.

## What this covers

Autonomous LLM agents: the loop, prompt authorship, control flow, structured output and tool calls, state and pause/resume, and how much of the agent you own versus delegate to a framework.

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
``````

#### `brain/topics/mcp.md`

``````markdown
# Topic: MCP (Model Context Protocol)

**Status:** seed (no source yet -> emerging at 1 source -> established at 2+ corroborating sources)

> Living, cross-source synthesis on mcp (model context protocol). Many sources feed this note; **merge and
> de-duplicate** as they arrive (architect persona). Every claim cited.

## What this covers

The Model Context Protocol: servers, tools, resources, prompts, transport (stdio / HTTP), the client-server handshake, and how agents consume MCP capabilities.

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
``````

#### `brain/topics/skills.md`

``````markdown
# Topic: Skills

**Status:** seed (no source yet -> emerging at 1 source -> established at 2+ corroborating sources)

> Living, cross-source synthesis on skills. Many sources feed this note; **merge and
> de-duplicate** as they arrive (architect persona). Every claim cited.

## What this covers

Agent skills: what a skill is, how it is defined and packaged, how it is invoked or auto-triggered, how to evaluate one, and how skills relate to tools and MCP.

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
``````

#### `brain/topics/rag.md`

``````markdown
# Topic: RAG

**Status:** seed (no source yet -> emerging at 1 source -> established at 2+ corroborating sources)

> Living, cross-source synthesis on rag. Many sources feed this note; **merge and
> de-duplicate** as they arrive (architect persona). Every claim cited.

## What this covers

Retrieval-augmented generation: chunking, embeddings, indexing, retrieval and reranking, and how retrieval quality is measured.

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
``````

#### `brain/topics/agent-security.md`

``````markdown
# Topic: Agent security

**Status:** seed (no source yet -> emerging at 1 source -> established at 2+ corroborating sources)

> Living, cross-source synthesis on agent security. Many sources feed this note; **merge and
> de-duplicate** as they arrive (architect persona). Every claim cited.

## What this covers

Threats and mitigations: prompt injection, tool poisoning, exfiltration, sandboxing, and the delegated-authorization substrate (scopes, consent, token handling).

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
``````

#### `brain/topics/inferencing.md`

``````markdown
# Topic: Inferencing

**Status:** seed (no source yet -> emerging at 1 source -> established at 2+ corroborating sources)

> Living, cross-source synthesis on inferencing. Many sources feed this note; **merge and
> de-duplicate** as they arrive (architect persona). Every claim cited.

## What this covers

LLM serving: KV cache, batching, quantization, speculative decoding, and the latency/throughput/cost trade-offs.

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
``````

#### `brain/claims.md`

``````markdown
# Brain - corroborated claims (cross-source)

> Durable, corroborated claims promoted from source `nodes.md` files. Each must be reusable
> across future queries and carry a citation. A claim confirmed by multiple sources is stronger -
> note them all. This is a signal store; task-specific scratch stays in the source folder.

| # | Claim | Topic | Sources (cited) | Confidence |
|---|---|---|---|---|

> When a new source corroborates an existing claim, add its citation to that row rather than
> creating a duplicate. When sources conflict, keep both and flag the conflict.
``````

#### `brain/glossary.md`

``````markdown
# Brain - glossary (reusable terms)

> 💡 terms defined once and reused across sources, promoted from source `LEARNING.md` files.
> Keep each to 1-2 sentences. Cite the source where the term was learned.

| Term | 💡 Explanation | First source |
|---|---|---|
``````

#### `brain/log.md`

``````markdown
# Brain - chronological log

> Append-only. One dated entry per source ingested or milestone worth remembering.

| Date | Source | Entry |
|---|---|---|
| 2026-08-02 | brain (kit) | Kit built from `BUILD.md` (a generated bundle of the reference clone). Empty brain: 6 seed topics, no sources, no claims. |
``````

#### `reports/README.md`

``````markdown
# Reports - synthesized cross-source study material

> Written by the **synthesizer** persona when you ask a question the brain can answer from more
> than one source. One file per report, named `YYMMDD_slug.md`. Every claim cited; every diagram
> carries a walkthrough (see `AGENTS.md`).

_(none yet)_
``````

---

## 7. Install, link, verify

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
chmod +x link-agents.sh && ./link-agents.sh      # Windows: .\link-agents.ps1
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
| `README.md`, `prd.md`, `how_to_use_this.md` | Their **procedural** role is this file, so a build from this bundle alone needs none of them. The durable design rationale lives in the ADRs (section 5.5), which **are** included. They are not dead weight, though: the reference repo ships all three, `README.md` is what a newcomer reads first, and `prd.md` carries the risk register and the changelog. Copy them across if you want the full documentation set. |
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
