# ADR 0023: No topic for agent runtime operations - the trigger that would create one

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260814 |
| Deciders | chamin |
| Persona | architect |

## Context

S24 ([Hermes Agent Architecture Part 1](../../sources/260814_hermes-agent-architecture-p1/LEARNING.md))
teaches a recognizable area that no note in this brain covers. Its subject is the **operational
runtime** of an agent rather than the shape of its loop: routing identity against conversation
identity, what is durable and what is not, mutual exclusion across processes, at-least-once delivery
against exactly-once, side-effect ordering under parallel tool dispatch, and failure boundaries with
per-boundary recovery.

That material is genuinely distinct from what the existing notes hold. [`agents.md`](../topics/agents.md)
covers the loop, tool use, state and pause/resume, and it argues those from reliability. It has nothing
on delivery semantics, nothing on idempotency, and nothing on the process-locality of a guard.
[`evals.md`](../topics/evals.md) covers offline measurement and says almost nothing about what a
running system must emit. So the question is real rather than manufactured: **does this earn
`brain/topics/agent-runtime-operations.md`?**

Two facts pull against each other. The area is clearly reusable, since every one of claims 184, 187,
189, 190, 191 and 195 survives losing the product name entirely, and none of them is a fact about
Hermes. But there is exactly **one** source, and `AGENTS.md` is explicit that a topic per source is the
failure mode to avoid: *"park a one-off under the nearest topic and promote it to its own note only
once it recurs or is clearly distinct."*

There is also a specific trap this brain has already fallen into and documented. [ADR-0014](0014-no-topic-for-organisational-context.md)
records declining a topic for organisational context, and [`skills.md`](../topics/skills.md) carries the
warning that its source count rose from 1 to 5 while its evidence did not move at all. A new note
created on one unmeasured T4 blog would start at `emerging` and would look, from the INDEX, exactly
like a topic with real backing.

## Decision

**Do not create the topic.** Park S24's material under the nearest existing notes, split by what each
claim is actually about:

- [`agents.md`](../topics/agents.md) takes the runtime half as a new synthesis section - claims 184,
  187, 189, 191, 195.
- [`agent-security.md`](../topics/agent-security.md) takes claims 185, 188, 192 and the S19
  identification, claim 196.
- [`context-engineering.md`](../topics/context-engineering.md) takes claim 186.
- [`evals.md`](../topics/evals.md) takes the operational-evidence claims 190, 193, 194.

**Record the trigger explicitly**, because the reason this is a close call is that the *next* source
could settle it. Create `brain/topics/agent-runtime-operations.md` when **either** of the following
holds:

1. **A second independent source teaches agent delivery, idempotency or runtime-state semantics** -
   not merely mentions them. Under [ADR-0012](0012-a-mention-is-not-a-source.md) a mention does not
   count, and under [ADR-0015](0015-an-architecture-is-not-an-identity-source.md) a source qualifies by
   **teaching within** the scope rather than by **depending on** it. Parts 2 and 4 of this same series
   would **not** qualify, because they are the same author on the same system.
2. **`agents.md`'s runtime section outgrows its host** - concretely, when it exceeds roughly a third of
   that note or when a reader looking for delivery semantics would not think to open a note titled
   "Agents".

## Consequences

**What this costs.** The material is less findable than it would be under its own name. A reader
looking for "how do I make agent delivery idempotent" has to know to open `agents.md`, and the INDEX
annotation now has to carry that pointer explicitly. This is accepted, and the INDEX row was written to
mitigate it.

**What it buys.** The taxonomy does not gain a note backed by one unmeasured blog post, and the
existing notes gain the connective tissue instead. Claim 188 sits **inside** `agent-security.md`'s
defence discussion where it functions as the premise under S18 and S20, and it would have been weaker
stranded in a runtime note. Claim 186 sits beside the two other arguments for the same discipline,
where the comparison between them is the interesting part.

**What to watch.** The honest risk in this decision is the opposite of ADR-0014's. There, the danger
was a topic inflating on mentions. Here the danger is a **real** area staying invisible because its
first source happened to arrive alone, and the runtime layer is one this brain has demonstrably
under-covered - twenty-four sources in, S24 is the first to work it at all. **Revisit on the next
source that touches it, rather than waiting to be asked.**

## Related

- [ADR-0012](0012-a-mention-is-not-a-source.md) - a mention is not a source.
- [ADR-0014](0014-no-topic-for-organisational-context.md) - the closest precedent, same call.
- [ADR-0015](0015-an-architecture-is-not-an-identity-source.md) - teaching within the scope, not
  depending on it.
- [ADR-0017](0017-autonomous-research-loops-topic.md) - the contrasting case, where a topic **was**
  created on one source because the area was clearly distinct and the merge-back trigger was recorded.
