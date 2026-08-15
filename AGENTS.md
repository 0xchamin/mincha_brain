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
| Env | `.venv` in this folder | `yt-dlp`, `yt-dlp-ejs`, `faster-whisper`, `imagehash`, `pillow` (see `requirements.txt`); `ffmpeg` is a system binary (macOS: `brew install ffmpeg`; Windows: `winget install Gyan.FFmpeg`); **`deno` is a system binary and is required for YouTube video capture** (`brew install deno`) - see the degrade table; `git` for cloning code repos; **`gh` (GitHub CLI) recommended** for code sources (license, commit SHA, orient-before-clone) - optional |
| Seed topics | agents, mcp, skills, rag, agent-security, inferencing | live under `brain/topics/`; **seeds, not a whitelist - the set is open (see "Scope: topics are open")** |
| Repo clones | `sources/<id>/repo/` (git-ignored) | clone-per-source, snapshot pinned by commit SHA in `SOURCE.md` |
| Kit scripts | `tools/ingest.py` (mechanical toolbox), `validate.py` (contract type checker), `tools/build_site.py` (the mobile reader) | the only three frozen scripts; everything else is assembled per source |

## Reserved terms - each means exactly one thing

> **Why this exists.** On 2026-08-15 this file used **`movement`** for two different objects in the
> same document - the roadmap's groups of walkthrough sections, and the units of a presentation - and
> nobody noticed until a reader said the presentation read wrong. That is the failure mode of a long
> specification: **not a contradiction, which git and a reader can both catch, but a word quietly
> doing two jobs.** This is claim 207 applied to the contract itself - a controlled vocabulary,
> read first, extended reluctantly.

| Term | Means exactly | Not |
|---|---|---|
| **node** | one gated claim in a source's `nodes.md`, `n7` | a claim in `brain/claims.md` |
| **claim** | one numbered row in `brain/claims.md`, promoted and cited | a node, or an ungated assertion |
| **conjecture** | one row in `brain/conjectures.md`, `h3` - **explicitly unproven** | a claim; never cite one as evidence |
| **frame** | an image extracted from a source, living in `visuals/` | a diagram |
| **diagram** | a mermaid picture **this brain generated** | a frame |
| **visual** | the umbrella: a frame **or** a diagram | - |
| **movement** | a group of numbered walkthrough sections, drawn in the roadmap | a presentation unit - that is a **slide** |
| **slide** | one unit of a `## Presentation narrative` | a movement |
| **stage** | `/verify`, `/research`, `/conjecture`, `/dream` - a user-triggered pass with its own spec in [`stages/`](stages/) | an ingest step |
| **pass** | one execution of a stage, logged and dated | the stage itself |
| **source** | an artifact someone else made, `sources/<id>/`, labelled `S<n>` | a foundation, a report or an experiment |
| **corroborated** | two legs of **this source** agree | true, verified, or externally confirmed |

**Adding a term here is cheap and renaming one is not.** If you need a word that is already in this
table, use a different word.

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
| The **TL;DR diagram**, inside that section, under the prose | **Hard wherever the argument has a shape** - the whole note in one glance, for a reader deciding whether to spend twenty minutes. Same conditional as the mental model, and it is **not** the same diagram. See below |
| `## The 1-minute version` | **Hard** - the whole article compressed to a scannable table. See below |
| `## Key claims` | **Hard** - also lifted onto the landing page |
| `## What you will learn, and in what order` | **Hard** - a mermaid roadmap of the walkthrough, grouped into movements. See below |
| A **movement diagram** at the head of each movement, inside the walkthrough | **Hard for sources from 2026-08-15.** One per movement (so typically 3-4), showing how that movement's sections relate. See "Diagrams for a visual reader" below |
| The walkthrough - **numbered sections, titled by what you learn** | **Hard** - the body; its shape follows the source |
| A **gap-fill diagram** in any numbered section carrying no visual at all | **Hard for sources from 2026-08-15.** Every section gets something to look at. A curated frame satisfies it, and so does the movement diagram for the **first** section of a movement, since it sits directly above |
| `## Diagram (mental model)` | **Hard** wherever the subject has structure |
| `## 💡 Terms` | **Hard** |
| `## What has aged (read before applying)` | **When the source is dated.** See below |
| `## What to distrust in this note` | **Hard** - source-level trust, not claim-level caveats |
| `## Open questions` | **Hard** - the deep-research backlog |
| `## Feeds these topics` | **Hard** |
| `## Presentation narrative` | **Hard for sources ingested from 2026-08-15 onward**, and the last section in the file. Adopt **presenter**. See below |

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

### The register (how the sentences read)

> **Why this exists.** The six properties above govern the **architecture** of a note and say nothing
> about its **prose**, so every note drifted to the same voice: dense, assertion-first, uniformly
> long sentences that a reader has to assemble into an argument themselves. Measured on S13's
> walkthrough on 2026-08-03 - `For example`, `In other words`, `However` and `Notice that` appeared
> **zero times** across 9,000 words; median sentence 21 words with a 94-word longest. Everything
> mandatory was present and it still read as a rich set of facts rather than an expert explaining.
> **The target voice is an AI architect who is also a subject-matter expert, teaching.**

**Four rules. They are cheap to check and they are not optional.**

1. **Signpost, and raise the objection before answering it.** Use the connective vocabulary that
   carries a reader through an argument they do not yet hold: *at first glance*, *to see why,
   consider*, *suppose instead*, *the reason is*, *for example*, *in other words*, *first / second /
   finally*, *in short*. **The strongest single move is to state the obvious objection to your own
   claim and then answer it** - "this looks like the least principled of the three options, so why
   choose it?" A reader who has felt the objection understands the answer; a reader handed only the
   answer has memorised it.
2. **Complete sentences, always.** A sentence ends fully, then the next one starts. **No colon-led
   lists mid-sentence** ("...run its own programme overnight: edit a script, run it, keep the
   change"), **no semicolon chains**, no fragments standing in for clauses. Where you were about to
   write a colon and three items, write three sentences - and you will usually find each sentence
   now has room to say what the item is *for*, which the list never did.
3. **Paragraphs must hand off, exactly as sections do.** Each paragraph **ends on the question the
   next one answers**, and opens by picking that question up. **Bold lead-in labels
   (`**What it costs.**`) do not count and are worse than nothing** - they segment the text into
   blocks and let the writer skip the connective work entirely.
4. **Walk the alternatives in prose, then tabulate as a recap.** A table alone makes the reader
   reconstruct the reasoning. Walk each option and say what goes wrong with it, then keep a compressed
   table underneath for the reader who is returning rather than arriving.

**The budget.** Applying this costs roughly **+25 to +30% words** on a rewritten section. That is the
right trade for a note whose job is teaching, and it is why the compressed forms exist beside it.

> **Sentence length is a symptom worth watching, not a target to hit.** Aim for a median near 16-18
> words with genuine variation - a short sentence landing a point after a complex one is the rhythm
> that dense technical prose loses first. If your median is above 21, you are almost certainly
> stacking subordinate clauses where a handoff belonged.

> **Reference implementation:** [`sources/260803_autoresearch/LEARNING.md`](sources/260803_autoresearch/LEARNING.md)
> - the source that forced this section. Its `1-minute version` and roadmap walkthrough are the two
> shapes to copy.

### The TL;DR diagram

> **Why this exists.** The notes run 5,000 to 9,000 words. A reader deciding whether to spend twenty
> minutes gets four sentences of prose, and prose is the slowest possible way to convey a *shape*. The
> three compressed forms this file already defines all answer questions in words - what is this, what
> does it say, what may I cite - and **none of them shows the reader the structure of the argument
> before they commit to reading it.** One diagram does that in about three seconds.

**Place it inside `## TL;DR`, immediately after the prose.** `build_site.py` lifts that whole section
onto the landing page, so the diagram travels with the summary and a reader sees the shape without
opening the note at all. That lift is also the constraint that governs everything below.

**The hard part is not drawing it, it is not drawing one of the other two.** A note in this shape
carries up to three diagrams and they are trivially easy to collapse into three views of one picture,
which wastes two of them. Keep the division of labour explicit:

| Diagram | Answers | Must not |
|---|---|---|
| **TL;DR diagram** | *what is the shape of the argument?* | be the flow, or the reading order |
| **Roadmap** (`What you will learn`) | *what order will I meet it in, and what may I skim?* | be the subject - it is about the note |
| **Mental model** (`Diagram`) | *how does the subject actually work?* | be a compressed table of contents |

The reliable way to make the first one distinct is to **draw the note's thesis rather than its
subject**. If the walkthrough keeps saying that two things get mistaken for each other, draw the
pairs. If it keeps saying a decision has to be made before some point, draw the point. *(Worked
example: [`sources/260814_hermes-agent-architecture-p1`](sources/260814_hermes-agent-architecture-p1/LEARNING.md)
hangs six "X is not Y" nodes off the source's own six-stage spine - the mental model already owned the
flow, so the TL;DR diagram took the collapses instead, and each one is pinned to the stage where it
bites.)*

**Keep it phone-sized, and prefer `flowchart TB`.** It renders on a landing card among two dozen
others and on a 390px screen. A diagram needing a laptop to read has failed at the one job it has.

**It must survive being the only thing read, which is the bar that was raised on 2026-08-15.** A
diagram set in `The 1-minute version` was considered and rejected, because that section's job is *the
argument in sixty seconds of scanning* and a set of diagrams makes it slower to scan than the prose it
compresses - and because its thesis-shape is already drawn here. **So this diagram absorbed that
requirement instead.** The test: a reader who looks at this and reads nothing else should be able to
state the note's argument, not merely its topic. If they would come away with the subject rather than
the claim, it is drawing the wrong thing.

**It still carries a walkthrough** - the hard rule in Global rules has no exemption, and orientation,
crux, why-this-shape and provenance all still apply. Write it as **one compact paragraph in flowing
prose**, not four labelled blocks, and remember the register rules forbid the bold lead-in labels
anyway. Four or five sentences is right; if it needs more, the diagram is too complicated for the slot.

**Skip it when the argument has no shape** - the same conditional the mental model carries. A source
whose contribution is a list of independent findings has nothing to draw here, and a diagram invented
to satisfy a table row is decoration, which the diagram rule already forbids. **Say nothing when you
skip it**; unlike the visual leg, there is no evidential cost to record.

> **Two costs, both real, both accepted.** It makes that source's landing-page card **taller** than
> its neighbours, which is a genuine asymmetry when only some notes have one. And it depends on
> `render_home` running the lifted section through `mermaidify` - **which it did not do until
> 2026-08-14**, publishing the diagram source as a visible code block on the homepage instead. That is
> fixed. It is recorded here because it is the failure mode a future agent would otherwise rediscover
> by shipping it.

> **Deliberately not enforced by `validate.py`.** Whether an argument *has* a shape, and whether a
> diagram duplicates its neighbours, are both judgement. The validator checks that mermaid fences
> balance and that diagrams exist where this file says they must; it cannot check that three diagrams
> are three different diagrams, and encoding that would launder judgement as a green check.

### The 1-minute version

**Narrative first, then the table.** The two are not alternatives and they answer different needs: the
narrative is read once by someone arriving, the table is scanned repeatedly by someone returning or
checking one row. Introduce the table with a line that says so, rather than letting it look like a
restatement.

The narrative runs **six to eight flowing paragraphs** following the reader's own questions, not the
source's running order: *what this article covers* -> *the problem it works on* -> *why that problem
is hard* -> *the naive approach and the ways it collapses* -> *the idea* -> *how it works* -> *what it
costs* -> *how far to trust it*. Every paragraph obeys the register rules above, and it carries the
same node IDs the table does.

> **Note what the narrative can hold that the table cannot.** The six standard rows have **no slot for
> why the problem is hard**, so every note built on the table alone silently skipped the beat that
> makes the design feel necessary rather than arbitrary. That gap is the reason this section changed.

The table stays directly beneath it, giving **the whole argument in about sixty seconds of scanning**.
It is not a third summary competing with its neighbours - the three do different jobs, and keeping
them distinct is the point:

| | Answers | Shape |
|---|---|---|
| `TL;DR` | *what is this and should I read it?* | 4-6 sentences of prose, lifted to the landing page |
| **`The 1-minute version`** | *what does it actually say?* | **flowing narrative, then the same arc compressed to a table** |
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

**Its walkthrough is narrative, not four labelled blocks.** The diagram rule's four elements
(orientation, crux, why-this-shape, provenance) are requirements about *content*, never a template of
headings - and writing them as `**How to read it:**` / `**The crux:**` / `**Why it is shaped this
way:**` is the block-labelling the register rules forbid. Walk the reader through the movements in
connected prose, saying for each what it does, who may skim it and what it costs them to skim.

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

### Diagrams for a visual reader (new sources only)

> **Why this exists.** The walkthrough is contractually visual-led, and on a slide-heavy source that
> works - S26 had a curated frame in 8 of its 10 sections. **But a frame and a diagram do different
> cognitive work.** A frame is *evidence*: here is the artifact. A diagram is a *model*: here is how
> the parts relate. A reader who learns visually needs both, and the kit was only guaranteeing the
> first - and guaranteeing it **not at all** on a source whose visual leg was skipped, where the
> walkthrough is entirely unillustrated.

**Two additions, both targeted rather than per-section.**

**A movement diagram at the head of each movement**, in the walkthrough, before that movement's first
numbered section. **Not stacked in the roadmap section** - four abstractions before the reader has any
content is worse than none, and the roadmap's job is the whole note's shape. At the head of a movement
it is an advance organiser: it shows how *these three sections* relate, which is the connective tissue
a per-section diagram structurally cannot show, because a diagram per section draws each step in
isolation and the joins are the hard part to hold.

**A gap-fill diagram wherever a numbered section has no visual at all.** A section already carrying a
curated frame needs nothing. **This is the rule that matters most on a transcript-only source**, where
the visual leg was skipped and *every* section qualifies - and it is the case the frame-led walkthrough
never covered.

> **Per-movement was chosen over per-section deliberately.** Per-section was the original request. On
> S26 it would have added ten diagrams of which eight duplicated a frame already teaching that step,
> for roughly +1,500 words, and it draws steps in isolation. Per-movement plus gap-fill gets full
> visual coverage in four to six diagrams and draws the relationships instead.

**The anti-collapse problem gets worse with more diagrams, so the division of labour is now explicit
and each row must answer a different question:**

| Diagram | Answers | Scope | Must not |
|---|---|---|---|
| **TL;DR** | what is the shape of the argument? | the whole note's **thesis** | be the flow, or the reading order |
| **Roadmap** | what order will I meet it in, what may I skim? | the whole note's **structure** | be the subject |
| **Movement** | how do the sections in this movement relate? | **one movement's** mechanism | restate the roadmap at smaller scale |
| **Gap-fill** | whatever that section teaches | **one section** | exist where a frame already teaches the step |
| **Mental model** | how does the subject actually work? | the whole **subject** | be a compressed table of contents |

**Every one of them carries a walkthrough** under the hard rule, and every walkthrough is written with
**presenter** - present the diagram, never narrate its arrows. Budget accordingly: a diagram plus its
walkthrough is roughly 150 words.

### The `Presentation narrative` (new sources only)

> **Why this exists.** Every compressed form above answers a **reader's** question - what is this,
> what does it say, what may I cite. None of them is a **speaking** artifact, and the notes run
> 5,000-9,000 words tuned for a solo reader ramping up. **This is also the first artifact in the kit
> written for people who will never open the repo**, which is the point: every other layer optimises
> for the brain's correctness, and this one optimises for transfer.

**Adopt [presenter](personas/presenter.md), which owns the full spec.** Placed **last, after
`Feeds these topics`** - so it cannot disturb the ramp, and `build_site.py` (which lifts only `TL;DR`
and `Key claims`) never pulls it onto the landing page. An audience-facing **framing note**, then
five to seven **slides** (`### Slide N - <the claim>`) with a visual each, closing on
`### Key takeaway message`. **Budget 900-1,500 words** - widened from 700-1,200 when the bullets went, on the same +25-30% precedent the Register rules already carry.

**It is a talk track, not slide notes, and the tone rules are in the persona.** The short version:
**no bullets anywhere**, slide titles that are claims rather than labels, one bolded declarative
sentence opening each slide, the audience named out loud where the register shifts
(*"the leadership significance is..."*), and questions posed then answered. **Say "slide", never
"movement"** - `movement` already names the roadmap's groups of walkthrough sections.

**Three rules are load-bearing and are restated here because they are the ones that will erode:**

1. **Nobody gets a second walkthrough.** The presentation **selects** load-bearing reasoning; it does
   not re-summarise. A movement restating a walkthrough section is deleted. This note already carries
   three compressed forms and a fourth that merely summarises is waste.
2. **It inverts the punchline-opening ban, deliberately.** The presentation leads with the takeaway
   and then earns it, which the walkthrough is forbidden from doing. **Both are right** - a ramp orders
   for someone who does not yet know, a presentation orders for someone who may leave after five
   minutes. **This is why the section is appended rather than folded in**, and a future agent must not
   read the two rules as a contradiction to resolve.
3. **The null close is first-class.** The most common honest conclusion here is that nobody measured
   the thing, and a persona told to end on what should be funded or changed **will manufacture
   actionability the evidence does not support** in front of the audience most likely to act on it.
   *"The decision is to not act yet, and here is precisely what would change that"* is the stronger
   close, because it converts "we do not know" into a scoped experiment.

**Reuse the curated frames.** A movement's visual should normally be one the walkthrough already
cites; synthesize a new diagram only where a movement's consequence has no existing visual. **A note
already struggles to keep three diagrams distinct** and five more would be decoration. This also keeps
the frame-prune rule satisfiable, and a frame earning its place twice was well chosen.

**No register carve-out, and an earlier one was withdrawn.** The first version of this section
exempted slide bullets from the Register rules. **The tone rules removed the bullets, so the
exemption had nothing left to cover** - and the register's demands, complete sentences and paragraphs
that hand off, are exactly what a spoken track needs. A slide's bolded opening is a **claim**, not the
lead-in label the register forbids.

> **Scoped to new ingests, and the reason is recorded in
> [ADR-0026](brain/decisions/0026-presenter-persona.md).** Twenty-six notes predate this section and
> making it retroactively mandatory would create twenty-six units of retrofit debt on the day it
> landed - which is what happened with the register retrofit, still unpaid on S2. **`validate.py`
> reports coverage instead of failing**, in the same informational block as `/verify` coverage and for
> the same reason: whether an old note earns a presentation is judgement, and a threshold in the
> validator would launder judgement as a green check. Retrofit on demand, highest-value sources first.

> **No reference implementation yet, and that is a known risk.** This file records that the
> `LEARNING.md` shape was twice specified wrongly before a worked example existed. **The next ingest is
> the test**; if the shape is wrong, fix the contract rather than the note.

## `foundations/` - supplied background, uncited by construction

> **Why this exists.** Every `Background, supplied` block in every `LEARNING.md` is currently the
> writing agent explaining a fundamental **from its own knowledge**. That is honest - the blocks say
> so - but it is inconsistent between notes, unreviewable, and it evaporates when the session ends.
> `foundations/` is the repo-level home for that material: written once, kept, and reused.

**It is a third category, deliberately not a fourth kind of source.**

| Layer | What it holds | Evidence status |
|---|---|---|
| `sources/<id>/` | external artifacts someone else made | **gated** - two legs, cited, promoted to `brain/` |
| `foundations/` | **background the reader needs and no source taught** | **uncited by construction** - never promoted |
| `reports/` | synthesis written *out* of the brain | cited to the nodes it draws on |

### The hard rules

- **A foundation never reaches `brain/claims.md`.** It is not a claim, it produces no nodes, and it
  is not counted as a source anywhere. If a foundation turns out to be load-bearing for something the
  brain wants to assert, **ingest the primary it points at** and let the claim come from there.
- **Every file declares its status in its own header** - that it is supplied background, uncited by
  construction, and not evidence about anything. `validate.py` checks this.
- **A `LEARNING.md` may cite a foundation, as background and never as evidence** - exactly as a
  `Background, supplied` block is cited today. Prose leaning on one says so in the sentence.
- **Preserve whatever citations the material already carries.** A foundation that points at an
  Anthropic post or an arXiv paper is strictly more useful than one that does not, and the pointer is
  what makes a later proper ingest cheap. **Those citations do not upgrade its status** - it is still
  background until the primary is gated.

> **The tier rule still applies and is the thing to stay honest about.** An agent-generated research
> note is roughly **T5** by this kit's own scale, and the T5 rule is *"use for discovery; cite the
> primary source they point to, not them."* Filing one under `foundations/` does not launder it -
> it puts it where its status is declared rather than assumed.

### Bringing material in

1. Drop the markdown into git-ignored **`staging/`**. There is no `_inputs/` - `staging/` already
   exists for exactly this, and the rule is the same: **material becomes part of the kit when it is
   filed, not when it is copied in.**
2. Read it and make the call: **is it teaching a fundamental, or is it making claims about the
   world?** Fundamentals become foundations. Claims about the world mean the *primary it cites* is
   the thing to ingest - add it to the reading list, not to `foundations/`.
3. File to `foundations/<slug>.md` with the status header, keeping its citations.
4. Promote genuinely reusable terms to [`brain/glossary.md`](brain/glossary.md), which is the
   one-or-two-sentence version of the same material.

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

**It also prints a `Coverage` block, which is counts and not checks.** Two numbers that nothing else
in the kit surfaces: **`/verify` coverage** (how many sources carry a `verify.md`) and **dream
staleness** (the last pass, and how many sources have been ingested since). Both are **informational
and can never fail the run** - `--no-coverage` suppresses them.

> **Why they are counts rather than checks, and this is the whole design of the block.** Whether 1 in
> 26 sources verified is acceptable, or whether a dream pass is overdue, are **judgement calls**, and
> a threshold in `validate.py` would launder judgement as a green check - the same line
> [ADR-0004](brain/decisions/0004-validator-as-type-checker.md) draws everywhere else.
> What the validator *can* honestly do is **make an invisible number visible at the one moment
> somebody is already looking at the brain's health**, which is every compound pass. The stages were
> never broken; they were unobservable, and a stage nobody can see the coverage of is a stage that
> silently stops running. **Read both numbers comparatively, never against a target.**

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

## Verifying one source on request (`/verify`)

This kit violates its own best-supported eval claim: **the agent that distils a source also gates it**
(claim 34, and claim 59's untunable trade). `validate.py` does not close that, because it checks
**form** and this is a **reading judgement**. This stage is the evaluator the gate lacks. **Trigger:
the user says "verify \<source>". Never automatic.** Adopt **fact-checker**, alone.

> **Full contract: [`stages/verify.md`](stages/verify.md). Read it before running the stage** - it owns
> the **six checks**, the three verdicts, the frames requirement ([ADR-0016](brain/decisions/0016-verify-reads-the-frames.md)),
> and the coverage expectation. **It is the one pass that may re-open the gate**, and the only one.

## Deep research on request (external evidence)

The corroboration gate buys *internal* consistency, which is not truth. **External** corroboration is
the only thing that raises real confidence, and this is the mechanism. **Trigger: the user says "deep
research". Never automatic** - most sources do not earn it and it is slow. Adopt **fact-checker +
synthesizer**. Output is a permanent `sources/<id>/context/<NN>_<slug>.md`, never a session artifact.

> **Full contract: [`stages/research.md`](stages/research.md). Read it before running the stage** - it
> owns the four verdicts, the **T1-T5 credibility tiers**, the **independence rule**, the search and
> fetch budget, and the calibration rule that aims one level above the source.

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
   | **Finished a `LEARNING.md`** -> append the `Presentation narrative` | **presenter** | + fact-checker when a movement's evidence strength is in question. **Never with curator** - curator owns the ramp, presenter owns the argument |
   | "How would I present this?" / explain a diagram to an audience | **presenter** | + mentor inside the technical body |
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

### The collision surface, measured

Six real ingest commits touch these, in this order of frequency. **Note what tops the list** - it is
not a `brain/` file:

| Files | Owner |
|---|---|
| `sources/<id>/**` | **The ingesting session, exclusively. Always safe.** |
| **`AGENTS.md` + `BUILD.md`** | **Shared, and touched more often than any single brain file** - an ingest that clarifies the contract drags `BUILD.md` with it |
| `INDEX.md`, `brain/claims.md`, `brain/log.md`, `brain/glossary.md` | Shared - every compound writes them |
| `brain/topics/*.md`, `brain/decisions/`, `brain/conjectures.md` | Shared |
| `validate.py`, `tools/*`, `personas/`, `sources/_TEMPLATE/` | Shared - contract layer |

**So parallelism is safe exactly up to the compound step, and not past it.** Capture, gate and
distil are source-local and are most of the wall clock; compounding is minutes and touches
everything. **Parallelise the expensive half; serialise the cheap one.**

### The compound gate

**Git is the gate, and it is not advisory.** Two sessions that compound simultaneously produce a
second push that the remote **rejects** (`! [rejected] main -> main (fetch first)`). No lockfile can
match that, because a lock is a convention an agent can forget and a rejected push is a failure it
cannot.

**Before compounding, run the preflight:**

1. `git fetch` and check whether `origin/main` moved since this session started.
2. `git status` - check for uncommitted changes to anything in the shared rows above.
3. **If either fires, stop and say so explicitly**, in these terms: *"a compound has landed (or is in
   flight) since I started; this one waits, and resumes once it lands."* Then re-read the shared
   files from disk, **take every number again** (next claim, next `S<n>`, next ADR), and proceed.
4. **Push immediately after compounding.** The exposure window is exactly the time your compound sits
   unpushed, and keeping it to seconds is what makes overlap rare rather than routine.

> **Stage explicit paths. Never `git add -A`.** This is the one hazard here that can silently destroy
> work rather than merely conflict: on 2026-08-02 a session staged everything while another's
> in-flight edits sat in the same tree, swept them into its commit, and had to reset. Nothing was
> lost **because it happened to notice**. Name the files you changed.

> **The contract layer is single-writer.** `AGENTS.md`, `validate.py`, `personas/` and the templates
> take one editor at a time - not for git reasons but because **a specification needs one author to
> stay coherent.** Two sessions editing *different sections* of `AGENTS.md` merge cleanly and can
> still produce two competing definitions of the same thing; that happened on 2026-08-02 with the
> `LEARNING.md` shape. **A clean merge is the dangerous case here, not the conflicting one** - git
> detects textual overlap, and the hazard is semantic overlap in non-overlapping text.

> **You do not need git worktrees at this scale.** They eliminate the `git add -A` hazard
> structurally, and they turn a silent claim-number collision into a visible merge conflict - but at
> two or three concurrent sessions the rule above costs nothing and a worktree costs branch
> discipline every day. **And they do not help with the failure that actually cost the most**, which
> was two sessions deciding the same design question independently. Revisit at five or more.

> **Do not build a locking scheme for this.** Scaffolding encodes an assumption that expires
> (claim 31), and this one has fired once. A lock also cannot see across worktrees when git-ignored,
> races when committed, and deadlocks when a session dies holding it. **Re-reading before writing,
> plus the push rejection above, is the whole mitigation.**

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

## Conjecturing on request (`/conjecture` - the generative pass)

The kit **gathers** (ingest, gate) and **reconciles** (dream). This is the third move - **abduce**:
propose an explanation the sources jointly imply and none of them states. **Trigger: the user says
"conjecture". Never automatic.** Adopt **synthesizer**. Output is `brain/conjectures.md`; a conjecture
is never a claim and never cited as one.

> **Full contract: [`stages/conjecture.md`](stages/conjecture.md). Read it before running the stage** -
> it owns the generative patterns, the lifecycle statuses, and **the one hard rule: a conjecture names
> its own falsifier**, without which it is an observation and belongs in a topic note.

## Dreaming on request (the reconciliation pass)

**The global reconciliation pass over `brain/` itself** - is what this brain believes still coherent
with itself? Not an ingest, not research, not lint. **Trigger: the user says "dream". Never automatic**,
and never as part of an ingest: an agent finishing a source holds two objectives and will trade the
second against the first silently (claim 59). Adopt **architect + fact-checker**.

> **Full contract: [`stages/dream.md`](stages/dream.md). Read it before running the stage** - it owns
> the eight drift classes, the pass procedure, and the rule that dreaming reconciles what was
> *promoted* and never re-opens a source's `nodes.md`.

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
  Write the walkthrough **as a mentor ramping up an engineer, in [presenter](personas/presenter.md)'s
  voice** - mentor decides what the reader needs, presenter decides how it is said - immediately
  after the diagram:

  1. **Orientation - one clause, and only where the notation is not self-evident.** If colour or
     shape carries meaning, give a legend, because a reader must never reverse-engineer your
     notation. **That is the whole of it.** Do **not** write "read it left to right" or "the flow runs
     top to bottom" - a reader can see which way the arrows point, and those sentences are the single
     most common filler in this repo's diagrams - **31 instances across 12 notes when it was first
     measured on 2026-08-15.**

     > **The move that replaces it: name what *kind* of diagram it is, and what it is not.** *"This is
     > an ownership diagram, not a component diagram."* *"This is a leverage diagram, not a component
     > diagram."* One clause, and it does the orientation work properly - it tells the reader what
     > question the picture answers and pre-empts the wrong reading, which no amount of describing
     > arrow direction can. **Use it as the opening clause of every diagram walkthrough in the kit.**
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
