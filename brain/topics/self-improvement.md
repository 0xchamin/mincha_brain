# Topic: Self-improvement

**Status:** emerging (1 source - **S14** Stanford CS329A lecture 1), created 2026-08-04 by
[ADR-0018](../decisions/0018-self-improvement-topic.md).
**Basis:** one source, and it is **lecture 1 of a university course** - a survey by two researchers
who work on the subject. That makes it a strong authority on *vocabulary and structure* and a weak
one on *findings*, and this note is written to that split. The taxonomy claims are trustworthy; the
two numeric claims are labelled and one of them carries a recorded divergence against its own slide.
**Cross-referenced with [`autonomous-research-loops.md`](autonomous-research-loops.md), deliberately
not merged** - they are the same loop shape at different layers, and the merge-back trigger is in
ADR-0018.

> Living, cross-source synthesis on **systems that improve themselves from their own output**. Many
> sources feed this note; **merge and de-duplicate** as they arrive (architect persona). Every claim
> cited.

## What this covers

The loop by which a model gets better from output it generated itself: sampling many candidates
rather than one, selecting among them, and feeding the survivors back as training data. Around that
sit the decomposition that makes the loop legible (**coverage** against **precision**), the scaling
behaviour that makes it affordable (test-time compute as an axis), and the constraint that decides
where the loop can run at all (**verification availability**). The field's own decomposition of
"self-improvement techniques" is four items - verifiers, feedback, RL, and search - which is a
decomposition by *where the improvement signal comes from* [S14 `n11`, figure-only].

**Adjacent, and deliberately not re-homed here** - these live in `evals`, `agents` and
`autonomous-research-loops` and are cross-referenced rather than restated: claim 34 (do not let the
producer grade its own work), claim 113 (a protected metric reaching the decision through editable
code), claim 114 (an accept rule with no variance handling banks noise), claim 12 (micro agents
inside deterministic code), claim 59 (one loop, one objective).

## Synthesis

### Self-improvement is loop closure, not a technique

The organising finding, and the reason the topic exists. Take the ordinary training pipeline -
pre-training, then fine-tuning, then inference - and add exactly one arrow running from inference
back into fine-tuning. That single addition converts a sequence into a cycle, and the cycle is what
the phrase "self-improving" denotes [S14 `n5`, `frame_1712`]. The lecture identifies it as what
DeepSeek-R1 and the frontier reasoning models are doing, and names it "the self-improving piece".

The mechanism is plainer than the name. Sample the model many times on a problem whose answer is
known but whose worked solution is not, filter to the attempts that reached the right answer, and
fine-tune on those traces. They are training data that did not exist minutes earlier and that no
human wrote. The model's *first* sample then improves, which is why the coverage/pass@1 distinction
below is load-bearing rather than pedantic.

**What makes the loop possible is that a model contains far more capability than one sample
reveals.** Sampled enough times, Llama-3-8B clears GPT-4o's single-attempt score on four reasoning
benchmarks [S14 `n2`]. **Read that with its caveat attached, always** - see the fine print below.

### The decomposition that makes all of it legible

The most portable thing in the topic so far, and it survives independent of any benchmark number.
Generate-and-select splits into two separately hard, separately named problems [S14 `n4`,
`frame_1206`]:

1. **Coverage** - can a correct solution be generated at all? Measured as pass@k, meaning whether
   *any* of k samples was right.
2. **Precision** - can a correct solution be *identified* among the candidates? This is where
   verifiers live, and the slide names them concretely as unit tests, proof checkers and majority
   voting.

The reason to keep the two apart is that they fail for unrelated reasons and are fixed by unrelated
means. Coverage is bought with compute, and it responds to it predictably. Precision is bought with a
verifier, and no amount of compute manufactures one. **Almost every overstatement in this area comes
from reporting a coverage result as though it were a precision result**, which is exactly what S14's
own headline slide does.

### The fine print on the headline result, recorded because it is the fine print

S14's most quotable slide asserts "Models Improve Drastically with Just Repeated Sampling!" while its
y-axis plots **Coverage (pass@k)**, and two of its four panels resolve selection with an "(Oracle
Verifier)" - a selection step given the ground-truth answer, which is a research instrument and not
something deployable [S14 `n3`, `d1`]. The lecture concedes the substance in narration, noting that
on some problems perhaps three or four of ten thousand samples were correct, and the co-lecturer
draws the metric distinction explicitly. **The overstatement lives in the artifact that gets
screenshotted; the correction lives in speech that does not travel with it.**

The two panels that do *not* say "Oracle Verifier" are formal proofs and competitive code. Both come
with a real, mechanical, deployable checker. That is not a coincidence, and it is the next finding.

### Verification, not generation, is the rate limit - and it is domain-shaped

**The claim worth carrying out of this topic into any other.** A self-improving system improves at
exactly the rate its verifier can distinguish good output from bad, so **the verifier sets the
ceiling, not the generator** [S14 `n6`]. The lecture names the obstacle the generator-verifier gap
and states the economics plainly: where an automatic check exists the loop runs, and where feedback
needs a person it stalls, because human feedback does not scale.

The prediction that follows is that gains should sort by how mechanisable a correctness check is, and
S14 shows exactly that without framing it as a test. o1-preview's win rate against GPT-4o runs from
**below 50% on personal writing**, through roughly 50% on editing text, to about 60% on programming,
59% on data analysis and **72% on mathematical calculation** [S14 `n6`, `frame_2098`].

> **The causal reading is this brain's synthesis.** S14 states the domain gradient in one place and
> the verification bottleneck in another, and never joins them. What the chart establishes alone is
> that reasoning training helps unevenly by domain.

### Having a verifier is not the same as having a verifier that works

**The sharpest thing this note holds, and neither source reaches it alone.** S13's autoresearch loop
had a real, automatic, cheap verifier in a bits-per-byte comparison, and its final banked improvement
was a change of random seed, because the verifier had no notion of run-to-run variance [claim 114,
S13 `n11`]. So the ceiling claim above needs a second clause: the verifier sets the ceiling, and a
verifier can be present, mechanical and free while still being wrong in a way the loop cannot detect
from the inside.

That is a stronger statement of claim 124 than S14 supplies, and it comes from a source in a
different topic about a different layer. It is the reason ADR-0018 cross-references
[`autonomous-research-loops.md`](autonomous-research-loops.md) rather than treating the two notes as
unrelated.

### Test-time compute is a third scaling axis

Why the loop became affordable and therefore a research programme. Accuracy responds to inference
compute on the same shape previously seen only for training compute, with pass@1 on AIME rising
roughly log-linearly against test-time compute and the weights entirely fixed [S14 `n1`,
`frame_1852`]. That promotes inference spending from a diminishing-returns trick to something with a
predictable curve, which is what makes it budgetable.

> **The chart is T2 vendor promotional material** (OpenAI, about its own model, reproduced in a
> lecture) with **no absolute compute value printed on either axis**. Trust the shape of the
> relationship, which the independent repeated-sampling result corroborates. Do not read magnitudes
> off it.

There is a consequence the lecture leaves implicit and worth making explicit: if capability is partly
purchasable at serving time in small increments, then it is no longer gated solely on a training run
that costs tens of millions and belongs to whoever can afford it.

### What the field admits it does not know

Recorded because it is the honesty signal that calibrates everything above. Asked why RL produces
such a large jump when pre-training supposedly already contains the capability, S14 answers that
there is no consensus on whether RL or diverse pre-training data does the work, and adds that "that
whole loop is not completely well understood. It's like the first signs of life and it starts to get
commercialized" [S14 `n12`]. **The loop's shape is well established, its mechanism is not, and
commercial systems ship on it.** That is why claim 122 is gated on the architecture rather than on
efficacy.

## Key claims

| Claim | Sources (cited) | Confidence |
|---|---|---|
| **120** - Generate-and-select decomposes into coverage (can a correct solution be generated?) and precision (can it be identified?), and the two fail for unrelated reasons | S14 (`n4`, `frame_1206`) | corroborated (slide + narration) |
| **121** - Repeated sampling lets a small model clear a much larger model's single attempt - **measured as coverage, with an oracle on half the benchmarks** | S14 (`n2`, `n3`, `d1`, `frame_1355`) | needs-check. The result is real; the slide's framing overstates it, and the presenter is the paper's senior author |
| **122** - Self-improvement is loop closure: verified test-time output becomes fine-tuning data | S14 (`n5`, `frame_1712`) | corroborated **as the stated architecture**; nothing in the source measures the loop over more than one turn (`n12`) |
| **123** - Test-time compute is a third scaling axis, raising accuracy without touching a weight | S14 (`n1`, `frame_1852`) | corroborated on the *shape*; the chart is T2 vendor material with unlabelled axes |
| **124** - **Verification, not generation, is the rate limit, and it is domain-shaped** | S14 (`n6`, `frame_2098`); the second clause from S13 (claim 114) | corroborated on the pattern. **The causal link is this brain's synthesis** |

Claims filed elsewhere from the same source: **125** and **126** in [`evals.md`](evals.md),
**127** in [`agents.md`](agents.md).

## Key visuals

- [`frame_1206`](../../sources/260804_cs329a-self-improving-agents/visuals/frame_1206.jpg) - the
  coverage/precision decomposition with verifiers named concretely. **The single most reusable frame
  in the topic** [S14 `n4`].
- [`frame_1712`](../../sources/260804_cs329a-self-improving-agents/visuals/frame_1712.jpg) - the
  ordinary training pipeline plus one arrow returning from test-time into fine-tuning. The whole
  thesis in three boxes [S14 `n5`].
- [`frame_2098`](../../sources/260804_cs329a-self-improving-agents/visuals/frame_2098.jpg) - o1
  against GPT-4o by domain, sorting almost exactly by how mechanisable the check is [S14 `n6`].

## Open questions / conflicts

- **Is the self-preference claim real, and how large?** S14 asserts that models prefer their own
  reasoning traces even to better ones from a stronger model, uncited and unmeasured [`n9`, promoted
  as claim 125 to `evals`]. **The highest-value research target this topic has**, because it would
  independently corroborate claim 34 through a different mechanism.
- **How many turns of the loop has anyone actually run?** S14 shows the architecture and no
  longitudinal result. Whether returns diminish, plateau or collapse after several rounds is the
  question that decides how much claim 122 is worth.
- **Does the domain gradient actually track verifier availability?** The correlation is visible and
  the causal claim is this brain's. A study covering domains of *intermediate* verifiability would
  settle it.
- **What happens when the verifier is model-written and wrong in the generator's direction?** Claim
  126 records the practice; nothing measures the failure.
- **What is the threat model for a system that writes its own training data?** Absent from S14's
  syllabus entirely, and adjacent to claim 106 (sharing a component converts a structural guarantee
  into an enforcement obligation).
- **Where is the boundary with [`autonomous-research-loops.md`](autonomous-research-loops.md)?**
  Currently: that note changes an artifact, this one changes the model. Re-test on the next source
  that lands claims in both (ADR-0018's merge-back trigger).

## Sources feeding this topic

- **S14** - [Stanford CS329A: Self-Improving AI Agents, lecture 1](../../sources/260804_cs329a-self-improving-agents/LEARNING.md)
  (video, 2026-08-03). T4 lecture presenting T3 preprints and T2 vendor charts. The course overview,
  so a map rather than a result.
