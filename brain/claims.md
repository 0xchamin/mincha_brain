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
| 26 | **Credential sharing is the anti-pattern delegated authorization exists to kill.** A password is unscopable, unrevocable and unexpiring, so handing it to a third party grants total, permanent access to the account that is the recovery path for every other account. | agent-security | S3 (`996OiexHze0` `&t=648s`) | emerging |
| 27 | **Scopes are least privilege made explicit and enforced at the resource server**: the client enumerates permissions up front, the token is bound to exactly those, and the API rejects out-of-scope calls even when the token is valid. The enforcement point is the resource server, not the client. | agent-security | S3 (`996OiexHze0` `&t=1549s`) | emerging |
| 28 | **The consent screen is generated from the requested scopes**, which is what makes approval specific rather than blanket - the human-in-the-loop mechanism only works because the ask is itemised. | agent-security | S3 (`996OiexHze0` `&t=1428s`) | emerging |
| 29 | **Make the untrusted leg carry only useless material.** The authorization code crosses the browser precisely because stealing it accomplishes nothing - redeeming it requires a secret that never leaves the back channel. Stronger than encrypting the channel: it assumes compromise and arranges for it not to matter. | agent-security | S3 (`996OiexHze0` `&t=1937s`) | emerging |
| 30 | **A near-fit standard adopted for an unnamed use case degrades into a non-standard.** OAuth had no way to return user identity, so every provider bolted on a proprietary extension for login and the implementations stopped being interchangeable; OpenID Connect exists to close that gap publicly. | agent-security | S3 (`996OiexHze0` `&t=2894s`) | needs-check (single-leg) |
| 31 | **Every harness component encodes an assumption about what the model cannot do on its own - and those assumptions expire.** Re-ask on each model release: not "what should I add?" but "which of these is still load-bearing?" | agents | S4 (§4c) | emerging |
| 32 | **Scaffolding value is boundary-relative, not intrinsic.** Whether a component earns its place depends on where the task sits against the model's capability frontier. This **refines claim 24**: decomposition helps *until the boundary moves past your task* - S4 deleted its sprint construct on a stronger model and ran coherently for 2+ hours unscaffolded. | agents | S4 (§4c) - refines claim 24 | emerging (n=1, vendor; claim 24's 10-model study is the stronger evidence if they ever conflict) |
| 33 | **When simplifying a harness, remove one component at a time.** Radical simultaneous cuts failed; methodical single-component removal worked. Delete four things and lose quality and you have learned nothing. | agents | S4 (§4c) | emerging |
| 34 | **Do not let the producer grade its own work.** Self-evaluation bias: agents asked to judge their own output confidently praise it even when a human would call the quality obviously mediocre. Not promptable-away - the generator has no independent vantage point on its own work. | evals | S4 (§1, §2) | emerging |
| 35 | **Subjective quality becomes gradable by fixing the question, not the model.** "Is this beautiful?" grades inconsistently; "does this follow our design principles?" supplies criteria. When a quality judgement grades inconsistently, suspect the question before the grader. | evals | S4 (§2, §3) | emerging |
| 36 | **The grader is not free.** Out-of-the-box models are lenient QA, biased toward AI-generated output; S4's evaluator took several log-driven tuning rounds to catch subtle bugs. It also needs **tools to perceive what it grades** (a browser to judge a UI), and **its modality is a hard ceiling on what "quality" can mean** - a model that cannot hear cannot grade audio. | evals | S4 (§4a, §5) | emerging |
| 37 | **"Context anxiety": a model may prematurely wrap up work as it nears its *perceived* context limit** - a behavioural failure distinct from degradation caused by a full window (claims 14, 22). **Compaction does not fix it; a context reset does**, at the cost of a handoff artifact that must carry enough state to resume - which is claim 21's serialisation requirement arriving from the opposite direction. | context-engineering | S4 (§2) | needs-check (single-leg, vendor, model-version-bound) |

> **S1** = `sources/260725_closed-loop-evals-multimodal-agent/` (Uber, "Building Closed-Loop Evals
> for a Multimodal Agent at Scale", AI Engineer World's Fair 2026).
> **S2** = `sources/260725_12-factor-agents/` (Dex Horthy / HumanLayer, "12-Factor Agents: Patterns
> of reliable LLM applications", AI Engineer World's Fair 2025).
> **S3** = `sources/260725_oauth2-oidc-plain-english/` (Nate Barbettini / Okta, "OAuth 2.0 and
> OpenID Connect (in plain English)", 2018). **8 years old** - the mechanics are current, the
> flow-selection advice is partly superseded; see that source's `n17`.
> **S4** = `sources/260725_harness-design-long-running-apps/` (Prithvi Rajasekaran, Anthropic Labs,
> "Harness Design for Long-Running Application Development", 2026-03-24). **T2 vendor source**
> writing about its own models, **n=1 per configuration**, no released harness code, **visual leg
> skipped** - so its mechanisms are more trustworthy than its numbers.
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

> **Claims 26-30 are the brain's first non-agent claims** - protocol substrate rather than agent
> practice. They are promoted on the judgement that delegated authorization *is* the agent
> permissions problem with a longer history, not on any cited link between them: **no source in this
> brain yet connects OAuth to agents or to MCP.** That link is currently agent commentary and is
> recorded as an open question in `topics/agent-security.md`, not as a claim here.

> When a new source corroborates an existing claim, add its citation to that row rather than
> creating a duplicate. When sources conflict, keep both and flag the conflict.
