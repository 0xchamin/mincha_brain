# ADR 0014: No new topic for organisational context - it is context engineering with a different corpus

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260802 |
| Deciders | chamin |

## Context

**S11** ([How we built LangChain's agent-first data
stack](../../sources/260802_agent-data-stack/LEARNING.md), 2026-07-27) is the first source in this
brain whose subject is **an agent reading a company's own proprietary knowledge** - metric
definitions, business rules, which dashboard is canonical - rather than reading a codebase, a tool
catalog, or its own memory.

That is a genuinely new corpus, and it came with a vocabulary the existing notes do not use: semantic
layers, data contracts, endorsements, dbt models, workspace guides. The deep-research pass
([R2](../../sources/260802_agent-data-stack/context/01_data-agent-accuracy-and-prior-art.md)) added
more: knowledge engineering, the knowledge acquisition bottleneck, authority control. A recognizable,
reusable area with an established name in an older discipline is exactly what `AGENTS.md` §"Scope:
topics are open" says to capture as a new topic.

So the question was real: does **`organisational-context`** (or `knowledge-engineering`, or
`data-context`) deserve its own note?

Against it stands the counter-rule in the same section - **"don't spawn a topic per source"** - and
the fact that S11's claims, once stripped of their domain vocabulary, kept landing in notes that
already existed.

## Decision

**No new topic.** S11's claims are distributed across three existing notes:

| Claims | Note | Why it fits |
|---|---|---|
| 91, 92, 93, 97, 99 | [`context-engineering.md`](../topics/context-engineering.md) | All five are about **which tokens reach the model and how they are shaped** - the note's stated scope. Claim 93 in particular *completes* an existing three-source pattern rather than starting a new one |
| 95, 96, 98 | [`rag.md`](../topics/rag.md) | Trust signals rank retrieval candidates; the query log is a source-selection signal; the labour claim extends claim 72, which already lives there |
| 94, 100 | [`evals.md`](../topics/evals.md) | Both are claims about **measurement**, not about data |

**The deciding argument: nothing in S11 is specific to data.** Re-read claim 92 with "table" replaced
by "API endpoint", or claim 95 with "dashboard" replaced by "internal wiki page", and both hold
unchanged. The five-store decomposition is a way to organise *any* proprietary context an agent must
read. **A new note would have collected the domain vocabulary while the transferable claims stayed
elsewhere** - which is the worst outcome, because the vocabulary is the disposable half.

**This is not a one-way door.** Opening the note later costs three cut-and-pastes and an INDEX row.

## Alternatives considered

- **Create `organisational-context.md`.** Rejected on the "one topic per source" guardrail, and
  because every claim already had a better home. It would have started life with one source, one
  vendor, no measurements, and heavy overlap with two established notes - and
  [`rag.md`](../topics/rag.md) already carries a standing watch item about overlapping with
  `context-engineering.md`. Adding a third note that straddles both would make that worse.
- **Create `knowledge-engineering.md`** on the strength of the R2 F5 hop. Rejected as **premature and
  backwards**: the hop is real and valuable, but it arrived from a *research pass on one source*, not
  from a source about knowledge engineering. Promoting a research finding into a topic would invert
  the evidence order this kit runs on. It is recorded as claim 98 in `rag.md`, where it strengthens
  claim 72.
- **File everything under `rag.md`.** Rejected because S11's context layer is not retrieved in the
  RAG sense - four of its five stores are *resident* context assembled per query by the agent's host,
  and the note would have had to redefine its own scope to absorb them.
- **File everything under `agents.md`.** Rejected: S11 says nothing about the loop, control flow,
  tools or orchestration. It was listed as a topic on the source folder during ingest and **removed
  before compounding** for exactly this reason.

## Consequences

- **Easier:** claim 93 now reads as a three-source pattern in one place, which is the strongest
  claim S11 produced and would have been split across two notes otherwise. Claim 99 (the head/tail
  inversion) only works because S10 and S11 sit in the same note.
- **Harder:** `context-engineering.md` grows again - it is now 6 sources and the longest note in the
  brain. **This is the note to watch for a split**, and the natural seam if one is ever needed is
  *authoring* context (prompts, definitions, contract documents) versus *managing* it at runtime
  (compaction, middleware, budgets). Not yet: the seam is not load-bearing while the same claims
  inform both.
- **`skills.md`** gained an S11 row but no claims, and its stale "1 source" status line was corrected
  to 4 in the same pass. **Note the trap that correction guards against:** the count rose from 1 to 4
  while the evidence did not move at all, because S7, S9 and S11 each contribute one peripheral
  observation and none studies skills. The status line now says so explicitly.

**Revisit when:** a **second** source arrives whose subject is an agent over a company's proprietary
non-code knowledge - a data-catalog, enterprise-search or internal-documentation source. At two
sources the vocabulary starts to corroborate rather than merely accumulate, and the split argument
becomes real. Until then, the claims are where a reader will look for them.
