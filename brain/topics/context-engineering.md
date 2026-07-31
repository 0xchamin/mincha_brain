# Topic: Context engineering

**Status:** established (2 sources - S2 12-factor agents, S4 Anthropic harness design; plus the R1
research pass). **Basis for the promotion:** S4 independently arrives at S2's serialisation claim
from the opposite direction - S2 argues you should own the thread format so you *can* pause and
resume; S4 needs exactly that artifact to make context resets work [S4 §2]. Most of S4's other
context claims are new and `single-leg`, not corroborating.

> Living, cross-source synthesis on context engineering. Many sources feed this note; **merge and
> de-duplicate** as they arrive (architect persona). Every claim cited.

## What this covers

Deciding **which tokens reach the model**, and how they are shaped: prompt authorship, context-window
construction and ownership, thread/event modelling and serialisation, token budget as a reliability
lever, error compaction, and what to drop or summarise. Deliberately the umbrella that treats prompt,
memory, RAG and conversation history as **one** problem rather than four subsystems.

> Relationship to neighbours: [`rag.md`](rag.md) is a *technique* within this umbrella (retrieval as
> one way of choosing tokens) and keeps its own note for chunking/embedding/reranking specifics.
> [`agents.md`](agents.md) owns the loop and control flow; this note owns what goes into the window
> each time round that loop. See [ADR-0001](../decisions/0001-context-engineering-topic.md) for why
> this was split out.

## Synthesis

### The premise

**LLMs are stateless pure functions - tokens in, tokens out.** Everything downstream follows from
that: the only lever on output quality, short of retraining, is care about the input tokens
[S2 `&t=547s`]. So prompt, memory, RAG and history are not four problems but one - "everything in
making agents good is context engineering" [S2 `&t=616s`].

### Own the prompt, token by token

A framework's prompt-builder will produce a genuinely good prompt fast - "you would have to go to
prompt school for like three months to build a prompt this good" - but past a quality bar you end up
writing **every single token by hand** [S2 `&t=531s`]. The honest position S2 repeats three times is
**"I don't know what's better, but I know you want to try everything"**: the value of owning the
prompt is not that hand-writing is inherently superior, it is that ownership is what makes the
knobs testable at all [S2 `&t=563s`].

### Own the context window: model the thread as typed events

You are not obliged to use the standard OpenAI messages format. Model the thread as a **list of typed
events** and stringify it however maximises density and clarity - S2's working example renders each
event as an XML-ish block (`<{event.type}>\n{data}\n</{event.type}>`) and joins them into a single
user message [S2 `&t=563s`]. At the moment you ask the model to pick the next step, your only job is
to tell it what has happened so far - the format is yours to choose.

Two consequences fall out of this that are easy to miss:

- **Pause/resume becomes possible.** Because you own the serialisation, you can interrupt a
  long-running call and write the context window to a store keyed by a state ID [S2 `&t=460s`]. You
  cannot do that with a context window you do not control.
- **Human turns stop being a special case.** A human's answer is just another typed event in the
  same thread, rendered the same way [S2 `&t=687s`].

### Token budget is a reliability lever, not a capacity limit

The naive loop appends everything and fails on longer workflows, principally because the context
window grows unboundedly [S2 `&t=371s`]. The nuance to keep: this is *not* "long context is
useless". You can put 2M tokens into Gemini and get an answer. The claim is that you will **always**
get tighter, higher-reliability results by controlling and limiting what goes in [S2 `&t=388s`].
Treat window size as a budget you spend deliberately, not a ceiling you fill.

**This is measured, and the measurements are harsher than S2's framing** [R1]. Degradation is not a
gentle slope you trade off against convenience - it is **non-uniform and adversarial**:

- **Position matters.** Performance "is often highest when relevant information occurs at the
  beginning or end of the input context, and significantly degrades" in the middle - a U-shaped curve
  reproduced across six model families ([Lost in the Middle](https://arxiv.org/abs/2307.03172), TACL,
  T1).
- **It starts early and hits simple tasks.** Isolating input length across 18 models, performance
  "varies significantly as input length changes, **even on simple tasks**" like retrieval and text
  replication; a 200K-window model can degrade materially by 50K
  ([Context Rot](https://www.trychroma.com/research/context-rot), T2).
- **There is a mechanism.** Attention is a finite **budget**: the transformer needs "every token to
  attend to every other token", giving "n² pairwise relationships for n tokens", so the ability to
  capture them "gets stretched thin" as context grows. Hence: find "the smallest possible set of
  high-signal tokens" ([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), T2).

> 💡 **Context rot** - the measurable decline in output quality as input length grows, independent of
> task difficulty. Not a capacity limit being hit; a gradient you are already on.

**The corollary S2 misses: decompose, don't remember.** The measured win is splitting long tasks into
short segments and restarting at each boundary (**+13.1 to +41.5 pp** reliability across 10 models);
a naive episodic memory scaffold "never improves long-horizon reliability, and hurts 6 of 10 models"
([Beyond pass@1](https://arxiv.org/abs/2603.29231), T3 preprint) [R1].

### Context anxiety: the failure that happens *before* the window fills

Everything above describes degradation caused by what is **in** the window. S4 names a separate
failure caused by what the model **believes about** the window [S4 §2]:

> 💡 **Context anxiety** - a model, sensing it is approaching its context limit, **prematurely wraps
> up**: declaring done, summarising, cutting scope. Behavioural, not capacity-driven, and it fires
> before the window is actually exhausted.

This matters because it changes which remedy works, and the two obvious ones are **not**
interchangeable [S4 §2]:

| | What it does | Effect on context anxiety |
|---|---|---|
| **Compaction** | Summarises earlier conversation in place | Preserves continuity, **does not remove it** |
| **Context reset** | Clears the window, restarts from a structured handoff | **Removes it**, at the cost of orchestration and a handoff artifact carrying enough state |

The reason compaction fails is worth holding: it reduces token *count*, but it is still the same
agent, mid-task, aware it has been running a long time. A reset produces an agent with no such
awareness - and **the handoff artifact becomes the load-bearing part**, which is exactly the
serialise-the-thread design above [S2 `&t=563s`]. Context resets are event-sourcing rehydration
under another name.

> ⚠️ **Model-version-bound.** S4 reports Sonnet 4.5 needing resets and Opus 4.5 largely eliminating
> the behaviour natively [S4 §2]. Treat this as a *class of failure to watch for* plus a technique,
> not as current guidance about any named model. Single-leg, vendor-reported, n=1, no external
> corroboration.

### Compact errors rather than appending them

The sharpest practical rule here. When a tool call fails, the naive move is to append the error and
retry - and doing that blindly is what makes agents **spin out**: lose the thread and get stuck.
Instead, once a valid tool call succeeds, **clear the pending errors**; summarise rather than pasting
the whole stack trace. "Figure out what you want to tell the model so you get better results"
[S2 `&t=653s`].

## Key claims

| Claim | Sources (cited) | Confidence |
|---|---|---|
| LLMs are stateless pure functions; input-token quality is the only lever on output quality short of retraining. | S2 `&t=547s` | emerging |
| Prompt, memory, RAG and history are one problem - which tokens reach the model. | S2 `&t=616s` | emerging |
| Past a quality bar you write every prompt token by hand; framework prompt-builders get you there fast but not past it. | S2 `&t=531s` | emerging |
| You need not use the standard messages format - model the thread as typed events and serialise for density and clarity. | S2 `&t=563s` | emerging |
| **Owning the serialisation is the precondition for pausing/resuming an agent** - and for context resets, where the handoff artifact must carry enough state for a fresh agent to continue cleanly. | **S2 `&t=460s` + S4 §2 (two sources, converging from opposite directions)** | **established** |
| Limiting context beats filling it: a 2M-token window returns an answer, not a better one. | S2 `&t=388s` | emerging |
| Compact errors - clear pending errors after a valid tool call, summarise instead of dumping stack traces - or the agent spins out. | S2 `&t=653s` + R1 (Anthropic names compaction a core technique, T2) | corroborated (external) |
| Context degradation is **non-uniform**: position-dependent (U-shaped), worsened by distractors, visible well before the advertised window. | R1 ([Lost in the Middle](https://arxiv.org/abs/2307.03172) T1; [Context Rot](https://www.trychroma.com/research/context-rot) T2) | **measured** |
| The measured win is **decomposition**, not memory: +13.1 to +41.5 pp reliability from short segments; naive memory scaffolds hurt 6 of 10 models. | R1 ([Beyond pass@1](https://arxiv.org/abs/2603.29231) T3 preprint) | needs-check (preprint) |
| The thread-as-event-log design is **Event Sourcing** (Fowler 2005), which already names its sharp edges: replay determinism, snapshotting, event versioning. | R1 ([Azure Arch Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) T1) | emerging |
| **"Context anxiety": a model may prematurely wrap up work as it nears its *perceived* limit** - a behavioural failure distinct from degradation caused by a full window. | S4 §2 | needs-check (single-leg, vendor, model-version-bound) |
| **Compaction and context reset are not interchangeable.** Compaction preserves continuity but does not remove context anxiety; a reset does, at the cost of a handoff artifact that must carry enough state to resume. | S4 §2 | needs-check (single-leg) |

## Key visuals

![Everything is Context Engineering: Prompt, Memory, RAG](../../sources/260725_12-factor-agents/visuals/frame_620.jpg)
> The unifying claim: four apparent subsystems, one question. S2 `&t=616s`.

![class Thread with events List[Event]; event_to_prompt renders each event as an XML-ish block; thread_to_prompt joins them](../../sources/260725_12-factor-agents/visuals/frame_590.jpg)
> Owning the context window in practice - typed events, your own serialisation. S2 `&t=563s`.

![Trace showing slack_message, request_human_input with options, human_response approved, then deploy_backend](../../sources/260725_12-factor-agents/visuals/frame_712.jpg)
> The same event format carrying a human turn - human input is not a special case. S2 `&t=687s`.

## Open questions / conflicts

- **A second ingested source has landed (S4), but it corroborates narrowly.** The bulk of this
  synthesis still rests on S2 plus the R1 external evidence - see
  [`../../sources/260725_12-factor-agents/context/01_context-limits-and-decomposition.md`](../../sources/260725_12-factor-agents/context/01_context-limits-and-decomposition.md).
  S4 confirms exactly one claim (serialisation as the precondition for resumption) and adds two new
  `single-leg` ones. **Do not read `established` as "well-evidenced throughout".**
- **Is "context anxiety" real and general?** S4 is the only source naming it, it is vendor-reported
  with n=1, and S4 itself says the behaviour largely disappeared between model versions [S4 §2]. It
  could be a genuine and important failure class, a one-generation artifact, or an
  anthropomorphic reading of ordinary output-length effects. **No external evidence either way** - the
  cleanest research target in this note.
- **Two distinct degradation stories now sit side by side.** R1's is *measured* and caused by what is
  in the window (position effects, context rot, the n² attention budget). S4's is *reported* and
  caused by what the model anticipates about the window. They are not the same phenomenon and should
  not be merged; whether they interact is unknown.
- ~~**No measurements anywhere.**~~ **Closed by R1 (2026-07-25).** The context claim is now the
  best-evidenced thing in the topic - and stronger than S2 stated it. See the measured version above.
- **Unresolved: where compaction should live.** S2 says summarise errors but does not say by what -
  a second LLM call, a heuristic, or hand-written rules - nor how to avoid summarising away the
  detail that would have fixed the bug. R1 partially helps: Anthropic names compaction as a
  technique, but likewise does not specify the mechanism.
- **New, from R1: the memory trap.** Naive episodic memory scaffolding **hurt 6 of 10 models** and
  never improved long-horizon reliability, losing to plain ReAct. Any future claim here that drifts
  toward "give the agent richer memory" must be checked against this - the measured win is
  *decomposition*, not *remembering more*.
  > **Now contested, and unresolved (2026-07-31).** S6 ([`memory.md`](memory.md)) argues that
  > append-everything episodic memory is precisely the broken design, and that a **maintained,
  > synthesized** memory rewritten by a background pass is a different object (claims 48, 50, 52).
  > **That argument carries no measurement** - S6's eval charts did not survive capture. So the
  > position stands: the measured evidence says memory scaffolds hurt, and the only source arguing
  > otherwise is a vendor with no numbers. **Do not resolve this in the vendor's favour.**
- **New, from R1: this design has an older name.** Modelling the thread as an append-only typed event
  log and replaying it is **Event Sourcing** (Fowler, 2005). Worth mining that literature for the
  three sharp edges it already names - replay determinism, snapshotting, event versioning - none of
  which S2 mentions.
- **Overlap with `rag.md` needs watching.** As RAG sources arrive, retrieval strategy claims belong
  there; only the "which tokens win the budget" framing belongs here. Revisit the split if the two
  notes start duplicating (see ADR-0001).
- **Boundary with [`memory.md`](memory.md), set by [ADR-0007](../decisions/0007-memory-topic.md).**
  Claim 20 ("prompt, memory, RAG and history are one problem") absorbs memory into this note, and that
  remains true *as a framing*. The split is by question: **a claim about which tokens win a budget
  belongs here; a claim about what is stored between calls, when it is rewritten, and who repairs it
  belongs in `memory.md`.** Memory is an input to context engineering, not a subset of it - which is
  why nesting it here would invert the dependency. Same watch item as `rag.md`: revisit if the two
  notes start duplicating.

## Sources feeding this topic

- **S2** - [12-Factor Agents: Patterns of reliable LLM applications](../../sources/260725_12-factor-agents/LEARNING.md) (Dex Horthy, HumanLayer, AI Engineer WF 2025) - factors 2, 3, 9 and the "everything is context engineering" framing.
- **R1** - [deep-research pass on S2](../../sources/260725_12-factor-agents/context/01_context-limits-and-decomposition.md) (2026-07-25) - external evidence: Lost in the Middle (T1), Context Rot (T2), Anthropic context engineering (T2), Beyond pass@1 (T3), Event Sourcing (T1). Each citation carries a tier and an independence call.
