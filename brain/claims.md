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
| 17 | Not every problem needs an agent - a deterministic script often beats hours of prompt engineering. **S5 reaches the same boundary from skill design: "if exact step-by-step execution is required, write a script instead of a skill".** | agents | S2 (`8kMaTybvDUw` `&t=71s`) + **S5 (`0vphxNt4wyk` `&t=558s`)** + **R1** ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents): "find the simplest solution possible, and only increasing complexity when needed", T2) | **corroborated (2 ingested sources + external)** |
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
| 38 | **A skill is a three-layer cost ladder, not a document.** Frontmatter (name + description) sits in context on *every* model call; the `SKILL.md` body loads on trigger; references and scripts cost nothing until the agent explicitly reads them. The description is a per-call tax of 100-200 tokens whether the skill fires or not. | skills | S5 (`0vphxNt4wyk` `&t=159s`,`&t=471s`) | emerging |
| 39 | **The reliability bar rises with the user's distance from the mechanism.** An engineer using their own agent repairs a mis-trigger in seconds and is the eval; a shipped user does not know the mechanism exists, has no fallback, and leaves on first failure - so the checking must be automated. | skills | S5 (`0vphxNt4wyk` `&t=126s`) | emerging |
| 40 | **Two kinds of skill with opposite lifespans.** Capability skills teach what the model cannot do consistently *yet* and are temporary; preference skills encode team workflow and convention and are durable. Evals are the retirement signal for the first and the regression guard for the second. | skills | S5 (`0vphxNt4wyk` `&t=194s`,`&t=213s`) | emerging |
| 41 | **Skills move performance in both directions.** Curated skills lift task resolution 33.9% -> 50.5% (+16.6 pts) on SkillsBench 1.1; **self-generated (AI-written) skills cost 8.1 to 11.5 points.** Human-written skills perform best. | skills | S5 (`0vphxNt4wyk` `&t=266s`,`&t=299s`) - **SkillsBench, a public third-party benchmark** | emerging |
| 42 | **Skill length is an inverted-U, not a slope.** <200 lines +19.0%; **200-500 lines +21.5% (peak)**; 500-1000 +14.5%; **>1000 lines +0.7%, statistically a no-op.** "As short as possible" is the wrong reading. | skills | S5 (`0vphxNt4wyk` `&t=315s`) - **the curve is visual-only; the narration states only a 500-line ceiling** | emerging |
| 43 | **The description is the trigger mechanism, and the trigger causes 50%+ of all skill failures** - the highest-leverage line in a skill. Write directives not essays, include the *what* and the *when*, and declare negative cases or a broad description hijacks the trigger on unrelated work. | skills | S5 (`0vphxNt4wyk` `&t=1036s`,`&t=437s`,`&t=594s`) | emerging |
| 44 | **Ablation is an eval method, and the delta is the verdict, not the absolute score.** Run the same suite with and without the component loaded: 94% vs 32% means keep it; 96% vs 95% means the base model absorbed the knowledge and the component is now pure context cost. **This is the measurement claim 31 lacked** - it converts "assumptions expire" from a judgement into a test. | evals | S5 (`0vphxNt4wyk` `&t=713s`,`&t=1268s`) - instruments claim 31 | emerging |
| 45 | **Keep the eval after you retire the component.** It becomes a regression detector on the bare model and is what tells you when to reintroduce the scaffolding. Closes the loop claim 31 leaves open: S4 can tell you a component stopped being load-bearing but cannot notice if that reverses. | evals | S5 (`0vphxNt4wyk` `&t=1181s`,`&t=1199s`) | needs-check (single-leg) |
| 46 | **Gate the diff, not the release.** At Google DeepMind evals sit alongside every skill, run on every change, and **a change cannot merge unless it improves the test cases.** The strongest instance in this brain of claim 34's independent checker - a merge gate is the only one a human cannot wave through. | evals | S5 (`0vphxNt4wyk` `&t=1002s`,`&t=1019s`) | emerging (self-reported practice, T2 vendor) |
| 47 | **Grade outcomes, not paths; and isolate every run, because agents cheat.** Assert the task succeeded rather than that the component was invoked on turn one. Run each case in a clean workspace - coding agents will read prior chats or executions to obtain the content without invoking the thing under test. | evals | S5 (`0vphxNt4wyk` `&t=1091s`,`&t=1109s`,`&t=1129s`) | emerging |
| 48 | **Write-once memory goes stale as a structural property, not as a bug.** Written during a conversation and never revisited, a memory keeps that conversation's tense and decays into **confident wrongness** rather than into irrelevance. A missing fact degrades an answer; a stale fact poisons it, because the system acts on it with full confidence. | memory | S6 (§How memory has evolved, prose + `fig_saved_memories`) | emerging |
| 49 | **Explicit-cue capture systematically under-collects**, and the category it misses is **implicit preferences** - context that governs what is relevant ("I live near San Francisco") but is never uttered as an instruction. Response instructions and stated constraints are easy to capture; the third kind is not. | memory | S6 (§How memory has evolved, §Following preferences) | needs-check (taxonomy is single-leg) |
| 50 | **Decouple the memory write from the conversation turn.** Synthesis runs as a background process on its own clock, reading across many past sessions - which is what makes revision possible at all, since a write that happens only while the user is talking can only record the present tense of that talk. | memory | S6 (§How memory has evolved, prose + "Updated 2h ago") | emerging |
| 51 | **Revision, not expiry.** Rewrite a stale memory into a new tense ("going to Singapore in July" -> "went to Singapore in July 2026") rather than deleting it on a TTL. **Expiry treats age as invalidity; revision treats age as information** - and the revised fact stays useful context. | memory | S6 (§Staying current over time, prose + paired worked example) | emerging |
| 52 | **Representation is a maintenance decision, not a storage one - pick the shape whose edits you can express.** A flat append-only list of atomic assertions makes revision inexpressible; a maintained narrative some process owns does not. | memory | S6 (§How memory has evolved, `fig_saved_memories` vs `fig_memory_summary`, same persona) | emerging |
| 53 | **Put the human on the synthesized artifact, not on the raw records.** Once a background process authors memory, asking the user to hand-curate its inputs is asking them to do the job you just automated. **Unresolved:** whether a correction is a durable override or merely another input to the next pass. | memory | S6 (§How memory has evolved, prose + `fig_memory_summary`) | emerging |
| 54 | **"Good memory" is not one metric.** It decomposes into three separately-evaluable objectives - carry forward context (catches under-capture), follow preferences (catches **recall without compliance**), stay current (catches staleness). Only the third can fail purely through the passage of time, and it is the one most memory evals omit. | memory | S6 (§How we evaluate memory) | emerging |
| 55 | **Memory synthesis is expensive enough to gate rollout: cost, not answer quality, was the stated constraint** on serving it universally (a claimed ~5x compute reduction unlocked the free tier). The durable part is the direction - maintaining memory is a recurring per-user compute cost, not a storage cost. | memory | S6 (§A more scalable foundation for the future) | needs-check (single-leg, vendor self-report, no method) |

> **Claims 48-55 arrive with no measurements, and that is load-bearing.** S6's three eval charts are
> client-rendered and did not survive capture, so every performance statement in the source reduces to
> "improves" or "a substantial lift". These are **design arguments corroborated by product
> screenshots** - the UI is real second-leg evidence that the described affordances shipped, but it
> cannot show they work.
>
> **They also sit in unresolved tension with claim 24.** That claim - the only *measured* evidence in
> this brain about agent memory - found naive episodic memory scaffolding never improved long-horizon
> reliability and **hurt 6 of 10 models**. S6 is best read as arguing that append-everything episodic
> memory is precisely the broken design (claims 48, 52) and that maintained synthesized memory is a
> different object. **That argument is entirely unmeasured, and must not be resolved in the vendor's
> favour.** See [`topics/memory.md`](topics/memory.md).

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
> **S5** = `sources/260726_dont-ship-skills-without-evals/` (Philipp Schmid, Google DeepMind, "Don't
> Ship Skills Without Evals", AI Engineer World's Fair 2026). **T4 conference talk by a T2 vendor
> employee.** Its numbers split into two credibility classes that must never be quoted as one:
> **SkillsBench** (claims 41, 42) is a **public third-party benchmark** and is the strongest evidence
> in this brain that is not peer-reviewed; the **DeepMind-internal** figures (claim 46, the
> 39.2% -> 91.6% case study) are self-reported, single-case and unreplicated.
> **S6** = `sources/260731_chatgpt-memory-dreaming/` (OpenAI, "Dreaming: Better memory for a more
> helpful ChatGPT", 2026-06-04). **T2 vendor post about its own consumer product.** Its mechanism
> claims carry a genuine second leg - product screenshots are a photograph of the artifact the prose
> describes, not the author restating himself - but **its three eval charts are client-rendered and
> did not survive capture, so the source contributes no measurement whatsoever.** Cite it for
> architecture and failure taxonomy; never for magnitude.
> **R1** = deep-research pass `sources/260725_12-factor-agents/context/01_context-limits-and-decomposition.md`
> (2026-07-25) - external evidence, each citation tiered T1-T5 with an independence call.

> **Claims 11 and 17 are corroborated by a second *ingested* source.** Claim 11: two talks, one
> arguing from first principles and one reporting production practice. Claim 17 gained S5 on
> 2026-07-26 - a talk about *skills* landing on the same boundary as a talk about *agents*, which is
> the more interesting of the two convergences because the authors were not addressing the same
> question. Shared weakness: all are practitioner talks by people selling adjacent products, none
> with measurements - convergence, not replication.
>
> **Claims 44 and 45 instrument claim 31.** S4 named the principle (harness assumptions expire) but
> offered only "remove one component at a time"; S5 supplies the ablation test that turns it into a
> measurement, and adds the part S4 lacks - keep the eval after removing the part, so a reversal is
> detectable. This is the brain's first case of one source supplying the *method* for another
> source's *principle*.
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
