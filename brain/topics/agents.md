# Topic: Agents

**Status:** established (2 sources - S1 Uber closed-loop evals, S2 12-factor agents)

> Living, cross-source synthesis on autonomous LLM agents. Many sources feed this note; **merge
> and de-duplicate** as they arrive (architect persona) - this should read as one coherent view,
> not stacked summaries. Every claim cited.

## What this covers

Autonomous LLM agents: the agent loop (perceive -> plan -> act -> observe), tool use, memory,
planning strategies, multi-agent patterns, control flow and state, and failure modes.

> Context-window ownership - how you decide which tokens reach the model - has grown into its own
> note: see [`context-engineering.md`](context-engineering.md). Evaluation of these pipelines is
> also its own topic: see [`evals.md`](evals.md).

## Synthesis

### What an agent actually is

Strip the mystique and an agent is **four owned parts**: a prompt that instructs the model how to
select the next step, a switch statement that dispatches on the model's JSON, a context-window
builder, and a loop with explicit exit conditions [S2 `&t=406s`]. Reliability problems tend to trace
back to a framework owning one of those four instead of you - the "70-80% wall", where the last 20%
of quality means being seven layers deep in a call stack reverse-engineering how the prompt was
built [S2 `&t=37s`].

The enabling capability underneath is narrower than it looks: an LLM turning a sentence into
**structured JSON** matching a schema you defined [S2 `&t=229s`]. "Tool use" adds nothing magical on
top - the model emits JSON, deterministic code switches on it, a result may be fed back. S2 pushes
this deliberately hard ("tool use is harmful", echoing Dijkstra) because treating tool use as an
ethereal entity acting on the world is what makes it undebuggable [S2 `&t=264s`].

### The shape that works in production: small islands in a deterministic sea

Both sources land on the same structural answer from opposite directions.

- **S2, from first principles:** the naive loop - event -> prompt -> pick next step -> append result
  -> repeat - materialises a DAG at runtime but **breaks down on longer workflows**, mainly because
  the context window grows unboundedly [S2 `&t=371s`]. What works instead is **micro agents**: a
  mostly deterministic pipeline with agent loops of **3-10 steps** at the genuinely ambiguous points,
  handing control back to ordinary code afterwards [S2 `&t=741s`].
- **S1, from production practice:** an agent "product" is a **routed pipeline of small,
  single-purpose agents** (image-understanding -> router -> prompt-gen -> generation -> QA gates ->
  post-processing), each independently evaluable, the whole orchestration logged to one flat trace
  [S1 `&t=376s`].

**These agree, and that convergence is the most load-bearing claim in this note**: nobody who ships
agents at scale ships one big autonomous loop. They ship small, scoped, individually-evaluable LLM
steps inside deterministic software. S1's spectrum framing - deterministic/brittle at one end,
unconstrained/unsafe at the other, with a **guardrailed middle** as the target [S1 `&t=251s`] - is
the same claim stated as a design space.

**And it is now measured, not just twice-asserted** [R1]. "Beyond pass@1" names task decomposition
the **highest-leverage reliability intervention**, quantified across 10 open-source models:
**+13.1 pp (DeepSeek V3)** and **+41.5 pp (Qwen3 30B)** reliability gain from splitting a long task
into short segments and restarting the agent at each boundary
([arXiv 2603.29231](https://arxiv.org/abs/2603.29231), T3 preprint). Anthropic reports the same shape
from its own deployments: the most successful implementations "weren't using complex frameworks or
specialized libraries. Instead, they were building with simple, composable patterns"
([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), T2).

> **The boundary the same paper draws - and S2 misses.** Decomposition helps; *memory scaffolding*
> does not. A naive episodic memory scaffold "never improves long-horizon reliability, and hurts 6 of
> 10 models" - plain ReAct beat it. The defensible move is **decompose and keep each segment short**,
> not **remember more**. Check any future "give the agent better memory" claim against this. [R1]

The expected trajectory is not a jump to full autonomy but **starting deterministic and sprinkling
LLM steps in**, widening their scope as models improve - while still doing the engineering to hit
quality at each stage [S2 `&t=814s`].

### State, control flow and pausing

Because an agent is software, treat it like software: **unify execution state** (current step, next
step, retry counts) **with business state** (messages, what the user has been shown, what awaits
approval), and put the agent behind a REST or MCP endpoint. On a long-running tool call, interrupt
and **serialise the context window to a store keyed by a state ID**; on callback, reload, append the
result, resume - "the agent doesn't even know that things happened in the background"
[S2 `&t=460s`, `&t=495s`]. Correspondingly, the agent itself should hold **no state of its own**
(factor 12, "stateless reducer") [S2 `&t=865s`].

Owning the loop is what makes mid-run interventions possible at all - break, summarise, insert
LLM-as-judge [S2 `&t=423s`].

### Humans as part of the architecture

Make contacting a human **a tool call** rather than a structural branch: `request_human_input` sits
alongside `deploy_backend` in the same intent enum. Two payoffs - the model gets richer modes (done /
need clarification / escalate), and the decision rides on a natural-language token the model
understands rather than a branch it was never trained on [S2 `&t=687s`]. Trigger from wherever users
already are (email, Slack, Discord, SMS) instead of a dedicated chat tab [S2 `&t=723s`]. In S2's
worked deploy-bot example the human approval and the rejection feedback ("can you deploy the backend
API first") are just more events in the same thread [S2 `&t=776s`].

### Agents that improve themselves

- **Self-tuning components.** Each agent can rewrite its own config: a **prompt-optimizer** of two
  sub-agents - *reflect* (find systemic issues in mismatches) and *synthesize* (rewrite the config) -
  registers a new version in an agent store that the next run picks up, with observability and quick
  rollback [S1 `&t=732s`].
- **A meta-agent (diagnoser) over the fleet.** A higher-level abstraction ingests any feedback
  signal, localises *which* sub-agent is failing, and routes the fix to that agent's config [S1
  `&t=1144s`].

### Two counterweights worth keeping

- **Not every problem needs an agent.** S2's DevOps agent got Makefile build steps in the wrong
  order; two hours of increasingly specific prompting later, the exact build order was spelled out -
  "I could have written the bash script to do this in about 90 seconds" [S2 `&t=71s`].
- **Find the bleeding edge.** The differentiator is picking work sitting right at the boundary of
  what the model can do *reliably* - something it cannot get right every time - and engineering
  reliability around it anyway [S2 `&t=848s`]. This is also the answer to "won't better models make
  this obsolete?": a better model moves the boundary, and the engineering moves with it.

## Key claims

| Claim | Sources (cited) | Confidence |
|---|---|---|
| An agent = prompt + switch statement + context builder + loop; own all four. | S2 `&t=406s` | emerging |
| The enabling capability is structured output (sentence -> JSON); "tool use" is just JSON plus deterministic code. | S2 `&t=229s`, `&t=264s` | emerging |
| **What ships in production is small, scoped LLM steps inside deterministic software - not one big autonomous loop.** | **S2 `&t=741s` + S1 `&t=376s` (two sources, converging from theory and practice)** | **established** |
| A production agent is often a routed pipeline of small single-purpose agents, each independently evaluable, all logged to one flat trace. | S1 `&t=376s` | emerging |
| The naive agent loop degrades on long workflows, primarily from unbounded context growth. | S2 `&t=371s` | emerging |
| Unify execution + business state behind a REST/MCP API; serialise the context window with a state ID to pause and resume. | S2 `&t=460s` | emerging |
| The agent should be stateless; you own the state (factor 12, "stateless reducer"). | S2 `&t=865s` | needs-check (mentioned in passing) |
| Make contacting a human a tool call / intent, not a structural branch before the first token. | S2 `&t=687s` | emerging |
| Agent design is a spectrum from brittle rules to unconstrained agency; aim for a guardrailed middle. | S1 `&t=251s` | emerging |
| Agents can self-tune: a reflect+synthesize prompt-optimizer rewrites an agent's config and registers a new version. | S1 `&t=732s` | needs-check (single-leg) |
| A diagnoser meta-agent localizes which sub-agent is failing and routes the config fix there. | S1 `&t=1144s` | emerging |
| Not every problem needs an agent - a deterministic script often beats two hours of prompt engineering. | S2 `&t=71s` + R1 (Anthropic: "find the simplest solution possible, and only increasing complexity when needed", T2) | corroborated (external) |
| Decomposition is measured (+13.1 to +41.5 pp reliability); naive memory scaffolds are measured *worse* (hurt 6 of 10 models, lost to plain ReAct). | R1 ([Beyond pass@1](https://arxiv.org/abs/2603.29231), T3 preprint) | needs-check (preprint) |
| Target work at the boundary of reliable model capability, then engineer reliability around it. | S2 `&t=848s` | emerging |

## Key visuals

![Routed multi-agent pipeline with per-stage QA and logging](../../sources/260725_closed-loop-evals-multimodal-agent/visuals/frame_1058.jpg)
> A production agent as a pipeline of small agents, every stage logged. S1 `&t=376s`.

![HumanLayer deploy pipeline: deterministic CI/CD, then a determine-next-step loop with human approval and a rejection routed back, then deterministic prod tests](../../sources/260725_12-factor-agents/visuals/frame_800.jpg)
> The micro-agent shape: a 3-10 step agent loop bracketed by "deterministic code" at both ends, with
> human approval as an ordinary event in the thread. S2 `&t=741s`.

![while True loop calling llm.determine_next_step, appending to context, exiting on intent "done"](../../sources/260725_12-factor-agents/visuals/frame_345.jpg)
> The whole of "agent" in ten lines - prompt, switch, context builder, loop. S2 `&t=406s`.

## Open questions / conflicts

- **No conflicts between S1 and S2 so far** - they converge on small-scoped agents inside
  deterministic pipelines. That agreement was weak evidence on its own (two practitioner talks by
  people selling adjacent products); **R1 has since strengthened it** with a measurement and an
  independent third party (Anthropic). Still worth looking for a source that argues the *opposite* -
  that large autonomous loops now work.
- **New from R1, unresolved:** decomposition is measured on coding/web/tool benchmarks (SWE-bench,
  WebArena, tau-bench), not on the deploy-bot-style workflows S1 and S2 describe. The transfer is
  plausible, not demonstrated.
- S2's factors are corroborated by the author's own repo, **not** by an independent party (S2
  `nodes.md` `en1`); the "100+ builders interviewed" basis is uncheckable from the source. No
  benchmarks, ablations or failure rates appear anywhere in S2.
- Self-tuning agents (reflect/synthesize, agent store) remain `single-leg` from S1 - still needs a
  second source.
- **Gap: nothing here yet on agent security.** Both sources treat tool calls as trusted; neither
  discusses prompt injection into the context window or tool poisoning. See
  [`agent-security.md`](agent-security.md) (still a seed).

## Sources feeding this topic

- **S1** - [Building Closed-Loop Evals for a Multimodal Agent at Scale](../../sources/260725_closed-loop-evals-multimodal-agent/LEARNING.md) (Uber, AI Engineer 2026).
- **S2** - [12-Factor Agents: Patterns of reliable LLM applications](../../sources/260725_12-factor-agents/LEARNING.md) (Dex Horthy, HumanLayer, AI Engineer WF 2025).
- **R1** - [deep-research pass on S2](../../sources/260725_12-factor-agents/context/01_context-limits-and-decomposition.md) (2026-07-25) - external evidence, tiered with independence calls.
