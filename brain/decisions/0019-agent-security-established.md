# ADR 0019: `agent-security` advances to `established`, on the first genuine corroboration in the note

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260804 |
| Deciders | chamin |

## Context

[`agent-security.md`](../topics/agent-security.md) has carried an unusually explicit bar since it was
created, restated at every ingest and enforced twice against sources that looked like they should
advance it:

> **A rising source count is still not rising evidence:** no two of these corroborate each other's
> claims - they occupy different halves of this note - so the bar for `established` is unchanged: a
> second source that studies the *same* material as an existing one.

Four sources have fed it, and until today none met that bar. **S3** (OAuth/OIDC) is the delegated
authorization substrate. **S7** (Anthropic memory and dreaming) does not discuss security at all and
feeds the note only through this brain's own commentary. **S12** (GCP multi-tenant architecture) is
containment topology, entirely unmeasured. **S16** (AgentPoison, ingested 2026-08-04) is the note's
first measured attack, and it was explicitly held at `emerging` hours earlier on exactly this
reasoning, because it studies a subject none of the other three studies.

**S17** ([Greshake et al., indirect prompt injection](../../sources/260804_indirect-prompt-injection/LEARNING.md))
changes that, on one specific node rather than on a general impression.

**The corroborating pair is `n6` against S16's `n1`/`n5`/`n11`.** Both establish that **an agent's
memory is a persistent compromise surface, and that a session reset does not clear it** - and they
reach it by opposite mechanisms:

| | S16 (AgentPoison) | S17 (Greshake et al.) |
|---|---|---|
| Who writes the poison | an **external attacker** with partial write access to the store | the **agent itself**, instructed by retrieved content |
| How it is retrieved later | embedding geometry, on a triggered query | the agent reading its own notes in a fresh session |
| What survives | poisoned records at attacker-chosen coordinates | the injection, re-executed on read |
| Evidence | quantitative: ~62% ASR-r from one record | qualitative: demonstrated on a GPT-4 synthetic app |

**Independence is clean and was checked rather than assumed.** S16 is Chen, Xiang, Xiao, Song and Li
(U Chicago, UIUC, U Wisconsin, UC Berkeley, 2024). S17 is Greshake, Abdelnabi, Mishra, Endres, Holz
and Fritz (Saarland, CISPA, sequire technology, 2023). **No author overlap, no institutional overlap,
no shared funder visible, different countries, different years, and neither is a vendor.** S17
predates S16 by seventeen months, so S16 could in principle have been influenced by it; that is
ordinary citation lineage between independent groups and is not the "same leg wearing a different
hat" the independence rule excludes.

There is a second, weaker convergence worth recording but **not** relied on here. S17's `n12` (Bing
Chat filtered the chat channel and not the retrieval channel) independently confirms a bound this
brain had written as **its own commentary** against S12's claim 103, that edge filtering "sees the
request, not the assembled prompt". That is a source confirming the brain's inference rather than two
sources confirming each other, which is a different and lesser thing.

## Decision

**`agent-security` advances from `emerging` to `established`**, on five sources of which **two now
corroborate each other on the same material** (S16 and S17, on agent memory as a persistence
surface).

The Status line records **both** counts, as [`self-improvement.md`](../topics/self-improvement.md)
does: five sources, one corroborating pair. **The corroborating pair, not the source count, is what
justifies the status**, and stating it that way is what stops the next ingest from reading "five
sources" as the reason.

**This is not a one-way door.** A status can be walked back, and the note's own history includes a
Status line corrected in dream 0001.

## Alternatives considered

- **Stay `emerging` until a defence is gated.** Tempting, because the note's most useful open
  question is now "what actually defends a retrieval store" and nothing here answers it. Rejected
  because `established` is a claim about **evidential coverage of what the note asserts**, not about
  whether the topic is solved. A note can be well evidenced about a problem and hold no solution;
  conflating the two would make every security topic permanently `emerging`.
- **Stay `emerging` because S17 is qualitative.** Rejected on the same reasoning that admitted S16's
  quantitative-but-narrow evidence. The two sources are complementary in exactly the way the
  corroboration gate wants - S16 measures a narrow attack precisely, S17 demonstrates a broad class
  on real products - and requiring both to be quantitative would discard the independence that makes
  the pair valuable.
- **Advance on source count alone (five sources, all on agent security).** Rejected explicitly, and
  it is the failure this note has been guarding against since it was written. It is the
  [`skills.md`](../topics/skills.md) trap, where a note went 1 to 5 sources while its evidence did
  not move at all. **The count moving is not the reason; the pair is.**
- **Create a separate `prompt-injection` topic for S16 and S17.** Rejected under the
  "don't spawn a topic per source" rule and [ADR-0012](0012-a-mention-is-not-a-source.md). The two
  papers attack the same architecture from different angles, and splitting them would put the
  corroborating pair in two notes, destroying the very thing this ADR records. Revisit if a third
  and fourth attack source arrive and the threat material outgrows the auth and containment
  material - at which point the natural split is **threats** against **substrate**, not
  per-attack-class.

## Consequences

**Easier.** The note can now be cited as a settled body on the *threat* half. Claims 135-141 (S16)
and 142-148 (S17) are the first material here with two-source backing on the mechanism, and claim 63
completes its journey from labelled commentary, through S16's measurement, to a corroborated pair.

**Harder, and this is the real cost.** `established` invites a reader to stop checking, and the
note's evidence remains lopsided in a way the status does not convey. **Everything gated here is an
attack; nothing is a defence.** S17's mitigations survey is `single-leg`, three years old, and
explicitly names no working solution. The note carries that asymmetry in its Status line for exactly
this reason, and it must not be dropped in a later edit for brevity.

**To revisit.** If a defence source is gated and it turns out the threat claims need re-reading in
its light, this status is the first thing to re-test. The specific trigger to watch for is a source
that *measures* a defence rather than proposing one, since the whole defensive literature between
2023 and 2026 is currently ungated here.

**Follow-up edits made in the same pass:** the Status line and synthesis in
[`agent-security.md`](../topics/agent-security.md), the Topics row in the root
[`INDEX.md`](../../INDEX.md), and a dated line in [`log.md`](../log.md).
