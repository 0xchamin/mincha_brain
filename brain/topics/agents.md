# Topic: Agents

**Status:** emerging (1 source -> established at 2+ corroborating sources)

> Living, cross-source synthesis on autonomous LLM agents. Many sources feed this note; **merge
> and de-duplicate** as they arrive (architect persona) - this should read as one coherent view,
> not stacked summaries. Every claim cited.

## What this covers

Autonomous LLM agents: the agent loop (perceive -> plan -> act -> observe), tool use, memory,
planning strategies, multi-agent patterns, and failure modes.

## Synthesis

A production agent "product" is often not one monolithic agent but a **routed pipeline of small,
single-purpose agents** (image-understanding -> router -> prompt-gen -> generation -> QA gates ->
post-processing), each independently evaluable, with the whole orchestration logged to one flat
trace [S1 `&t=376s`]. Two structural patterns stand out:

- **Agents as self-tuning components.** Rather than a static model, each agent can rewrite its own
  config: a **prompt-optimizer** built from two sub-agents - *reflect* (find systemic issues in
  mismatches) and *synthesize* (rewrite the config) - registers a new version in an agent store
  that the next run picks up, with observability and quick rollback [S1 `&t=732s`].
- **A meta-agent (diagnoser) over the fleet.** A higher-level abstraction ingests any feedback
  signal, localizes *which* sub-agent is failing, and routes the fix to that agent's config -
  generalizing self-tuning across a multi-agent system [S1 `&t=1144s`].
- **Where agents fit.** The design space is a spectrum from deterministic/rules-based (controllable
  but brittle, won't scale) to fully agentic (creative, high agency but unsafe unconstrained); the
  target is a **guardrailed** middle [S1 `&t=251s`].

> Evaluation of these pipelines is its own topic - see [`evals.md`](evals.md).

## Key claims

| Claim | Sources (cited) | Confidence |
|---|---|---|
| A production agent is often a routed pipeline of small single-purpose agents, each independently evaluable, all logged to one flat trace. | S1 `&t=376s` | emerging |
| Agents can self-tune: a reflect+synthesize prompt-optimizer rewrites an agent's config and registers a new version, no human in the loop. | S1 `&t=732s` | needs-check (single-leg) |
| A diagnoser meta-agent localizes which sub-agent is failing and routes the config fix there. | S1 `&t=1144s` | emerging |
| Agent design is a spectrum from brittle rules to unconstrained agency; aim for a guardrailed middle. | S1 `&t=251s` | emerging |

## Key visuals

![Routed multi-agent pipeline with per-stage QA and logging](../../sources/260725_closed-loop-evals-multimodal-agent/visuals/frame_1058.jpg)
> A production agent as a pipeline of small agents, every stage logged. S1 `&t=376s`.

## Open questions / conflicts

- Self-tuning agents (reflect/synthesize, agent store) are `single-leg` (narration only) - needs a
  second source to corroborate the pattern.

## Sources feeding this topic

- **S1** - [Building Closed-Loop Evals for a Multimodal Agent at Scale](../../sources/260725_closed-loop-evals-multimodal-agent/LEARNING.md) (Uber, AI Engineer 2026).
