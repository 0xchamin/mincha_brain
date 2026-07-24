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

> **S1** = `sources/260725_closed-loop-evals-multimodal-agent/` (Uber, "Building Closed-Loop Evals
> for a Multimodal Agent at Scale", AI Engineer World's Fair 2026).

> When a new source corroborates an existing claim, add its citation to that row rather than
> creating a duplicate. When sources conflict, keep both and flag the conflict.
