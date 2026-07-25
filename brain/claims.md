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
| 14 | The naive agent loop degrades on long workflows, primarily from unbounded context growth. | agents | S2 (`8kMaTybvDUw` `&t=371s`) | emerging |
| 15 | Unify execution + business state behind a REST/MCP API; serialise the context window with a state ID to pause and resume - the agent never knows it was suspended. | agents | S2 (`8kMaTybvDUw` `&t=460s`) | emerging |
| 16 | Make contacting a human a tool call / intent among the others, not a structural branch before the first output token. | agents | S2 (`8kMaTybvDUw` `&t=687s`) | emerging |
| 17 | Not every problem needs an agent - a deterministic script often beats hours of prompt engineering. | agents | S2 (`8kMaTybvDUw` `&t=71s`) | needs-check (single-leg) |
| 18 | Target work at the boundary of what the model does *reliably*, then engineer reliability around it - that is where the differentiation is. | agents | S2 (`8kMaTybvDUw` `&t=848s`) | emerging |
| 19 | LLMs are stateless pure functions; input-token quality is the only lever on output quality short of retraining. | context-engineering | S2 (`8kMaTybvDUw` `&t=547s`) | emerging |
| 20 | Prompt, memory, RAG and history are one problem - which tokens reach the model. | context-engineering | S2 (`8kMaTybvDUw` `&t=616s`) | emerging |
| 21 | You need not use the standard messages format - model the thread as typed events and serialise for density and clarity; this is also what makes pause/resume possible. | context-engineering | S2 (`8kMaTybvDUw` `&t=563s`) | emerging |
| 22 | Limiting context beats filling it: a 2M-token window returns an answer, not a better one. | context-engineering | S2 (`8kMaTybvDUw` `&t=388s`) | emerging |
| 23 | Compact errors - clear pending errors after a valid tool call, summarise instead of dumping stack traces - or the agent spins out. | context-engineering | S2 (`8kMaTybvDUw` `&t=653s`) | emerging |

> **S1** = `sources/260725_closed-loop-evals-multimodal-agent/` (Uber, "Building Closed-Loop Evals
> for a Multimodal Agent at Scale", AI Engineer World's Fair 2026).
> **S2** = `sources/260725_12-factor-agents/` (Dex Horthy / HumanLayer, "12-Factor Agents: Patterns
> of reliable LLM applications", AI Engineer World's Fair 2025).

> **Claim 11 is the only cross-source claim so far** - two separate talks, one arguing from first
> principles and one reporting production practice, converging on the same structure. Note the
> weakness before leaning on it: both are practitioner talks by people selling adjacent products,
> delivered a year apart into the same discourse, and neither offers measurements - so this is
> convergence, not independent replication. Claims 12-23 rest on S2 alone; S2's own external
> corroboration is the author's own repo, so it is not independent either.

> When a new source corroborates an existing claim, add its citation to that row rather than
> creating a duplicate. When sources conflict, keep both and flag the conflict.
