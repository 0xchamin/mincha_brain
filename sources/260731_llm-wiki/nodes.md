# Knowledge nodes - LLM Wiki

> Persona: **fact-checker** - re-adopt when working this file.

> The atomic units of knowledge extracted from this source. Each node has a **stable ID** (`n1`,
> `n2`, ... - never renumber; topic notes reference these), a claim, **both legs each with its own
> citation** (or one leg marked `single-leg`), a gate verdict, and a confidence. Only
> `corroborated`/`single-leg` nodes (and recorded `divergence` findings) feed `LEARNING.md` and get
> promoted to `../../brain/`. The **fact-checker** persona owns the verdicts; see `../../AGENTS.md`
> and `prd.md` §6.

## What counts as a second leg here: nothing

**There is no second leg in this source and there is no honest way to manufacture one.** It is ~1,960
words of prose with no figures, no diagrams, no code, no data, no linked implementation and no worked
example. Both of the kit's pairings fail: there is no visual to set against the text, and there is no
code to set against the docs.

So the gate's floor applies to **every** node without exception: **`single-leg`, confidence
`needs-check`.** Nothing here is `corroborated`, and nothing may be retro-marked as such later
(`AGENTS.md` degrade table). The route to a second leg is external, and it was not requested.

**A single-leg source can still yield a divergence, and this one did.** `d1` is an inconsistency
between two sections *of the document itself* - not between two legs. It is weaker evidence than a
real docs-vs-code divergence, and it lands on precisely the claim the document is weakest on.

## Evidence class - split the source in two before citing it

This is **T4: one practitioner describing his own workflow.** The two halves are not equally strong:

| Class | Nodes | How to weigh |
|---|---|---|
| **Pattern** - what the design is, and why it is shaped that way | `n1`-`n9`, `n11`-`n12`, `n14`-`n18` | The transferable half. It stands on its own logic: you can follow the argument from "retrieval re-derives" to "so compile once and maintain it" without trusting the author about anything. Adopt or reject on the reasoning. |
| **Efficacy** - that it works, and how well | `n10`, `n13` | **Zero measurement.** No baseline, no eval, no comparison against the RAG systems the document opens by dismissing, no reported failure. `n10`'s "~100 sources" is an author estimate with no method attached. `n13` is a closing argument, and `d1` catches it contradicting the document's own operations section. **Never cite these as results.** |

**Two things count in this source's favour**, and they are worth stating because most sources in this
brain do not have them:

- **Nothing is being sold.** A personal gist: no product, no company, no affiliation stated, no call
  to action. The one tool it recommends (`qmd`, `n11`) is someone else's. That is a materially
  different position from a vendor describing the vendor's own system.
- **It declares its own epistemic status, unprompted** (`n16`): "intentionally abstract... It
  describes the idea, not a specific implementation." A source that calls itself a pattern rather
  than a result is easier to gate honestly than one that blurs the line.

Neither makes it evidence. **An unmeasured claim from a disinterested expert is still an unmeasured
claim** - it just fails differently from a vendor's. The efficacy nodes stay `needs-check`.

## What I had already seen at gate time (disclosure)

These nodes were derived from `raw/llm-wiki.md` **before** opening `../../brain/topics/memory.md`, so
that any agreement with the brain's existing memory synthesis would be *observed* rather than
reverse-engineered from it. What was nonetheless in context when I gated:

- **[ADR-0009](../../brain/decisions/0009-dreaming-reconciliation-pass.md), read in full and on
  purpose** - it is a prior claim on this source and testing it was the point. Its one-sentence
  characterisation of the gist is what `n8` re-derives and rejects.
- **Claims 60-64 of `brain/claims.md`**, surfaced incidentally while reading the file's tail for the
  next free claim number. They concern S7's memory tooling. Claim 61 overlaps `n18`; that node flags
  the overlap rather than presenting it as a discovery.
- **`brain/topics/memory.md` was not opened**, nor any other topic note, until this file was written.

## Nodes

| ID | Claim (crux) | Evidence leg + citation | Corroborating leg | Gate | Confidence |
|---|---|---|---|---|---|
| n1 | **Retrieval answers the question and forgets it - nothing accumulates.** RAG-shaped systems re-derive on every query: "the LLM is rediscovering knowledge from scratch on every question. There's no accumulation." The named failure case is the **synthesis question**: "Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time." NotebookLM, ChatGPT file uploads and "most RAG systems" are named as working this way. | S8 (gist @ac46de1, §The core idea) | (none - text-only source) | single-leg | needs-check - **sharper than the usual complaint about RAG**: not that retrieval returns bad chunks, but that it is **stateless across queries**, so synthesis is paid for again every time, while the user waits |
| n2 | **Compile once and keep it current, rather than re-deriving per query.** The LLM "incrementally builds and maintains a persistent wiki - a structured, interlinked collection of markdown files that sits between you and the raw sources... The knowledge is compiled once and then *kept current*, not re-derived on every query." What it buys is work already done: "The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read." | S8 (gist @ac46de1, §The core idea) | (none) | single-leg | needs-check - "compiled" is load-bearing: synthesis moves from **query time to ingest time**, the same trade as a build step versus an interpreter. The cost is that the artifact can go stale, which is what `n8` exists to handle |
| n3 | **Ingest integrates, it does not index.** "the LLM doesn't just index it for later retrieval. It reads it, extracts the key information, and integrates it into the existing wiki - updating entity pages, revising topic summaries, **noting where new data contradicts old claims**, strengthening or challenging the evolving synthesis." | S8 (gist @ac46de1, §The core idea) | (none) | single-leg | needs-check - note that contradiction-flagging is placed here **at ingest time**, and then **again** in the periodic pass (`n8`), with no account of why both are needed. `d1` presses on that silence |
| n4 | **Three layers, defined by who may write to them, not by what they store.** **Raw sources** are immutable - "the LLM reads from them but never modifies them. This is your source of truth." **The wiki** is LLM-only - "The LLM owns this layer entirely... You read it; the LLM writes it." **The schema** is co-evolved - "You and the LLM co-evolve this over time." | S8 (gist @ac46de1, §Architecture) | (none) | single-leg | needs-check - the immutable raw layer is the quiet load-bearing rule: it is what keeps every derived page auditable, since a claim can always be walked back to something the LLM could not have edited |
| n5 | **The schema document is what separates a maintainer from a chatbot.** "a document (e.g. CLAUDE.md for Claude Code or AGENTS.md for Codex) that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow... **This is the key configuration file - it's what makes the LLM a disciplined wiki maintainer rather than a generic chatbot.**" | S8 (gist @ac46de1, §Architecture) | (none) | single-leg | needs-check - the strongest claim about **where the engineering effort goes**, and an unusual answer: not the retrieval stack, not chunking, not the embedding model, but the prose contract |
| n6 | **Three operations over the wiki: ingest, query, lint.** Each gets its own section under §Operations. | S8 (gist @ac46de1, §Operations) | (none) | single-leg | needs-check - recorded as a plain fact about the document because a prior kit decision turns on it (`n8`). The three-verb framing is accurate; what the **third verb contains** is where the prior reading went wrong |
| n7 | **Answers are filed back, so querying compounds too.** "The important insight: **good answers can be filed back into the wiki as new pages.** A comparison you asked for, an analysis, a connection you discovered - these are valuable and shouldn't disappear into chat history. This way your explorations compound in the knowledge base just like ingested sources do." Formats named: markdown page, comparison table, Marp deck, matplotlib chart, canvas. | S8 (gist @ac46de1, §Operations - Query) | (none) | single-leg | needs-check - the non-obvious half of the pattern. The obvious input is sources; this says the **questions** are an input too, and that an answer dying in a chat log is a loss of the same kind as never ingesting the source |
| n8 | **Lint is a periodic, out-of-band drift pass, and it enumerates the drift classes.** "Periodically, ask the LLM to health-check the wiki. Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search. The LLM is good at suggesting new questions to investigate and new sources to look for." Six defect classes plus a generative role; "Periodically" and "ask the LLM to" put it **outside** the ingest, on its own trigger. | S8 (gist @ac46de1, §Operations - Lint) | (none) | single-leg | needs-check - **but this node overturns a prior claim in this brain; see the section below** |
| n9 | **Two navigation files with different jobs.** **index.md** is content-oriented: "a catalog of everything in the wiki - each page listed with a link, a one-line summary, and optionally metadata like date or source count... The LLM updates it on every ingest. When answering a query, the LLM reads the index first to find relevant pages, then drills into them." **log.md** is chronological: "an append-only record of what happened and when - ingests, queries, lint passes", with a consistent entry prefix (`## [2026-04-02] ingest \| Article Title`) so that `grep "^## \[" log.md \| tail -5` works. | S8 (gist @ac46de1, §Indexing and logging) | (none) | single-leg | needs-check - the split is the point: **what the wiki contains** versus **what happened to it**. One is read first on every query and constantly rewritten; the other is append-only and read for history. Collapse them and you get a file that is either useless as an index or lying as a log |
| n10 | **EFFICACY, UNMEASURED - an index file replaces embedding RAG at moderate scale.** "This works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and **avoids the need for embedding-based RAG infrastructure.**" | S8 (gist @ac46de1, §Indexing and logging) | (none) | single-leg | **needs-check - do not cite as a result.** The document's one falsifiable, quantified claim, and it arrives with nothing attached: no eval set, no comparison against the infrastructure it says you can skip, no definition of "works well", no account of what breaks past the ceiling, no derivation of the ~100. "Surprisingly" is doing the work a measurement should. **The best deep-research target in this source** |
| n11 | **Search is deferred until the index stops working, then named concretely.** "at small scale the index file is enough, but as the wiki grows you want proper search." The option given is `qmd` - "a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device. It has both a CLI (so the LLM can shell out to it) and an MCP server (so the LLM can use it as a native tool)." Alternative: "vibe-code a naive search script as the need arises". | S8 (gist @ac46de1, §Optional: CLI tools) | (none) | single-leg | needs-check - the **CLI-or-MCP** framing is the durable bit: a tool shipping both is usable by an agent two ways, and the choice belongs to the harness, not the tool |
| n12 | **An LLM cannot read markdown and its inline images in one pass.** "the workaround is to have the LLM read the text first, then view some or all of the referenced images separately to gain additional context. It's a bit clunky but works well enough." Surrounding advice: download images to local disk rather than rely on URLs "that may break". | S8 (gist @ac46de1, §Tips and tricks) | (none) | single-leg | needs-check - a mechanical constraint, not a preference, and it forces a **two-pass shape**: text first, then selected images. Note the selectivity ("some or all") - that is a cost decision, not a completeness one |
| n13 | **EFFICACY, UNMEASURED - wikis die of bookkeeping, and bookkeeping is what LLMs are free at.** "The tedious part of maintaining a knowledge base is not the reading or the thinking - it's the bookkeeping... **Humans abandon wikis because the maintenance burden grows faster than the value.** LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass. **The wiki stays maintained because the cost of maintenance is near zero.**" | S8 (gist @ac46de1, §Why this works) | (none) | single-leg | **needs-check - do not cite as a result.** The load-bearing "why now" argument, and entirely assertion: no abandoned wiki cited, no maintenance cost measured before or after, and "near zero" is false on its face for anyone paying per token - the cost **moved and shrank**, it did not vanish. See `d1`: the middle sentence is contradicted by the document's own §Lint |
| n14 | **The division of labour: the human keeps taste, the LLM takes the bookkeeping.** "You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work - the summarizing, cross-referencing, filing, and bookkeeping." Restated at the close: "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else." The analogy is explicit: "**Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.**" | S8 (gist @ac46de1, §The core idea, §Why this works) | (none) | single-leg | needs-check - the analogy assigns the human **reviewer and product owner**, not author. What is kept is judgement about *what is worth knowing*; what is given away is the writing. Whether that split survives the human never writing anything is not addressed |
| n15 | **Lineage: this is the Memex, with the maintenance problem solved.** "related in spirit to Vannevar Bush's Memex (1945) - a personal, curated knowledge store with associative trails between documents. Bush's vision was closer to this than to what the web became: private, actively curated, with the connections between documents as valuable as the documents themselves. **The part he couldn't solve was who does the maintenance. The LLM handles that.**" | S8 (gist @ac46de1, §Why this works) | (none) | single-leg | needs-check - the most useful sentence for placing the idea. It says the pattern is **80 years old and was blocked on one missing component**, and names that component as **labour** - not storage, retrieval or linking. That makes the LLM's contribution economic rather than intellectual |
| n16 | **The artifact is a pattern to be instantiated by the reader's agent, not a spec.** "This document is intentionally abstract. It describes the idea, not a specific implementation... Everything mentioned above is optional and modular - pick what's useful, ignore what isn't... **The right way to use this is to share it with your LLM agent and work together to instantiate a version that fits your needs. The document's only job is to communicate the pattern. Your LLM can figure out the rest.**" Stated up front too: "This is an idea file, it is designed to be copy pasted to your own LLM Agent." | S8 (gist @ac46de1, §Note, §preamble) | (none) | single-leg | needs-check - a claim about **distribution format**: the unit shipped is neither a library nor a spec but **prose sized for an agent's context window**, deliberately underspecified so the agent fills in the particulars. It also conveniently immunises the document against implementation critique |
| n17 | **Ingest is a wide write, and supervision is offered as taste.** "A single source might touch 10-15 wiki pages." And: "Personally I prefer to ingest sources one at a time and stay involved - I read the summaries, check the updates, and guide the LLM on what to emphasize. But you could also batch-ingest many sources at once with less supervision. It's up to you to develop the workflow that fits your style and document it in the schema." | S8 (gist @ac46de1, §Operations - Ingest) | (none) | single-leg | needs-check - **10-15 pages** says a source is not filed in one place: ingest is inherently a wide write, which is what makes drift possible at all. The consequence of choosing "batch, unsupervised" is left unexamined |
| n18 | **Git supplies versioning, branching and collaboration for the price of the format.** "The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free." | S8 (gist @ac46de1, §Tips and tricks) | (none) | single-leg | needs-check - **overlap disclosed**: adjacent to `claims.md` claim 61 (multi-writer memory needs versioning, attribution, arbitration), which was in context at gate time. **Not the same claim, and the gap matters**: 61 says a second writer *requires* that machinery, this says git *supplies* it free. Both hold only while the writers commit at human pace. Git gives history and attribution; it does not give **admission control or a write precondition**, and this single-writer design never has to find out |

## Dropped / divergences (audit trail)

| Candidate | Verdict | Note |
|---|---|---|
| `d1` **"LLMs don't forget to update a cross-reference" (§Why this works) vs "Look for: ...missing cross-references" (§Operations - Lint)** | **divergence - kept, and it is the sharpest finding in the source** | Both cannot be true. If the maintainer never drops a cross-reference, a recurring pass hunting for dropped cross-references is dead code. **Believe §Lint:** it is operational, it tells you what you will actually find, and it was evidently written by someone who found those things; §Why this works is a closing argument whose job is persuasion. The whole six-item lint list is an admission that integrate-on-ingest (`n3`) leaves defects behind. **This matters because it is the same failure the document diagnoses in humans, relocated:** the argument for the pattern is that maintenance is free, and the design includes a recurring maintenance pass because it is not. The honest version of `n13` is that **LLM bookkeeping is cheap enough to be worth doing repeatedly, not so reliable it need only be done once.** |
| Obsidian tooling specifics - Web Clipper, the attachment-folder hotkey binding, graph view, Marp, the Dataview plugin (§Tips and tricks) | dropped | Real and useful, but configuration for one person's app - source-specific trivia by the kit's own rule. `n12`'s constraint was lifted out of this section because it is about **LLMs**, not about Obsidian. |
| The application-domain list - personal/health, research, reading a book, business teams, competitive analysis, trip planning (§The core idea) | dropped | Illustrative breadth with no claim attached; nothing to gate. |
| The Tolkien Gateway comparison - a fan wiki built by volunteers over years, offered as the shape of what one person plus an LLM could now produce (§The core idea) | dropped | A vivid analogy, but it makes the same point as `n13` and `n15` with less precision. |

## The prior claim this source was filed under, and why it does not survive

[ADR-0009](../../brain/decisions/0009-dreaming-reconciliation-pass.md) cites this gist before it was
ingested, as the third source that "sharpened the framing" for the dream stage:

> Karpathy's *LLM Wiki* gist describes this same pattern (raw sources / maintained wiki / schema) and
> names three operations: **ingest, query, lint**. The kit has all three. **What it does not have is
> what S6 and S7 both argue is the load-bearing one** - a maintenance pass that runs on its own clock
> rather than inside the ingest.

Gated against the text, that breaks into three assertions:

| Assertion | Verdict | Evidence |
|---|---|---|
| The gist describes raw sources / maintained wiki / schema | **holds** | `n4` |
| The gist names three operations: ingest, query, lint | **holds** | `n6` |
| The gist does **not** supply the out-of-band maintenance pass; S6 and S7 do | **does not hold** | `n8` |

**§Lint *is* the maintenance pass.** It is periodic, it is invoked separately from ingest, and four of
its six defect classes are verbatim members of the dream stage's eight - contradictions, stale claims
superseded by newer sources, orphans, missing cross-references. A fifth, "important concepts mentioned
but lacking their own page", is the topic-creation call the architect persona owns. The sixth, "data
gaps that could be filled with a web search", is the kit's deep-research trigger.

**How the prior reading went wrong is worth naming, because it is a repeatable error:** it matched the
*word* "lint" to `validate.py`, concluded the kit already had that operation, and moved on.
`validate.py` shares nothing with §Lint but the name - it checks form, and every item on Karpathy's
list is a judgement. The kit's own contract says as much in the sentence directly above where the ADR
reasons: *"a green validator means the shape is right, not that the thinking is."*

Consequences, both filed in the compound pass:

1. The dream stage has an **independent third proponent** - and the most useful of the three, since S6
   and S7 are vendors describing products while this is a practitioner describing a workflow with
   nothing to sell.
2. ADR-0009's account of **why** the stage was built is wrong on the facts and is corrected by
   [ADR-0010](../../brain/decisions/0010-lint-is-the-dream-pass.md). The decision itself stands; only
   its reading of this source changes.

> **This is exactly the class of defect the dream stage exists to catch** - a claim that was wrong the
> day it was written, in a file nothing re-reads. It was found by ingesting the source rather than by
> a dream pass, which says something about where the drift comes from: **claims made *about* sources
> that have not been ingested yet.**
