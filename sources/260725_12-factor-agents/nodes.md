# Knowledge nodes - 12-Factor Agents (Dex Horthy, HumanLayer)

> Persona: **fact-checker** - re-adopt when working this file.

> The atomic units of knowledge extracted from this source. Each node has a **stable ID** (`n1`,
> `n2`, ... - never renumber; topic notes reference these), a claim, **both legs each with its own
> citation** (or one leg marked `single-leg`), a gate verdict, and a confidence. Only
> `corroborated`/`single-leg` nodes (and recorded `divergence` findings) feed `LEARNING.md` and get
> promoted to `../../brain/`. The **fact-checker** persona owns the verdicts; see `../../AGENTS.md`
> and `prd.md` §6.

Video base: `https://www.youtube.com/watch?v=8kMaTybvDUw&t=<s>s`
Canonical companion artifact: `github.com/humanlayer/12-factor-agents` README (content CC BY-SA 4.0).

## A note on the legs available here

This is a **slide-heavy conference talk**, so most nodes get the normal two internal legs
(narration <-> slide). Unusually, this source also has a **canonical external artifact** - the
open-source repo the talk is based on. Where a factor's number and title in the repo README match
what the talk says, that is a **second source**, not merely internal consistency, so those nodes are
gated `corroborated (external)`. See `en1` for why that mattered here.

## Nodes

| ID | Claim (crux) | Evidence leg + citation | Corroborating leg + citation | Gate | Confidence |
|---|---|---|---|---|---|
| n1 | Most production agents **are not very agentic** - they are mostly ordinary deterministic software with small LLM steps inside. The winning patterns were modular concepts retrofitted onto existing code, not greenfield rewrites, and need no AI background - "this is software engineering 101". | narration @ `&t=105s`..`&t=141s` (drawn from 100+ founders/builders interviewed) | `frame_800.jpg` - the worked example is bracketed top-left and bottom-right by labels reading "deterministic code" | corroborated | OK |
| n2 | **Factor 1 - Natural language to tool calls.** The single most magical LLM capability has nothing to do with loops, tools or agency: it is turning a sentence ("create a payment link to Terri for $750") into structured JSON. What you do with that JSON is a *separate* concern handled by the other factors. | narration @ `&t=229s` | `frame_290.jpg` - `class CreateIssue: intent "create_issue"` / `class SearchIssues: intent "search_issues"` typed structures | corroborated (external) | OK |
| n3 | **Factor 4 - Tools are just structured outputs.** "Tool use is harmful" - deliberately echoing *Go To Statement Considered Harmful* - aimed not at the capability but at the *abstraction*. There is no ethereal entity touching the world: the LLM emits JSON, deterministic code switches on it and maybe feeds a result back. Removing the magic restores ordinary engineering control. | narration @ `&t=247s`..`&t=299s` | `frame_290.jpg` (the JSON structures) + `frame_345.jpg` (the plain loop/`if` that consumes them) | corroborated (external) | OK |
| n4 | The **naive agent loop** - event -> prompt -> LLM picks next step -> append result to context -> repeat until `done` - is the right baseline abstraction but **does not survive longer workflows**, mainly because the context window grows long. You can push 2M tokens into Gemini and get *an* answer, but you get tighter, higher-reliability results by controlling and limiting what goes in. | `frame_345.jpg` - `while True: next_step = await llm.determine_next_step(context); context.append(...)`, exiting on `next_step.intent === "done"` | narration @ `&t=334s`..`&t=406s` | corroborated | OK |
| n5 | **Factor 8 - Own your control flow.** An agent decomposes into exactly four parts you should own: (1) a **prompt** that instructs how to select the next step, (2) a **switch statement** that dispatches on the model's JSON, (3) a **context-window builder**, (4) a **loop** with explicit exit conditions. Owning the loop is what lets you break, summarise, or insert LLM-as-judge mid-run. | narration @ `&t=406s`..`&t=423s` (enumerated aloud) | `frame_345.jpg` - all four are visible in ~10 lines of code; `frame_378.jpg` - the materialised DAG that loop produces | corroborated (external) | OK |
| n6 | **Factors 5 + 6 - Unify execution state with business state; launch/pause/resume via simple APIs.** Execution state (current step, next step, retry counts) and business state (messages, data shown to the user, pending approvals) should be one thing. Put the agent behind a REST or MCP endpoint; on a long-running tool call, **interrupt and serialise the context window to a DB keyed by a state ID**; on callback, reload by state ID, append the result, resume. **The agent never knows it was suspended.** | `frame_480.jpg` - `REST/MCP -> Launch -> Context -> Determine Next Step -> long running tool`, annotated "interrupt + serialize w/ stateID" | narration @ `&t=442s`..`&t=495s` ("the agent doesn't even know that things happened in the background") | corroborated (external) | OK |
| n7 | **Factor 2 - Own your prompts.** Framework prompt-builders give you a genuinely good prompt fast ("you would have to go to prompt school for like three months to build a prompt this good"), but past a quality bar you end up writing **every single token by hand**. Rationale: LLMs are pure functions, so the only lever on output quality - short of retraining - is care about the input tokens. | narration @ `&t=512s`..`&t=547s` | repo README **Factor 2 "Own your prompts"** (external artifact; the talk's own slide here is a title card) | corroborated (external) | OK |
| n8 | **Factor 3 - Own your context window.** You are not obliged to use the standard OpenAI messages format. Model the thread as a **list of typed events** and stringify it however maximises density and clarity - e.g. render each event as an XML-ish block and join them into a single user message. At the moment you ask "pick the next step", your only job is to tell the model what has happened so far. | `frame_590.jpg` - `class Thread: events: List[Event]`; `event_to_prompt` returns `f"<{event.type}>\n{data}\n</{event.type}>"`; `thread_to_prompt` joins them with `\n\n` | narration @ `&t=563s`..`&t=599s` | corroborated (external) | OK |
| n9 | **Everything is context engineering.** Prompt, memory, RAG and history are not four problems but one: which tokens reach the model. LLMs are stateless pure functions - tokens in, tokens out - so if you are not optimising the density and clarity of what you pass in, you are leaving quality on the table. | `frame_620.jpg` - "**Everything** is Context Engineering / Prompt / Memory / RAG" | narration @ `&t=599s`..`&t=616s` | corroborated | OK |
| n10 | **Factor 9 - Compact errors into the context window.** Blindly appending raw errors and stack traces is what makes agents **spin out** - lose context and get stuck. Instead: once a valid tool call succeeds, **clear the pending errors**; summarise rather than dumping the whole stack trace. Decide deliberately what to tell the model. | narration @ `&t=634s`..`&t=670s` (audience asked "anyone ever had a bad time with this?") | repo README **Factor 9 "Compact Errors into Context Window"**; the talk's slide here is the section header "What about Spin-Outs" | corroborated (external) | OK |
| n11 | **Factor 7 - Contact humans with tool calls.** Almost everyone in the wild ducks a key decision at the *first output token*: "tool call" vs "message to human". Make human contact an explicit intent **among** the tool options (`request_human_input`, `done_for_now`). Two payoffs: the model gets richer modes (done / need clarification / need a manager), and the intent rides on a **natural-language token the model actually understands** rather than a structural branch. | `frame_712.jpg` - trace showing `<request_human_input>` with `intent`/`question`/`context`/`options{urgency, format}`, then `<human_response> approved: true`, then `<deploy_backend>` | narration @ `&t=670s`..`&t=706s` | corroborated (external) | OK |
| n12 | **Factor 11 - Trigger from anywhere; meet users where they are.** People do not want seven tabs of ChatGPT-style agents open. Let them email, Slack, Discord or SMS the agent instead. | narration @ `&t=723s`..`&t=741s` | repo README **Factor 11 "Trigger from anywhere, meet users where they are"** (no dedicated content slide) | corroborated (external) | needs-check |
| n13 | **Factor 10 - Small, focused agents.** What actually works in production is **micro agents**: a mostly deterministic DAG with small agent loops of **~3-10 steps** dropped in at the hard points. HumanLayer's own deploy bot is the worked example - CI/CD is deterministic; once the PR is merged and dev tests pass, a small agent proposes deploy steps; a human approves or redirects in Slack ("can you deploy the backend API first"); control then returns to deterministic code for prod e2e tests, with a separate small rollback agent on failure. | `frame_800.jpg` - the full pipeline: `github PR merged -> deploy to dev -> e2e test dev` (deterministic) -> `determine next step` loop with `human approval` / `rejected` feedback edges -> `done` -> `e2e test prod -> deploy done` (deterministic) | narration @ `&t=741s`..`&t=793s` | corroborated (external) | OK |
| n14 | The payoff of small agents is **manageable context and clear responsibilities** - "100 tools, 20 steps, easy". The expected trajectory as models improve is not one giant agent but **starting deterministic and sprinkling LLM steps in**, widening their scope over time until a whole endpoint is agent-run - and you still need the engineering discipline to hit quality at each stage. | narration @ `&t=814s`..`&t=831s` | `frame_800.jpg` - the explicit "deterministic code" boundaries the agent loop sits between | corroborated | OK |
| n15 | **Find the bleeding edge.** The differentiator is choosing work that sits **right at the boundary of what the model can do reliably** - something it *cannot* get right every time - and then engineering reliability around it anyway. Do that and you have built something better than what everyone else is shipping. | `frame_855.jpg` - Usama Bin Shafqat (NotebookLM team, via Latent Space): "the most magical moments out of AI building come about for me when I'm really, really, really just close to the edge of the model capability" | narration @ `&t=831s`..`&t=865s` | corroborated | OK |
| n16 | **Factor 12 - Make your agent a stateless reducer.** The agent itself should hold no state; you own it and manage it however you like. (Horthy relays the pedantic correction that with multiple steps it is really a *transducer*.) | narration @ `&t=865s`..`&t=875s` | repo README **Factor 12 "Make your agent a stateless reducer"** (no dedicated content slide) | corroborated (external) | needs-check |
| n17 | **Not every problem needs an agent.** Horthy's first DevOps agent was handed a Makefile and told to build the project; it ran the steps in the wrong order. Two hours of increasingly specific prompting later - to the point of spelling out the exact build order - the honest conclusion was "I could have written the bash script to do this in about 90 seconds." | narration @ `&t=71s`..`&t=89s` | (anecdote, no slide) | single-leg | needs-check |
| n18 | The failure mode that motivates the whole talk: pick a framework, reach **70-80% quality** fast - "enough to get the CEO excited and get six more people added to your team" - then discover that clearing the last 20% means being **seven layers deep in a call stack** reverse-engineering how the prompt got built and how tools got passed in. Many people then throw it away and start from scratch. | narration @ `&t=37s`..`&t=55s` | (anecdote, no slide) | single-leg | OK |

## External corroboration (second source)

| ID | Finding | Citation |
|---|---|---|
| en1 | The repo README's canonical 12 factors match the talk's numbering **exactly**, including the ones delivered out of order: 1 Natural Language to Tool Calls, 2 Own your prompts, 3 Own your context window, 4 Tools are just structured outputs, 5 Unify execution state and business state, 6 Launch/Pause/Resume with simple APIs, 7 Contact humans with tool calls, 8 Own your control flow, 9 Compact Errors into Context Window, 10 Small Focused Agents, 11 Trigger from anywhere meet users where they are, 12 Make your agent a stateless reducer. | `github.com/humanlayer/12-factor-agents` README, fetched 2026-07-25; author Dex Horthy; code Apache-2.0, content CC BY-SA 4.0 |

> Why this mattered: the talk deliberately reorders and bundles factors - "if you want all 12 factors
> in order, that's a 30-minute talk, so we're going to bundle some stuff together" `&t=211s`. Mapping
> spoken content back onto factor numbers is exactly where a transcript-only ingest would guess
> wrong, so the README was fetched as an independent check on that mapping.

## Divergences and nuance (audit trail)

| ID | Finding | Citation |
|---|---|---|
| d1 | **Not an anti-framework talk**, despite how the repo tends to be read. Horthy explicitly reframes the 12 factors as "a wish list, a list of feature requests" - how can frameworks serve builders who need high reliability *and* speed? Recorded because the popular reading of the artifact diverges from the author's stated intent. | narration @ `&t=178s`..`&t=195s` |
| d2 | The proposed direction is **scaffold, not wrapper**: `create-12-factor-agent` modelled on shadcn/ui - scaffold the code out, then you own it - rather than a bootstrap that wraps an internal framework. Open question whether this holds up; the underlying trade-off is named in the talk as duplication vs abstraction (an old Ruby Conf argument). | narration @ `&t=875s`..`&t=900s` |

## Dropped (audit trail)

| Candidate | Verdict | Note |
|---|---|---|
| Repo traction (4k stars in a month or two, 14 contributors, HN front page, 200k impressions) | dropped | source-specific trivia; says nothing transferable about building agents. |
| `f_415` ("what's an agent really?!"), `f_520` ("Factor 2"), `f_662` ("What about Spin-Outs"), `f_910` ("In Summary") | dropped | section title cards - they mark structure but carry no content a node cites. |
| `f_233` (the "payment link to Terri" sentence) | dropped | the input half of n2; `frame_290.jpg` (the output structures) carries the claim on its own. |
| `f_320` ("60 years ago software is a Directed Graph"), `f_828` (deterministic -> agent progression) | dropped | good framing, but the narration legs at `&t=317s` / `&t=814s` already carry it; `f_828` is also barely legible at source resolution. |
| A2 protocol / HumanLayer product pitch @ `&t=970s`..`&t=1010s` | dropped | vendor pitch, not transferable knowledge. |

> **Citations - cite BOTH legs.** Video -> `<youtube-url>&t=<seconds>s`. `single-leg` nodes (n17, n18)
> rest on narration alone. Standing caveat from `AGENTS.md`: two *internal* legs agreeing proves the
> slide and the talk are **consistent**, not that the advice is correct. The `corroborated (external)`
> nodes are stronger - backed by a second artifact - but the repo and the talk **share one author**,
> so this corroborates *the framework as stated*, not that the 12 factors work in practice. Real
> validation needs an unrelated source; the closest thing here is n1's claim to be distilled from
> 100+ builder interviews, which is itself uncheckable from this source.
