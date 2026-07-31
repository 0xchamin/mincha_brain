# ADR 0008: `memory` goes `established` on two-vendor convergence - but the evidence bar does not move

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260731 |
| Deciders | chamin |

## Context

[ADR-0007](0007-memory-topic.md) created `brain/topics/memory.md` at Status `emerging` on one source
(S6, OpenAI's *Dreaming: Better memory for a more helpful ChatGPT*), and named its own revisit
trigger: *"the parked Anthropic source is distilled (which should take `memory` to `established`)"*.

That source is now ingested as **S7** ([Memory and dreaming for self learning
agents](../../sources/260731_claude-memory-dreaming/LEARNING.md), Anthropic, 2026-05-21): 23 gated
nodes, 19 corroborated, slides plus a live product demo.

`AGENTS.md` defines `established` as **"two or more corroborating sources"**. On a literal reading
the promotion is automatic. It is worth an ADR anyway, because **the obvious reading of "corroborating"
is wrong here in a way that would quietly inflate confidence across the whole topic.**

The two sources agree to an unusual degree:

- Both ship a **background batch process** that curates memory a session wrote.
- Both **decouple it from the session** and run it on its own clock.
- Both independently named it **dreaming**.
- Both are **T2 vendors describing their own products**.

## Decision

**Promote `memory` to `established`, and record explicitly that the promotion is about the design
and not about the results.**

The topic note, `claims.md` claim 58 and the INDEX row all carry the same qualification: two
independent vendors converging on one architecture is strong evidence that **this is the natural
answer to maintaining memory across sessions**. It is **not** evidence that the architecture works.

**The independence rule is satisfied, and it buys less than it usually does.** `AGENTS.md` requires
external evidence to be independent of the original source - not the same author, organisation or
commercial interest. S6 and S7 clear that bar completely: different organisations, different
products, different system classes (consumer chat assistant vs multi-agent platform), competing
commercial interests. What they do **not** clear is disinterest. Two vendors agreeing about their
own products are two positions that happen to rhyme, and **convergence would look identical if both
designs were wrong.**

So the status advances on the axis the status actually measures - *is this a recognisable, recurring
area with more than one source?* - while the confidence column on individual claims does not move.
Claims 59-64 land at `emerging` or `needs-check`, not `corroborated`, because **only claim 58 has two
legs; the rest are S7 alone.**

## The finding that mattered more than the promotion

S7 was expected to close the topic's headline open question, inherited from claim 24: **naive
episodic append-and-retrieve memory hurt agent long-horizon reliability on 6 of 10 models (T3
preprint, measured), while S6's numbers come from a chat assistant. Nobody has measured whether a
*maintained* memory helps an *agent*.**

S7 is the first source in this brain on the right side of both axes - maintained memory, agent
platform, long-horizon, multi-agent - and **it does not close the gap.**

| | What would close it | What S7 supplies |
|---|---|---|
| System class | An agent loop on long-horizon tasks | **Yes** |
| Memory design | Maintained, not append-only | **Yes** |
| Measurement | A disclosed method on a stated eval set | **No** - three customer testimonials on a slide |

**The evidence bar moved down, not up.** S6's figures were recovered from the publisher's own chart
specs: exact numbers, undisclosed method. S7's are marketing testimonials with no baseline, no
sample size and no eval set. **A second source made the topic broader and its evidence weaker**, and
recording that is more useful than letting "97% fewer first-pass errors" or "~6x completion rate"
stand in for a result.

## Alternatives considered

- **Leave at `emerging` until something is measured.** Rejected: it conflates two different axes.
  Status tracks whether an area recurs across sources, and confidence tracks how well individual
  claims are evidenced. Freezing the status to signal weak evidence would break the meaning of every
  other topic's status, and the note already carries the evidence warning in three places.
- **Promote and treat claim 58 as external corroboration** (raising confidence on the shared
  mechanism claims). **Rejected, and this is the substantive call.** The independence rule is about
  *provenance*, not *disinterest*. Two vendors marketing competing products arrive at the same design
  for reasons that include imitation, shared talent and a shared read of the same public research -
  none of which is an experiment. Raising confidence here would launder marketing convergence into
  measurement.
- **Split multi-agent memory into its own note.** Rejected as premature at one source. S7's
  multi-agent material (scopes, optimistic concurrency, attribution, cross-agent instruction passing)
  is a genuinely distinct sub-area that a consumer assistant cannot reach, but it is one source deep.
  Recorded as the watch item below.

## Consequences

- **Easier:** the topic now covers both system classes, and the maintenance-vs-retrieval boundary
  ADR-0007 drew held without amendment - S7's material sorted cleanly into it, which is a real test
  passed.
- **Two of ADR-0007's open questions close.** Memory as a tool-accessible file system, and memory
  shared across agents, are both covered by S7. **A third only half-closes**: `content_sha256` write
  preconditions solve *concurrent writes to one file*, not *two agents learning contradictory
  things* - a distinction easy to miss and now recorded explicitly.
- **One question got worse, and is the most actionable thing here.** `memory.md` already flagged
  memory as an unexamined prompt-injection sink. S7's demo shows agents writing **imperatives** to
  their successors ("Next agent: skip dep checks") and successors complying, which supplies the
  **propagation mechanism** the security note lacked. Attribution and versioning give forensics; there
  is **no admission control**. Promoted as claim 63 and labelled commentary, since S7 never discusses
  it.
- **Harder:** the topic now carries numbers from one vendor and none from the other, so a careless
  reader could attach S6's precision to S7's architecture. The note keeps them in separate sections
  for that reason.
- **Revisit when:** any source publishes a **method** for measuring memory quality (the standing
  highest-value target); or multi-agent memory reaches a second source, at which point the split
  above should be reconsidered; or a deep-research pass makes the cognitive-science hop that both
  vendors invoke by name and neither cites.
- **Follow-up edits:** Topics row in the root [`INDEX.md`](../../INDEX.md) (Status + source count);
  Sources row for S7; claims 58-64 in [`claims.md`](../claims.md); 5 terms in
  [`glossary.md`](../glossary.md); S7 legend lines in both.
