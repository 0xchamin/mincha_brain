# Topic: Context engineering

**Status:** established (5 sources - S2 12-factor agents, S4 Anthropic harness design, **S8 LLM Wiki
(a partial feeder, 2 claims)**, **S9 Agent Framework (a partial feeder, 1 claim)**, **S10 Tool search
(a partial feeder, 2 claims - and the first *measurement* of a claim S9 could only place)**; plus the
R1 research pass). **Basis for the promotion:** S4
independently arrives at S2's serialisation claim from the opposite direction - S2 argues you should
own the thread format so you *can* pause and resume; S4 needs exactly that artifact to make context
resets work [S4 §2]. Most of S4's other context claims are new and `single-leg`, not corroborating.
**S8 corroborates nothing here** - it contributes two new claims (the contract document as the
persistent counterpart to owning the prompt; the two-pass text-then-images constraint) and is T4 and
unmeasured. It does not move the status, which S2 and S4 already carried.

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

### Context management as middleware, not as ad-hoc prompt work

A small but useful reframing from S9, and it is a **placement** claim rather than a technique. In its
harness inventory, `context compaction`, `tool selection` and `permissions` sit together in a column
labelled **Middleware** [S9 `fig_AgentHarness`] - the same architectural slot as request logging or
auth in an ordinary web stack: cross-cutting, applied uniformly on every pass through the loop,
configured once rather than reasoned about per call.

**Why that placement earns a paragraph.** Everything else in this note is something you do while
authoring a call - choose the tokens, model the thread, compact the errors. Middleware is the claim
that some of it should stop being authored at all and become policy the loop applies for you. S9 says
the same thing in prose about the loop generally: making the loop explicit gives you **a consistent
place to apply controls** - limit which tools an agent may call, require approval for certain
actions, compact context when conversations grow, log every step [S9 §Agent loops].

`tool selection` is the item worth noticing: choosing *which subset of the available tools reaches the
model on this call* is treated as a context-window decision, which is exactly the framing claim 20
argues for - prompt, memory, RAG and history are one problem, and so, it turns out, is the tool list.
**Figure-only in S9** - its prose never mentions tool selection.

> **Do not read the placement as a recommendation to adopt a middleware stack.** S9 is an SDK vendor
> and this is its product's shape. The transferable part is the *distinction* - authored per call vs
> applied as policy - not the packaging.

### The tool list is a context-budget line item, and it is now measured

~~No source in this brain measures tool selection.~~ **Closed by S10 (2026-08-01)**, which is about
nothing else. Two things it settles, and one it opens.

**Settled: the tool manifest is resident context whose size tracks the catalog, not the task.** A
hundred tools makes every turn open with "thousands of tokens of names, descriptions, JSON schemas,
argument definitions, and nested parameters before you've asked anything useful" [S10 §intro, `n1`].
Measured on ToolRet (44,000+ tools): **541k tokens of manifest at 1,180 tools** [S10
`fig_tokens-chart`, `n9`].

**Settled: deferring the manifest and retrieving into it decouples context cost from catalog size.**
Replacing `tools/list` with two meta-tools - a search and a dispatcher - cut that 541k to **15k, a 36x
reduction**, and the chart shows the shape the prose undersells: the tool-search series is roughly
**flat** across a 24x increase in catalog size while the baseline climbs [S10 `fig_tokens-chart`,
`n10`]. The transferable claim is not "tools got cheaper" but **catalog size stops being a
context-budget decision**.

**The distinction this note already cared about, restated in tokens:**

| | Cost per turn | Attention cost |
|---|---|---|
| Full manifest, no caching | full price | full |
| Full manifest, **prompt caching on** | ~90% cheaper | **unchanged** |
| Manifest deferred behind search | ~3% of baseline at scale | ~3% |

**The middle row is the one that matters here.** "Caching isn't the same as not loading... cached
context **still competes for the model's attention**" [S10 §The default agent tax, `n2`]. That is this
note's central measured finding stated by an independent vendor: degradation tracks what is **in** the
window, not what it cost to put there. A cached manifest is a fully-priced attention liability at a
90% discount on the invoice.

> 💡 **Prompt caching** - reusing an unchanged prompt prefix so the provider charges a fraction of the
> input price for it. It buys money and latency, never attention.

**Opened: what the tail of the distribution costs.** S10's own retrieval numbers are Recall@10 of
39-46% against a default shortlist of five [S10 Figure 3, `n11`]. Deferring the manifest is a token
win of a size nothing else in this brain matches; whether it is a **reliability** win depends on a
retrieval quality the source measures and then does not discuss. See [`rag.md`](rag.md), which owns
the retrieval half, and the open question below.

**And the corollary for the head of the distribution:** what must never be missed does not get
retrieved at all, it gets **pinned** - which is also what keeps the prompt prefix stable enough for
caching to work [S10 §Search is for the long tail, `n16`, `n17`]. **Prefix stability is a context
design constraint, not a billing detail**: it decides where in the window a dynamic list may sit.

### The prompt you own for one call has a persistent counterpart: the contract document

S2's rule is about the tokens in a single call. **S8 pushes the same idea onto a file that persists
across every call**: the schema document - "e.g. CLAUDE.md for Claude Code or AGENTS.md for Codex" -
that tells the model how the store is structured, what the conventions are, and what workflow each
operation follows. It is "**the key configuration file - it's what makes the LLM a disciplined wiki
maintainer rather than a generic chatbot**" [S8 §Architecture, `n5`].

Two things make this worth keeping rather than filing as trivia:

- **It is an unusual answer to *where the difficulty lives*.** Asked what makes an LLM knowledge
  system work, the expected answers are the retrieval stack, the chunking, the embedding model. S8
  says none of them - the load-bearing artifact is **prose**.
- **It is the only layer both parties write.** Raw sources are immutable and the wiki is the LLM's;
  the schema is explicitly "**co-evolved**" [`n4`]. That makes it the place where a correction to
  *behaviour* - as opposed to a correction to a *fact* - can actually be recorded and survive.

The same source turns this into a claim about how such designs should be **shipped**: as
"intentionally abstract" prose sized for an agent's context window, deliberately underspecified so
the reader's own agent instantiates it [`n16`]. **The artifact distributed is a context document, not
a library** - which is what makes the schema file the place instantiation lands.

> ⚠️ **Unmeasured, and self-descriptive.** S8 is a practitioner describing a workflow he already
> prefers, with no evaluation of any kind. The framing is valuable; the confidence is not earned.

### A mechanical constraint: text and its inline images cannot be read in one pass

"LLMs can't natively read markdown with inline images in one pass - the workaround is to have the LLM
read the text first, **then view some or all of the referenced images separately**" [S8 §Tips and
tricks, `n12`].

This is a constraint on what can reach the model per call, not a preference, and it forces a two-pass
shape on any document with figures. Note the selectivity - "**some or all**" - which makes the second
pass a **budget decision**, not a completeness one: you choose which images are worth the tokens.

> This brain's ingest flow is an independent instance of exactly that shape - read the transcript or
> article text, then `view` a pre-filtered handful of frames - arrived at for the same reason and
> costed the same way (`AGENTS.md`, "The visual leg"). S8 states the constraint that makes it
> necessary; it does not corroborate any claim about how well the two-pass split works.

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
| **The persistent counterpart to owning the prompt is the contract document** (`AGENTS.md` / `CLAUDE.md`) - "the key configuration file", and the load-bearing engineering artifact of an LLM knowledge system rather than the retrieval stack. It is also **the only layer both human and model write**, so it is where a correction to *behaviour* can persist. | S8 §Architecture (`n5`, `n4`) | needs-check (single-leg, T4, unmeasured, self-descriptive) |
| **Ship an agent-oriented design as deliberately underspecified prose sized for a context window**, to be instantiated by the reader's own agent - the unit distributed is a context document, not a library or a spec. | S8 §Note (`n16`) | needs-check (single-leg) |
| **Text and its inline images cannot be read in one pass** - read the text, then view selected images. A mechanical constraint that forces a two-pass shape on any document with figures, and makes the second pass a token-budget decision ("some or all"). | S8 §Tips and tricks (`n12`) | needs-check (single-leg) |
| **Some context management belongs in middleware, not in per-call authoring** - compaction, tool selection and permissions applied uniformly by the loop rather than reasoned about each pass. The explicit loop is what gives controls a consistent place to live. | S9 `fig_AgentHarness` + §Agent loops; **S10 is the same placement built and measured** (`n3`, `n9`) | emerging (two T2 vendors, independent of each other; still nothing comparing middleware to per-call authoring) |
| **The tool manifest is resident context that scales with the catalog, not the task** - 541k tokens at 1,180 tools - and **prompt caching makes it ~90% cheaper without making it cost less attention**. | S10 §intro + §The default agent tax + `fig_tokens-chart` (`n1`, `n2`, `n9`) | **measured** on the token counts (ToolRet); needs-check on the attention argument (single-leg, though it agrees with claim 27) |
| **Deferring the manifest behind a search tool decouples context cost from catalog size** - 36x fewer tokens at 1,180 tools, and roughly flat across a 24x catalog increase. The head of the distribution is **pinned** rather than retrieved, which is also what keeps the prompt prefix cacheable. | S10 `fig_tokens-chart` + §Search is for the long tail (`n9`, `n10`, `n16`, `n17`) | **measured** on tokens; the reliability half is unresolved - see `rag.md` and claim 87 |

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
  > **Refined, not contested (2026-07-31).** S6 ([`memory.md`](memory.md)) argues append-everything
  > episodic memory is precisely the broken design, and that a **maintained, synthesized** memory is a
  > different object (claims 48, 50, 52) - so it *agrees* with this finding's premise. Its own numbers
  > (claims 56-57) measure a **chat assistant's** recall and freshness, not an **agent's** task
  > reliability, so they do not speak to this bullet at all. **The rule stands unchanged: the measured
  > win on agent loops is decomposition, not remembering more.** What nobody has measured is whether a
  > *maintained* memory helps an agent - the open question worth carrying.
- **New, from R1: this design has an older name.** Modelling the thread as an append-only typed event
  log and replaying it is **Event Sourcing** (Fowler, 2005). Worth mining that literature for the
  three sharp edges it already names - replay determinism, snapshotting, event versioning - none of
  which S2 mentions.
- **New, from S10: the token win on tool selection is huge and its reliability cost is unmeasured.**
  36x fewer tokens is the largest measured context saving in this note. But the same source reports
  Recall@10 of 39-46% with a default shortlist of five, and never asks what happens on a miss
  [S10 Figure 3, `n11`]. **Every technique in this note that removes tokens has this shape** - error
  compaction can summarise away the detail that would have fixed the bug, a context reset can drop
  state the handoff artifact failed to carry - and S10 is the first source that measures one side of
  the trade precisely while leaving the other side blank. Treat that as the pattern to watch, not as a
  fault unique to tool search.
- **Overlap with `rag.md` needs watching, and S10 is the first source to actually straddle the line.**
  Its retrieval mechanics (sparse vs neural reranking, Recall@k, index tuning) live in
  [`rag.md`](rag.md); its budget framing (the manifest as resident context, prefix stability) lives
  here. The two notes cite the same nodes for different purposes, which is the intended shape under
  [ADR-0001](../decisions/0001-context-engineering-topic.md) - revisit if they start restating each
  other rather than dividing the source.
- **Boundary with [`memory.md`](memory.md), set by [ADR-0007](../decisions/0007-memory-topic.md).**
  Claim 20 ("prompt, memory, RAG and history are one problem") absorbs memory into this note, and that
  remains true *as a framing*. The split is by question: **a claim about which tokens win a budget
  belongs here; a claim about what is stored between calls, when it is rewritten, and who repairs it
  belongs in `memory.md`.** Memory is an input to context engineering, not a subset of it - which is
  why nesting it here would invert the dependency. Same watch item as `rag.md`: revisit if the two
  notes start duplicating.

## Sources feeding this topic

- **S2** - [12-Factor Agents: Patterns of reliable LLM applications](../../sources/260725_12-factor-agents/LEARNING.md) (Dex Horthy, HumanLayer, AI Engineer WF 2025) - factors 2, 3, 9 and the "everything is context engineering" framing.
- **S4** - [Harness Design for Long-Running Application Development](../../sources/260725_harness-design-long-running-apps/LEARNING.md) (Prithvi Rajasekaran, Anthropic Labs, 2026) - the serialisation artifact that makes context resets work, **context anxiety**, and compaction-vs-reset. **T2 vendor, n=1 self-reported runs, visual leg skipped** - mechanisms transfer, numbers are not replicated. *(Row added 2026-07-31: S4 was named in this note's status line and cited by two claims but had no row here - an orphan of exactly the class [ADR-0009](../decisions/0009-dreaming-reconciliation-pass.md) exists to catch, found incidentally while ingesting S8.)*
- **S8** - [LLM Wiki](../../sources/260731_llm-wiki/LEARNING.md) (Andrej Karpathy, 2026-04-04) - **a partial feeder**, contributing two claims only: the schema document as the load-bearing artifact, and the mechanical two-pass constraint on markdown with inline images. **T4, unmeasured, no figures** - read it for the framing, never as evidence.
- **S9** - [Inside the Microsoft Agent Framework](../../sources/260801_agent-framework-layered-sdk/LEARNING.md) (2026-05-28) - **a partial feeder, contributing one placement claim**: compaction, tool selection and permissions as **middleware** applied by the loop rather than authored per call. Also the only mention of *tool selection* anywhere in this brain, and it is figure-only. **T2 vendor design post, nothing measured** - take the authored-vs-policy distinction, not the packaging.
- **S10** - [Tool search: Finding the right tool at the right time](../../sources/260801_tool-search-toolboxes/LEARNING.md)
  (Microsoft, 2026-07-29) - **a partial feeder, contributing two claims**, and the source that turns
  S9's figure-only `tool selection` box into a measured technique: the manifest as resident context
  (541k tokens at 1,180 tools), 36x reduction by deferral, caching as a price cut that is not an
  attention cut, and pinning as prefix-stability control. **T2 vendor post on its own preview
  product**, but the token result runs on a public benchmark (ToolRet). Its retrieval half belongs to
  [`rag.md`](rag.md).
- **R1** - [deep-research pass on S2](../../sources/260725_12-factor-agents/context/01_context-limits-and-decomposition.md) (2026-07-25) - external evidence: Lost in the Middle (T1), Context Rot (T2), Anthropic context engineering (T2), Beyond pass@1 (T3), Event Sourcing (T1). Each citation carries a tier and an independence call.
