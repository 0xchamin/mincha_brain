# Knowledge nodes - Inside the Microsoft Agent Framework

> Persona: **fact-checker** - re-adopt when working this file.

> The atomic units of knowledge extracted from this source. Each node has a **stable ID** (`n1`,
> `n2`, ... - never renumber; topic notes reference these), a claim, **both legs each with its own
> citation** (or one leg marked `single-leg`), a gate verdict, and a confidence. Only
> `corroborated`/`single-leg` nodes (and recorded `divergence` findings) feed `LEARNING.md` and get
> promoted to `../../brain/`. The **fact-checker** persona owns the verdicts; see `../../AGENTS.md`
> and `prd.md` §6.

## What counts as a second leg here

**Prose vs figure - and here that is a real pairing rather than a formality.** The four figures are
authored architecture diagrams with named boxes, not stock art. Where a figure names something the
prose also states, the node is `corroborated` *internally*. Where a figure names something the prose
is silent on, the node is `single-leg` **on the figure** - the unusual direction for this kit, and
worth flagging: normally text is the primary leg and the visual confirms it. Here the diagrams are
the richer leg.

**Internal corroboration is the ceiling this source can reach.** Both legs were authored by the same
team, about the same product, in the same post. Agreement proves the article is self-consistent; it
proves nothing about whether the design works.

## Evidence class

**T2 - first-party engineering writing about the vendor's own SDK.** Strong on *what the framework is
and how it is factored*; positioned on *whether this factoring is right*, since the post exists to
recommend the product. No benchmarks, no measurements, no baseline, no comparison to any other
framework. **No node here may exceed `emerging` on an efficacy question.**

## Nodes

| ID | Claim (crux) | Evidence leg + citation | Corroborating leg + citation | Gate | Confidence |
|---|---|---|---|---|---|
| n1 | The framework is organised as three separable ideas: **agent loop** (the execution cycle over models, conversations, tools, state), **workflows** (structured orchestration), **harnesses** (reusable runtime capabilities). | article, §intro - the three enumerated as the core organising ideas, each with its own section | `visuals/fig_AgentFramework.png` - exactly three boxes, those three names, no others | corroborated (internal) | emerging |
| n2 | The loop itself is a six-line while-loop; the difficulty is everything around it - messages, tool schemas, results, errors, streaming, permissions, state - **and the article's conclusion is that the SDK should own that structure** so the developer works on agent behaviour. | article, §Agent loops - pseudocode block, then the list of what makes it hard | `visuals/fig_AgentLoop.png` - the `MAF AIAgent` box is small; the substrate of models, tools, hosting and providers beneath it is most of the frame | corroborated (internal) | emerging - **see `d1`, this contradicts claim 12** |
| n3 | Agentic applications should not be locked to one model, tool provider or hosting environment. | article, §Provider-agnostic by design - names Foundry, OpenAI, Anthropic, Copilot Studio, GitHub Copilot, A2A | `visuals/fig_AgentLoop.png` - strictly richer: models (OpenAI, Anthropic, Bedrock, Gemini, Ollama), tools (OpenAPI, **MCP**), hosting (Functions, Container Apps), all beside the first-party column | corroborated (internal) | emerging |
| n4 | **An "agent provider" can be another vendor's entire coding harness.** `Claude Code Agent` and `GitHub Copilot CLI Agent` sit as peer tiles beside a prompt-configured first-party agent and A2A, a wire protocol. | `visuals/fig_AgentLoop.png` - the `Agent Providers` box, five peer tiles | **(none)** - the prose says only that the framework can "interact with agents hosted elsewhere, including Copilot Studio or GitHub Copilot, or through A2A"; it never names Claude Code, and "interact with" is weaker than the figure's peer-slot framing | single-leg (figure) | needs-check |
| n5 | Workflows exist because many real processes need **predictable steps, not more autonomy** - support triage, bug-to-PR, research-with-review are fixed sequences, not conversations. | article, §Workflows - the argument plus three worked examples | `visuals/fig_Workflows.png` - five patterns drawn as fixed-topology graphs, boxes and arrows rather than cycles | corroborated (internal) | emerging |
| n6 | Five named orchestration patterns: **Sequential**, **Handoff**, **Author/Critic**, **Magentic** (a coordinator plans and supervises subagents), **Custom**. | article, §Workflows - all five with one-line definitions | `visuals/fig_Workflows.png` - all five as labelled panels; Author/Critic drawn as `worker` and `reviewer` with a cycle arrow between them | corroborated (internal) | emerging |
| n7 | The harness is an **inventory**: Common Tools (file system, code execution, shell execution), Context (prompts, **skills**, memory), Planning (**todo**, subagents), Middleware (context compaction, **tool selection**, permissions) - under a row of **preset harnesses by task archetype** (deep research, content generation, coding, data analysis, custom). | `visuals/fig_AgentHarness.png` - four named columns plus the preset row | article, §Harnesses - **partial**: covers file systems, code/shell execution, prompts, memory, subagents, compaction, permissions, approval gates, logging, tracing. **Silent on skills, todo, tool selection and the presets** | corroborated on the overlap; **single-leg (figure) on skills / todo / tool selection / presets** | emerging / needs-check on the figure-only items |
| n8 | **Environment quality bounds agent quality regardless of model strength** - a strong model with poor tools, weak context and no controls still produces a poor result. | article, §Harnesses - stated directly as why the harness layer exists | `visuals/fig_AgentHarness.png` - the model appears in no box; every box is something the developer supplies | corroborated (internal) | emerging |
| n9 | The three layers are **not a stack**: the loop is the base, workflows and harness are two independent optional surrounds, and choosing among them is the thesis - "not every agent needs a complex workflow. Not every workflow needs a highly autonomous agent." | `visuals/fig_AgentFramework.png` - `Workflows` and `Harness` side by side above `Agent Loop` alone, inside one container; the two peers do not touch | article, §Why this matters - the pull-quote and closing paragraph state the choice explicitly | corroborated (internal) | emerging |

### Notes on the nodes that carry weight

- **`n4` is the most conceptually interesting thing in the source and the weakest-evidenced.** The
  unit of composition has moved up a level, from *model* to *whole agent harness*. But it rests on
  five tiles in one diagram and the prose declines to make the claim. A tile in a vendor architecture
  diagram is exactly the kind of thing this kit must not read as a capability statement.
- **`n6` Author/Critic is the brain's claim 34 (self-evaluation bias, S4) and claim 59 (split a loop
  before it holds two objectives, S7) shipped as a named SDK primitive by a third vendor.** That
  corroborates the pattern's *currency*, not its *efficacy* - this source measures nothing, and S4
  remains the only source that measured anything about it.
- **`n7` matters to the brain for two things beyond the inventory.** `Skills` sits under **Context**
  as a peer of prompts and memory - a second vendor independently filing skills in the same family as
  memory, which is what claim 64 asserts from a single Anthropic source. And `Todo` is named a
  **Planning** primitive, making the todo list architectural rather than a prompting trick.
- **`n8` is the one point where this source agrees with S4 rather than cutting across it** - but note
  what is missing. **S4's finding that harness components expire** (claim 31) has no counterpart
  here. An SDK that ships the harness as a catalog has a structural reason not to say that.
- **`n9`: read the shape, not just the boxes.** A stack would mean every agent pays for every layer.
  Two optional surrounds over a mandatory base is the claim that the loop is the only thing you
  always need - the brain's claim 17 ("not every problem needs an agent") moved one level up.

## Dropped / divergences (audit trail)

| Candidate | Verdict | Note |
|---|---|---|
| hero image (`...-hero.svg`) | dropped | Decorative title-card art; carries no named content. Never downloaded. |
| "Next Stop" article teasers | dropped | Site furniture from the page template, not part of this article. |
| `d1` own-the-loop | **divergence** | Flat contradiction with S2 / claim 12 - **kept and flagged**, see below. |

### d1 - Own the loop, or let the framework own it?

**The divergence.** This source and S2 (12-factor agents) start from a near-identical premise and
reach opposite conclusions.

| | S2 (12-factor agents, T4) | S9 (this source, T2) |
|---|---|---|
| The loop is | prompt + switch + context builder + loop | send to model, execute tools, append, repeat |
| Implementing it well is | the whole job | difficult, repetitive plumbing |
| Therefore | **own all four** - the 70-80% wall comes from a framework owning one [S2 `8kMaTybvDUw` `&t=406s`, `&t=37s`] | **let the SDK own it**, so you work on agent behaviour [article, §Agent loops] |

**Not a docs-vs-code divergence** - this source has no code to check its prose against. It is a
conflict *between sources*, which the global rules say to keep and flag rather than resolve.

**The fact-checker's read, recorded without resolving it.** Neither party is disinterested: S2's
author sells an agent framework, and this article is a product post for an SDK. Neither offers
evidence. But the two claims are less opposed than they look, because they answer different
questions - S2 argues about **where the debuggable seam sits when quality stalls at 80%**, and this
article argues about **how much plumbing you write before reaching 80% at all**. A framework whose
loop is *inspectable and overridable* satisfies both; one that hides it satisfies only the second.
**What would settle it is the one thing neither source supplies**: what happens at the 80% wall with
this SDK, which the article never discusses.

Recorded as a conflict in [`agents.md`](../../brain/topics/agents.md) "Open questions". Do not
silently pick a winner.

## Gate summary

**Nine nodes, one divergence. Six internally corroborated, one single-leg, one split, plus `n2`
which is corroborated but implicated in `d1`.** Nothing here is externally corroborated and nothing
is measured; deep research was not requested.

> **Citations - cite BOTH legs.** Video -> `<youtube-url>&t=<seconds>s`; blog -> `source, <section
> heading>`; paper -> `source, Figure/Table N, §`; **code -> an immutable GitHub blob permalink
> containing the SHA**. A `single-leg` node cites its one leg and leaves the other cell `(none)`.

> **S9** = this source. Cross-referenced: **S1** Uber closed-loop evals, **S2** 12-factor agents,
> **S4** Anthropic harness design, **S5** skills evals, **S7** Anthropic memory and dreaming.
