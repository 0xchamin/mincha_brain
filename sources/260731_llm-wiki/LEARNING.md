# Learning - LLM Wiki

> Persona: **curator** + **mentor, always**. Re-adopt when working this file.

> The distilled document you learn from. Built from the gated nodes in `nodes.md`. Every claim is
> cited. **This source has no visuals of any kind** - the two diagrams below are *generated*, and
> their provenance says so. See `SOURCE.md` for metadata.

> **Deviation from the standard shape, stated rather than hidden.** A `LEARNING.md` is normally
> **visual-led**. This source is ~1,960 words of prose with **no figures, no diagrams, no code, no
> data and no worked example**, so there is nothing to lead with and no honest way to manufacture a
> second leg. **Every node here is `single-leg`, `needs-check`, without exception** - and nothing may
> be retro-marked `corroborated` later. The walkthrough is led by the argument instead.

> **Two kinds of material, kept visually distinct.** Claims from the gist carry a node ID (`n8`) and
> a section. Blocks marked **"Background, supplied"** are context *I* am adding - established prior
> art the gist assumes or never names. They are uncited by construction.

## TL;DR

A knowledge base built on retrieval **re-derives its synthesis on every question and keeps none of
it**; the alternative is to compile the knowledge once into a maintained markdown wiki that an LLM
owns, and pay the synthesis cost at **ingest** time instead of at query time (`n1`, `n2`). Three
layers - immutable raw sources, an LLM-written wiki, and a schema document both parties co-evolve -
plus three operations: **ingest, query, lint** (`n4`, `n6`). The pattern is Vannevar Bush's **Memex**
(1945), which was blocked for eighty years on one thing: **who does the maintenance** (`n15`).
`https://gist.github.com/karpathy` (revision `ac46de1`)

```mermaid
flowchart TB
    Q{"which cost are you paying,<br/>and how often?"}
    L["<b>lookup</b> - finding the documents<br/><i>better chunking, better embeddings,<br/>a reranker on top</i>"]
    S["<b>synthesis</b> - relating them<br/>to each other<br/><i>happens after the right documents<br/>are already in hand</i>"]
    R["retrieval re-pays it on every<br/>single question, then discards it - n1"]
    C["compile it once at ingest,<br/>and keep it current - n2"]
    W["and the whole rest of the design<br/>falls out of that one move"]

    Q --> L
    Q --> S --> R
    S --> C --> W

    classDef aimed fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d
    classDef right fill:#dcfce7,stroke:#15803d,color:#14532d
    class L,R aimed
    class C,W right
```

This is a diagnosis diagram, not an architecture diagram, and the left branch is what the industry
spends its money on. **The crux is that this is not the usual complaint about retrieval, because it
holds even when retrieval is perfect: what is being re-paid is the relating of documents rather than
the finding of them.** It is drawn as a fork on a cost question rather than as a pipeline because the
two branches are not stages you pass through, and the failure of the naive approach is not that it
works badly but that it is aimed at the cheaper of the two costs. Everything the note describes after
this, the three layers and the three operations, is a consequence of moving the right-hand cost from
query time to ingest time. *Synthesized from `n1` and `n2`.*

## The 1-minute version

This article covers a short gist that proposes replacing a retrieval-based knowledge base with a
markdown wiki an LLM owns, writes and keeps current on your behalf. It is roughly nineteen hundred
words of prose with no figures, no code, no data and no worked example, which makes it a design
argument rather than a report of something built and measured. That is worth knowing before you read
it, because it means the value has to come from the diagnosis rather than from a result. The
diagnosis is where the gist starts, and it is the strongest part of it.

The problem it works on is that retrieval is stateless across queries. Ask a question that needs five
documents synthesised, and the model finds and pieces the same fragments together every single time,
while the user waits, and then the answer is thrown away (`n1`). Nothing accumulates from one
question to the next, so the hundredth question costs exactly what the first one did. At first glance
this reads as the familiar complaint about RAG, and the distinction is worth drawing carefully.

The usual complaint is that retrieval returns the wrong chunks, which is a problem about lookup. This
one holds even when retrieval is perfect. What is being re-paid is not the finding of documents but
the relating of them to each other, and that relating happens after the right documents are already
in hand. The reason the problem is hard, in other words, is that the levers everyone reaches for are
aimed somewhere else entirely.

Suppose instead you attack it the way the field usually does, with better chunking, a stronger
embedding model and a reranker on top. Each of those genuinely improves which documents come back,
and none of them changes the moment at which synthesis happens. You end up paying for a more accurate
set of fragments and then re-deriving the same synthesis over them, question after question, and
discarding it every time. The naive approach does not fail because it works badly. It fails because
it is aimed at the cheaper of the two costs.

The idea is to move synthesis from query time to ingest time and then keep the result current
(`n2`). Compile the knowledge once rather than interpreting it afresh on every question, which is the
trade a build step makes against an interpreter. The word compiled is worth taking literally, because
the whole of the rest of the design follows from that one move rather than being proposed alongside
it.

It works by layering the store according to who may write to it (`n4`). Raw sources are immutable and
nobody edits them. The wiki is written by the LLM and only read by you. The schema document, which is
the contract telling the LLM how the wiki is structured, is the one layer both parties co-evolve.
Three operations then run over those layers. Ingest integrates a new source into the pages that
already exist rather than indexing it for later, and may weaken the synthesis already written
(`n3`). Query files good answers back into the wiki as new pages, which makes the questions an input
of the same standing as the sources (`n7`). Lint is a periodic pass, invoked out of band, that hunts
six named defect classes (`n8`). That third operation is the one that gives the design away, because
a store needing no repair would never have earned it.

The cost is a failure mode a retrieval result structurally cannot have, which is that the artifact
can now be stale. An ingest is a wide write touching ten to fifteen pages at once (`n17`), so fifteen
unreviewed edits accumulate per source, and that arithmetic is what makes drift possible at all.
Somebody therefore has to maintain the thing, which is the entire reason the third operation exists.
That constraint is also the oldest part of the story. The gist places itself as Vannevar Bush's
Memex from 1945, a design blocked for eighty years not on storage or linking but on who does the
bookkeeping, which reframes the LLM's contribution as economic rather than intellectual (`n15`).

How far to trust it is the part to be blunt about. This is one practitioner writing about a workflow
he already prefers, with no eval, no baseline and no comparison against the retrieval systems the
gist opens by dismissing. Its two efficacy claims are pure assertion, and one of them contradicts the
document's own operations section (`d1`). Nothing is being sold here, which is rarer in this brain
than it sounds, and an unmeasured claim from a disinterested expert is still unmeasured. Take the
pattern, which stands on its own logic, and leave the numbers alone.

The same argument, compressed for reference rather than for reading:

| | |
|---|---|
| **The problem** | Retrieval is **stateless across queries**. Ask a question needing five documents synthesised and the model re-finds and re-pieces the same fragments every time, while the user waits, then throws the result away (`n1`). |
| **Why the obvious answer fails** | This is not the usual RAG complaint. It holds **even when retrieval is perfect** - the cost being re-paid is *synthesis*, not lookup, and no amount of better chunking touches it. |
| **The idea** | **Compile once, then maintain.** Move synthesis from query time to ingest time - the trade a build step makes against an interpreter (`n2`). |
| **How it works** | Layer the store by **who may write**: immutable raw sources, an LLM-owned wiki, a co-evolved schema document (`n4`). Three operations over it: **ingest** integrates rather than indexes (`n3`), **query** files good answers back as new pages (`n7`), **lint** is a periodic out-of-band pass hunting six named defect classes (`n8`). |
| **What it costs** | The artifact can now be **stale** - a failure mode a retrieval result structurally cannot have. An ingest is a **wide write**, touching 10-15 pages (`n17`), which is what makes drift possible. Somebody must maintain it, which is the whole reason for the third operation. |
| **The lineage** | **Memex, 1945.** Bush proposed exactly this and could not solve *who does the bookkeeping*. The LLM's contribution is therefore **economic, not intellectual** (`n15`). |
| **How far to trust it** | **T4, one practitioner, zero measurement.** No eval, no baseline, no comparison against the RAG systems it opens by dismissing. Its two efficacy claims are assertion, and one contradicts the document's own operations section (`d1`). **Nothing is being sold, which is rarer here than it sounds - but an unmeasured claim from a disinterested expert is still unmeasured.** |

## Key claims

- **Retrieval is stateless across queries** - synthesis is re-paid per question and discarded. `n1`
- **Compile once and keep current** rather than re-deriving per query. `n2`
- **Layer a knowledge base by who may write to it**: immutable raw / LLM-owned / co-evolved schema.
  `n4`
- **The schema document, not the retrieval stack, is where the engineering goes.** `n5`
- **Ingest integrates; it does not index** - and may *weaken* the existing synthesis. `n3`
- **Queries are an input to the store, not just a load on it** - file answers back as pages. `n7`
- **Lint is a periodic out-of-band pass** with six enumerable defect classes. `n8`
- **Split the catalog from the log** - opposite requirements on the same bytes. `n9`
- **The binding constraint is maintenance labour** (Memex, 1945). `n13` `n15`
- ⚠️ **An index file replaces embedding RAG at ~100 sources** - `n10`, **unmeasured, do not cite as a
  result.**

## What you will learn, and in what order

```mermaid
flowchart TB
    subgraph A["A. The diagnosis, which is not the usual RAG complaint"]
        S1["1 - Retrieval is stateless<br/>across queries"]
        S2["2 - Compile once,<br/>then maintain"]
    end
    subgraph B["B. The design that falls out of that one choice"]
        S3["3 - Layer by who<br/>may WRITE"]
        S4["4 - The schema doc is<br/>where the work goes"]
    end
    subgraph C["C. Three operations, and the third is the interesting one"]
        S5["5 - Ingest integrates,<br/>does not index"]
        S6["6 - Query writes back"]
        S7["7 - Lint: the out-of-band<br/>drift pass"]
    end
    subgraph D["D. Navigation, scale, and the argument that overreaches"]
        S8["8 - Catalog vs log"]
        S9["9 - Defer search until<br/>the index breaks"]
        S10["10 - Memex, labour,<br/>and where it overclaims"]
    end
    A --> B --> C --> D
    S1 --- S2
    S3 --- S4
    S5 --- S6 --- S7
    S8 --- S9 --- S10

    style C fill:#e8f0fc
    style D fill:#fbf1dc
```

This is a reading-order diagram about the note rather than about the wiki, gathered into four movements. Blue
marks the payload and amber marks the stretch to read most carefully, and it is worth saying at the
outset why those two are different things. **The crux is that every property of this design falls out
of a single choice, which is moving synthesis from query time to ingest time, and that includes the
new failure mode the choice buys.**

Movement A is the whole argument in miniature, and everything after it is consequence. That is why
the design in movement B reads as *derived* rather than proposed. If you follow the diagnosis in A,
the shape of B should feel forced rather than chosen, and if it does not, the fault is in the
derivation rather than in your reading.

Movement C is the payload, and it holds three operations. One of them, `lint`, is the reason this
source earned an ADR, because it overturned a claim this brain already held. Read that operation
closely even if you skim the other two.

Movement D is separated from everything before it because the document changes what it is doing
there. It stops describing a design and starts persuading you of one, and it is also where the
source's only quantified claim and its only self-contradiction both sit. **Your reading posture has
to change at that boundary**, which is the reason the roadmap draws it as a boundary at all.

*Synthesized roadmap of this note - not from the source.*

## Movement A - the diagnosis, which is not the usual RAG complaint

```mermaid
flowchart TB
    U["the familiar complaint:<br/>retrieval returns the wrong chunks"]
    T["this one:<br/>retrieval returns the <b>right</b> chunks<br/>and still re-derives the synthesis - n1"]
    N["so the hundredth question costs<br/>exactly what the first one did"]
    F["the fix cannot be a better retriever,<br/>because a perfect retriever does not<br/>change when synthesis happens"]

    U -.->|"easy to mistake<br/>one for the other"| T
    T --> N --> F

    style U fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d
    style F fill:#dcfce7,stroke:#15803d,color:#14532d
```

This is a distinction diagram, not a problem statement, and the dashed edge is the confusion the
movement exists to prevent. **The crux is that the two complaints sound identical and have opposite
remedies, so a reader who collapses them will spend the next year improving a retriever that was never
the bottleneck.** It is drawn with the wrong reading on top and explicitly labelled, rather than
omitted, because the argument only lands once you have felt the pull of the familiar version. If you
take one thing from this movement, take the test: does the problem survive a perfect retriever? Here it
does, which is what makes it a different problem.

*Synthesized from `n1` and `n2`.*

### 1. The diagnosis: retrieval has no memory of having answered

The gist opens on a complaint about RAG, and it is **not** the complaint you expect. The usual one is
that retrieval returns the wrong chunks. This one holds **even when retrieval is perfect**:

> "the LLM is rediscovering knowledge from scratch on every question. **There's no accumulation.**"
> (`n1`, §The core idea)

The named failure case makes it concrete: ask a subtle question requiring five documents to be
synthesised, and the model must find and piece together the same fragments **every single time**.

> 💡 **Query-time synthesis** - relating documents to each other *at the moment the question arrives*.
> Cheap to build, because nothing must be maintained. Paid on every question, while the user waits.
> And the result is discarded.

**Separate the two costs, because the whole argument turns on it.** Retrieval is *lookup*; what is
being re-paid here is *synthesis* - the expensive relating of one document to another. Better
chunking, better embeddings and better rerankers all improve lookup and leave synthesis exactly where
it was: at query time, repeated, discarded.

So if the expensive thing is being done at the wrong moment, when should it be done instead?

### 2. Compile once, then keep it current

```mermaid
flowchart TB
    INT["<b>interpreter</b><br/>re-derive on every question<br/><i>always current, always re-paid</i>"]
    CMP["<b>compiler</b><br/>derive once at ingest<br/><i>paid once, and can go stale</i>"]
    Q["the trade is not speed.<br/>It is <b>when</b> you pay and<br/><b>what</b> can rot"]

    INT --> Q
    CMP --> Q

    style CMP fill:#dcfce7,stroke:#15803d,color:#14532d
    style Q fill:#fff4e5,stroke:#b45309,color:#78350f
```

This is an analogy diagram, and the word "compiled" in the section title is meant literally rather than
loosely. **The crux is that moving synthesis to ingest time buys exactly what a build step buys over an
interpreter, and it also inherits the corresponding liability: a compiled artifact can be out of date
in a way a freshly interpreted one cannot.** It is drawn as two options reaching one trade-off node
rather than as a recommendation because the gist is not claiming the compiler is better in general,
only that it is aimed at the cost that matters here. Staleness is the price, and the third operation in
Movement C exists to pay it.

*Synthesized from `n2`.*


> "The knowledge is **compiled once and then *kept current***, not re-derived on every query."
> (`n2`, §The core idea)

**Take "compiled" literally, because it is the most useful word in the document.** This is a **build
step versus an interpreter**. Do the expensive relating early, once, and hand the reader an artifact
where "the cross-references are already there. The contradictions have already been flagged."

> **Background, supplied.** The compile/interpret trade is one of the oldest in computing and its
> shape is well understood: you pay more up front and at every *change*, in exchange for paying far
> less at every *use* - and you accept that the compiled artifact can now be **out of date with
> respect to its source**. That last clause is the entire cost of this design, and the document names
> it without quite framing it that way. A retrieval result cannot be stale, because it did not exist
> until you asked. **A compiled artifact can.**

Every other property falls out of that single choice:

| Because synthesis moves to ingest time... | ...you gain | ...and you owe |
|---|---|---|
| the artifact exists before the question | answering is a **read**, not a computation | the artifact can be **stale** - a failure a retrieval result structurally cannot have |
| one source is integrated across many pages | connections persist between sessions | an ingest is a **wide write**: 10-15 pages per source (`n17`) |
| the store is written, not derived on demand | it is greppable, diffable, reviewable | **somebody must maintain it** |

**The right-hand column is where the third operation comes from**, and it is the half that
retrieval-based designs get for free. Hold it - section 7 is where it is paid.

## Movement B - the design that falls out of one choice

```mermaid
flowchart TB
    C["compile once at ingest"]
    Q1{"if an LLM writes the store,<br/>who may write what?"}
    L["3. layer by <b>write access</b>:<br/>raw sources immutable, wiki LLM-owned,<br/>schema co-evolved by both - n4"]
    Q2{"how does the LLM know<br/>what shape to write?"}
    S["4. the schema document is the contract,<br/>and it is where the engineering goes -<br/>not the retrieval stack - n5"]

    C --> Q1 --> L --> Q2 --> S

    style S fill:#dcfce7,stroke:#15803d,color:#14532d
```

This is an ownership diagram, not a storage diagram, and the distinction is the movement's whole
content. **The crux is that once a machine is writing your knowledge base, the interesting axis stops
being where bytes live and becomes who is permitted to change them**, which is a question no retrieval
architecture has to answer. It is drawn as two questions descending from the compile decision because
both are forced by it rather than chosen: nothing in a query-time system needs a write-permission model
or a schema contract. The second box is the one practitioners under-invest in, since it looks like
documentation and behaves like an interface definition.

*Synthesized from `n4` and `n5`.*

### 3. The architecture is an ownership diagram, not a storage diagram

Most knowledge-base architectures are drawn by *what is stored where*. This one is drawn by **who is
allowed to write** (`n4`, §Architecture), and that is the more interesting axis.

| Layer | Contents | Who writes |
|---|---|---|
| **Raw sources** | articles, papers, images, data | **Nobody.** "the LLM reads from them but never modifies them. This is your source of truth." |
| **The wiki** | summaries, entity and concept pages, comparisons, synthesis | **LLM only.** "You read it; the LLM writes it." |
| **The schema** | the contract document (`AGENTS.md` / `CLAUDE.md`) | **Both.** "You and the LLM co-evolve this over time." |

**The immutable raw layer is the quiet load-bearing rule.** Because the LLM can never edit it, every
derived page can be walked back to something that did not move underneath it. Remove that constraint
and the knowledge base becomes **its own only witness** - free to drift with nothing left to check it
against.

> **Background, supplied.** This is the same discipline as an **append-only source of truth with
> derived views** - an immutable log plus materialised projections you can always rebuild. The
> property it buys is *reconstructability*: if the derived layer is corrupted, you regenerate it. The
> gist never says this, and it matters more here than in a database, because the derivation is
> performed by a non-deterministic process that cannot be replayed exactly.

That leaves the middle layer as the odd one. The LLM owns it entirely - so what keeps the LLM
disciplined?

### 4. The schema document, not the retrieval stack, is where the engineering goes

```mermaid
flowchart TB
    R["where a RAG team spends:<br/>chunker, embedding model,<br/>reranker, vector store"]
    W["where this design spends:<br/>one markdown document describing<br/>how the wiki is structured - n5"]
    B["it is the contract between<br/>you and the writer"]
    C["and it is the one layer both<br/>parties co-evolve - n4"]

    R -.->|"the budget moves"| W --> B --> C

    style R fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d
    style W fill:#dcfce7,stroke:#15803d,color:#14532d
```

This is a budget-relocation diagram, not an architecture. **The crux is that the engineering does not
disappear when you delete the retrieval stack, it moves into a prose document that looks like
documentation and behaves like an interface definition.** It is drawn as a transfer rather than as a
comparison because the failure mode is under-investment: a team that reads "no vector database" as
"less work" will write a thin schema and get a wiki whose structure drifts every time the model is
asked to extend it. The co-evolution property in the last box is what makes it a contract rather than
a spec, since the writer is allowed to propose changes to the shape it writes into.

*Synthesized from `n4` and `n5`.*


> "a document (e.g. `CLAUDE.md` for Claude Code or `AGENTS.md` for Codex) that tells the LLM how the
> wiki is structured, what the conventions are, and what workflows to follow... **This is the key
> configuration file - it's what makes the LLM a disciplined wiki maintainer rather than a generic
> chatbot.**" (`n5`, §Architecture)

**This is an unusual answer and it is worth registering the surprise.** Asked what makes an LLM
knowledge system work, the expected answers are the retrieval stack, the chunking strategy, the
embedding model. This says none of them. The load-bearing engineering artifact is **prose**.

It is also **the only layer both parties write** - which makes it the one place a correction to
*behaviour*, as opposed to a correction to a *fact*, can be recorded and survive. A wrong fact gets
fixed on a page. A wrong *convention* has nowhere else to live.

> ⚠️ **Unmeasured, and self-descriptive.** The author is describing a workflow he already prefers,
> with no evaluation of any kind. The framing is valuable; the confidence is not earned.

With the layers settled, the operations become the substance.

## Movement C - three operations, and the third gives the design away

```mermaid
flowchart TB
    I["5. <b>ingest</b> integrates a new source into<br/>pages that already exist, and may<br/><i>weaken</i> the synthesis already there - n3"]
    Q["6. <b>query</b> files good answers back as<br/>new pages, so questions are an input<br/>of the same standing as sources - n7"]
    L["7. <b>lint</b> is a periodic out-of-band pass<br/>hunting six named defect classes - n8"]
    T["A store needing no repair<br/>would never have earned a lint pass"]

    I --> T
    Q --> T
    L --> T

    style L fill:#e8f0fc,stroke:#4338ca,color:#312e81
    style T fill:#fff4e5,stroke:#b45309,color:#78350f
```

This is an admission diagram, not an operations manual. **The crux is that the third operation is a
confession: a design that ships with a periodic repair pass is telling you it expects to drift, and
that is the honest part of the gist rather than a weakness in it.** The three are drawn converging on
a single inference rather than as a lifecycle because their sequence is not the point; what matters is
what their existence jointly implies. Notice that ingest is the operation carrying the risk, since it
is a wide write that may make the existing synthesis worse, and lint is the only thing standing between
that and a store nobody trusts.

*Synthesized from `n3`, `n7`, `n8` and `n17`.*

### 5. Ingest integrates; it does not index

> The pass "doesn't just index it for later retrieval. It reads it, extracts the key information, and
> integrates it into the existing wiki - updating entity pages, revising topic summaries, **noting
> where new data contradicts old claims**, strengthening or challenging the evolving synthesis."
> (`n3`, §The core idea)

**That commits you to something a document store never does: an ingest may *weaken* the existing
synthesis.** A new source is not additive. It can undermine a page written six months ago, and the
design says so out loud - which is a strong claim, because it means ingest is not a pure function
over new material but an edit to accumulated belief.

Note also the scale: "a single source might touch **10-15 wiki pages**" (`n17`, §Operations - Ingest).
**Ingest is inherently a wide write, and that is precisely what makes drift possible at all.** Fifteen
edits per source, none reviewed in full, compounding over a hundred sources.

Hold that number too. It is the arithmetic behind section 7.

### 6. Queries are an input, not just a load

```mermaid
flowchart TB
    U["a user asks a question"]
    A["the LLM composes a good answer"]
    D1["<b>retrieval</b>: the answer is<br/>returned and discarded"]
    D2["<b>this design</b>: the answer is filed<br/>back into the wiki as a new page - n7"]
    R["so the store gets better because<br/>it was used, and a question has the<br/>same standing as a source"]

    U --> A
    A --> D1
    A --> D2 --> R

    style D1 fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d
    style R fill:#dcfce7,stroke:#15803d,color:#14532d
```

This is a comparison diagram, not a data flow, and the interesting claim is about standing rather than
about caching. **The crux is that filing answers back makes usage a write channel, so the questions
people actually ask become part of the knowledge base rather than a load on it.** It is drawn with both
fates branching from the same answer because the difference is one decision at one moment, and it is
cheap. Worth noting what this quietly implies and the gist does not: a question nobody asks never gets
a page, so the store's shape ends up tracking demand, which is a good property for a working reference
and a bad one for completeness.

*Synthesized from `n7`; the demand-tracking consequence is this brain's reading.*


This is the half of the pattern most designs skip, and the one most worth stealing.

> "**good answers can be filed back into the wiki as new pages**... these are valuable and shouldn't
> disappear into chat history. This way your explorations compound in the knowledge base just like
> ingested sources do." (`n7`, §Operations - Query)

The obvious input to a knowledge base is the sources. This says **the questions are an input of equal
standing**, and that an analysis dying in a chat log is a loss of the same kind as an uningested
source.

**And there is a second-order effect the document does not draw out.** Filing answers back makes the
store reflect **what its owner actually cared about**, not merely what crossed their desk. Two people
ingesting the same hundred sources end up with different wikis, and the difference is the questions
they asked. That is a feature - it is the store becoming *personal* in a way pure ingestion cannot
achieve.

So: ingest writes, query writes. What cleans up after both?

### 7. Lint is a periodic, out-of-band pass - and it overturned a claim in this brain

```mermaid
flowchart TB
    I["each ingest is a <b>wide write</b>,<br/>touching 10-15 pages at once - n17"]
    N["nobody reviews 15 edits per source"]
    D["so drift is arithmetically inevitable,<br/>not a risk to be managed"]
    L["lint: a periodic pass, invoked<br/><b>out of band</b>, hunting six<br/>named defect classes - n8"]
    B["and it overturned a claim<br/>in this brain"]

    I --> N --> D --> L --> B

    style D fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d
    style B fill:#e8f0fc,stroke:#4338ca,color:#312e81
```

This is a necessity diagram, not a feature description, and the arithmetic in the first two boxes is
what makes lint non-optional. **The crux is that drift here is not a failure mode to be avoided but a
guaranteed output of the write pattern, so the design is only honest because it ships the repair pass
alongside.** It is drawn as a forced chain because each step follows from the one before with no
judgement involved: wide writes plus no review equals accumulated unreviewed change. The out-of-band
property matters more than it looks, since a lint that runs inside an ingest would be grading work it
had just done, which is the conflict of interest this brain records elsewhere as claim 34.

*Synthesized from `n8` and `n17`.*


> "**Periodically**, ask the LLM to health-check the wiki. Look for: contradictions between pages,
> stale claims that newer sources have superseded, orphan pages with no inbound links, important
> concepts mentioned but lacking their own page, missing cross-references, data gaps that could be
> filled with a web search." (`n8`, §Operations - Lint)

**Two words carry the design.** "**Periodically**" and "**ask**": it is neither a step of ingest nor a
daemon, but a **separately invoked operation on its own clock**. And it enumerates **six defect
classes**, which is unusual precision for a document this abstract.

This is where the source did real work on this brain, and the story is worth telling because the error
is repeatable.

[ADR-0009](../../brain/decisions/0009-dreaming-reconciliation-pass.md) **cited this gist before it had
been ingested**, and said the kit already had all three operations - that what the gist lacked was an
out-of-band maintenance pass. Gated against the actual text, that breaks into three assertions:

| Assertion | Verdict |
|---|---|
| The gist describes raw / wiki / schema layers | **holds** (`n4`) |
| It names three operations: ingest, query, lint | **holds** (`n6`) |
| It does **not** supply the out-of-band maintenance pass | **does not hold** (`n8`) |

**§Lint *is* the maintenance pass.** Four of its six defect classes are verbatim members of this kit's
dream stage - contradictions, stale claims superseded by newer sources, orphans, missing
cross-references. A fifth is the topic-creation call the architect persona owns; the sixth is the
deep-research trigger.

**How the prior reading went wrong is the transferable part:** it matched the *word* "lint" to
`validate.py`, concluded the operation was already covered, and moved on. **`validate.py` shares
nothing with §Lint but the name** - it checks *form*, and every item on Karpathy's list is a
*judgement*. Corrected in [ADR-0010](../../brain/decisions/0010-lint-is-the-dream-pass.md).

> **Why this matters beyond the bookkeeping.** It is a claim that was **wrong the day it was written**,
> in a file nothing re-reads, and it survived until someone ingested the source it was about. That
> names where drift actually comes from in a system like this: **claims made *about* sources that have
> not been ingested yet.**

The operations are complete. What about finding anything?

## Movement D - navigation, scale, and where the argument overreaches

```mermaid
flowchart TB
    S8["8. split the catalog from the log<br/><i>opposite requirements on the same bytes</i> - n9"]
    S9["9. defer search infrastructure<br/>until the index breaks - n10"]
    S10["10. Memex 1945: the pattern was blocked<br/>for eighty years on who does<br/>the bookkeeping - n15"]
    A["so the LLM's contribution is<br/><b>economic</b>, not intellectual"]
    W["and the one number offered - '~100 sources' -<br/>is assertion, contradicted by the gist's<br/>own operations section - n10, d1"]

    S8 --> S9 --> W
    S10 --> A
    S9 --> A

    style W fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d
    style A fill:#dcfce7,stroke:#15803d,color:#14532d
```

This is a claim-strength diagram, not a summary, and the two terminal boxes are the reason this
movement is marked as the one to read carefully. **The crux is that the strongest and the weakest
claims in the gist sit side by side in the same movement, and nothing in the text distinguishes
them.** The Memex framing is well supported and reframes the whole pattern as a labour-economics
result. The "~100 sources" threshold is a bare number with no measurement behind it, and it disagrees
with the document's own description of how ingest works. Drawing them as separate terminals is the
point, since a reader taking the movement as one block will carry the number with the same confidence
as the history.

*Synthesized from `n9`, `n10`, `n15` and divergence `d1`.*

### 8. Split the catalog from the log

Two files, two jobs, and the reason to keep them apart is sharper than it first appears (`n9`,
§Indexing and logging).

| | `index.md` | `log.md` |
|---|---|---|
| Oriented by | **content** - what exists | **time** - what happened |
| Shape | a catalog: link, one-line summary, optional metadata | append-only entries |
| Written | rewritten on every ingest | appended, never edited |
| Read | **first, on every query**, to find the right pages | for history and recent activity |

**Collapse them and you get a file that is either useless as an index or lying as a log.** An index
**must** be rewritten to stay accurate; a log **must never** be rewritten to stay trustworthy. Those
are opposite requirements on the same bytes, and no amount of care reconciles them.

The small tip attached to the log is good engineering: a consistent entry prefix
(`## [2026-04-02] ingest | Article Title`) makes it parseable with
`grep "^## \[" log.md | tail -5` - **structure cheap enough that plain unix tools are the query
engine.**

Which raises the obvious scaling question: when does reading an index file stop working?

### 9. Defer the search infrastructure until the index breaks

```mermaid
flowchart TB
    S["start: no search infrastructure.<br/>An index file the model reads."]
    G["the corpus grows"]
    B{"has the index<br/>stopped working?"}
    N["no: add nothing"]
    Y["yes: <i>now</i> add retrieval"]
    C["the gist says this happens at<br/>~100 sources - n10"]
    W["that number is assertion, and it<br/>contradicts the document's own<br/>operations section - d1"]

    S --> G --> B
    B --> N --> G
    B --> Y
    C -.-> B
    W -.-> C

    style W fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d
```

This is a deferral diagram, not a scaling plan, and the loop is the recommendation. **The crux is that
the advice is sound and the threshold attached to it is not, which is an unusually clean case of a good
argument carrying a bad number.** It is drawn with the number dangling off the decision rather than
inside it, because that is exactly its status: the practice of deferring infrastructure until it is
needed stands on its own logic, and "~100" is a figure nobody measured. This brain later refined it
through external research, and the short version is that what binds is the token volume the navigation
ranges over rather than any count of sources.

*Synthesized from `n10` and divergence `d1`.*


The document's answer is its **one falsifiable, quantified claim**, and it arrives with nothing
attached:

> "This works surprisingly well at moderate scale (**~100 sources, ~hundreds of pages**) and **avoids
> the need for embedding-based RAG infrastructure**." (`n10`, §Indexing and logging)

⚠️ **Do not cite this as a result.** No eval set, no comparison against the infrastructure it says you
can skip, no definition of "works well", no account of what breaks past the ceiling, and no derivation
of the ~100. **The word "surprisingly" is doing the work a measurement should.** It is simultaneously
the most useful sentence in the document to *test* and the least safe to *repeat*.

> **It has since been tested, and the answer is in
> [`context/01`](context/01_where-the-index-file-ceiling-actually-sits.md) rather than here** - this
> section reports what the source said, and external evidence lives in `context/`. The three-line
> version: the ceiling is **real and measured twice independently**, the two measurements **agree
> with each other**, and **`n10`'s unit is wrong** - what binds is the token volume the navigation
> ranges over, not the number of sources, so the same ~100 is far too low for short notes and far too
> high for books. **Nobody has tested the design this section actually describes**, because reading a
> summary index attends to a fraction of the corpus that both studies made the model attend to.
> `n10` stays `needs-check`.

**The staged position is defensible regardless of the number**: defer search until the index stops
working, then reach for a real engine (`n11`). `qmd` is named - local, hybrid BM25/vector, LLM
re-ranking, on-device, shipping **both a CLI and an MCP server**.

> That last detail is the durable one and it is not about search. **A tool shipping both a CLI and an
> MCP server is usable by an agent two ways** - shell out to it, or bind it as a native tool - and the
> choice belongs to the harness rather than the tool. Worth noticing as an integration pattern.

Which leaves the question the document closes on, and it is the one it handles worst.

### 10. Why now: the Memex, the labour constraint, and where the argument overreaches

```mermaid
flowchart TB
    M["Memex, 1945 - Bush proposes<br/>exactly this pattern"]
    B["blocked for eighty years, and not<br/>on storage or on linking"]
    W["blocked on <b>who does the bookkeeping</b> - n15"]
    L["the LLM does the bookkeeping"]
    E["so its contribution here is<br/><b>economic</b>, not intellectual"]
    O["which is also where the argument overreaches:<br/>a labour constraint lifting is not<br/>evidence the result is good - n13"]

    M --> B --> W --> L --> E --> O

    style E fill:#dcfce7,stroke:#15803d,color:#14532d
    style O fill:#fff4e5,stroke:#b45309,color:#78350f
```

This is a lineage diagram, not a history lesson, and the payoff is the reframe in the second-to-last
box. **The crux is that the idea was never the hard part, so the LLM is not supplying insight here, it
is supplying labour at a price that makes an eighty-year-old design newly affordable.** It is drawn as
a single unbranching descent because the history genuinely runs that way and the value is in following
it to the economic conclusion rather than stopping at the citation. The amber terminal is this note's
own caution: removing the constraint that blocked a design tells you the design is now buildable, and
says nothing whatever about whether it works, which is the gap every unmeasured claim in this gist
sits in.

*Synthesized from `n13` and `n15`; the overreach reading is this brain's.*


The lineage is the most useful sentence for placing this whole idea:

> "related in spirit to Vannevar Bush's **Memex** (1945)... private, actively curated, with the
> connections between documents as valuable as the documents themselves. **The part he couldn't solve
> was who does the maintenance. The LLM handles that.**" (`n15`, §Why this works)

> 💡 **Memex** - Bush's 1945 proposal for a personal document store with associative trails between
> documents. Blocked for eighty years on **maintenance labour** rather than on storage, retrieval or
> linking.

**That reframes what the LLM contributes as economic rather than intellectual**, which is both more
modest and more interesting than "AI enables new knowledge systems". The idea was fully specified in
1945. What was missing was somebody willing to do the filing.

The supporting argument is that wikis die of bookkeeping: "**Humans abandon wikis because the
maintenance burden grows faster than the value.** LLMs don't get bored, don't forget to update a
cross-reference, and can touch 15 files in one pass. **The wiki stays maintained because the cost of
maintenance is near zero**" (`n13`, §Why this works).

⚠️ **Two sentences of that are the weakest thing in the document, and one of them contradicts the
document itself.**

- **"Near zero" is false on its face** for anyone paying per token. The cost **moved and shrank**; it
  did not vanish.
- **"LLMs don't forget to update a cross-reference" is contradicted by §Lint**, which instructs you to
  go hunting for **missing cross-references** (`d1`). Both cannot be true.

**Believe §Lint.** It is the operational section, evidently written by someone who found those
defects; §Why this works is a closing argument whose job is persuasion. **The six-item lint list is an
admission that integrate-on-ingest leaves defects behind** - which is section 5's wide write coming
due.

> **The honest version, and the one worth promoting: LLM bookkeeping is cheap enough to be worth doing
> repeatedly, not so reliable that doing it once is enough.** Weaker, and far more useful - it is the
> version that actually *implies* the third operation rather than undercutting it.

Two closing claims worth carrying, both about the document rather than the design:

- **The division of labour** hands the human **taste** and the LLM the **writing**: "You're in charge
  of sourcing, exploration, and asking the right questions. The LLM does all the grunt work" (`n14`).
  The analogy is explicit - *Obsidian is the IDE; the LLM is the programmer; the wiki is the
  codebase.* Note what that assigns the human: **reviewer and product owner, not author.**
- **The artifact is a pattern to be instantiated, not a spec** (`n16`): "intentionally abstract...
  share it with your LLM agent and work together to instantiate a version that fits your needs."
  Read as a claim about **distribution format** this is the interesting one - the unit shipped is
  neither a library nor a specification but **prose sized for an agent's context window**. It is also
  conveniently unfalsifiable: a document that specifies nothing cannot be wrong about an
  implementation.

## Diagram (mental model)

```mermaid
flowchart LR
    RAW[("Raw sources<br/>IMMUTABLE<br/>nobody writes")] -->|ingest: INTEGRATE<br/>10-15 pages touched| WIKI
    WIKI[("The wiki<br/>LLM writes<br/>you read")] -->|query| ANS["Answer"]
    ANS -.->|"filed back<br/>as a new page"| WIKI
    SCHEMA[/"Schema doc<br/>BOTH write<br/>conventions + workflow"/] -.->|"governs every<br/>operation"| WIKI
    WIKI -->|"lint: PERIODIC,<br/>out of band"| DEF{"6 defect classes<br/>contradictions, stale claims,<br/>orphans, missing pages,<br/>missing cross-refs, gaps"}
    DEF -.->|repairs| WIKI

    style WIKI fill:#cfe8cf
    style SCHEMA fill:#fbf1dc
    style RAW fill:#e8e8e8
```

**How to read it:** the three cylinders and the parallelogram are the three layers, coloured by **who
may write** - grey is immutable, green is LLM-owned, amber is co-evolved by both. Solid arrows are the
three operations; dotted arrows are the two writes that are easy to miss.

**The crux: the two dotted arrows into the wiki are what make this a compounding store rather than a
cache - answers come back in, and a periodic pass repairs what ingest broke.**

**Why it is shaped this way:** note that `lint` leaves *and re-enters* the wiki without touching raw
sources - it can only repair the derived layer, which is exactly why the immutable layer has to exist:
it is the fixed point the repair is measured against. Note too that the schema governs every operation
but is not itself an operation; it is the only box a human writes to, which makes it the sole place a
correction to *behaviour* can persist. And the ingest arrow is labelled **integrate**, not index,
because the alternative reading - ingest as a pure append - would remove the need for lint entirely and
is precisely the mistake `d1` catches the document making about itself.

*Synthesized from `n3`, `n4`, `n5`, `n7`, `n8`, `n17` - **this source contains no diagrams**, so the
structure is assembled from prose and may impose more shape than the author intended.*

## 💡 Terms

| Term | Explanation |
|---|---|
| LLM Wiki | A persistent, interlinked markdown knowledge base an LLM writes and maintains between you and your raw sources - compiled once at ingest and kept current, rather than retrieved and re-synthesized per query. |
| Query-time synthesis | Relating documents to each other *when the question arrives*. Cheap to build, paid on every question while the user waits, and discarded. The thing an LLM Wiki trades away. |
| Lint (knowledge base) | A periodic, separately invoked health check over the **whole** store, hunting contradictions, superseded claims, orphans, missing pages and missing cross-references. **Not a form checker** - every item is a judgement, which is why this kit calls its version `dream` ([ADR-0010](../../brain/decisions/0010-lint-is-the-dream-pass.md)). |
| Memex | Bush's 1945 personal document store with associative trails between documents. Blocked for eighty years on maintenance labour rather than storage or linking - which reframes the LLM's contribution as economic, not intellectual. |
| Wide write | An ingest touching 10-15 pages at once. The property that makes drift possible: fifteen unreviewed edits per source, compounding. |

## What to distrust in this note

- **Every single node is `single-leg`, and that is structural rather than a curation failure.** The
  source has no figures, no code, no data and no worked example, so neither of the kit's pairings is
  available. **Nothing here is `corroborated` and nothing may be retro-marked so later.**
- **Split the source in two before citing it.** The **pattern** half (`n1`-`n9`, `n11`-`n12`,
  `n14`-`n18`) stands on its own logic - you can follow "retrieval re-derives, so compile once"
  without trusting the author about anything. The **efficacy** half (`n10`, `n13`) has **zero
  measurement** and one of its two claims contradicts the document's own operations section.
  **Never cite the efficacy claims as results.**
- **Two things count in its favour, and neither is evidence.** **Nothing is being sold** - a personal
  gist, no product, no affiliation, and the one tool it recommends is someone else's. And it
  **declares its own epistemic status unprompted** ("intentionally abstract... describes the idea, not
  a specific implementation"). Both make it easier to gate honestly. **An unmeasured claim from a
  disinterested expert is still an unmeasured claim** - it just fails differently from a vendor's.
- **This brain is a live instance of the pattern and proves nothing about it.** It runs exactly this
  design - immutable `raw/`, an agent-written `brain/`, `AGENTS.md` as the schema, `INDEX.md` read
  first, an append-only `log.md` - at a source count **still below `n10`'s claimed ~100 ceiling**
  (see [`INDEX.md`](../../INDEX.md) for the live total; **the number was hard-coded here and went
  stale**, so it is a pointer now, matching the same fix already made in
  [`rag.md`](../../brain/topics/rag.md)). **n=1, and still inside the easy regime.** Worth saying
  before the coincidence gets mistaken for corroboration.
- **The "Background, supplied" blocks are mine** - the compile/interpret trade and its staleness cost,
  append-only-plus-derived-views and reconstructability, and the generation effect under the last open
  question. Uncited by construction.

## Open questions

- ~~**Where does index-file navigation actually break?**~~ **Researched 2026-08-15 -
  [`context/01`](context/01_where-the-index-file-ceiling-actually-sits.md), verdict `refines`.** It
  was indeed the sort of thing someone had measured: **twice, independently, and in agreement.** The
  ceiling is real, it is **denominated in tokens rather than sources**, and `n10`'s magnitude is a
  coincidence of its author's corpus size. **What replaced the question is sharper**: neither study
  tested a *summary index*, which attends to ~2k tokens where they made the model attend to ~1.5M, so
  **the design this note describes still has no measurement at all** - and its likely failure mode is
  not attention but whether a one-line summary discriminates well enough to pick the right page.
- **Why is contradiction-flagging in both ingest and lint?** `n3` puts it at ingest time and `n8` puts
  it in the periodic pass, with no account of why both are needed. The honest reading is that ingest's
  version is unreliable - which is `d1` again, and the document never says it.
- **Does the human keep their grip on knowledge they never wrote?** `n14` hands the human taste and
  the LLM the writing. **Nothing in the source addresses what a reader retains of a corpus they have
  only ever read.**

  > **Background, supplied.** The **generation effect** is a long-standing finding in memory
  > research: material you produce yourself is retained better than the same material read
  > passively. The gist never mentions it, and it is what makes this question sharp rather than
  > rhetorical - **if it transfers, then `n14`'s division of labour trades retention for throughput,
  > and the trade is invisible to the person making it**, because a wiki you can navigate feels like
  > a subject you know. **Whether it transfers to reviewing LLM-written prose is exactly what nobody
  > has tested**, so this is a hypothesis worth checking and not an answer. *(Uncited by
  > construction, and the direction is deliberately not asserted.)*
- **What does the lint pass cost, and how often is "periodically"?** It reads everything by
  construction. The gist neither budgets nor triggers it. This kit's own answer - on request,
  unbudgeted ([ADR-0009](../../brain/decisions/0009-dreaming-reconciliation-pass.md)) - is a decision,
  not a finding.
- **Does the single-writer assumption hold?** `n18` says git supplies versioning and collaboration
  free. Git gives history and attribution; it does not give **admission control or a write
  precondition**, and a single-writer design never has to find out. Compare claim 61, which says a
  second writer *requires* that machinery.

## Feeds these topics

- `../../brain/topics/rag.md` - the compiled-layer alternative to retrieval, layering by write access,
  ingest-integrates-not-indexes, queries filed back, the catalog/log split, maintenance labour as the
  binding constraint.
- `../../brain/topics/memory.md` - the periodic out-of-band reconciliation pass, and its status as the
  third and earliest proponent of the decoupled write.
- `../../brain/topics/context-engineering.md` - the contract document as the persistent counterpart to
  owning the prompt, and the two-pass text-then-images constraint.

## Presentation narrative

*A talk track for a room deciding how to build an internal knowledge base, derived entirely from the
gated nodes above. The source is a nineteen-hundred-word design argument with no figures, no code, no
data and no worked example, so this presents a diagnosis and a pattern, never a result. Every node here
is `single-leg` by construction: the document has no second leg to gate against.*

### Slide 1 - This is not the usual complaint about retrieval, and the difference decides your budget

**The familiar complaint is that retrieval returns the wrong chunks, and this one holds even when
retrieval is perfect [n1].** Ask a question that needs five documents synthesised and the model finds
and pieces the same fragments together every single time, while the user waits, and then the answer is
discarded. Nothing accumulates, so the hundredth question costs exactly what the first one did.

The test that separates the two is worth carrying out of the room. Does the problem survive a perfect
retriever? Here it does, because what is being re-paid is the relating of documents rather than the
finding of them, and relating happens after the right documents are already in hand. That matters
commercially rather than academically: better chunking, a stronger embedding model and a reranker all
genuinely improve which documents come back, and not one of them changes the moment synthesis happens.
A team can spend a year on the cheaper of the two costs without noticing.

*Visual: the TL;DR diagnosis diagram, which forks on exactly that question. Provenance: `n1`, `n2`.*

### Slide 2 - Compile once at ingest, and inherit a build step's liability along with its speed

**The idea is to move synthesis from query time to ingest time and then keep the result current
[n2].** The word compiled is meant literally, and taking it literally is what makes the rest of the
design predictable rather than a list of proposals. You get what a build step gets over an
interpreter, and you also inherit the corresponding liability, which is that a compiled artifact can be
out of date in a way a freshly interpreted one structurally cannot.

That single trade is the whole architecture. Everything after it, the layers and the operations, is a
consequence rather than an addition, which is the useful thing to tell a team evaluating this: if you
accept the compile decision, you have mostly accepted the rest.

*Visual: the section 2 analogy diagram. Provenance: `n2`.*

### Slide 3 - Once a machine writes your knowledge base, the architecture is about write access

**Layer the store by who may write to it: raw sources are immutable, the wiki is written by the LLM and
only read by you, and the schema document is the one layer both parties co-evolve [n4].** This is an
ownership diagram rather than a storage diagram, and no retrieval architecture has to answer the
question it answers, because in a retrieval system nothing writes.

What engineers should take from this is where the work actually lands. The engineering does not
disappear when you delete the vector database, it relocates into a prose document describing how the
wiki is structured [n5]. That document looks like documentation and behaves like an interface
definition, and the predictable failure is a team reading "no retrieval stack" as "less work", writing
a thin schema, and getting a wiki whose shape drifts every time the model extends it.

*Visual: the Movement B ownership diagram, with the section 4 budget-relocation diagram beside it.
Provenance: `n4`, `n5`.*

### Slide 4 - The design ships with a repair pass, and that is the honest part

**Three operations run over those layers, and the third one gives the design away.** Ingest integrates
a new source into pages that already exist rather than indexing it for later, and may weaken the
synthesis already written [n3]. Query files good answers back into the wiki as new pages, which makes
questions an input of the same standing as sources [n7]. Lint is a periodic pass, invoked out of band,
hunting six named defect classes [n8].

The arithmetic behind the third one is the part to state plainly. An ingest is a wide write touching
ten to fifteen pages at once [n17], and nobody reviews fifteen edits per source, so drift is not a risk
to be managed but a guaranteed output of the write pattern. A store that needed no repair would never
have earned a lint pass. The out-of-band property matters more than it looks: a lint running inside an
ingest would be grading work it had just done, which is the conflict of interest this brain records
separately as claim 34.

*Visual: the Movement C admission diagram, with the section 7 necessity diagram. Provenance: `n3`,
`n7`, `n8`, `n17`.*

### Slide 5 - The pattern is eighty years old and was blocked on labour, not on ideas

**The gist places itself as Vannevar Bush's Memex from 1945, a design blocked for eighty years not on
storage and not on linking but on who does the bookkeeping [n15].** That reframe is the strongest
thing in the source and it changes what the LLM is contributing here. It is not supplying the insight,
which has been published since before computers. It is supplying labour at a price that makes an
old design newly affordable.

The leadership significance is that this is an economics argument, so it should be evaluated as one.
The question is not whether the pattern is clever. It is whether the maintenance cost, now paid in
tokens rather than in librarians, stays below the value of having synthesis already done. And the
caution belongs in the same breath: a constraint lifting tells you a design is buildable and says
nothing whatever about whether it works.

*Visual: the section 10 lineage diagram. Provenance: `n13`, `n15`.*

### Slide 6 - Take the pattern, leave the numbers, and note that nothing here was measured

**This is one practitioner writing about a workflow he already prefers, with no eval, no baseline and
no comparison against the retrieval systems the gist opens by dismissing.** Its two efficacy claims are
pure assertion, and one of them contradicts the document's own operations section [d1].

I want to give the source its due, because one thing about it is genuinely unusual in this brain:
nothing is being sold. There is no product, no vendor position and no commercial interest pointing the
argument anywhere. That is rarer than it sounds and it is why the diagnosis is worth taking seriously.
It also changes nothing about the evidence, because an unmeasured claim from a disinterested expert is
still unmeasured.

So the verdict is adopt the diagnosis, pilot the pattern, and discard the one number on offer. The
"~100 sources" threshold in particular should not be quoted [n10]. This brain later researched it
externally, and what binds turns out to be the token volume the navigation ranges over rather than any
count of sources, which makes the figure far too low for short notes and far too high for books.

*Visual: the Movement D claim-strength diagram, where the best and worst claims in the gist sit side by
side. Provenance: `n10`, `d1`.*

### Key takeaway message

Retrieval re-pays the cost of relating documents on every question and keeps none of it, and that
problem survives a perfect retriever, which is why better chunking never touches it. The alternative is
to compile the synthesis once at ingest and maintain it, accepting a build step's liability along with
its speed: the artifact can now go stale. Layer the store by who may write, put the engineering into
the schema document rather than the retrieval stack, and ship the repair pass, because wide writes with
no review make drift arithmetic rather than risk. The pattern is Bush's Memex and it was always blocked
on labour rather than on ideas, so what changed is a price. None of it is measured, so adopt the
diagnosis and treat the single number in the document as the assertion it is.
