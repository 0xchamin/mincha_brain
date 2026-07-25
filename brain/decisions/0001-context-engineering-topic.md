# ADR 0001: Split "context engineering" out as its own topic

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260725 |
| Deciders | chamin |

## Context

Ingesting S2 ([12-Factor Agents](../../sources/260725_12-factor-agents/LEARNING.md)) produced a
cluster of corroborated nodes that are about **which tokens reach the model**, not about agency or
control flow: n4 (context growth is what breaks the naive loop), n8 (own your context window; model
the thread as typed events), n9 ("everything is context engineering" - prompt, memory, RAG and
history are one problem), n10 (compact errors or the agent spins out). Plus n7 (own your prompts).

Three existing notes had a claim on this material and none fit:

- `agents.md` was already the longest note and would have absorbed roughly half of S2, burying the
  agent-loop material it is actually about.
- `rag.md` is scoped to retrieval mechanics (chunking, embeddings, reranking). S2's claim is
  explicitly that RAG is *one instance* of a larger problem - filing the umbrella under one of its
  own instances inverts the hierarchy.
- A generic "prompting" note would be narrower than the material: n8 and n10 are about serialisation
  and error handling, not prompt wording.

The kit's guardrail also applies: **don't spawn a topic per source**. So the question was whether
this is a recognisable, reusable area or a one-off framing from one talk.

## Decision

**Create `brain/topics/context-engineering.md` as an `emerging` topic**, covering prompt authorship,
context-window construction and ownership, thread/event serialisation, token budget as a reliability
lever, and error compaction.

It clears the "recognisable, reusable area" bar for three reasons: it is an established term of art
in the field rather than S2's coinage; the material is **transferable** (it applies to any LLM
application, not just agents); and it is the layer most future agent, RAG and evals sources will
touch, so it will accumulate rather than sit as a stub.

Not a one-way door. If it stays thin after two or three more sources, it merges back into
`agents.md` cheaply - only the INDEX row, the cross-links in `agents.md` / `rag.md`, and the
`claims.md` topic column would change.

## Alternatives considered

- **Park it all under `agents.md`** - rejected: it makes the largest note larger and mixes two
  different questions (how the loop is structured vs what goes into the window each turn). It also
  mis-scopes the material, which applies to non-agentic LLM apps too.
- **Park it under `rag.md`** - rejected: inverts the hierarchy. S2's central claim is that retrieval
  is one technique for choosing tokens, so RAG is a child of this topic, not a parent.
- **Wait for a second source before creating it** - rejected: `emerging` status already carries
  exactly that caveat, and the note records that its single source is not independently
  corroborated. Deferring would have meant writing the claims into `agents.md` and moving them
  later, which is more churn, not less.

## Consequences

- **Easier:** "how should I build the context window / prompt / handle tool errors?" now has one
  place to land, independent of whether the caller is an agent. `agents.md` stays focused on loop,
  state and control flow.
- **Harder:** a boundary to police between this note and `rag.md`. Rule adopted: **retrieval
  mechanics -> `rag.md`; which tokens win the budget and how they are rendered -> here.** Both notes
  cross-link. Revisit if they start duplicating claims.
- **Follow-ups completed in this pass:** row added to the root `INDEX.md` Topics table (status
  `emerging`); cross-links added in `agents.md` and this note; claims registered in `claims.md`
  under topic `context-engineering`; `log.md` entry appended.
- **Revisit when:** a second source lands on this topic (promote to `established` and re-test the
  RAG boundary), or after three more sources if the note is still thin (merge back into `agents.md`).
