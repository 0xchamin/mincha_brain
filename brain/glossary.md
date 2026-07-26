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

| Context rot | The measurable decline in LLM output quality as input length grows, independent of task difficulty - not a capacity limit being hit, but a gradient you are already on. Measured across 18 models. | R1 ([Chroma](https://www.trychroma.com/research/context-rot), T2) |
| Attention budget | The framing of context as a finite resource: a transformer needs every token to attend to every other, giving n² pairwise relationships, so capacity to model them is "stretched thin" as context grows. Hence: seek the smallest set of high-signal tokens. | R1 ([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), T2) |
| Lost in the middle | The U-shaped position effect: models use information best at the start or end of a context and significantly worse in the middle. Reproduced across six model families. | R1 ([arXiv 2307.03172](https://arxiv.org/abs/2307.03172), TACL, T1) |
| Event sourcing | Persisting state as an append-only sequence of events and reconstructing it by replaying them ("rehydration"), rather than storing current values. Named by Fowler in 2005 - and the pattern the 12-factor thread/state design rediscovers. | R1 ([Azure Arch Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing), T1) |

| Delegated authorization | Granting a *third party* a *subset* of your permissions on a *fourth party's* system, without sharing your credentials. The four-party shape is what makes it hard enough to need a protocol - and it is the shape of an agent calling a tool on your behalf. | S3 (`996OiexHze0` `&t=539s`) |
| Resource owner | OAuth's term for **you** - the human who owns the data and can click Yes. Most of OAuth's difficulty is vocabulary: the seven core terms are renames of ordinary things. | S3 (`996OiexHze0` `&t=990s`) |
| Front channel / back channel | Network-security terms, not OAuth ones. **Front channel** = the browser: usable to interact with a human, but observable (URL bar, extensions, shoulders). **Back channel** = server to server over TLS: unobservable. The whole flow shape follows from trusting the browser with the human and never with a secret. | S3 (`996OiexHze0` `&t=1634s`) |
| Scope | A named permission (`contacts.read`) the client requests up front, the user sees in plain language on the consent screen, and the issued token is bound to. Turns "access my account" into "read my contacts". | S3 (`996OiexHze0` `&t=1377s`) |
| Authorization code | A deliberately **useless** token: it crosses the browser in the open because redeeming it requires a `client_secret` that only exists on the back channel. The design assumes the channel is compromised and arranges for that not to matter. | S3 (`996OiexHze0` `&t=1937s`) |
| Access token vs ID token | An **access token** is for a *machine* - presented to an API, which decides what it permits; the client is not meant to read it. An **ID token** is for the *app* - it says who signed in and is never sent to an API. Confusing the two is the root of most OAuth/OIDC mix-ups. | S3 (`996OiexHze0` `&t=3126s`) |
| JWT ("jot") | JSON Web Token: a signed, base64url-encoded JSON envelope in three dot-separated parts (header, claims, signature). The signature lets a client verify authenticity locally, with no call back to the issuer. **Signed, not encrypted** - never put secrets in one. | S3 (`996OiexHze0` `&t=3234s`) |
| PKCE ("pixie") | Proof Key for Code Exchange: the fix for clients that cannot hold a `client_secret`. The client invents a per-request secret, sends only its hash up front, and reveals the original at exchange time - restoring "a stolen code is useless" **without a back channel**. | S3 (`996OiexHze0` `&t=3562s`) |

| Harness | The orchestration around a model: how work is decomposed, what state passes between steps, who checks the output, when context is cleared. Not the model and not the prompt. Each component encodes an expiring assumption about what the model cannot do alone. | S4 (§1, §4c) |
| Context anxiety | A model sensing it is near its context limit and **prematurely wrapping up** - declaring done, summarising, cutting scope - *before* the window is actually exhausted. Behavioural, not capacity-driven, and distinct from context rot. | S4 (§2) |
| Context reset | Clearing the context window and restarting from a structured handoff artifact, as opposed to **compaction** (summarising in place). Only the reset removes context anxiety; the handoff artifact becomes the load-bearing part. | S4 (§2) |
| Self-evaluation bias | The tendency of an agent asked to judge its own output to confidently praise it, even when a human would call the quality obviously mediocre. The reason a separate evaluator beats a self-critical generator. | S4 (§1, §2) |
| Capability boundary | The frontier of what a model does reliably. Scaffolding is worth keeping only for tasks at or beyond it - so a component's value is **boundary-relative**, and a new model can turn essential scaffolding into pure overhead. | S4 (§4c) |

| Progressive disclosure (skills) | The three-layer loading contract of a skill: **frontmatter** (name + description) in context on every turn, **`SKILL.md` body** on trigger, **references and scripts** on demand. Each layer has a different price, which is the whole design constraint. | S5 (`0vphxNt4wyk` `&t=159s`) |
| Capability skill vs preference skill | **Capability**: teaches what the model cannot do consistently yet - *temporary*, retire as models improve. **Preference**: encodes team workflow and convention - *durable*, must track the team. Opposite lifespans, so opposite eval purposes. | S5 (`0vphxNt4wyk` `&t=194s`) |
| Trigger hijacking | A skill description broad enough that it fires on unrelated work ("use for any web development task" firing on Angular when it is a React skill), stealing context from tasks it cannot help. The fix is declaring **negative cases**. | S5 (`0vphxNt4wyk` `&t=611s`) |
| No-op (skill instruction) | An instruction that does not alter the agent's behaviour - "write clear, high-quality code", "make the implementation easy to read". Common in AI-authored skills; burns reasoning tokens and obscures the real instructions. Credited to Matt Pocock. | S5 (`0vphxNt4wyk` `&t=680s`) |
| Ablation (eval) | Running the same eval suite **with and without** a component loaded, and reading the *delta* rather than the absolute score. 94% vs 32% means the component is load-bearing; 96% vs 95% means the base model absorbed it and it is now pure context cost. The retirement test for any expiring scaffold. | S5 (`0vphxNt4wyk` `&t=713s`) |
| Skill lift | The performance delta a skill produces in an ablation. SkillsBench 1.1: curated skills +16.6 pts (33.9% -> 50.5%); self-generated skills **negative** (-8.1 to -11.5). Also the merge criterion at Google DeepMind - no skill PR lands without proof of positive lift. | S5 (`0vphxNt4wyk` `&t=266s`,`&t=1002s`) |

> **S1** = `sources/260725_closed-loop-evals-multimodal-agent/` (Uber, AI Engineer World's Fair 2026).
> **S2** = `sources/260725_12-factor-agents/` (Dex Horthy / HumanLayer, AI Engineer World's Fair 2025).
> **S3** = `sources/260725_oauth2-oidc-plain-english/` (Nate Barbettini / Okta, 2018).
> **S4** = `sources/260725_harness-design-long-running-apps/` (Prithvi Rajasekaran, Anthropic Labs, 2026).
> **S5** = `sources/260726_dont-ship-skills-without-evals/` (Philipp Schmid, Google DeepMind, AI Engineer WF 2026).
> **R1** = deep-research pass on S2, `sources/260725_12-factor-agents/context/01_context-limits-and-decomposition.md`.
