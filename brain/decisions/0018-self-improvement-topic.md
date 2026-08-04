# ADR 0018: a topic for self-improvement, and why it is not `autonomous-research-loops` or `inferencing`

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260804 |
| Deciders | chamin |

## Context

S14 ([Stanford CS329A lecture 1](../../sources/260804_cs329a-self-improving-agents/LEARNING.md)) is
the brain's first source on **a model improving itself from its own verified output**. Its gated
claims are about a loop: sample the model many times, select the outputs that survive a check, feed
those back as training data, repeat (`n5`). Around that sit the decomposition that makes the loop
legible (coverage against precision, `n4`), the scaling behaviour that makes it affordable (`n1`),
and the constraint that decides where it can run at all (verification availability, `n6`).

The kit's standing guidance pushes against new topics, and three ADRs have declined one on that
basis ([0013](0013-secondary-but-substantial.md),
[0014](0014-no-topic-for-organisational-context.md),
[0015](0015-an-architecture-is-not-an-identity-source.md)) against one that accepted
([0017](0017-autonomous-research-loops-topic.md)). So the question is which pile this falls into,
and there are three plausible existing homes to rule out first.

## The three candidate homes, and why each fails

**`evals` is the closest and it fails on direction.** That note is about *measuring* a system
someone built - per-stage metrics, pass@k, QA gates, ablation, and how to design a metric an
optimizer cannot game. S14's verifier is not a measurement of the loop, it is **a load-bearing
component inside it**, and the difference is consequential rather than semantic: an eval that is
wrong gives you a bad reading, while a verifier that is wrong writes its error into the next set of
weights. That said, two of S14's claims genuinely *are* eval claims and are filed there rather than
hoarded here - **claim 125** (models prefer their own reasoning traces) and **claim 126** (the
verifier increasingly written by the system it judges), both of which extend claims 34 and 113 and
are reusable well outside any self-improvement loop.

**`agents` fails on layer.** That note is about building agents, meaning the loop, the prompt, the
context, the tools, the orchestration. S14 is about the model underneath the agent getting better at
being a model. Only one of its claims is genuinely about agent construction (**claim 127**, that what
ships is still a hand-drawn static graph), and that one is filed under `agents`.

**`autonomous-research-loops` is the interesting near-miss, and the distinction is worth writing
down because a future pass will be tempted to merge them.** The two are **the same shape at
different layers**. ADR-0017's note covers an agent iterating *an artifact* unattended against an
automated metric, where the thing that changes is a training script and the loop runs on one machine
overnight. S14's loop changes **the model's own weights**, runs inside a lab's training pipeline, and
is not unattended at all. Apply ADR-0014's swap test in both directions. Swap S14's language model
for a theorem prover or a code generator and every claim survives, which is the signature of a
transferable area. Swap S14's *loop closure* for a one-shot generate-and-select pipeline and the
entire subject evaporates, which identifies the closure as the defining feature rather than an
incidental one. Filed under `autonomous-research-loops`, the coverage/precision split and the
domain-gradient argument would sit beside claims about `git reset` and wall-clock budgets and read as
someone else's subject.

## Decision

**Create `brain/topics/self-improvement.md`, Status `emerging`** (one source), covering the loop
closure, the coverage/precision decomposition, test-time compute as a scaling axis, and verification
as the rate limit. Claims 120-124 land there; 125 and 126 go to `evals`, and 127 to `agents`.

**Cross-reference `autonomous-research-loops` rather than merging.** The link is worth stating
explicitly in both notes because it is genuinely productive in one direction: **claim 124
(verification is the bottleneck and sets the ceiling) is the frame that explains claim 114** (S13's
accept rule banking a random-seed change as an improvement). S13 had a real, cheap, automatic
verifier and it still failed, because having a verifier and having a verifier that works are
different things. That is a stronger statement of 124 than S14 itself supplies, and neither note
reaches it alone.

**Merge-back trigger, written down now rather than re-derived later.** If a second primary source on
self-improvement never arrives, and the next two sources on either note keep landing claims that
could sit in both, merge the two notes under the broader name and demote the distinction to a
section heading. Do not merge on aesthetic grounds while both notes are still accumulating.

## Also decided: `inferencing` stays empty

Claim 123 (test-time compute as a third scaling axis) is about inference, and it does **not** go into
`brain/topics/inferencing.md`. That note's declared scope is *serving* - prefill and decode, the KV
cache, batching, quantization, speculative decoding, throughput against latency. Test-time scaling
buys **accuracy** rather than efficiency, and the two share a word rather than a subject. Filing it
there would misfile the claim and, worse, would make a still-empty seed note look populated. The
`inferencing` note remains at `seed` with zero sources, which is an accurate description of this
brain's coverage.

## Consequences

- One new topic note, `INDEX.md` Topics table grows to 11 rows, and the brain has its first topic
  about the model layer rather than the system layer.
- **The new note is one T4 lecture deep and says so.** It is a survey source, so the note inherits a
  taxonomy it can trust and measurements it cannot. Its headline claim (124) is corroborated
  internally, and the *causal* form of it is this brain's synthesis rather than the lecture's.
- The `evals` note reaches 6 sources and gains its second and third claims about **self-preference**,
  which is now asserted by two independent sources through different mechanisms (claim 34 from a
  vendor postmortem, claim 125 from an academic lecture) and measured by neither.
- A future dream pass should check whether `self-improvement` and `autonomous-research-loops` have
  started duplicating each other; the merge-back trigger above is the test.
