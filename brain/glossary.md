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

> **S1** = `sources/260725_closed-loop-evals-multimodal-agent/` (Uber, AI Engineer World's Fair 2026).
