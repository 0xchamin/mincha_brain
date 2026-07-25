# Brain - corroborated claims (cross-source)

> Durable, corroborated claims promoted from source `nodes.md` files. Each must be reusable
> across future queries and carry a citation. A claim confirmed by multiple sources is stronger -
> note them all. This is a signal store; task-specific scratch stays in the source folder.

| # | Claim | Topic | Sources (cited) | Confidence |
|---|---|---|---|---|
| 1 | Log the full flat end-to-end trace first - it is the precondition for evals and any self-learning loop. | evals | S1 (`31GUkCBD-Uc` `&t=418s`) | emerging |
| 2 | Eval a router as a classifier (confusion matrix, precision/recall); guardrail metric = recall so nothing bad slips through. | evals | S1 (`31GUkCBD-Uc` `&t=459s`,`&t=578s`) | emerging |
| 3 | Two router failure modes: precision miss (over-process a good input) and recall miss (approve a bad input -> hallucination risk). | evals | S1 (`31GUkCBD-Uc` `&t=588s`) | emerging |
| 4 | Generation/editing evals are iterative: QA feedback -> prompt rewrite -> retry; measure pass@k. | evals | S1 (`31GUkCBD-Uc` `&t=850s`) | emerging |
| 5 | Editing tasks: eval by pairwise comparison (better than input? faithful/complete/natural? regressions?) -> yes/no/unsure. | evals | S1 (`31GUkCBD-Uc` `&t=896s`) | emerging |
| 6 | Stack redundant QA gates (Swiss-cheese model) to keep failures out of production. | evals | S1 (`31GUkCBD-Uc` `&t=1082s`) | emerging |
| 7 | Close the loop: auto-tune on sampled + re-labeled production data, config-driven, no human in the loop. | evals | S1 (`31GUkCBD-Uc` `&t=650s`) | emerging |
| 8 | Layer three feedback loops: model (drift), dogfooding (human), marketplace (A/B on funnel metrics). | evals | S1 (`31GUkCBD-Uc` `&t=1103s`) | emerging |
| 9 | A production agent is often a routed pipeline of small single-purpose agents, each independently evaluable. | agents | S1 (`31GUkCBD-Uc` `&t=376s`) | emerging |
| 10 | Agents can self-tune via a reflect+synthesize prompt-optimizer that rewrites config and registers a new version. | agents | S1 (`31GUkCBD-Uc` `&t=732s`) | needs-check |
| 11 | **What ships in production is small, scoped LLM steps inside deterministic software - not one big autonomous loop.** S2 reaches it from first principles (micro agents, 3-10 steps), S1 from production practice (routed pipeline of single-purpose agents). | agents | **S2 (`8kMaTybvDUw` `&t=741s`) + S1 (`31GUkCBD-Uc` `&t=376s`)** | **corroborated (2 sources)** |
| 12 | An agent = prompt + switch statement + context builder + loop; own all four. | agents | S2 (`8kMaTybvDUw` `&t=406s`) | emerging |
| 13 | The enabling LLM capability is structured output (sentence -> JSON); "tool use" is just that JSON plus deterministic code. | agents | S2 (`8kMaTybvDUw` `&t=229s`,`&t=264s`) | emerging |
| 14 | The naive agent loop degrades on long workflows, primarily from unbounded context growth. | agents | S2 (`8kMaTybvDUw` `&t=371s`) + **R1** ([Lost in the Middle](https://arxiv.org/abs/2307.03172), TACL, T1; [Context Rot](https://www.trychroma.com/research/context-rot), 18 models, T2) | **corroborated (external, measured)** |
| 15 | Unify execution + business state behind a REST/MCP API; serialise the context window with a state ID to pause and resume - the agent never knows it was suspended. | agents | S2 (`8kMaTybvDUw` `&t=460s`) | emerging |
| 16 | Make contacting a human a tool call / intent among the others, not a structural branch before the first output token. | agents | S2 (`8kMaTybvDUw` `&t=687s`) | emerging |
| 17 | Not every problem needs an agent - a deterministic script often beats hours of prompt engineering. | agents | S2 (`8kMaTybvDUw` `&t=71s`) + **R1** ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents): "find the simplest solution possible, and only increasing complexity when needed", T2) | corroborated (external) |
| 18 | Target work at the boundary of what the model does *reliably*, then engineer reliability around it - that is where the differentiation is. | agents | S2 (`8kMaTybvDUw` `&t=848s`) | emerging |
| 19 | LLMs are stateless pure functions; input-token quality is the only lever on output quality short of retraining. | context-engineering | S2 (`8kMaTybvDUw` `&t=547s`) | emerging |
| 20 | Prompt, memory, RAG and history are one problem - which tokens reach the model. | context-engineering | S2 (`8kMaTybvDUw` `&t=616s`) | emerging |
| 21 | You need not use the standard messages format - model the thread as typed events and serialise for density and clarity; this is also what makes pause/resume possible. | context-engineering | S2 (`8kMaTybvDUw` `&t=563s`) | emerging |
| 22 | Limiting context beats filling it - and degradation is **non-uniform**: it depends on where in the window the information sits, on distractors, and on structure, and it appears well before the advertised limit (a 200K-window model degrading by 50K). Mechanism: an n² "attention budget". | context-engineering | S2 (`8kMaTybvDUw` `&t=388s`) + **R1** ([Lost in the Middle](https://arxiv.org/abs/2307.03172) T1; [Context Rot](https://www.trychroma.com/research/context-rot) T2; [Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) T2) | **corroborated (external, measured)** |
| 23 | Compact errors - clear pending errors after a valid tool call, summarise instead of dumping stack traces - or the agent spins out. | context-engineering | S2 (`8kMaTybvDUw` `&t=653s`) + **R1** (Anthropic names **compaction** a core long-task technique, T2) | corroborated (external) |
| 24 | **Decomposition is measured, memory scaffolding is measured worse.** Splitting a long task into short segments and restarting at each boundary gives **+13.1 pp (DeepSeek V3) to +41.5 pp (Qwen3 30B)** reliability; but a naive episodic memory scaffold "never improves long-horizon reliability, and hurts 6 of 10 models" - plain ReAct beat it. Decompose and keep segments short; do not bolt memory onto a long loop. | agents | **R1** ([Beyond pass@1](https://arxiv.org/abs/2603.29231), 10 models, T3 preprint) | needs-check (preprint, not peer-reviewed) |
| 25 | The thread-as-typed-events + serialise-and-resume design (factors 3, 5, 6, 12) is **Event Sourcing**, named by Fowler in 2005 - which carries known sharp edges S2 never mentions: replay determinism, snapshotting (= compaction), and event versioning. | context-engineering | **R1** ([Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) T1) | emerging (cross-domain framing) |

> **S1** = `sources/260725_closed-loop-evals-multimodal-agent/` (Uber, "Building Closed-Loop Evals
> for a Multimodal Agent at Scale", AI Engineer World's Fair 2026).
> **S2** = `sources/260725_12-factor-agents/` (Dex Horthy / HumanLayer, "12-Factor Agents: Patterns
> of reliable LLM applications", AI Engineer World's Fair 2025).
> **R1** = deep-research pass `sources/260725_12-factor-agents/context/01_context-limits-and-decomposition.md`
> (2026-07-25) - external evidence, each citation tiered T1-T5 with an independence call.

> **Claim 11** is the only claim corroborated by a second *ingested* source - two separate talks, one
> arguing from first principles and one reporting production practice. Weakness: both are
> practitioner talks by people selling adjacent products, delivered a year apart into the same
> discourse, neither with measurements - convergence, not replication.
>
> **Claims 14, 17, 22, 23 carry external corroboration** from the R1 research pass, and 14/22 are now
> **measured** rather than asserted (peer-reviewed position effects + an 18-model degradation study).
> Claim 24 is external-only and rests on a preprint. Read the tier and independence call before
> leaning on any of them: a vendor writing about context budgets is independent of S2 but not
> disinterested about the field.

> When a new source corroborates an existing claim, add its citation to that row rather than
> creating a duplicate. When sources conflict, keep both and flag the conflict.
