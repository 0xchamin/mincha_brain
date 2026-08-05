# Topic: Context engineering

**Status:** established (10 sources - S2 12-factor agents, S4 Anthropic harness design, **S8 LLM Wiki
(a partial feeder, 2 claims)**, **S9 Agent Framework (a partial feeder, 1 claim)**, **S10 Tool search
(a partial feeder, 2 claims - and the first *measurement* of a claim S9 could only place)**, **S11
agent-first data stack (4 claims - the first source here where the context is written for a
*proprietary business domain* rather than for a codebase or a tool catalog)**, **S12 multi-tenant
reference architecture (a partial feeder, 1 claim - the token cap read as a loop guard rather than a
budget)**, **S13 `karpathy/autoresearch` (a partial feeder, 1 claim - the *per-iteration* budget of
an unattended loop, which is the first time this note has had to think about a multiplier)**, **S18
CaMeL (a partial feeder, 1 claim - the strictest statement here of *who may write into the context
window*, and the first arguing it from authority rather than from attention)**, **S21 Spotlighting (a partial feeder, 1 claim - provenance as a property of the tokens themselves)**; plus
the R1 research passes). **Basis for the promotion:** S4
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

**And there is a third reason to cap the budget that has nothing to do with quality: a token limit is
the cheapest available loop guard.** S12 files a "session maximum token limit" under cost optimisation
and states its purpose as "to help prevent **infinite loops** and to help control costs"
([S12](../../sources/260802_gcp-multi-tenant-agentic-ai/LEARNING.md) `n17`, claim 109). That is a
different argument from either of the two above: it terminates a runaway **without having to detect
that the runaway is a loop**, which is the hard part. Worth keeping as the crude backstop underneath
whatever loop detection you build, never as a substitute for it. S12's neighbouring levers - summarise
older turns with a model, prune tool outputs down to the fields actually needed - restate claims 85 and
90 from a third vendor with a **cost** motive rather than a quality one: mild independent support for
the practice, and none at all for the rationale. `single-leg`, T2, unmeasured.

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

### Metadata becomes a control surface the moment an agent reads it

**This note's most robust claim now rests on three unrelated sources, and none of them set out to make
it** (claim 93). Each found the same thing in a different domain:

| Source | The field | What it turned out to be |
|---|---|---|
| S5 | a **skill's** description | the **trigger** - and the cause of 50%+ of all skill failures (claim 43) |
| S10 | a **tool's** name and description | **ranking features** in a retrieval index, so the first tuning pass is editorial (claim 88) |
| S11 | a **column's** description | a **default policy** the agent applies |

S11's before-and-after is the clearest illustration in this brain. `account_status: The status of the
account.` becomes a paragraph naming the system of record, enumerating each value's *business*
meaning, and then issuing an imperative: "**For customer reporting, filter to Active unless the
analysis explicitly includes churned or prospective accounts**" [S11 §How we define the data models,
`n3`]. The stated purpose is to prevent "a technically correct answer based on the wrong business
interpretation" - the failure that looks exactly like success.

**The generalisation: a metadata field written for a human to skim is being promoted to a control
surface, and nobody notices until an agent reads it.** In all three cases the incumbent vocabulary is
the failure - implementer shorthand ("get", "manage", "REST API") in S10, "the status of the account"
in S11 - because it was written for a reader who already knows the answer.

> **This is the first claim in this note with external measurement behind it that is not about token
> budgets.** Documented columns are worth **+20% accuracy on completely uninformative column names**
> ([arXiv:2408.04691](https://arxiv.org/abs/2408.04691), T3, BIRD-Bench), and - the finding worth
> keeping - descriptions annotators judged **"superfluous" outperformed manually curated gold ones**.
> Write more than feels necessary. See [S11 R1 F1](../../sources/260802_agent-data-stack/context/01_data-agent-accuracy-and-prior-art.md).

### Sort context by the question it answers, not by the tool that stores it

S11 supplies this note's first **decomposition of a context layer into stores** (claim 92), and its
value is that the split is by *question*, not by technology [S11 §How we think about context,
`visuals/fig3`, `n2`]: what is this data (column definitions), what does this metric mean (semantic
model), how does this business work (prose guides), which source do I trust (endorsements), how is
this number computed (the transformation repo).

The discipline is in the negative form. **A layer that cannot name a question only it can answer is a
duplicate - and duplicated context is worse than missing context, because the two copies drift.** A
column description structurally cannot say which of three ARR dashboards is canonical: that is a fact
about the *relationship* between assets, not about any one of them.

Two connections back into this note. First, S11's "workspace guides" - versioned prose in a git repo,
carrying business rules that fit no schema field - are the **contract document** of claim 68 applied
to a business domain instead of a codebase, and the author independently calls them "like skills for
the data agent" [`n5`]. Second, and less comfortably, **all five stores are prose**. The layer that
made a 3-person team's knowledge reachable by everyone in the company contains no new machinery at
all.

### The head/tail split is universal; its treatment inverts with whichever resource is scarce

S10 and S11 give **opposite** prescriptions on the same distribution, and both are right (claim 99):

- **S10: retrieve the tail, pin the head.** The binding cost is **tokens**. Indexing the tail is
  nearly free once the index exists, so the tail gets retrieved and the head gets pinned - pinning
  protects what must never be missed, and keeps the prefix cacheable [S10 `n16`].
- **S11: curate the head, defer the tail.** The binding cost is **human authorship**. Every tail item
  is a definition a person writes, reviews and maintains forever, so covering "roughly 80% of the
  questions people ask" first is the only affordable order [S11 §Start with the questions that matter
  most, `n11`].

**The question is never "head or tail". It is "what runs out first - context window or people".**

And when the answer is people, the constraint is softer than it looks: MotherDuck generated schema
descriptions **from the query log** for roughly **$0.50 per warehouse**, and those generated
descriptions produced a **+16pp** accuracy gain on a real warehouse (T2, [S11 R1
F2](../../sources/260802_agent-data-stack/context/01_data-agent-accuracy-and-prior-art.md)). **The
first draft of the long tail can be machine-written from usage; only the genuinely ambiguous cases
need the expert** - which is precisely where the same study found LLM generation falls down.

### The loop that maintains context writes context, not answers

S11 is the first source here to describe the **maintenance** side of a context layer as an operating
routine rather than an aspiration (claim 97). Observability over agent conversations yields a
symptom-to-layer triage rule, and the loop's output is a write back into the store - never an answer
to a user [S11 §How we improve the system, `visuals/fig3`, `n7`, `n8`].

> ⚠️ **The source's own architecture figure omits the human, and the omission matters.** The prose
> insists that only the data team may set trust flags and that endorsed assets need review before
> changes ship; in the figure, the feedback arrow runs from usage trends straight back into the store
> with no review step [`d2`]. Build it as drawn and you get a loop with no ground truth: usage
> promotes a source, promotion increases usage. **The one control that makes the design safe is the
> one the diagram leaves out.**

This is claim 59's shape (a loop holding two objectives trades them off silently) arriving in a new
place - and note that S11 resolves it the way [`memory.md`](memory.md) predicts, by putting the
curation in a separate loop run by different people on a different cadence.

### In a loop, the budget is per-iteration and the cost is multiplied

Everything above treats context as a budget for **a** call, or for a session. S13 is the first source
here where the same tokens are spent **once per iteration of a loop that runs about a hundred times
unattended**, and that changes which number you design against.

Its answer is aggressive and worth copying wholesale [S13 `n8`, claim 118]. A five-minute training
run is compressed to roughly **two lines** before it re-enters the agent's context, by three
mechanisms that all push the same way:

- **The artifact's log is one line.** Progress is printed with a carriage return and no newline, so
  a run of ~950 steps collapses to a single rewritten line rather than 950 of them
  [`train.py:590`].
- **Streaming is forbidden.** "redirect everything - do NOT use tee or let output flood your context"
  [`program.md:99`] - an instruction against a *convenience*, since `tee` is exactly what you would
  reach for to watch a job while capturing it.
- **The result is grepped, not read.** Two fields out of a nine-field summary block, with the full
  log opened only on failure and only its last fifty lines [`program.md:100-101`].

The enabling design is that the artifact was given a **machine-readable reporting interface** - nine
`key: value` lines with stable prefixes, existing to be grepped [`train.py:621-630`]. The thing being
driven was modified so the driver never has to parse prose.

**Two transfers.** First, **the per-iteration figure is the one to design against, because the
multiplier is the iteration count**: 500 wasted tokens per experiment is 50,000 across a night, and
unlike a one-off cost it competes directly with the thing you actually want resident, which is the
history of what has already been tried. This specialises claim 22 (limiting context beats filling it)
to the loop case. Second, **absence of output is a zero-cost error signal** - "if the grep output is
empty, the run crashed" is the entire exception handler, with no exit-code check and no structured
error, paired with a fast-fail inside the artifact that kills a diverged run rather than spending the
remaining budget [S13 `n17`].

> **Note what S13 does *not* do, because it is the gap this note would flag.** Nothing is carried
> between iterations except a five-column TSV. There is no compaction strategy, no summarisation, no
> retrieval over past experiments - the agent's accumulated reasoning simply lives in its context
> until the session ends and is then gone [S13 `g1`]. S13 solves the per-iteration *input* cost and
> ignores the cross-iteration *memory* problem entirely. See [`memory.md`](memory.md) for the half
> it leaves out.

### The strictest possible answer to "who may write into the context window"

This note's premise is that context engineering is one problem - deciding which tokens reach the
model. **S18 is the first source here to answer it as a security property rather than a quality one**,
and its answer is more restrictive than anything else in this note
([S18](../../sources/260804_camel-prompt-injection-defense/LEARNING.md) `n3`, `n4`, claim 151).

Two rules do the work. The planning model **never sees tool output at all** - values returned by tools
go into variables, and the planner manipulates the variable while never reading its contents. And the
model that *does* read untrusted data may return **only schema-conforming structured output plus one
boolean**, with no free-text channel back, because a natural-language reply would carry an injection
straight into the planning context.

Sit with the second rule, because it is the one a working engineer would delete first. Letting the
parser say "I could not find the address, try searching the archive" is an obvious usability
improvement and CaMeL forbids it explicitly, on the grounds that it "could be a vector for prompt
injections" (S18 `n4`). **The convenience feature and the vulnerability are the same feature**, which
is the sharpest instance in this note of context admission being a decision with consequences rather
than a plumbing detail.

> **Read against claim 22, and notice they are different arguments for the same discipline.** Claim 22
> says limiting context beats filling it, for *attention* reasons - the model degrades as the window
> fills. S18 says limiting context beats filling it for *authority* reasons - text in the window is
> indistinguishable from instruction. **Both conclude that what you exclude is the design, and neither
> needs the other to be true.**

The mechanism generalises past this architecture. Once a value's provenance is tracked, "which tokens
reach the model" stops being a single decision made at prompt-assembly time and becomes a property
carried by each value through the whole execution (S18 `n5`, `n7`). That is a stronger form of context
ownership than anything else this note holds, and its cost is measured: **2.82x input tokens** for the
median task (claim 154).

### Provenance is a property of the tokens, not of the prompt structure

This note has always framed the question as *which tokens reach the model*. S21 adds a dimension it
did not have: **how those tokens are written carries security meaning independent of what they say**
([S21](../../sources/260805_spotlighting/LEARNING.md) `n5`, claim 170).

The technique is small. Interleave a marker token throughout untrusted text - `In^this^manner^Cosette`
- and tell the model in the system prompt that this transformation happened. Attack success falls from
about 50% to 3.1%, and **task accuracy is unchanged** across SQuAD, sentiment, WiC and BoolQ (claim
170). The model reads mangled text as competently as clean text, which is the surprising half.

The design lesson is why marking the **body** beats marking the **edges**. Delimiters put the
provenance signal at the boundaries, where an adversary who knows the convention can forge one.
Datamarking makes provenance a property of every token, so forging it requires knowing the marker.
**A boundary an attacker can forge is not a boundary**, and this note should generalise that past
security: any structure you impose on the context window that an untrusted source can reproduce is
decoration.

> **Read against claim 22 and claim 151 together, because the three are different arguments for the
> same discipline.** Claim 22 limits context for **attention** reasons - the model degrades as the
> window fills. Claim 151 restricts who may write into it for **authority** reasons - text in the
> window is indistinguishable from instruction. S21 adds a third: **the same tokens carry different
> meaning depending on how they are marked**, so the window's *encoding* is a design surface and not
> just its contents.

Full synthesis in [`agent-security.md`](agent-security.md), including where this sits among the other
defences and why its own authors call it in-band signalling.

## Key claims

| Claim | Sources (cited) | Confidence |
|---|---|---|
| LLMs are stateless pure functions; input-token quality is the only lever on output quality short of retraining. | S2 `&t=547s` | emerging |
| **In an unattended loop the context budget is per-iteration and its cost is multiplied by the iteration count** (claim 118). S13 compresses a 5-minute run to ~2 grepped lines via a single-line log, a prohibition on `tee`, and a greppable summary block. Corollary: **empty output is the error signal**, costing zero tokens in the common case. | S13 (`program.md:99-101` + `train.py:590`,`:621-630`,`:570-572` @ `228791f`, `n8`, `n17`) | corroborated (docs+code). Specialises claim 22 to the loop case |
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
| **Metadata written for humans becomes a control surface the moment an agent reads it**, and the incumbent human-facing vocabulary is the dominant failure. A skill's description is its trigger; a tool's description is a ranking feature; a column's description is a default policy the agent applies. | **S5 (claim 43) + S10 (claim 88) + S11 §How we define the data models (`n3`)**, measured by [arXiv:2408.04691](https://arxiv.org/abs/2408.04691) (T3) via S11 R1 F1 | **corroborated (3 sources + external measurement)** - the best-supported claim in this note |
| **Sort context by the question it answers, not by the tool that stores it.** Five stores, five questions no other store can answer. A layer that cannot name a question only it can answer is a duplicate, and duplicated context drifts. | S11 §How we think about context + `visuals/fig3` (`n2`) | emerging (single-leg on one company's design; the *decomposition* is corroborated by `fig3`, its *sufficiency* is not) |
| **The head/tail split is universal but its treatment inverts with whichever resource is scarce** - retrieve the tail when tokens bind (S10), defer the tail when human authorship binds (S11). | **S10 (`n16`) + S11 §Start with the questions that matter most (`n11`)** | **corroborated as a pattern across 2 sources reaching opposite prescriptions**; each prescription is single-leg in its own source |
| **The output of a working context loop is a write to the context store, not an answer** - which converts a service team into maintainers. Remove the human from that loop and it self-reinforces with no ground truth. | S11 Key Takeaways + `visuals/fig3` (`n8`, `d2`) | emerging - mechanism corroborated, organisational consequence prose-only, self-reinforcement risk is this brain's reading of `d2` |
| **An "agent-first" data layer turned out to be a documentation layer over an unchanged pipeline.** Check whether any box moved or only the documentation did. | S11 §Closing + `visuals/fig2` (`n1`, `d1`) | emerging (single company, and the reading is the figure's, not the prose's) |
| **A session token cap is a loop guard filed under cost** - it terminates a runaway without having to detect that the runaway is a loop, which is the hard part. The crude backstop under whatever loop detection you build. | S12 `n17` (claim 109) | needs-check (single-leg, T2, unmeasured) |

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
- **S11** - [How we built LangChain's agent-first data stack](../../sources/260802_agent-data-stack/LEARNING.md)
  (Emily Hawkins, LangChain, 2026-07-27) - **contributing four claims**, and the first source here
  where the context is written for a **proprietary business domain** rather than a codebase or a tool
  catalog: the five-store decomposition by question, a column definition carrying a default policy,
  the head/tail inversion against S10, and the maintenance loop whose output is context rather than
  answers. **T4 practitioner experience on a T2 vendor blog, n = 1 company, nothing measured** - but
  its central mechanism is measured externally by parties with no stake in it (R2).
- **S12** - [Multi-tenant agentic AI system](../../sources/260802_gcp-multi-tenant-agentic-ai/LEARNING.md)
  (Google Cloud Architecture Center, reviewed 2026-06-18) - **a partial feeder, one claim.** Its
  context-management advice sits in a **cost** section, which is the interesting part: summarisation and
  tool-output pruning arrive here from a vendor with a billing motive rather than a quality one, and the
  session token cap turns out to be a loop guard wearing a budget label (claim 109). **T2, unmeasured,
  and it corroborates the practice of claims 85 and 90 without touching their rationale.** Full synthesis
  in [`agent-security.md`](agent-security.md), which is where most of that source lives.
- **S13** - [`karpathy/autoresearch`](../../sources/260803_autoresearch/LEARNING.md) (Andrej
  Karpathy, code, snapshot `228791f`, 2026-03-26) - **a partial feeder, contributing one claim**: the
  per-iteration context budget of an unattended loop (claim 118), which is the first time this note
  has had a *multiplier* to reason about rather than a single window. Unusually for this note, the
  claim is read off code rather than asserted in prose. Full synthesis in
  [`autonomous-research-loops.md`](autonomous-research-loops.md). **⚠️ T4 personal repository; the
  design claims pass the docs-vs-code gate, the results are one unreproducible PNG.**
- **R1** - [deep-research pass on S2](../../sources/260725_12-factor-agents/context/01_context-limits-and-decomposition.md) (2026-07-25) - external evidence: Lost in the Middle (T1), Context Rot (T2), Anthropic context engineering (T2), Beyond pass@1 (T3), Event Sourcing (T1). Each citation carries a tier and an independence call.
- **R2** - [deep-research pass on S11](../../sources/260802_agent-data-stack/context/01_data-agent-accuracy-and-prior-art.md)
  (2026-08-02) - external evidence for the metadata-as-control-surface claim: MotherDuck
  query-log-informed schema descriptions (T2, +2pp on a benchmark vs +16pp on a real warehouse),
  [arXiv:2408.04691](https://arxiv.org/abs/2408.04691) (T3, +20% on uninformative column names),
  Spider 2.0 (T1/T3, the accuracy ceiling), Power BI endorsement (T1, prior art), Feigenbaum's
  knowledge acquisition bottleneck (T1, 1977). Tiers and independence calls recorded in the note.
