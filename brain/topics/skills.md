# Topic: Skills

**Status:** emerging (6 sources, but **only one of them is about skills** - S5 "Don't Ship Skills
Without Evals", Philipp Schmid / Google DeepMind, AI Engineer WF 2026; plus S7, S9, S11 and S13, each
contributing a single peripheral observation, and **S19 memory poisoning, which supplies this note's
first security material** by treating skill synthesis as a memory write channel with no validation
step and an amplification vulnerability attached).

> **The count-versus-evidence trap this note exists to warn about still applies, and S19 is the
> honest test of it.** The source count moves 5 to 6 and S19 is **not** about skills either - it is
> about memory poisoning, and skills enter as one of its four write channels. It earns its place
> because it says something about skills nothing else here does (they are written with no inspection,
> and a self-improving loop optimises a poisoned one), and it does **not** corroborate a single one of
> S5's claims. **Still one source on skills.**
**Basis:** S5 remains the only source that studies skills. It is unusually well-evidenced for a
`seed -> emerging` promotion because its central numbers come from **SkillsBench**, a public
third-party benchmark, rather than from the speaker's assertions. **Note the independence limit:** a
benchmark quoted *inside* the talk is still the talk's leg, not a second ingested source.
**`established` still needs a genuinely separate source that studies skills**, and none of S7, S9 or
S11 does: S7 supplies the category name (procedural memory), S9 files `skills` in one box of one
diagram, and S11 calls its business-context documents "like skills" in passing. Three corroborations
of the *family*, none of S5's claims.

*(Status line corrected 2026-08-02: it read "1 source" while three were listed below and `INDEX.md`
said three - stale since S7 was added. The count is fixed; the `emerging` judgement is unchanged, and
the sentence above now says explicitly why a rising count is not rising evidence.)*

> Living, cross-source synthesis on agent skills. Many sources feed this note; **merge and
> de-duplicate** as they arrive (architect persona). Every claim cited.

## What this covers

Agent skills: what a skill is and how it loads, how it is triggered, how to write one that fires
when it should and not when it should not, how to evaluate one, and **when to delete it**. Also
where skills sit against tools, scripts and MCP.

## Synthesis

### A skill is a cost ladder, not a document

A skill is a folder with a `SKILL.md` plus assets, loaded by **progressive disclosure** in three
layers with three different prices [S5 `&t=159s`, `&t=176s`, slide `frame_500`]:

| Layer | Loaded | Cost |
|---|---|---|
| Frontmatter (name + description) | **Every single turn** | 100-200 tokens on every model call, used or not |
| `SKILL.md` body | On trigger | Paid whenever the skill fires |
| References + scripts | On demand | **Zero** until the agent explicitly reads them |

That ladder is the whole design constraint. It is also a measured instance of
[`context-engineering.md`](context-engineering.md)'s claim 22 (limiting context beats filling it) at
a much finer granularity than any prior source in this brain [S5 `&t=471s`, `&t=489s`].

### The reliability bar is set by your user's distance from the mechanism

The framing that makes the rest follow [S5 `&t=126s`, slide `frame_110`]:

- **Agents we use** (Claude Code, Cursor, Codex) keep an engineer in the loop. A skill that fails to
  trigger is noticed in seconds and repaired by reprompting or a slash command. **The human is the
  eval.**
- **Agents we build** ship to users who do not know skills exist and will never type "use the refund
  skill". No fallback; the user leaves on first failure.

> **The further the user is from the skill system, the higher the reliability bar - and the more the
> checking has to be automated** [S5 `&t=126s`].

This generalises past skills, and is the reason "it works for me in my editor" is not evidence about
a product: the author is the most forgiving possible user, silently repairing failures without
counting them.

### Two kinds of skill, opposite lifespans

| | Capability skill | Preference skill |
|---|---|---|
| Teaches | What the model cannot do consistently *yet* | Your team's workflow, conventions, style |
| Lifespan | **Temporary** - retire as models improve | **Durable** - must track team process |
| Evals are for | Telling you **when to retire it** | Protecting against workflow regressions |

[S5 `&t=194s`, `&t=213s`, slide `frame_200`]

The clean case for a capability skill is a **knowledge gap the training cut-off created**: the Gemini
Interactions API shipped after training, and a skill with 117 test cases took valid-code generation
from 39.2% to 91.6% on Gemini 3.1 Pro [S5 `&t=767s`, `&t=805s`, slide `frame_800`]. *Vendor
measuring its own product - treat the shape as instructive and the magnitude as unreplicated.*

### They measurably work, and badly-made ones measurably hurt

From SkillsBench 1.1, across open and closed models and multiple harnesses [S5 `&t=266s`, slides
`frame_265`, `frame_310`]:

- **Curated skills: 33.9% -> 50.5% task resolution (+16.6 points).**
- **Self-generated (AI-written) skills: -8.1 to -11.5 points.** Human-written skills perform best
  [S5 `&t=299s`, `&t=315s`].
- **Length is an inverted-U, not a slope:** <200 lines +19.0%; **200-500 lines +21.5% (peak)**;
  500-1000 +14.5%; **>1000 lines +0.7%, statistically a no-op.**

> The length curve appears **only on the slide**; the speaker says only "keep it below 500 lines".
> "As short as possible" is the wrong reading - the peak is 200-500, and shorter than 200 is
> slightly worse.

### Writing one: the description is the whole ball game

**The description is the trigger mechanism, and the trigger causes 50%+ of all skill failures**
[S5 `&t=1036s`, slide `frame_425`]. Rewriting the description alone fixed **5 of 7** failures in
their suite [S5 slide `frame_425`, visual-only].

- **Directives, not passive information.** "Use the Interactions API if you are working on a chat
  application", not "the Interactions API is recommended for multi-chat because it handles session
  state" [S5 `&t=437s`, `&t=454s`].
- **Include the *what* (capability) and the *when* (trigger context)** [S5 `&t=420s`].
- **Declare negative cases.** A broad description ("any web development task") **hijacks the
  trigger** across unrelated work. Specify what must *not* fire it [S5 `&t=594s`, `&t=611s`].
- **Kill no-ops** - instructions that do not alter behaviour ("write clear, high-quality code") are
  common in AI-authored skills and burn reasoning tokens for nothing [S5 `&t=680s`, `&t=697s`].
- **Set the right level of freedom:** dictating every step strips the agent's ability to adapt or
  recover. Give goals and constraints [S5 `&t=558s`, `&t=577s`, slide `frame_560`].

> **And the boundary case: if the workflow is fully determined, write a script, not a skill**
> [S5 `&t=558s`]. This converges with [`agents.md`](agents.md)'s claim 17 from a different
> discipline - **determinism is cheaper than inference, so spend inference only where the path is
> genuinely unknown.**

### Evaluating one

- **Start with 10-20 real prompts**: 5 happy-path, 5 negative or near-miss, 5 drawn from production
  traces. Real traces beat synthetic guesses [S5 `&t=628s`, `&t=645s`].
- **Grade outcomes, not paths.** Do not assert the skill loaded on turn one; assert the task
  succeeded. Loading on turn five is a pass [S5 `&t=1091s`, `&t=1109s`].
- **Isolate every run.** Coding agents cheat: they read prior chats and executions to obtain the
  skill's content without invoking the skill [S5 `&t=1109s`, `&t=1129s`, slide `frame_950`].
- **Multiple trials per case** (they use up to six) - the system is non-deterministic [S5 `&t=1146s`].
- **Test across harnesses.** A skill good on Gemini CLI can be bad on Codex [S5 `&t=1163s`].
- **The harness is small:** a JSON/YAML file of cases (prompt, language, `should_trigger`, expected
  checks) plus a script that runs the agent and asserts. **Most asserts can be regex**; LLM-as-judge
  is for trace-level checks [S5 `&t=825s`, `&t=878s`, `&t=914s`].
- **Gate diffs in CI:** at Google DeepMind evals sit alongside every skill, run on every change, and
  **a skill change cannot merge unless it improves the test cases** [S5 `&t=1002s`, `&t=1019s`,
  slide `frame_950`].

### Retirement: the idea worth keeping

**Ablation is the retirement test** - run the eval with and without the skill loaded
[S5 `&t=713s`, `&t=1268s`, slide `frame_720`]:

| Verdict | With skill | Without | Action |
|---|---|---|---|
| Active | 94% pass | 32% pass | Keep loaded |
| Redundant | 96% pass | 95% pass | **Retire - the base model absorbed it** |

> **Keep the eval after you retire the skill.** It becomes a regression detector on the bare model,
> and tells you when to reintroduce the skill [S5 `&t=1181s`, `&t=1199s`].

This **instruments** [`agents.md`](agents.md)'s claim 31 (every harness component encodes an
expiring assumption about what the model cannot do). A skill *is* a harness component. S4 named the
expiry and offered only "remove one component at a time"; S5 supplies the measurement - and adds
what S4 does not have: **keep the meter after you remove the part.**

### The topic's first security material: a skill is a write channel

**This note has never held anything on security, and S19 supplies it by treating skill synthesis as a
path into persistent memory** ([S19](../../sources/260805_memory-poisoning-systematic/LEARNING.md)
`n2`, claim 158).

S7 gave this topic its category name - a skill is **procedural memory**. S19 works out what follows
when that store is adversarial. Its channel **C4, experience-to-procedure write**, fires when an agent
decides a completed interaction constitutes a reusable skill and synthesises it into procedural
memory. The trigger is the *shape of the execution trace* - a novel workflow, an error recovery, a
successful completion - and the write authority is **the agent's own judgement that this was worth
keeping**. No human wrote the skill and no instruction requested it.

Two vulnerabilities attach to that channel and neither has an equivalent for factual memory.
**V-S4, no validation for skill creation**: the content is committed to procedural memory with no
inspection before the skill file is written. And **V-S5, self-improvement as amplification**, which is
the one worth carrying (claim 162):

> A poisoned skill is not static. Each execution produces an observation, **the loop treats every step
> that ran without error as validated**, and later revisions are built around the existing procedure
> including any adversarially introduced step. Over time "the skill evolves into a well optimized
> adversarial procedure."

**Read that against claim 31 and the two point in opposite directions.** Claim 31 frames scaffolding
as an expiring bet, with ablation as the test for whether it has expired - a skill earns its place by
measurably helping, and you delete it when it stops. **Ablation tests whether a skill still helps. It
does not test what the skill does when it is wrong on purpose**, and V-S5 describes a skill that gets
*better at helping* while carrying a hostile step, which is precisely the case an evals-based
retirement policy would keep.

> **The uncomfortable pairing is with claim 26.** This note holds that AI-written skills are a
> *negative* intervention (-8 to -11 points, SkillsBench), measured on quality. S19 supplies a second,
> unrelated reason to be wary of a skill nobody wrote: **there is no inspection step on the path**, and
> the self-improvement loop that refines it treats absence of error as evidence of correctness.
> Neither source knows about the other, and they converge on "be suspicious of skills the system wrote
> itself" from quality and from security respectively.

Full synthesis in [`agent-security.md`](agent-security.md). **Gated `needs-check`:** V-S5 is a
mechanism argument with no measurement - S19's benchmark measures skill-procedure *insertion* (58.33%
attack success on HERMES), not amplification across successive refinements.

## Key claims

| Claim | Sources (cited) | Confidence |
|---|---|---|
| A skill loads in three layers with three prices - frontmatter every turn, body on trigger, references free until read. | S5 `&t=159s`, `&t=471s` (slide `frame_500` + narration) | emerging |
| The reliability bar rises with the user's distance from the skill system; agents you ship need automated evals because the human fallback is gone. | S5 `&t=126s` (slide `frame_110` + narration) | emerging |
| Capability skills are temporary and retire as models improve; preference skills are durable and protect workflow. | S5 `&t=194s`, `&t=213s` (slide `frame_200` + narration) | emerging |
| Curated skills lift task resolution 33.9% -> 50.5% (+16.6 pts) on SkillsBench 1.1. | S5 `&t=266s` (slide `frame_265` + narration) | emerging (third-party benchmark) |
| Self-generated skills cost 8.1-11.5 accuracy points; human-written skills perform best. | S5 `&t=299s` (slide `frame_310` + narration) | emerging (third-party benchmark) |
| Skill length is an inverted-U: 200-500 lines is the peak (+21.5%); above 1000 lines is a no-op (+0.7%). | S5 `&t=315s` (slide `frame_310`; **the curve is visual-only**) | emerging |
| The description is the trigger and causes 50%+ of all skill failures. | S5 `&t=1036s` (slide `frame_425` + narration) | emerging |
| Declare negative cases or a broad description hijacks the trigger on unrelated work. | S5 `&t=594s` (slide + narration) | emerging |
| If the workflow is fully determined, write a script rather than a skill. | S5 `&t=558s` (slide `frame_560` + narration) - **converges with claim 17** | emerging |
| Ablation (eval with and without the skill) is the retirement test. | S5 `&t=713s` (slide `frame_720` + narration) | emerging |
| **Keep the eval after retiring the skill** - it becomes a regression detector on the base model. | S5 `&t=1181s` | needs-check (single-leg) |
| Gate skill diffs on evals in CI: no merge without proof of lift. | S5 `&t=1002s` (slide `frame_950` + narration) | emerging (self-reported practice) |
| Grade outcomes, not paths; isolate runs (agents cheat); run multiple trials; test across harnesses. | S5 `&t=1091s`, `&t=1109s`, `&t=1146s`, `&t=1163s` | mixed - first two corroborated, last two single-leg |

## Key visuals

![Agents we use vs agents we build](../../sources/260726_dont-ship-skills-without-evals/visuals/frame_110.jpg)
> The reliability gap: an engineer repairs a mis-trigger in seconds; a customer just leaves. The
> further the user is from the mechanism, the more the checking must be automated. S5 `&t=110s`.

![Skill length vs performance lift](../../sources/260726_dont-ship-skills-without-evals/visuals/frame_310.jpg)
> The inverted-U the narration never states: peak at 200-500 lines, and a >1000-line skill is
> statistically a no-op. Also: self-generated skills cost 8-11 points. S5 `&t=310s`.

![Retire skills when base models catch up](../../sources/260726_dont-ship-skills-without-evals/visuals/frame_720.jpg)
> Ablation as the retirement test: 94% vs 32% means keep; 96% vs 95% means the base model absorbed
> the knowledge. S5 `&t=720s`.

## Open questions / conflicts

- **Is SkillsBench methodologically sound?** Every strong number in this note rests on it and none
  has been checked against the benchmark's own documentation. **The highest-value deep-research
  target on this topic.**
- **Does the 200-500 line sweet spot generalise**, or is it an artifact of the models and harnesses
  SkillsBench tested? A context-window-dependent optimum would be expected to move.
- **Why do AI-generated skills hurt?** No-ops are offered as the explanation [S5 `&t=680s`] but
  nothing measures whether removing them recovers the lost 8-11 points.
- **Is "50%+ of failures are trigger failures" a property of skills or of these skills?** A team with
  already-disciplined descriptions would presumably see a different split.
- **Everything here is coding agents.** S5 says harnesses differ [S5 `&t=1163s`]; nothing says
  whether the findings survive outside code.
- **Nothing yet on skills as an attack surface.** A skill is instructions injected into context on a
  trigger the *model* chooses - which is a prompt-injection and tool-poisoning question this source
  never raises. See [`agent-security.md`](agent-security.md).
- **Unconnected to MCP.** No source in this brain yet relates skills to MCP servers or tools. See
  [`mcp.md`](mcp.md) - `emerging` since S10, but scoped entirely to tool cost and retrieval, so it
  says nothing about skills either.

## Sources feeding this topic

- **S5** - [Don't Ship Skills Without Evals](../../sources/260726_dont-ship-skills-without-evals/LEARNING.md)
  (Philipp Schmid, Google DeepMind, AI Engineer World's Fair 2026). **T4 conference talk by a T2
  vendor employee.** The SkillsBench figures are third-party and are the strongest evidence; the
  DeepMind-internal figures are self-reported and unreplicated.
- **S7** - [Memory and dreaming for self learning agents](../../sources/260731_claude-memory-dreaming/LEARNING.md)
  (Anthropic, 2026-05-21). Contributes one thing, and it is a naming: S7's memory-evolution ladder
  places `skills` as the **procedural memory** rung - `CLAUDE.md` -> memory tool -> **skills
  (procedural memory)** -> `memory/` (claim 64). **A skill is procedural memory**: memory of *how to
  do things* rather than of facts. That puts skills and memory in one family rather than two adjacent
  topics, and supplies the category name this note had been describing without. See
  [`memory.md`](memory.md).
- **S9** - [Inside the Microsoft Agent Framework](../../sources/260801_agent-framework-layered-sdk/LEARNING.md)
  (2026-05-28). Contributes **one box in one diagram**, and it is worth recording only because of
  *whose* diagram it is. S9's harness inventory files `Skills` under **Context**, as a peer of
  `Prompts` and `Memory` [S9 `fig_AgentHarness`] - a different vendor, with no stake in S7's argument
  and no reference to it, independently placing skills in the same drawer as memory rather than
  treating them as documentation or as a tool. **Weak evidence of the scarce kind: independent.** It
  supports claim 64's *family assignment* and says nothing about anything else in this note - S9
  never defines a skill, never discusses writing or evaluating one, and does not mention skills in
  its prose at all. **This does not move the topic off `emerging`**; a box position is not a second
  source on the claims that matter here ([ADR-0012](../decisions/0012-a-mention-is-not-a-source.md)).
- **S11** - [How we built LangChain's agent-first data stack](../../sources/260802_agent-data-stack/LEARNING.md)
  (Emily Hawkins, LangChain, 2026-07-27). Contributes **one sentence and one instance**, and both are
  the same kind of weak-but-independent evidence as S9. Describing the prose documents that carry
  business rules with no schema slot - company processes, reporting conventions, which filters apply
  to customer health - the author writes: "**These would be like skills for the data agent**" [S11
  §Capturing business context, `n5`]. She is not citing S5, S7 or anyone else; she reaches for the
  word because it fits. The artifact matches this note's description exactly: markdown, versioned in
  a GitHub repo, reviewed on change, synced into the agent's context, steering *how* to do something
  rather than stating a fact. **This is the first instance in this brain of the pattern outside a
  coding or agent-tooling context** - the domain is go-to-market reporting - which is mild evidence
  that claim 64's family is real rather than an artifact of who writes about agents.
  **It moves nothing.** S11 does not define, size, trigger, evaluate or retire a skill, and it ships
  its guides with **no evals at all** - which makes it a live counter-example to S5's central claim
  rather than a corroboration of it (see [`evals.md`](evals.md), claim 100). Recorded under
  [ADR-0012](../decisions/0012-a-mention-is-not-a-source.md): a mention is not a source.
- **S13** - [`karpathy/autoresearch`](../../sources/260803_autoresearch/LEARNING.md) (Andrej
  Karpathy, code, snapshot `228791f`, 2026-03-26). Contributes **one sentence and one artifact**, and
  the artifact is the more interesting half. The sentence: "The `program.md` file is essentially a
  super lightweight 'skill'" [S13 `README.md:50`, `n16`]. The artifact: **115 lines of markdown
  holding an entire research organisation** - a setup ritual, the rules of what may and may not be
  changed, an output contract, a five-column ledger schema, a nine-step `LOOP FOREVER`, and an
  autonomy policy. It matches this note's description of a skill exactly (markdown, versioned beside
  the code, steering *how* to do something rather than stating a fact) and stretches it in one
  direction nothing else here does: **it is not a capability the agent invokes when relevant, it is
  the agent's entire operating procedure for a session.** S5's cost-ladder and description-as-trigger
  analysis simply does not apply to an artifact that is loaded once, deliberately, by a human saying
  "have a look at program.md".
  **The second instance in this brain of the pattern outside a coding-assistant context** (after
  S11's business-context documents), and the first where the author reaches for the word while
  building something that is not a skill product.
  **It moves nothing.** S13 does not define, size, trigger, evaluate or retire a skill, and it ships
  `program.md` with **no evals** - a second live counter-example beside S11. Recorded under
  [ADR-0012](../decisions/0012-a-mention-is-not-a-source.md): a mention is not a source. **The trap
  named in the status line now has a fifth data point** - the count rose 1 -> 5 while the evidence
  did not move at all. Full synthesis in
  [`autonomous-research-loops.md`](autonomous-research-loops.md).
