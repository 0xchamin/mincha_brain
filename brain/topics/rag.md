# Topic: RAG (Retrieval-Augmented Generation)

**Status:** **emerging** (1 source - S8 "LLM Wiki", Andrej Karpathy, 2026-04-04).
**Basis:** the topic's first source, and it arrives from an unexpected direction - **it is an argument
against query-time retrieval**, not a description of how to do it. That is still the right home for
it: a claim about what to build *instead* of RAG belongs in the note that owns RAG, and splitting it
into a `knowledge-bases` note would put two halves of one argument in two places (architect call, see
"Scope" below).

**Read the evidence limit first.** S8 is **T4 - one practitioner describing his own workflow** - with
**no measurement of any kind**: no eval, no baseline, no comparison against the retrieval systems it
opens by dismissing, no cost figure, no reported failure. Every claim below is `single-leg`,
`needs-check`. The source has no figures, no code and no data, so it **cannot** produce an internally
corroborated claim, and none is marked as one. Two things count in its favour and neither is evidence:
**nothing is being sold**, and **the document declares its own abstractness** rather than blurring
pattern into result.

> Living, cross-source synthesis on RAG. Many sources feed this note; **merge and de-duplicate** as
> they arrive (architect persona). Every claim cited.

## What this covers

Retrieval-augmented generation: chunking, embeddings, vector stores, retrieval strategies (semantic /
hybrid / reranking), and grounding generations in retrieved context.

**Widened on S8's arrival** to cover the other answer to the same question: **maintained knowledge
layers** - compiling sources once into a persistent artifact that is kept current, instead of
re-retrieving and re-synthesizing per query. The two are alternatives to one problem (*how does a
model answer from a corpus it was not trained on?*), so they belong in one note.

**Boundary with the neighbours:**

- [`context-engineering.md`](context-engineering.md) treats retrieval as *one technique* for choosing
  which tokens reach the model ([ADR-0001](../decisions/0001-context-engineering-topic.md)). This note
  owns the corpus-side machinery: what is stored, in what shape, and how it is kept true.
- [`memory.md`](memory.md) draws the line as **"retrieval over a corpus someone else authored"** here
  versus **"a corpus the system authors about its user"** there ([ADR-0007](../decisions/0007-memory-topic.md)).
  **S8 is the first source to straddle that line, and the boundary needs a qualifier because of it.**
  An LLM Wiki is a corpus **the system authors about documents someone else authored** - derived like
  memory, about the world rather than about the user, and **layered on top of** an immutable
  third-party raw layer (`n4`). The refined rule: **this note owns knowledge derived from external
  sources; `memory.md` owns knowledge derived from the system's own experience.** Both can be
  system-authored; what differs is what the knowledge is *about*. Maintenance machinery is shared,
  which is why S8 feeds both notes.

## Synthesis

### The diagnosis: retrieval is stateless across queries

S8's opening is not the usual complaint about RAG. The usual complaint is that retrieval returns the
wrong chunks. This one holds **even when retrieval is perfect**: "the LLM is rediscovering knowledge
from scratch on every question. **There's no accumulation.**" The named failure case is the synthesis
question - "Ask a subtle question that requires synthesizing five documents, and the LLM has to find
and piece together the relevant fragments every time" [S8 §The core idea, `n1`].

> 💡 **Query-time synthesis** - relating documents to each other *when the question arrives*. Cheap to
> build, because nothing must be maintained; paid for on every question, while the user waits; and
> the result is discarded.

**The cost being described is not retrieval, it is synthesis** - and it is paid at the worst possible
moment, repeatedly, for the same answer.

### The alternative: compile once, then maintain

"The knowledge is **compiled once and then *kept current***, not re-derived on every query" [S8 §The
core idea, `n2`]. Take "compiled" literally: this is a **build step versus an interpreter**. Do the
expensive relating early and hand the reader an artifact where "the cross-references are already
there. The contradictions have already been flagged."

Every other property of the design falls out of that one choice:

| Because synthesis moves to ingest time... | ...you gain | ...and you owe |
|---|---|---|
| the artifact exists before the question | answering is a read, not a computation | the artifact can be **stale** - a failure mode a retrieval result structurally cannot have |
| one source is integrated across many pages | connections persist between sessions | an ingest is a **wide write**: "10-15 wiki pages" per source [`n17`] |
| the store is written, not derived on demand | it is greppable, diffable, reviewable | somebody must maintain it - the constraint the whole pattern turns on |

**The right column is where the third operation comes from**, and it is the half of the trade that
retrieval-based designs get for free.

### Layer the store by write access, not by content

The architecture is an **ownership** diagram [S8 §Architecture, `n4`]:

| Layer | Contents | Who writes |
|---|---|---|
| **Raw sources** | articles, papers, images, data | **Nobody.** "the LLM reads from them but never modifies them. This is your source of truth." |
| **The wiki** | summaries, entity/concept pages, comparisons, synthesis | **LLM only.** "You read it; the LLM writes it." |
| **The schema** | the contract document (`AGENTS.md` / `CLAUDE.md`) | **Both.** "You and the LLM co-evolve this over time." |

**The immutable raw layer is the quiet load-bearing rule.** Because the LLM can never edit it, every
derived page can be walked back to something that did not move under it. Remove that constraint and
the knowledge base becomes its own only witness - it can drift with nothing left to check it against.

**And the schema document, not the retrieval stack, is where the engineering goes**: it is "the key
configuration file - it's what makes the LLM a disciplined wiki maintainer rather than a generic
chatbot" [`n5`]. That is an unusual answer to *where does the difficulty live*, and it is the claim
most at risk of being self-serving, since the author is describing a workflow he already likes.

### Three operations, and two of them are not obvious

**Ingest integrates; it does not index** [`n3`]. The pass updates entity pages, revises topic
summaries, and **notes where new data contradicts old claims** - which commits you to something a
document store never does: an ingest may **weaken** the existing synthesis.

**Query writes back** [`n7`]. "**good answers can be filed back into the wiki as new pages**... these
are valuable and shouldn't disappear into chat history." This is the half most designs skip. The
obvious input to a knowledge base is the sources; this says the **questions** are an input of equal
standing, and an analysis dying in a chat log is a loss of the same kind as an uningested source. It
also makes the store reflect what its owner *cared about*, not merely what crossed his desk.

**Lint is a periodic pass over the whole store** [`n8`], enumerated as six defects: contradictions
between pages, stale claims superseded by newer sources, orphan pages with no inbound links, important
concepts lacking their own page, missing cross-references, and data gaps a web search could fill. Two
words carry the design - "**Periodically**" and "**ask**": it is neither a step of ingest nor a
daemon, but a separately invoked operation on its own clock. See [`memory.md`](memory.md), where this
converges with two other sources.

### Navigation: a catalog and a log, deliberately not one file

Two files with two different jobs [S8 §Indexing and logging, `n9`]:

| | `index.md` | `log.md` |
|---|---|---|
| Oriented by | **content** - what exists | **time** - what happened |
| Shape | a catalog: link, one-line summary, optional metadata | append-only entries |
| Written | rewritten on every ingest | appended, never edited |
| Read | **first, on every query**, to find the right pages before drilling in | for history and recent activity |

The tip attached to the log is small and good: a consistent entry prefix (`## [2026-04-02] ingest |
Article Title`) makes it parseable with `grep "^## \[" log.md | tail -5` - **structure cheap enough
that plain unix tools are the query engine.**

**Collapse the two and you get a file that is either useless as an index or lying as a log.** An index
must be rewritten to stay accurate; a log must never be rewritten to stay trustworthy. Those are
opposite requirements on the same bytes.

### The claim that would matter most, if it were measured

> "This works surprisingly well at moderate scale (**~100 sources, ~hundreds of pages**) and **avoids
> the need for embedding-based RAG infrastructure**" [S8 §Indexing and logging, `n10`].

**This is the topic's headline open question, not its headline finding.** It is the source's one
falsifiable, quantified claim, and it arrives with no eval set, no comparison against the
infrastructure it says you can skip, no definition of "works well", no account of what breaks past
the ceiling, and no derivation of the ~100. The word "surprisingly" is doing the work a measurement
should.

The staged position is the defensible part regardless: **defer the search infrastructure until the
index stops working** [`n11`], then reach for a real engine - `qmd` is named (local, hybrid
BM25/vector, LLM re-ranking, on-device, shipping **both a CLI and an MCP server**, so an agent can
shell out to it *or* bind it as a native tool).

### Why the pattern is only now buildable: the constraint is labour

"The tedious part of maintaining a knowledge base is not the reading or the thinking - **it's the
bookkeeping**... Humans abandon wikis because the maintenance burden grows faster than the value"
[S8 §Why this works, `n13`]. The lineage makes it land: this is Vannevar Bush's **Memex** (1945),
"private, actively curated, with the connections between documents as valuable as the documents
themselves", and "**the part he couldn't solve was who does the maintenance**" [`n15`].

> 💡 **Memex** - Bush's 1945 personal document store with associative trails between documents.
> Blocked for eighty years on maintenance labour rather than on storage, retrieval or linking - which
> reframes what an LLM contributes here as **economic rather than intellectual**.

**But do not carry the sentence that follows it.** "The wiki stays maintained because the cost of
maintenance is **near zero**" is unmeasured and false on its face for anyone paying per token - the
cost **moved and shrank**, it did not vanish. And the claim that "LLMs... don't forget to update a
cross-reference" is contradicted by the document's own §Lint, which instructs you to go hunting for
**missing cross-references** [`d1`].

**Believe §Lint.** It is the operational section, written by someone who evidently found those
defects; §Why this works is a closing argument. The six-item list is an admission that
integrate-on-ingest leaves defects behind.

> **The honest version, and the one worth promoting: LLM bookkeeping is cheap enough to be worth doing
> repeatedly, not so reliable that doing it once is enough.** Weaker, and far more useful - it is the
> version that actually implies the third operation.

### Ship the pattern as prose, let the agent instantiate it

"This document is **intentionally abstract**... **The right way to use this is to share it with your
LLM agent and work together to instantiate a version that fits your needs**" [S8 §Note, `n16`].

Read as a claim about **distribution format**, this is the interesting one: the unit shipped is
neither a library nor a specification but **prose sized for an agent's context window**, deliberately
underspecified so the agent fills in the particulars for its own harness and domain - with the schema
document [`n5`] as where that instantiation lands and persists. It is also conveniently
unfalsifiable: a document that specifies nothing cannot be wrong about an implementation.

## Key claims

| Claim | Sources (cited) | Confidence |
|---|---|---|
| **Retrieval is stateless across queries.** Query-time synthesis re-pieces the same fragments for every question, at the moment the user waits, and keeps none of it. The complaint holds even when retrieval is perfect. | S8 §The core idea (`n1`) | emerging (single-leg) |
| **Compile once and keep current, rather than re-deriving per query** - moving synthesis from query time to ingest time, the same trade as a build step versus an interpreter. The cost is that the artifact can now be *stale*. | S8 §The core idea (`n2`) | emerging (single-leg) |
| **Layer a knowledge base by who may write to it**: immutable raw sources, an LLM-owned derived layer, a co-evolved schema. The immutable layer is what keeps every derived claim auditable. | S8 §Architecture (`n4`) | emerging (single-leg) |
| **Queries are an input to the knowledge base, not just sources** - file good answers back as pages, so exploration compounds like ingestion. | S8 §Operations - Query (`n7`) | emerging (single-leg) |
| **Split the catalog from the log.** An index must be rewritten to stay accurate; a log must never be rewritten to stay trustworthy. One file cannot do both. | S8 §Indexing and logging (`n9`) | emerging (single-leg) |
| **The binding constraint on a knowledge base is maintenance labour** - not storage, retrieval or linking. Bush's Memex was blocked on exactly this in 1945. | S8 §Why this works (`n13`, `n15`) | emerging (single-leg) |
| **An index file may substitute for embedding-retrieval infrastructure at moderate scale (~100 sources).** | S8 §Indexing and logging (`n10`) | **needs-check - unmeasured.** The one falsifiable claim here, with no eval, baseline or derivation. Do not cite as a result |
| **Defer search infrastructure until the index stops working**, then use a real engine; prefer one shipping both a CLI and an MCP server, so the harness chooses how to call it. | S8 §Optional: CLI tools (`n11`) | emerging (single-leg) |

## Key visuals

_None. **S8 contains no figures, diagrams, images or data of any kind** - which is also why every claim
above is single-leg. The two generated diagrams for this source live in its
[`LEARNING.md`](../../sources/260731_llm-wiki/LEARNING.md) and are labelled as synthesized, not
sourced._

## Open questions / conflicts

- **Where does index-file navigation actually break?** [`n10`] claims ~100 sources / hundreds of pages
  with no derivation and no account of the failure past it. **The highest-value deep-research target
  in this topic**, and unlike most claims in this brain it is the sort of thing someone may genuinely
  have measured (index-based vs embedding retrieval at that scale).
- **This brain is a live instance of the pattern and currently proves nothing.** It runs exactly the
  described design - immutable `raw/`, an agent-written `brain/`, `AGENTS.md` as the schema,
  `INDEX.md` read first, an append-only `log.md` - at **8 sources**, an order of magnitude below the
  claimed ceiling. **n=1, well inside the easy regime**: no evidence either way, and worth saying so
  before the coincidence gets mistaken for corroboration.
- **Nothing here addresses retrieval mechanics at all.** Chunking, embeddings, reranking, hybrid
  search and grounding evaluation - the topic's original scope - still have **zero sources**. The one
  source arrived arguing you may not need them, which is not the same as covering them.
- **Does the human keep their grip on knowledge they never wrote?** The division of labour [`n14`]
  hands the human taste and the LLM the writing. Nothing addresses what a reader retains of a corpus
  they have only ever read.
- **What does the lint pass cost, and how often is "periodically"?** It reads everything by
  construction. S8 neither budgets nor triggers it. The kit's own answer - on request, unbudgeted
  ([ADR-0009](../decisions/0009-dreaming-reconciliation-pass.md)) - is a decision, not a finding.

## Sources feeding this topic

- **S8** - [LLM Wiki](../../sources/260731_llm-wiki/LEARNING.md) (Andrej Karpathy, 2026-04-04).
  **T4 practitioner essay, ~1,960 words, no figures and no implementation.** Read it for the design
  argument, which stands on its own logic: you can follow "retrieval re-derives" to "so compile once
  and maintain it" without trusting the author about anything. **Do not read it for evidence** - the
  two efficacy claims (`n10`, `n13`) are assertion phrased with a confidence nothing behind them
  supports, and `d1` catches one of them contradicting the document's own operations section. Its
  unusual virtue among this brain's sources is that **nothing is being sold**.
