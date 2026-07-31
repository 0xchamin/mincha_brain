# ADR 0007: Memory gets its own topic note

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260731 |
| Deciders | chamin |

## Context

Ingesting S6 ([Dreaming: Better memory for a more helpful ChatGPT](../../sources/260731_chatgpt-memory-dreaming/LEARNING.md),
OpenAI, 2026-06-04) produced 11 gated nodes about **what persists between sessions and who maintains
it**: staleness as a structural property of write-once stores (`n1`), background synthesis decoupled
from the conversation turn (`n3`), revision instead of expiry (`n5`), representation as a maintenance
decision (`n4`), correction on the synthesized artifact (`n6`), and a three-objective evaluation frame
(`n7`).

Three existing notes had a plausible claim on this material, and the tension is real rather than
bookkeeping:

- [`context-engineering.md`](../topics/context-engineering.md) is the strongest competitor. Its own
  claim 20 - "prompt, memory, RAG and history are one problem" - **explicitly absorbs memory**, and it
  already carries a memory finding from R1 (naive episodic scaffolds hurt 6 of 10 models).
- [`rag.md`](../topics/rag.md) (seed, 0 sources) covers retrieval, and memory retrieval is retrieval.
- [`agents.md`](../topics/agents.md) covers agent architecture generally.

`AGENTS.md` warns against spawning a topic per source, and this is a single source. It also requires
capturing a recognisable, reusable area rather than forcing a bad fit.

## Decision

**Create `brain/topics/memory.md`, Status `emerging`.**

The boundary that justifies it: **context engineering owns which tokens reach the model in one call;
memory owns what persists between calls and who maintains it.** Claim 20 is right that memory *feeds*
the context problem - but S6's content is almost entirely about the **maintenance** of a durable
artifact (when the write happens, what shape it takes so revision is expressible, who repairs it,
how you tell it is still true). None of that is a question about token budget, and filing it under
context engineering would bury it under a claim that treats memory as one input among four.

Against `rag.md`, the distinction is authorship: **RAG retrieves a corpus someone else wrote; memory
retrieves a corpus the system wrote about its user.** That is why memory can be *wrong* in a way a
document store cannot - a retrieved document is stale as a document, a memory is stale as a belief.
That failure mode is the entire subject of S6 and has no RAG analogue.

**Not a one-way door.** One source, one note, three cross-links. If a second memory source lands and
turns out to be about retrieval strategy rather than maintenance, merging into `rag.md` costs one
edit.

## Alternatives considered

- **Fold into `context-engineering.md`** - the closest call, and rejected on scope rather than
  relevance. That note is already the longest in the brain (~250 lines, 4 sources) and OQ3 flags it as
  the likeliest split candidate; adding a maintenance sub-discipline to a token-budget note makes the
  split harder later, not easier. It also inverts the dependency: memory is an input to context
  engineering, so nesting it there implies the reverse.
- **Fold into `rag.md`** - rejected. Filing a first source under a seed topic it does not match would
  have made `rag.md` `emerging` on evidence about neither chunking, embeddings nor retrieval quality,
  which is worse than leaving the seed empty.
- **Park under `agents.md`** - rejected. `agents.md` is at 4 sources and covers agent *architecture*;
  S6 is not about agents at all (it is a consumer chat assistant), and the material would read as an
  aside in a note about loops and control flow.
- **Wait for a second source before creating the note** - rejected on a specific ground: a second
  source is already captured on disk
  ([`staging/260731_anthropic-memory-and-dreaming`](../../staging/README.md),
  an Anthropic talk on memory and dreaming in Claude Managed Agents), so the recurrence test
  `AGENTS.md` asks for is already met in substance. Creating the note now means that source merges
  into a structure rather than triggering a restructure.

## Consequences

- **Easier:** the second memory source has somewhere to land, and the agent-platform framing (shared
  memory across agents, memory as a tool-accessible file system) has a home that the consumer framing
  does not crowd out.
- **Harder:** three notes now have adjacent scope, and the memory/context-engineering line will need
  policing. The rule to apply: **a claim about which tokens win a budget goes to context engineering;
  a claim about what is stored, when it is rewritten, and who fixes it goes here.**
- **Recorded honestly:** the note ships with **zero measurements** - S6's eval charts did not survive
  capture - and with an unresolved tension against claim 24, whose measured evidence says naive memory
  scaffolds hurt. The note states both rather than resolving them in the vendor's favour.
- **Revisit when:** the parked Anthropic source is distilled (which should take `memory` to
  `established` and will test whether the maintenance-vs-retrieval boundary holds), or if `rag.md`
  gains sources and starts duplicating retrieval claims (same watch item ADR-0001 set for
  context engineering).
- **Follow-up edits:** a Topics row in the root [`INDEX.md`](../../INDEX.md); cross-links added to
  [`context-engineering.md`](../topics/context-engineering.md) and [`evals.md`](../topics/evals.md);
  claims 48-55 in [`claims.md`](../claims.md); 5 terms in [`glossary.md`](../glossary.md).
