# Knowledge nodes - Closed-Loop Evals for a Multimodal Agent at Scale

> Persona: **fact-checker** - re-adopt when working this file.

> The atomic units of knowledge extracted from this source. Each node has a **stable ID** (`n1`..),
> a claim, **both legs each with its own citation** (or one leg marked `single-leg`), a gate
> verdict, and a confidence. Only `corroborated`/`single-leg` nodes (and recorded `divergence`
> findings) feed `LEARNING.md` and get promoted to `../../brain/`.

Video base: `https://www.youtube.com/watch?v=31GUkCBD-Uc&t=<s>s`

## Nodes

| ID | Claim (crux) | Evidence leg + citation | Corroborating leg + citation | Gate | Confidence |
|---|---|---|---|---|---|
| n1 | Log everything first: the flat end-to-end trace is the prerequisite for evals - "if you don't start with it, you have nothing to optimize for, let alone set up a self-learning loop." | narration @ `&t=418s` | `frame_1058.jpg` - architecture ends in "Logging/Traces" wired to every stage | corroborated | OK |
| n2 | The agent is a routed pipeline: Input -> Image Quality Understanding -> Routing (skip=keep original / enhance) -> Prompting -> Generation -> LLM QA (pass/fail+retry) -> Post-Processing -> Publish-Ready QA -> Menu Output. | `frame_1058.jpg` - full flowchart | narration @ `&t=314s`..`&t=376s` describes each stage | corroborated | OK |
| n3 | Evaluate a **router** like a classifier: build a confusion matrix, measure precision/recall; multi-branch routers become an n x n matrix (one cell per branch). | narration @ `&t=459s` | `frame_583.jpg` - "Routing Failures" with pass/below-bar per dimension | corroborated | OK |
| n4 | The router's **guardrail metric is recall** - optimize so no bad input slips through ("we don't want any bad image to slip through"). | narration @ `&t=578s` | `frame_222.jpg` goal "Ship safely" + `frame_583.jpg` failure framing | corroborated | OK |
| n5 | Two routing failure modes: **precision miss** (over-process a high-quality input -> pay compute for zero lift + risk degrading it) and **recall miss** (approve a bad input -> downstream model may hallucinate to match the description). | narration @ `&t=588s`..`&t=629s` | `frame_583.jpg` - "Over-Processing High-Quality Input", "Precision Miss" | corroborated | OK |
| n6 | **Human labels are the golden source of truth**; align the model to a representative labeled set (geo, dish type, quality) with objective guidelines to strip subjective bias; tune until guardrail metrics pass. | narration @ `&t=528s`..`&t=568s` | (no dedicated slide) | single-leg | needs-check |
| n7 | **Online auto-tuning for drift**: sample production traffic at a cadence -> human-label with the same guidelines -> diagnose mismatches -> auto-tune -> benchmark vs the golden set -> ship. Config-driven, no human in the loop. | `frame_658.jpg` - "Routing: Online Tuning Focused on Drift" loop (Routing/Verify/Diagnose+Tune/Benchmark/Ship, re-runs on fresh traffic) | narration @ `&t=650s`..`&t=712s` | corroborated | OK |
| n8 | The auto-tuner's **prompt optimizer is itself two sub-agents**: a *reflect* agent (find systemic issues, remove noise from mismatches) and a *synthesize* agent (rewrite the agent config from that feedback); the new version is registered in an **agent store** and picked up on the next run, with observability + quick rollback. | narration @ `&t=732s`..`&t=792s` | (no dedicated slide) | single-leg | needs-check |
| n9 | **Generation evals = iterative QA + retry**: generate an image-specific prompt -> enhance -> multi-dimensional QA gate (plating, faithfulness, colors); pass=publish, fail=push QA feedback back into the prompt and retry; measure **pass@k** (pass rate at the k-th iteration), which rises with more feedback iterations. | `frame_850.jpg` - sweet-potato-fries, QA fail (iter 1) -> QA pass (iter 2), "pass@k" | narration @ `&t=792s`..`&t=874s` | corroborated | OK |
| n10 | For editing/enhancement tasks, eval with **pairwise comparison** (output vs input): is it faithful / complete / natural / realistic, and *did anything regress*? Output = yes/no/unsure. | `frame_890.jpg` - "Generation Evals: Pairwise Comparison" bullets | narration @ `&t=896s`..`&t=937s` | corroborated | OK |
| n11 | Stack redundant QA gates as a **Swiss-cheese model**: a final holistic "publish-ready QA" after generation QA reduces the odds a failure reaches production and also flags what upstream should have caught. | narration @ `&t=1062s`..`&t=1103s` | `frame_1058.jpg` - separate "LLM QA" then "Publish Ready QA" gates | corroborated | OK |
| n12 | Three complementary feedback loops keep the system aligned: **Model loop** (drift/regression, auto-tuner on sampled prod data), **Dogfooding loop** (merchant + internal thumbs-up/down + free-form feedback), **Marketplace loop** (A/B tests on funnel metrics like conversion / add-to-cart). | `frame_1118.jpg` - "3 Feedback Loops" | narration @ `&t=1103s`..`&t=1248s` | corroborated | OK |
| n13 | A higher-level **diagnoser** abstraction generalizes self-tuning: it ingests any feedback loop's signal, reflects on *which* agent(s) in the system need fixing, and routes the config fix there (one or many agents). | narration @ `&t=1144s`..`&t=1185s` | `frame_658.jpg` "Diagnoser + Tune" node | corroborated | OK |
| n14 | Agents fit this problem because the design space is a spectrum from deterministic/rules-based (controllable but brittle, won't scale) to fully agentic (creative, high agency but unsafe unconstrained); the goal is a guardrailed balance. | narration @ `&t=251s`..`&t=293s` | `frame_222.jpg` goals (authenticity, ship safely, scale) | corroborated | OK |
| n15 | Reward hacking shows up as **nugatory changes**: told its edit failed, the agent oversteers to an overly-conservative generic output (e.g. a plain ceramic bowl) - raw pixels differ a lot but nothing meaningful improved. | narration @ `&t=979s`..`&t=1000s` | (described, example slide not captured) | single-leg | needs-check |

## Dropped / divergences (audit trail)

| Candidate | Verdict | Note |
|---|---|---|
| `frame_5` (title card) | dropped | "World's Fair" intro, no knowledge content. |
| `frame_1276` (podium) | dropped | talking-head/closing shot, no slide content. |
| Business-scale stats (Uber Eats $90B run-rate, 10k cities) | dropped | source-specific trivia, not transferable knowledge. |

> Citations cite BOTH legs where both exist. `single-leg` nodes (n6, n8, n15) rest on the narration
> only - the slide either wasn't captured or the point was spoken - so confidence is `needs-check`,
> not `corroborated`. Note: two legs agreeing here proves the slide and the talk are **internally
> consistent**, not that the approach is externally validated - that needs a second source.
