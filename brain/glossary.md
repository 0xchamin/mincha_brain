# Brain - glossary (reusable terms)

> 💡 terms defined once and reused across sources, promoted from source `LEARNING.md` files.
> Keep each to 1-2 sentences. Cite the source where the term was learned.

| Term | 💡 Explanation | First source |
|---|---|---|
| Corroboration gate | The check that keeps a visual's meaning only when the agent's reading of it agrees with the surrounding text. Two-modality agreement is what makes a kept visual trustworthy. | (kit design) |
| Knowledge node | The atomic unit of the brain: one corroborated claim + its visual + its text quote + citation + confidence. | (kit design) |
| Valid (in Brain) | Corroborated + coherent + on-topic - **not** fact-checked against reality. The brain surfaces and cites; the human judges truth. | (kit design) |
| pass@k | Pass rate at the k-th retry of an agent; when each retry folds the QA gate's failure reasoning back into the prompt, pass rate rises with more iterations. | S1 (`31GUkCBD-Uc` `&t=850s`) |
| Pairwise comparison (evals) | Evaluating an edit by comparing output against input (better? faithful? complete? natural? did anything regress?) rather than scoring in isolation; output is yes/no/unsure. | S1 (`31GUkCBD-Uc` `&t=896s`) |
| Swiss-cheese model | Stacking several imperfect QA gates so their "holes" rarely line up - deliberate redundancy that stops failures reaching production. | S1 (`31GUkCBD-Uc` `&t=1082s`) |
| Golden dataset | A representative, objectively human-labeled truth set an agent is aligned to and benchmarked against. | S1 (`31GUkCBD-Uc` `&t=528s`) |
| Diagnoser (agent) | A meta-agent that reads any feedback loop, localizes which sub-agent is failing, and triggers its config auto-tune. | S1 (`31GUkCBD-Uc` `&t=1144s`) |
| Closed-loop eval | An eval system that samples production output, re-labels it, diagnoses drift, and auto-tunes the agent config with no human editing prompts. | S1 (`31GUkCBD-Uc` `&t=650s`) |
| 12-factor agent | Dex Horthy's list of 12 design rules for reliable LLM applications, named after Heroku's 12-factor app. Each factor names a piece of the system you should own rather than delegate to a framework. | S2 (`8kMaTybvDUw` `&t=141s`) |
| Context engineering | The single discipline behind prompt, memory, RAG and history: deciding exactly which tokens reach the model. Treats them as one problem, not four subsystems. | S2 (`8kMaTybvDUw` `&t=616s`) |
| Micro agent | A small agent loop of roughly 3-10 steps embedded at a hard point inside an otherwise deterministic pipeline - the shape that works in production. | S2 (`8kMaTybvDUw` `&t=741s`) |
| Structured output | The model emitting JSON conforming to a schema you defined, rather than prose. The capability all "tool use" actually rests on. | S2 (`8kMaTybvDUw` `&t=229s`) |
| Materialised DAG | The graph of steps an agent loop produces at runtime, as opposed to a DAG written up front in Airflow or Prefect. | S2 (`8kMaTybvDUw` `&t=371s`) |
| Spin-out (agent) | The failure mode where raw errors are blindly appended to the context window until the agent loses the thread and gets stuck retrying. | S2 (`8kMaTybvDUw` `&t=653s`) |
| Stateless reducer | An agent that holds no state of its own, folding each event into a thread you own. Pedantically a *transducer*, since there are multiple steps. | S2 (`8kMaTybvDUw` `&t=865s`) |
| Own your control flow | Keeping the loop, the switch on model output, the prompt and the context builder in your own code, so you can break, summarise or judge mid-run instead of waiting for a framework to return. | S2 (`8kMaTybvDUw` `&t=406s`) |

> **S1** = `sources/260725_closed-loop-evals-multimodal-agent/` (Uber, AI Engineer World's Fair 2026).
> **S2** = `sources/260725_12-factor-agents/` (Dex Horthy / HumanLayer, AI Engineer World's Fair 2025).
