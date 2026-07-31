# Topic: Evals

**Status:** established (3 sources - S1 Uber closed-loop evals, S4 Anthropic harness design, S5
Google DeepMind skill evals).
**Basis:** all three independently arrive at *an independent checking stage that can fail the work* -
S1's Swiss-cheese QA gates on a production pipeline, S4's evaluator agent with hard thresholds on a
build loop, and S5's CI gate that blocks a skill diff from merging without proof of lift. **S5 is the
strongest instance**: a hard merge gate is the only one of the three that a human cannot wave
through. S4's other eval claims are new and `single-leg`.

> Living, cross-source synthesis on **evaluating LLM / agent systems** - how you measure, gate, and
> continuously align an agent pipeline in production. Many sources feed this note; **merge and
> de-duplicate** as they arrive (architect persona). Every claim cited.
>
> New topic created 2026-07-25 from the Uber closed-loop-evals talk. `emerging` until a second
> source corroborates.

## What this covers

Production evaluation of agent pipelines: per-stage metrics (routers as classifiers, generation via
pass@k and pairwise comparison), layered QA gates, golden datasets and human alignment, and
**closed-loop / self-tuning** systems that detect drift and auto-tune without a human editing
prompts.

## Synthesis

An agent "product" is a **routed pipeline of small agents**, and evals attach **per stage** rather
than to the system as a whole - each stage gets the metric that fits its job. The precondition for
any of it is **logging first**: one flat end-to-end trace, or there is nothing to optimize and no
self-learning loop to build [S1 `&t=418s`]. From there:

- **Route** decisions are a classification problem - eval with a confusion matrix and
  precision/recall; a multi-branch router generalizes to an n x n matrix. The **guardrail metric is
  recall** so nothing bad slips through [S1 `&t=459s`, `&t=578s`]. Watch both failure modes:
  **precision miss** (over-processing a good input wastes compute and risks degrading it) and
  **recall miss** (approving a bad input, which lets a downstream model hallucinate to fit the
  description) [S1 `&t=588s`].
- **Generation / editing** is evaluated **iteratively**: a multi-dimensional QA gate explains *why*
  it failed, that reasoning is fed back to rewrite the prompt, and it retries - the metric is
  **pass@k** (pass rate at the k-th try), which climbs as feedback accumulates [S1 `&t=850s`]. For
  edit tasks, **pairwise comparison** (output vs input: faithful? complete? natural? did anything
  regress?) yields yes/no/unsure [S1 `&t=896s`].
- **Redundancy is deliberate**: stack QA gates as a **Swiss-cheese model** - a final holistic
  publish-ready gate catches what upstream missed [S1 `&t=1082s`].
- **Close the loop**: sample production traffic, re-label against the same objective guidelines,
  **diagnose** which agent drifted, **auto-tune** its config, benchmark against the golden set, and
  ship a new version - config-driven, no human in the loop [S1 `&t=650s`]. Alignment is layered
  across **three feedback loops** (model / dogfooding / marketplace) operating at different
  timescales [S1 `&t=1103s`].

> ⚠️ Confidence: single source, `emerging`. Two agreeing legs (slide + narration) show the talk is
> **internally consistent**, not that these practices are externally validated. Needs a second
> source.

## Key claims

| Claim | Sources (cited) | Confidence |
|---|---|---|
| Log the full flat trace first - it is the precondition for evals and any self-learning loop. | S1 `&t=418s` (slide `frame_1058` + narration) | emerging |
| Eval a router as a classifier (confusion matrix, precision/recall); guardrail metric = recall. | S1 `&t=459s`, `&t=578s` | emerging |
| Two router failure modes: precision miss (over-process good input) and recall miss (approve bad input -> hallucination risk). | S1 `&t=588s` (slide `frame_583` + narration) | emerging |
| Generation evals are iterative: QA feedback -> prompt rewrite -> retry; measure pass@k. | S1 `&t=850s` (slide `frame_850` + narration) | emerging |
| Editing tasks: eval by pairwise comparison (better than input? faithful/complete/natural? regressions?). | S1 `&t=896s` (slide `frame_890` + narration) | emerging |
| Stack redundant QA gates (Swiss-cheese model) to keep failures out of production. | S1 `&t=1082s` | emerging |
| Close the loop with online auto-tuning on sampled+re-labeled prod data; config-driven, no human in loop. | S1 `&t=650s` (slide `frame_658` + narration) | emerging |
| Layer three feedback loops: model (drift), dogfooding (human), marketplace (A/B funnel metrics). | S1 `&t=1103s` (slide `frame_1118` + narration) | emerging |
| Human labels as golden source of truth; representative set + objective guidelines to strip bias. | S1 `&t=528s` | needs-check (single-leg) |
| **Do not let the producer grade its own work - self-evaluation bias means an agent confidently praises mediocre output it produced.** Use a separate evaluator with its own context. | S4 §1, §2 | emerging |
| **Subjective quality becomes gradable by fixing the question, not the model:** "is this beautiful?" grades inconsistently, "does this follow our design principles?" supplies criteria. Rubrics beat taste. | S4 §2, §3 | emerging |
| **Hard thresholds, not weighted averages** - any criterion below threshold fails the whole gate, so a strong score elsewhere cannot mask a specific failure. | S4 §4a | emerging |
| **The grader needs tools to perceive what it grades** (a browser via Playwright MCP to judge a running UI), and **its modality is a hard ceiling on what "quality" can mean** - a model that cannot hear cannot grade audio. | S4 §3, §4a, §5 | emerging |
| **The grader is not free: out-of-the-box models are lenient QA**, and it took several log-driven tuning rounds to make the evaluator catch subtle bugs and stop favouring AI-generated output. | S4 §4a | emerging |
| **Negotiate "done" before producing** - generator and evaluator agree acceptance criteria up front, bridging a product-language spec to something testable. | S4 §4a | emerging |
| An independent QA pass cost ~8% of a build's total spend and caught core features shipped as display-only stubs. | S4 §5 | needs-check (n=1, self-reported, vendor) |
| **A third object of evaluation: the instruction artifact.** S1 evaluates a pipeline, S4 evaluates generated output, **S5 evaluates the prompt-side asset itself** (a skill) - and does it by ablation rather than by scoring. | S5 `&t=713s` (slide `frame_720` + narration) | emerging |
| **Ablation as an eval method:** run the same suite with and without the component loaded. The delta, not the absolute score, is the verdict - 94% vs 32% means keep, 96% vs 95% means delete. | S5 `&t=713s`, `&t=1268s` | emerging |
| **Gate the diff, not the release:** evals sit alongside every skill, run on every change, and a change cannot merge unless it improves the test cases. | S5 `&t=1002s`, `&t=1019s` (slide `frame_950` + narration) | emerging (self-reported practice) |
| **Grade outcomes, not paths** - assert the task succeeded, not that the component was invoked on turn one. Invocation on turn five is still a pass. | S5 `&t=1091s`, `&t=1109s` | emerging |
| **Isolate every run in a clean workspace - agents cheat**, reading prior chats or executions to obtain content without invoking the thing under test. | S5 `&t=1109s`, `&t=1129s` (slide `frame_950` + narration) | emerging |
| **Run multiple trials per case** (up to six) and report reliability rather than a single pass/fail, because the system is non-deterministic. | S5 `&t=1146s` | needs-check (single-leg) |
| **Test across harnesses.** The same asset can pass on one agent harness and fail on another, and your users may be on the one you never tested. | S5 `&t=1163s` | needs-check (single-leg) |
| **Most asserts can be cheap regex** (correct SDK, model ID, methods, no deprecated patterns), which is what makes many trials affordable; LLM-as-judge is reserved for trace-level checks. | S5 `&t=878s`, `&t=914s` | emerging |
| **Start with 10-20 real prompts** - 5 happy-path, 5 negative/near-miss, 5 production traces. Real traces beat synthetic guesses, and a small suite beats none. | S5 `&t=628s`, `&t=645s` | emerging |

## Key visuals

![Full agent architecture with per-stage QA gates and logging](../../sources/260725_closed-loop-evals-multimodal-agent/visuals/frame_1058.jpg)
> The routed pipeline: every stage logged; two QA gates (LLM QA + publish-ready QA). S1 `&t=376s`.

![Online tuning loop focused on drift](../../sources/260725_closed-loop-evals-multimodal-agent/visuals/frame_658.jpg)
> Closed loop: live traffic -> route/verify/diagnose+tune/benchmark/ship, re-running on fresh data. S1 `&t=658s`.

## Open questions / conflicts

- pass@k retry with QA-reasoning-in-the-prompt: does pass rate always rise, or can feedback induce
  reward hacking (the "nugatory change" oversteer at S1 `&t=979s`)? **S4 supplies a related warning
  from the other end:** its generator/evaluator loop improved **non-monotonically** - a middle
  iteration was sometimes preferred to the last [S4 §3]. More loop is not uniformly more quality.
  Still needs a source that measures this rather than observing it.
- Golden-dataset construction and the reflect/synthesize optimizer internals are `single-leg`
  (narration only) - corroborate when another source covers auto-tuning.
- **The two sources evaluate different things, which limits how much they corroborate.** S1 evaluates
  a *production pipeline* against labelled data with statistical metrics (precision/recall, pass@k).
  S4 evaluates a *build in progress* against a rubric, with the evaluator acting as a QA engineer. The
  shared claim is structural (independent checker, hard gates); the methods do not transfer directly.
- **Unresolved: who grades the grader?** S4 reports the evaluator needing several tuning rounds to
  become competent [S4 §4a], with a human reading logs to judge. Neither source describes a way to
  evaluate an evaluator that does not bottom out in human review.
- **The modality ceiling is a real limit with no answer here.** S4's DAW QA could confirm audio played
  but not that it sounded good [S4 §5]. Anything needing taste, hearing, or physical interaction has
  this problem, and both sources' methods assume the grader can perceive the artifact.
- **Ablation sidesteps "who grades the grader", and it may be the more general answer.** S1 and S4
  both bottom out in a judgement of quality that needs a competent grader. S5's ablation asks a
  *comparative* question instead - is the system better **with** this component than **without** it -
  which needs only a consistent metric, not a good one [S5 `&t=713s`]. Open: how far does that
  generalise beyond components you can cleanly remove?
- **S5's numbers split into two credibility classes and should never be quoted as one.** SkillsBench
  (+16.6 pts, the length curve, the -8 to -11 pt self-generated penalty) is a public third-party
  benchmark; the CI gate and the 39.2% -> 91.6% case study are Google DeepMind reporting on itself.
- **Cross-reference, not promoted here: decomposing a fuzzy quality into objectives with different
  failure modes.** S6 splits "good memory" into three separately-evaluable objectives - carry forward
  context, follow preferences, stay current - where the second separates **recall from compliance** (a
  system can retrieve "I'm vegetarian" and still recommend a steak house) and the third fails only
  through **the passage of time**. That is the same move S4 makes on subjective quality: make it
  gradable by fixing the *question*, not by finding a better judge. Kept in
  [`memory.md`](memory.md) (claim 54) because the objectives are memory-specific; noted here because
  the *method* is not. **S6 supplies no results** - its eval charts did not survive capture - so it is
  not counted as a source feeding this topic.

## Sources feeding this topic

- **S1** - [Building Closed-Loop Evals for a Multimodal Agent at Scale](../../sources/260725_closed-loop-evals-multimodal-agent/LEARNING.md) (Uber, AI Engineer 2026) - the founding source.
- **S4** - [Harness Design for Long-Running Application Development](../../sources/260725_harness-design-long-running-apps/LEARNING.md)
  (Prithvi Rajasekaran, Anthropic Labs, 2026-03-24). **T2 vendor source, n=1 runs, visual leg
  skipped - most nodes `single-leg`.** Strongest here for the generator/evaluator split and for
  making subjective quality gradable.
- **S5** - [Don't Ship Skills Without Evals](../../sources/260726_dont-ship-skills-without-evals/LEARNING.md)
  (Philipp Schmid, Google DeepMind, AI Engineer WF 2026). **T4 talk by a T2 vendor employee.**
  Strongest here for **ablation as an eval method** and for the **CI merge gate**. See
  [`skills.md`](skills.md) for the full skill-side synthesis.
