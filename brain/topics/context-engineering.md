# Topic: Context engineering

**Status:** emerging (1 source -> established at 2+ corroborating sources)

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
| Owning the serialisation is the precondition for pausing/resuming an agent. | S2 `&t=460s` | emerging |
| Limiting context beats filling it: a 2M-token window returns an answer, not a better one. | S2 `&t=388s` | emerging |
| Compact errors - clear pending errors after a valid tool call, summarise instead of dumping stack traces - or the agent spins out. | S2 `&t=653s` | emerging |

## Key visuals

![Everything is Context Engineering: Prompt, Memory, RAG](../../sources/260725_12-factor-agents/visuals/frame_620.jpg)
> The unifying claim: four apparent subsystems, one question. S2 `&t=616s`.

![class Thread with events List[Event]; event_to_prompt renders each event as an XML-ish block; thread_to_prompt joins them](../../sources/260725_12-factor-agents/visuals/frame_590.jpg)
> Owning the context window in practice - typed events, your own serialisation. S2 `&t=563s`.

![Trace showing slack_message, request_human_input with options, human_response approved, then deploy_backend](../../sources/260725_12-factor-agents/visuals/frame_712.jpg)
> The same event format carrying a human turn - human input is not a special case. S2 `&t=687s`.

## Open questions / conflicts

- **Single source so far.** Everything here comes from S2; the topic stays `emerging` until a second,
  unrelated source corroborates. S2's own external leg is the author's own repo, so it is not
  independent (S2 `nodes.md` `en1`).
- **No measurements anywhere.** "Limit the tokens and reliability improves" is asserted, never
  quantified - no benchmark, ablation or failure rate. Actively worth seeking a source with data,
  because this claim is testable and load-bearing.
- **Unresolved: where compaction should live.** S2 says summarise errors but does not say by what -
  a second LLM call, a heuristic, or hand-written rules - nor how to avoid summarising away the
  detail that would have fixed the bug.
- **Overlap with `rag.md` needs watching.** As RAG sources arrive, retrieval strategy claims belong
  there; only the "which tokens win the budget" framing belongs here. Revisit the split if the two
  notes start duplicating (see ADR-0001).

## Sources feeding this topic

- **S2** - [12-Factor Agents: Patterns of reliable LLM applications](../../sources/260725_12-factor-agents/LEARNING.md) (Dex Horthy, HumanLayer, AI Engineer WF 2025) - factors 2, 3, 9 and the "everything is context engineering" framing.
