# Topic: Self-improvement

**Status:** emerging (**2 sources / 1 independent** - **S14** and **S15**, CS329A lectures 1 and 2),
created 2026-08-04 by [ADR-0018](../decisions/0018-self-improvement-topic.md). **Both numbers are
tracked because they were expected to diverge, and on 2026-08-04 they did** - the raw count moved and
the independent count did not, exactly as the warning below predicted. **Status stays `emerging`.**
**Basis:** one source, and it is **lecture 1 of a university course** - a survey by two researchers
who work on the subject. That makes it a strong authority on *vocabulary and structure* and a weak
one on *findings*, and this note is written to that split. The taxonomy claims are trustworthy; the
two numeric claims are labelled and one of them carries a recorded divergence against its own slide.
**Cross-referenced with [`autonomous-research-loops.md`](autonomous-research-loops.md), deliberately
not merged** - they are the same loop shape at different layers, and the merge-back trigger is in
ADR-0018.

> ⚠️ **S14 is lecture 1 of a playlist, and further lectures from it do NOT advance this note's
> status.** CS329A is a multi-lecture course, so more of it is expected to arrive. Every one of those
> lectures is **the same leg wearing a different hat** under the independence rule - same two
> lecturers, same course, same academic and commercial position - and a later lecture agreeing with
> this one is **not corroboration**. Ingest them for *mechanism* (lecture 1 defers nearly everything
> to a later session), never for confidence.
>
> **So: `emerging -> established` requires a second *independent* source, not a second CS329A
> lecture.** Record additional lectures as S15, S16 and so on, and keep the **independent** source
> count separate from the raw one in the Status line above.
>
> **This trap has already been sprung once in this brain.** [`skills.md`](skills.md) went from 1 to 5
> sources while its evidence did not move at all, and that note now carries the warning as its
> headline. Written here on 2026-08-04, *before* the second lecture arrives, because the count rises
> silently and nobody re-derives this at ingest time.
>
> **It worked, same day.** S15 (lecture 2) arrived hours later and was filed under this rule with no
> re-derivation needed: raw count 1 -> 2, independent count unchanged at 1, status unchanged. **The
> note's own claims 120-124 were not re-confidenced by anything in S15**, even where lecture 2 repeats
> lecture 1 nearly verbatim. Worth recording as the mechanism working, because a warning written
> before the event is the only kind that gets obeyed.

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

### The gap has a size, and it widens exactly where you wanted the technique

S14 named the generator-verifier gap and never measured it. S15 measures it, and the number is the
reason this topic exists rather than being a footnote to `evals` [S15 `n10`, `frame_1000`].

Take repeated sampling and swap the oracle for something deployable - majority voting, a reward model
taking best-of-N, or both combined. **Every one of them plateaus after roughly ten to fifty samples**
while coverage keeps climbing for another three orders of magnitude. On Llama-3-8B against MATH the
deployable methods sit near 0.40 while coverage reaches about 0.95.

**Then notice the direction, which is the finding rather than the number.** The gap is narrow on easy
benchmarks and enormous on hard ones - roughly 0.87 against 1.0 on GSM8K, against 0.40 against 0.95 on
MATH, same model and same axes [S15 `n11`]. So the technique looks most impressive exactly where its
deployable value is lowest, which is a fair description of how it gets reported.

The mechanism underneath is arithmetic and it is the most transferable single idea in either lecture.
On the hardest problems **the correct answer appears once to three times in ten thousand samples**
[S15 `n12`]. A selector working from frequency is not merely wrong there; the right answer is
indistinguishable from noise *by the statistic it uses*. That generalises past voting to any selector
whose signal is agreement among samples, because on the problems where sampling helped most there is
by construction almost no agreement to measure.

### You can beat the gap without closing it, by not selecting at all

The most surprising result in either lecture, and the one most likely to change how someone builds
[S15 `n25`, `frame_3100`]. Every method above frames the task as **selection**: you hold k candidates
and must choose one. Framed that way the gap looks unbeatable, because choosing correctly is precisely
what nothing does reliably.

**Fusion** drops the frame. Hand a model all k candidates and ask it to write one answer informed by
all of them. That **beats oracle selection** - it scores higher than picking the single best candidate
with the answer key in hand. Under the selection frame that is impossible, which is how you know the
frame was wrong: the best single candidate is not the ceiling, because a synthesis can combine a
correct approach from one candidate with a correct calculation from another.

> **This is the least corroborated of the reusable claims here and it is gated `needs-check`.** It is
> the lecturer's own lab's result, presented to her own students, on a benchmark she does not name in
> the talk. **It is also this topic's highest-value research target**, because if it replicates the
> default architecture for sampling-based systems changes.

A second finding on the same chart is cheaper to trust and nearly as useful. As more models join the
ensemble, **random selection actively degrades** (0.457 -> 0.358) while every selection and fusion
curve rises [S15 `n27`]. The pool improves and worsens at once, which resolves as soon as you see that
the value is in the selection step and none of it is in generation.

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

**S15 gives that axis a functional form.** Coverage against sample count fits an exponentiated power
law, `c = exp(a·k^b)`, across eight model and benchmark pairs from 70M to 70B parameters [S15 `n3`,
`frame_400`], which converts an inference budget from a guess into an estimate - you can answer "how
many samples for 80% coverage" before spending anything [S15 `n4`].

**And it explains why the law exists, which is the only peer-reviewed result in either lecture (ICML
2025) and the more useful half.** Per-problem success is *exponential* in k, since
`pass_i@k = 1-(1-p)^k`, and exponentials saturate fast. A slow power law in the *average* therefore
cannot come from any single problem; it comes from the difficulty *distribution*. A heavy tail of ever
harder problems means that at every scale of k some band is just becoming reachable, and the envelope
of staggered exponentials is a power law. **The long tail is stated as necessary as well as
sufficient** [S15 `n5`, `frame_590`], which inverts what the law is evidence *about*: a power law in
average `pass@k` is a fact about your benchmark before it is a fact about your model. That inversion
is why claim 129 was filed to [`evals.md`](evals.md) rather than kept here.

### Where the axis stops paying, which S14 never said

Recorded because it **bounds claim 123 rather than supporting it**, and bounding is the one thing a
non-independent source may do. FLOPs-matched against pre-training, the gain from test-time compute
**flips sign**, and it depends on two variables rather than one [S15 `n20`, `frame_2310`]. At a low
inference-to-pre-training token ratio every difficulty band gains, hard questions included (+11.8%).
At parity, hard questions are already negative (-11.9%). At a high ratio, medium collapses to -24.3%
and hard to -37.2%.

So the accurate statement is not that test-time compute wins on easy problems. **It is a good deal in
small doses across the board and a bad deal in large doses on anything hard** - which means the regime
you would most want it for, spending heavily on your hardest problems, is the regime where it performs
worst. The lecturer adds unprompted that pre-training is paid once while test-time compute is paid per
query [S15 `n21`], a concession against interest and therefore worth weighting up.

> **The narration flattens this to "easy and medium favour test-time compute" and drops the ratio
> entirely** [S15 `d4`]. Recorded because the spoken form is the one that travels, and it licenses a
> conclusion the chart does not support.

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
| **128** - Coverage against sample count follows an exponentiated power law `c = exp(a·k^b)` from 70M to 70B parameters, making inference spend predictable in advance | S15 (`n3`, `n4`, `frame_400`) | corroborated **on the functional form**; magnitudes are the authors' own fits, and the fit degrades ~10x at 70M (`d3`) |
| **130** - **The generation-verification gap is measurable, and it widens with difficulty.** Deployable selectors plateau at 10-50 samples while coverage climbs three more orders of magnitude; ~0.87 vs 1.0 on GSM8K against ~0.40 vs ~0.95 on MATH | S15 (`n10`, `n11`, `n12`, `frame_1000`) | corroborated. **The measured form of claim 124**, and the strongest thing this topic holds |
| **131** - Test-time compute does **not** dominate pre-training; FLOPs-matched, the gain flips sign on both difficulty and the inference-to-pre-training ratio, from +27.8% to -37.2% | S15 (`n20`, `n21`, `frame_2310`) | corroborated on the chart. **Bounds claim 123 rather than supporting it**; narration is lossy (`d4`) |
| **133** - **Synthesis beats selection**: fusing all k candidates into one answer outperforms picking the best candidate with a perfect oracle | S15 (`n25`, `n26`, `n27`, `frame_3100`) | **needs-check.** Authors' own result, one unnamed benchmark. The topic's highest-value research target |

Claims filed elsewhere from the same sources: **125**, **126** and **129**, **132** in
[`evals.md`](evals.md); **127** and **134** in [`agents.md`](agents.md).

> **None of claims 128-133 corroborates 120-124, and that is deliberate.** S15 is the same two
> lecturers, the same course and the same commercial position as S14, so it may supply *mechanism* and
> may *bound* an existing claim, and it may not raise anyone's confidence. Claim 130 is the measured
> form of claim 124 by the same author; claim 131 narrows claim 123. **Both are the same voice going
> into more detail, not a second witness.**

## Key visuals

- [`frame_1206`](../../sources/260804_cs329a-self-improving-agents/visuals/frame_1206.jpg) - the
  coverage/precision decomposition with verifiers named concretely. **The single most reusable frame
  in the topic** [S14 `n4`].
- [`frame_1712`](../../sources/260804_cs329a-self-improving-agents/visuals/frame_1712.jpg) - the
  ordinary training pipeline plus one arrow returning from test-time into fine-tuning. The whole
  thesis in three boxes [S14 `n5`].
- [`frame_2098`](../../sources/260804_cs329a-self-improving-agents/visuals/frame_2098.jpg) - o1
  against GPT-4o by domain, sorting almost exactly by how mechanisable the check is [S14 `n6`].
- [`frame_1000`](../../sources/260804_cs329a-test-time-compute/visuals/frame_1000.jpg) - **the
  generation-verification gap, and the single most important frame in this topic.** Three deployable
  selectors flat while coverage climbs, across two models and two benchmarks, with the shortfall
  visibly larger on the harder one [S15 `n10`, `n11`].
- [`frame_590`](../../sources/260804_cs329a-test-time-compute/visuals/frame_590.jpg) - why the scaling
  law exists at all, factorised into per-problem exponentials and the difficulty distribution. The
  only peer-reviewed result the topic holds [S15 `n5`].
- [`frame_2310`](../../sources/260804_cs329a-test-time-compute/visuals/frame_2310.jpg) - the boundary,
  in two dimensions. Read this before quoting claim 123 to anyone [S15 `n20`].

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
  settle it. **Partially advanced by S15 and explicitly not closed** - S15 names the mechanical
  checkers (proofs, unit tests, output equivalence) and shows the gap widening where none exists
  [`n8`, `n10`], which is the mechanism the causal claim needs. It is the same lecturer, so it
  strengthens the *account* without adding a witness. **Still needs an independent source.**
- **Does fusion really beat oracle selection?** [claim 133, S15 `n25`] **The topic's highest-value
  research target as of 2026-08-04**, displacing nothing above it because it is the only open question
  here whose answer would change what someone builds tomorrow.
- **Can the scaling exponent be predicted cheaply?** S15's slide claims a method needing 2-4 orders of
  magnitude less inference compute [`n7`], **figure-only and never narrated** - the lecturer walks
  past it. If real, it makes claim 128 operational rather than retrospective.
- **Does stacking inference-time operations have a turnover point?** S15 shows depth helping and
  analogises to network depth [`n28`], which is rhetorical rather than mechanistic. Networks have a
  limit; nothing here shows where this one is.
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
- **S15** - [Stanford CS329A, lecture 2: Test-Time Compute Scaling](../../sources/260804_cs329a-test-time-compute/LEARNING.md)
  (video, 2026-08-03). **Not independent of S14** - same course, same lecturers. T4 on T3 preprints,
  three of the four authored by the presenter, plus one ICML 2025 paper which is the strongest
  citation either lecture offers. **Ingested for mechanism**: it supplies the scaling law, its cause,
  the measured gap and a way around it, all of which lecture 1 deferred.

> **A note for whoever ingests lecture 3.** S15 confirmed the playlist warning is doing real work, and
> the ingest also found something the warning did not anticipate: **the source refutes its own headline
> slide sixteen minutes later** [S15 `d1` against `n10`]. Lecture 1 had the same defect [S14 `d1`], so
> **it is a property of how this course writes slides rather than a one-off**, and it is worth
> expecting rather than rediscovering. The rule that catches it every time: check whether a chart plots
> **coverage** or **pass@1** before believing any comparison drawn on it.
