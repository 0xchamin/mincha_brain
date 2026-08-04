# Learning - Memory and dreaming for self learning agents

> Persona: **curator** + **mentor, always** - re-adopt when working this file.

> The distilled document you learn from - text anchored by a few curated visuals. Built from the
> corroborated nodes in `nodes.md`. Every claim is cited. Signal, not archive. See `SOURCE.md` for
> metadata.

> **Two kinds of material, kept visually distinct.** Claims from the talk carry a node ID (`n12`) and
> a timestamp. Blocks marked **"Background, supplied"** are context *I* am adding - established prior
> art the talk assumes or never names. They are uncited by construction.

## TL;DR

This is the agent-platform half of the memory pair, and the independent counterpart to
[S6](../260731_chatgpt-memory-dreaming/LEARNING.md). Same architecture, same name, different vendor.
Agents write memory **during** work, and a decoupled batch pass rewrites it **between** sessions
(`n11`, `n14`). **The reason to split the loops is objective conflict, not throughput**, because one
loop asked to both finish the task and curate memory trades them off untunably (`n12`). Memory is
deliberately a **file system** the model drives with `bash` and `grep`, on the same bet that produced
skills (`n2`, `n3`). To that it adds everything a consumer assistant never needs, namely scoped
stores, optimistic concurrency via a `content_sha256` precondition, and per-session attribution
(`n5`-`n7`). A live demo shows agents leaving **instructions** for their successors, not just facts
(`n20`).

## The 1-minute version

This article covers a vendor conference talk about giving many agents one shared memory, and about
the second process the vendor runs to stop that memory rotting. It is the agent-platform half of a
pair of talks, and it is worth reading beside its counterpart because two vendors arrived at the same
shape independently. A reader arriving expecting a talk about recall will find something else, since
the problem it works on is not the one the word "memory" usually names.

The problem is not forgetting. It is that **every agent learns alone**. At multi-agent scale the
platform's own operators watched agents repeat each other's mistakes, because each agent learned from
its mistakes independently, and the store they shared drifted into duplication and fragmentation
(`n10`). Notice what is strange about that failure. No individual write was wrong.

The reason it is hard is that the damage is invisible from inside any one of its causes. Each agent's
write is locally reasonable, and the store degrades anyway, because nothing is responsible for the
store as a whole. The talk's own phrase is that memory was updated in a locally optimal way that was
not globally optimal (`n10`). A failure with no single culprit cannot be fixed by improving any
single culprit, which is what separates this from an ordinary quality problem. At first glance it
still looks like something you could prompt your way out of.

Suppose instead you try exactly that, and simply tell the agent to curate more carefully as it works.
That collapses for the sharpest reason in the talk. An agent asked to finish its task **and** to
maintain memory quality is one loop holding two objectives, and it will trade them off silently under
whatever pressure the task is applying (`n12`). You cannot observe the trade, because the agent never
reports having made it. You cannot tune it, because there is no dial to turn. A second failure sits
beside the first and is easier to miss, since patterns that only appear *across* sessions are
invisible from inside any single session by construction. Both failures point at the same missing
thing, which is a vantage point outside the work.

The idea, then, is to run **two clocks**. Memory does real-time writes while agents are working, and
**dreaming** is a periodic batch pass that runs out of band, reads session transcripts, and rewrites
the store between sessions (`n11`, `n14`). The second process completes no user task, which is
precisely what makes it trustworthy as a curator, because it has exactly one objective and nothing to
trade that objective against.

How it works starts with a deliberately plain choice about the thing being curated. Memory is modelled
as a file system the model drives with `bash` and `grep` rather than through a bespoke memory API, on
the stated bet that the right move is to get out of the model's way, which is the same bet that
produced skills (`n2`, `n3`). Sharing that file system between many agents then demands three things a
single-user store never needs. It needs **scopes**, so that a slow-changing org-wide store can be
read-only while a team store stays read-write. It needs **optimistic concurrency**, supplied here as a
`content_sha256` write precondition so that a conflict fails loudly instead of clobbering silently. And
it needs **per-session attribution**, so that any memory can be traced to the session that wrote it
(`n5`-`n7`). A live demo shows the whole arrangement running, and it carries one detail the narration
never states, which is that agents leave **instructions** for their successors and not only facts
(`n20`).

What it costs comes in two parts, one budgeted and one not. The budgeted cost is test-time compute,
paid once by a process that finishes no user task and repaid to every downstream agent that reads the
result (`n13`, `single-leg`). The unbudgeted cost is an attack surface the source never raises at all,
because a shared store that carries imperatives is a coordination channel rather than a knowledge
base, and the talk supplies attribution and version history as forensics while supplying no admission
control. Sitting between the two is a gap in the design itself. Dreaming's output is described as "a
verified, better organized snapshot", and nothing in the talk or the demo says what verification
means, who performs it, or what happens when it fails (`d4`). For a system whose entire premise is
that unsupervised writes drift, that is the load-bearing step.

How far to trust it turns on splitting the source in two. This is a **T2 vendor talk about the
vendor's own product, at the vendor's own conference**, and every outcome number in it is a customer
testimonial with no baseline, no n and no eval set. Read it for the architecture and never for the
figures. The genuinely strong evidence is the live demo, because a running console showing a version
strip, a session ID and a `content_sha256` precondition is a photograph of the artifact rather than a
restatement of the pitch.

The same argument, compressed for reference rather than for reading:

| | |
|---|---|
| **The problem** | Not forgetting - **every agent learns alone.** At multi-agent scale agents repeat each other's mistakes because "they learn from their mistakes independently", producing duplication and fragmentation (`n10`). |
| **Why the obvious answer fails** | "Make the agent curate better" cannot work, and the reason is the sharpest idea in the talk: an agent asked to **finish its task** *and* **maintain memory quality** trades them off silently. One loop, two objectives, untunable (`n12`). |
| **The idea** | **Two clocks.** Memory does real-time writes as agents work; **dreaming** is a periodic batch pass that runs out of band, reads session transcripts, and rewrites the store between sessions (`n11`, `n14`). |
| **How it works** | Memory is a **plain file system** the model drives with familiar tools, chosen over a bespoke API on the "get out of the model's way" bet that produced skills (`n2`, `n3`). Multi-agent needs three things a single-user store does not: **scopes** (read-only org-wide + read-write team), **optimistic concurrency** via a `content_sha256` write precondition, and **per-session attribution** (`n5`-`n7`). |
| **What it costs** | Test-time compute, paid by a process that completes no user task and repaid to every downstream agent (`n13`). And an unexamined attack surface: a shared store carrying **imperatives** is a coordination channel, with attribution as forensics but **no admission control**. |
| **The gap** | Dreaming's output is called "**a verified**, better organized snapshot". **Nothing says what verification means, who performs it, or what happens on failure** (`d4`). For a system premised on unsupervised writes drifting, that is the load-bearing step and the only one with no mechanism. |
| **How far to trust it** | **T2 vendor talk about its own product, at its own conference. Every outcome number is a customer testimonial** with no baseline, no n and no eval set. **Read it for the architecture; never for the numbers.** The live demo is the real evidence. |

## Key claims

- **Decouple curation from the work loop because of objective conflict, not throughput.** `n12`
  `&t=764s`
- **Two clocks**: real-time writes as agents work, periodic batch updates between sessions. `n14`
  `&t=921s`
- **Model memory as a file system, not a memory API** - the same bet that produced skills. `n2` `n3`
  `&t=386s`
- **Multi-agent memory needs scopes, optimistic concurrency and attribution.** `n5`-`n7` `&t=466s`
- **Agents write instructions to their successors, not just facts.** `n20` `&t=1004s`
- **A memory architecture decomposes into storage / structure / process.** `n9` `&t=566s`
- **Curation is test-time compute with an asymmetric payer.** `n13` `&t=890s` ⚠️ `single-leg`
- ⚠️ **Every outcome figure is a vendor-selected customer testimonial.** `n17` `n18` - direction only.

## What you will learn, and in what order

```mermaid
flowchart TB
    subgraph A["A. The problem is coordination, not forgetting"]
        S1["1 - Every agent<br/>learns alone"]
        S2["2 - Why 'curate better'<br/>cannot work"]
    end
    subgraph B["B. The storage bet"]
        S3["3 - Memory as a<br/>file system"]
        S4["4 - What multi-agent<br/>needs that solo does not"]
    end
    subgraph C["C. The second clock"]
        S5["5 - Dreaming:<br/>out of band, batch"]
        S6["6 - Seen running:<br/>the demo"]
    end
    subgraph D["D. Where it points, and what it leaves open"]
        S7["7 - Organizational<br/>memory"]
        S8["8 - The hole:<br/>'verified' by what?"]
    end
    A --> B --> C --> D
    S1 --- S2
    S3 --- S4
    S5 --- S6
    S7 --- S8

    style A fill:#e8f0fc
    style D fill:#fbf1dc
```

The diagram runs top to bottom in the order of the argument, in four movements, and every box is a
numbered section below. Two of the movements are shaded. Blue marks the transferable idea, and amber
marks the place where the talk stops short. **The crux is that the blue movement, unusually, carries a
*diagnosis* rather than a mechanism - objective conflict generalises far past memory - while the amber
movement holds the hole the whole design rests on.**

Movement A does no design work at all, and that is deliberate. Its only job is to move the reader off
the word "memory" and onto coordination, because the storage decisions that follow look arbitrary
until you accept that the problem is many agents failing to learn from each other rather than one
agent failing to recall. A reader who already holds that framing can skim it, at the cost of losing
the reason the rest is shaped the way it is.

Movement B is where the design becomes concrete, and it is written as a derivation. Section 3 fixes
what memory *is*, which immediately forces section 4 to ask what breaks the moment a second writer
exists. Reading those two out of order will still tell you what the components are, but it hides which
of them are load-bearing, and the answer is not the one a reader guesses.

Movement C is the payload. It introduces the second clock and then, in section 6, shows it running,
which matters more than usual here because the demo is the only evidence in the source that is not the
vendor describing itself. If you read one movement, read this one.

Movement D is separated from the rest for a reason worth stating, since it holds both the most
ambitious claim in the talk and its largest gap, and the two only make sense together. **Section 8 is
the part to carry away**, because the design's premise is that unsupervised writes drift, and the step
that is supposed to catch the drift is the one step with no mechanism behind it.

*Synthesized roadmap of this note - not from the source.*

## 1. The problem is not forgetting - it is that every agent learns alone

A memory talk usually starts with recall. This one starts with **coordination**, and that reframe is
what makes the rest worth reading, because it changes which problems count as memory problems at all.

![Slide "Memory lets agents learn": three columns - learning about tasks, about environments, and from other agents](visuals/frame_200.jpg)

- What it teaches: agents learn from **three** sources, not one - about **tasks** (success criteria,
  common mistakes), about **environments** (tools, codebases, users), and **from other agents**
  (patterns across many agents working together). `n16` `&t=210s`
- Corroborated by: "agents can learn from common strategies and previous mistakes... And finally, they
  can transfer these learnings to and from other agents."

Two of those three columns are familiar. A single-user assistant learns about tasks and about its
environment, and both of those are recall problems in the ordinary sense. The third column is the one
a single-user memory system never has to think about, and it is where the diagnosis lands.

> At multi-agent scale, agents "were prone to making many of the same mistakes, and **they learn from
> their mistakes independently**... memory was being updated in a **locally optimal way, but it wasn't
> globally optimal**. In some cases, there was duplication or fragmentation." (`n10`, `&t=615s`)

The slide that goes with it draws the shape of the fix before the talk has argued for it, which is
worth looking at now and holding until section 5.

![Slide "Out-of-band memory updates": shared learnings across agents contrasted against independent memory curation](visuals/frame_772.jpg)

- What it teaches: the two panels separate the **shared write path** (Agent A / B / C sessions writing
  separately) from an **independent memory curation** box - curation drawn *outside* the session lane.
  `n10` `n12` `&t=615s`
- Corroborated by: the narration naming duplication and fragmentation as the observed symptoms.

Read "locally optimal, globally suboptimal" as the whole problem statement. Each agent's write is
individually reasonable, and the store degrades anyway, because nothing is responsible for the store
as a whole. In other words this is a coordination failure rather than a memory failure. That
distinction is what decides the shape of the answer, since a coordination failure is not something any
one participant can fix from where it stands.

At first glance there is still a cheaper answer available, and it is the one most teams reach for.

## 2. Why "just make the agent curate better" cannot work

The cheaper answer is to keep one loop and simply instruct it better, telling the agent to tidy the
store as it goes. The talk rejects that, and its reasoning is the sharpest idea in the source
(`n12`, `&t=764s`). It is worth walking the three things a decoupled curation loop buys, because only
one of them is the real argument and the other two are easy to mistake for it.

The first is cross-session pattern detection. A pattern that only shows up across many sessions is
invisible from inside any one of them, not because the agent is careless but because the evidence is
not in its context. That is an information argument, and it is genuine, but a sufficiently clever
in-session prompt could in principle be handed a summary of other sessions.

The third is latency, and it is the weakest of the three. Moving curation off the hot path means it
can afford to be expensive, which is a real operational benefit and no kind of correctness argument.

The second is the one that actually decides the design. **An agent told to finish its task *and* to
maintain memory quality will trade the two off silently.** It does not report "I spent 15% less effort
on memory in order to finish faster". It simply does it, invisibly, under whatever pressure the task
is applying. A separate process has exactly one objective and therefore has nothing to trade. The
first argument says a single loop lacks information; the second says it lacks *incentive*, and no
amount of extra information fixes an incentive.

Compressed for reference:

| Reason to run curation out of band | What it buys |
|---|---|
| Cross-session pattern detection | Patterns *across* sessions are invisible from inside any one of them. An **information** argument. |
| **No objective conflict** | **An agent told to finish its task *and* maintain memory quality will trade them off silently.** A separate process has exactly one objective. |
| No added latency | Curation is off the hot path, so it can afford to be expensive. |

The durable idea in the middle row is not really about memory at all. Whenever one loop is asked to
optimise two things, you have created a trade-off you can neither observe nor tune. That generalises
to anything with a producer and a critic inside the same process, which is why it is the claim from
this source most worth carrying elsewhere.

> **Background, supplied.** This is a **conflict of interest**, and every discipline that has met it
> answers the same way, which is structural separation rather than better instructions. Auditors do
> not audit their own accounts. Code review is performed by someone other than the author. Separation
> of duties exists as a control precisely because "just be careful" does not survive incentive
> pressure. **The design move is always the same - remove the conflicted party from the decision
> rather than asking them to hold both objectives honestly.**

> **And this brain records the same shape twice more.** S4's generator/evaluator split exists to
> defeat **self-evaluation bias**, not to add capability
> ([`brain/claims.md`](../../brain/claims.md) claim 34). S1 stacks QA gates as separate stages. **Three
> sources, three domains, one answer: when a loop has two objectives, split the loop.**

So curation gets its own process. Before that second process can be described, though, the thing it
curates needs a shape, and the choice made there is a bet rather than an engineering detail.

## 3. Memory as a file system, on the skills bet

![Slide "How agent memory evolved": a four-stage ladder from CLAUDE.md to memory tool to skills to memory/](visuals/frame_330.jpg)

- What it teaches: agent memory evolved as a **ladder of four formats**, each loosening who may write
  - `CLAUDE.md` (a single file) -> `memory tool` (a bespoke API) -> **`skills` (procedural memory)**
  -> `memory/` (files agents read and write). `n1` `n3` `&t=338s`
- Corroborated by: "previously, we built memory focusing on capabilities in the harness... you might
  be familiar with Claude.md for Claude code, or dedicated memory tools in the SDKs."

Note where `skills` sits on that ladder, because it is a gift to a neighbouring topic. Skills are
labelled **procedural memory**, which places skills and memory in one family rather than treating them
as two adjacent subjects. One is memory of *how to do things*, and the other is memory of facts. Where
the ladder ends is the more consequential part, and the next slide states the rationale.

![Slide "Built to maximize intelligence": filesystem-native, flexible and agent-native, over an org-conventions tree](visuals/frame_392.jpg)

- What it teaches: memory is modelled as a **plain file system to the model** - deliberately - because
  the model is already strong at navigating file systems with `bash` and `grep` rather than at a
  bespoke memory API. `n2` `n4` `&t=386s`
- Corroborated by: "Models and Claude are great at navigating virtual environments and a file
  system... with memory, we've modeled it as a file system to Claude."

The reasoning is stated openly, and it is a bet rather than a result. The talk's words are that *"as
models improve, we really just want to get out of Claude's way, **similar to what we did with
skills**. And skills was a very basic format that was highly flexible"* (`n3`). In other words the
argument is not that a file system is a better data model. It is that the model has already outgrown
the abstraction the alternative would impose on it.

> **This is claim 31 applied to memory.** Every harness component encodes an assumption about what the
> model cannot do alone, and those assumptions expire. **A bespoke memory API assumes the model cannot
> manage files. This design bets that assumption has already expired.** It is a bet, not a result -
> and if it is wrong, it is wrong quietly, because a model that navigates files *badly* still produces
> plausible-looking memory.

⚠️ The capability claim offered alongside it needs a label at the point of use. The assertion that
Opus 4.7 is "state-of-the-art at file system-based memory" and therefore needs less up-front context
(`n4`) is a **vendor claim about its own model, with no benchmark, no comparison point and no method.**
Treat the design rationale as transferable and the capability figure as marketing.

A file system is enough for one agent. It stops being enough the moment there is a second one, and
what it stops being enough for is not what most readers guess.

## 4. What multi-agent memory needs that a single-user store never does

![Slide "Built for multi-agent systems": sharing across agents, read/write scopes, optimistic concurrency, with a read-only org-conventions store paired against a read-write team-memory store](visuals/frame_460.jpg)

- What it teaches: **scopes form a hierarchy** - a read-only org-wide store updated infrequently and
  readable by all agents, plus granular read-write stores the same agents write freely, with multiple
  stores attached per session at different access levels. Plus **optimistic concurrency**: "agents can
  safely write to the same memory files without overwriting each other's learnings". `n5` `n6`
  `&t=466s`
- Corroborated by: "we offer read-only scopes and read-write scopes... And so, this creates a
  hierarchy."

Scopes answer who may write where, and concurrency answers what happens when two writers arrive at
once. Neither answers the question a reader should ask next, which is how anyone later reconstructs
what happened. That is the third slide's job.

![Slide "Built for auditability and developer control": versioning with rollback and diffing, attribution linking every memory to its session, and a portable standalone API](visuals/frame_522.jpg)

- What it teaches: **versioning** (history, rollback, diffing), **attribution** (every memory links to
  the session that produced it), and **portability** (a standalone CRUD API with export and redaction,
  decoupled from the agent runtime). `n7` `n8` `&t=514s`
- Corroborated by: "version control creates an audit trail as agents make changes... And there's
  attribution to see which agent wrote which part of the memory."

> **Background, supplied - and the concurrency choice is the interesting one.** **Optimistic**
> concurrency assumes conflicts are rare. You read, you compute, and at write time you assert that
> nothing changed underneath you, here via a **content hash precondition**, failing loudly if it did.
> **Pessimistic** concurrency takes a lock up front instead. The optimistic choice is right when
> conflicts are rare and holding a lock is expensive, which describes agents writing notes precisely.
> **What it buys is that a conflict becomes a visible, retryable failure rather than a silent
> overwrite** - and "silent" is the word doing the work, because a clobbered memory is exactly the kind
> of loss nobody would ever notice.

The generalisable rule is that the moment a second writer exists, memory needs the machinery of a
versioned multi-writer store, meaning preconditions, attribution and history. A single-loop design
needs none of it. That is exactly why single-loop designs look simpler and why they stop working at
the second agent.

All of that governs writes made while agents work. Now the second clock.

## 5. Dreaming: the batch pass that runs out of band

![Slide "How dreaming works": transcripts from agents' daily sessions feeding a periodic batch process, producing an updated memory state with new insights and organized structure](visuals/frame_708.jpg)

- What it teaches: each run **analyses session transcripts**, inspects existing memory state, and
  **proposes optimisations** where sessions were inefficient, made mistakes, or needed better
  guidance. The output is a reorganised snapshot agents "can choose to adopt". `n11` `&t=700s`
- Corroborated by: "**It is a batch process. It runs out of band from sessions. It's completely
  decoupled.**"

The input is transcripts rather than the memory store itself, which is the detail that makes the
information argument from section 2 concrete. Dreaming can see what agents *did* and not merely what
they chose to write down. The architecture that results fits into one picture.

![Slide "A unified memory system": agent sessions and a team-memory store on the left, session transcripts feeding a Dreaming pass that verifies, organizes and enriches on the right](visuals/frame_925.jpg)

- What it teaches: **the two-clock architecture in one picture, and the best single visual in the
  source.** The footers name the distinction the whole topic turns on - "**Memory** - real-time
  updates as agents work" against "**Dreaming** - periodic batch updates between sessions". `n14`
  `&t=921s`
- Corroborated by: "Memory on the left helps agents learn and remember from task to task. And dreaming
  on the right verifies, organizes, and enriches the memory."

The talk then generalises away from its own product, and this is the piece most worth stealing.

![Slide "Components of the memory architecture": three panels - storage, structure, and process](visuals/frame_574.jpg)

- What it teaches: a memory architecture decomposes into exactly three components - **storage** (where
  data lives, what metadata is tracked), **structure** (how memory is formatted, what the model is
  steered to remember), and **process** (how often memory is updated, where it is derived from).
  `n9` `&t=566s`
- Corroborated by: the narration walking all three in order.

Keep that decomposition as a checklist, because most memory discussions collapse all three into "what
do we store". Structure and process are separate decisions from storage, and this talk's entire
contribution lives in the third of them.

Two further details are worth recording, and both are `single-leg`. Dreaming is framed as **test-time
compute applied to memory**, meaning you spend tokens up front and the return is paid to every
downstream agent (`n13`, `&t=890s`). And its trigger is programmable, so a run can be fired ad hoc,
nightly, hourly or on an event, all through the API (`n22`, `&t=715s`).

> **The economics are worth stating plainly, because they are what make an expensive pass sane.** The
> cost is borne **once, by a process that completes no user task**, and the return is paid to **every
> downstream agent**. That asymmetry only works because the curator runs on a different clock. A
> curator sitting inside the session would be spending the user's latency budget on someone else's
> benefit.

Everything to this point is the vendor describing itself. The next section is the one place that
changes.

## 6. Seen running: the strongest evidence in the source

Slides show what a vendor believes. The demo shows the artifact, and here it carries detail the
narration never states.

![A live memory file showing a version strip, session attribution, and a content_sha256 write precondition](visuals/frame_1030.jpg)

- What it teaches: three metadata rows do the work - `version` (`v1..v6 head`), `written by` (a session
  ID), and **`precondition content_sha256`** - optimistic concurrency made concrete. **The demo
  supplies the mechanism the narration never names.** `n6` `n7` `&t=1004s`
- And in the body: `sre-agent-a07` ends a triage note with "**Next agent: skip dep checks, go straight
  to config diff**", and one minute later `sre-agent-a16` writes "Confirmed... **per a07's lead,
  skipped dep checks**". `n20`

Read those two lines again before moving on, because the speaker passes over them and they are the
most interesting thing in the talk. What one agent wrote was not a fact. It was an order, and the next
agent followed it.

> **A memory store carrying imperatives is a coordination channel, not a knowledge base.** That is a
> different object with different failure modes: **a wrong *fact* degrades one answer; a wrong
> *instruction* redirects every agent that reads it.** Nothing in the source addresses what happens
> when a bad instruction lands there - see the security note below, which this finding makes
> considerably less theoretical.

The console showing dreaming itself is the second half of the demo, and it answers how the pass is
implemented rather than what it produces.

![The dreaming console: a dream detail pane showing input sessions and duration, beside a memory-updates pane showing a red/green line diff](visuals/frame_1188.jpg)

- What it teaches: dreaming is itself built on the same agent platform it serves, fanning out
  **parallel sub-agents** to analyse transcripts - the pane shows an input store, **6 input sessions**,
  an output store and a duration of `7m 12s`. And its output is **a reviewable diff**. `n19` `n21`
  `&t=1161s`
- Corroborated by: "it spins off a series of sub-agents to analyze transcripts in parallel."

What dreaming actually added in that run is the useful detail. It detected a common pattern of an
alert triggering 60 seconds after a CPU spike, found it **across sessions and agents**, inferred a
likely retry-behaviour problem, and rewrote the triage log "in a more holistic way rather than just
being a rote log of all the events that happened" (`n21`). That is precisely the cross-session
generalisation section 2 argued a single agent structurally cannot reach, observed rather than
asserted.

Having shown the mechanism working at the scale of one team, the talk turns to where it is meant to
end up.

## 7. Where it points: organizational memory

![Slide "From task memory to organizational memory": per-task notes, to a curated memory tree, to org-wide memory](visuals/frame_835.jpg)

- What it teaches: the intended end state - `task-notes.md` (per-task notes) -> `memory/` (curated,
  organized) -> **organizational memory** (large scale, org-wide sharing and contributions; agents
  read and write, dreaming organizes). `n15` `&t=873s`
- Corroborated by: "memory becomes a huge source of knowledge that Claude can use to understand the
  organization and the world that it's operating in."

The ambition is explicit, which is memory as the model's understanding of how a whole company works.
Take it as a direction of travel rather than a shipped capability. Note also that it makes every gap in
the next section larger rather than smaller, because a poisoned entry in a per-task note misleads one
agent while a poisoned entry in org-wide memory misleads everyone.

⚠️ The outcome figures offered alongside that vision are the weakest evidence in the source, and they
are worth looking at precisely so you know not to reuse them.

![Slide "Teams using memory today": three attributed customer pull-quotes](visuals/frame_280.jpg)

- What it teaches: Rakuten reports "97% fewer first-pass errors at 27% lower cost and 34% lower
  latency"; Wisedocs that cross-session memory "sped verification up 30%"; Ando that it let them stop
  building memory infrastructure. `n17` `&t=275s`
- ⚠️ **These are vendor-curated testimonials on a marketing slide.** No methodology is given. No
  baseline is defined. There is no eval set and no replication. The same applies to Harvey's "~6x"
  completion-rate figure for dreaming on a private internal benchmark (`n18`). **Direction only, never
  a measurement.**

Weak numbers are an ordinary hazard in a vendor talk and are easy to discount. The gap in the next
section is not, because it sits inside the design rather than inside the marketing.

## 8. The hole: "verified" by what?

The talk says dreaming's output is "**a verified**, better organized snapshot" that agents "can choose
to adopt" (`d4`, `&t=748s`). Read that sentence as a specification and see how little of it is
specified.

**Nothing in the talk or the demo says what verification means, who or what performs it, what happens
when it fails, or how adoption is decided.**

> **For a system whose entire premise is that unsupervised memory writes drift, this is the
> load-bearing step - and it is the only one with no mechanism, no slide and no demo.** Every other
> claim in the talk has a slide or a running console behind it. This one has a word.

A second gap sits beside it and is easier to miss, because the neighbouring problem *was* solved
(`d5`). The `content_sha256` preconditions from `n6` stop two agents clobbering the same **file**.
Nothing addresses two agents learning contradictory *things*, and the scope hierarchy from section 4
guarantees the case exists, since a read-only org store and a read-write team store can disagree and
nothing states which one wins.

> **Write conflicts are solved; semantic conflicts are not.** The mechanical half is easily mistaken
> for the whole, and it is the half that matters least - two agents overwriting a file is a bug you
> can detect, while two agents believing incompatible things is a bug that reads as normal operation.

One more gap goes unmentioned by the source entirely, and section 6 is what makes it concrete. Memory
here is an **unexamined attack surface**. A background process that ingests session content and writes
durable, automatically-applied instructions is a **persistent prompt-injection sink**, because an
attacker injects once and the instruction is re-applied in every future session with no further access
needed. The demo in section 6 shows that propagation path working exactly as such an attacker would
need it to. The source supplies attribution and version history, and both of those are **forensics
after the fact**. There is **no admission control**, so nothing validates a memory before the next
agent acts on it.

## Diagram (mental model)

```mermaid
flowchart LR
    subgraph WORK["real-time - while agents work"]
        A1["Agent A"] --> ST[("Shared store<br/>scoped, versioned<br/>content_sha256 precondition")]
        A2["Agent B"] --> ST
        A3["Agent C"] --> ST
    end
    ST -->|"session transcripts"| DR{{"DREAMING<br/>batch, out of band<br/>parallel sub-agents"}}
    DR -->|"reviewable diff<br/>verify / organize / enrich"| ST
    DR -.->|"'verified' by WHAT?<br/>no mechanism given"| GAP(("the hole"))
    ORG[("Org-wide store<br/>READ-ONLY")] -->|attach| A1
    ORG --> A2

    style DR fill:#cfe8cf
    style GAP fill:#fbf1dc
    style WORK fill:#f7f7f7
```

Read it left to right, with colour marking which clock a box belongs to. The grey box is the first
clock, where agents write while they work. Green is the second clock, running between sessions. The
amber circle is not a component at all, and it marks the step the talk names and never specifies.
**The crux is that three agents write to one store on one clock while a fourth process rewrites that
same store on a different clock, and the second clock exists so that nothing is ever asked to do both
jobs at once.**

The shape carries three decisions worth noticing, and the first is where dreaming's output arrow
lands. It returns to the **same store** the agents write to rather than to a separate curated copy,
which is what turns adoption into a live question and why "agents can choose to adopt" needs a
mechanism it does not have. The second is that the org-wide store is drawn read-only and *attached*
rather than written, and that asymmetry is the scope hierarchy from section 4. It is also where the
unresolved semantic conflict lives, since nothing says what happens when the org store disagrees with
the team store. The third is that the amber circle is drawn as a gap instead of being omitted, because
a diagram that quietly completed the design would be claiming more than the source does.

*Synthesized from `n5`, `n6`, `n11`, `n12`, `n14`, `n19`, `d4`, `d5` - not a slide from the talk.*

## 💡 Terms

| Term | Explanation |
|---|---|
| Out-of-band (processing) | Work done **outside the request path it affects** - memory curation running between sessions rather than during them. Buys cross-session vantage, **no objective conflict**, and no latency cost. |
| Optimistic concurrency control | Allowing concurrent writes without locking: each write carries a **precondition** (here a `content_sha256` of the content the writer believed it was editing) and **fails rather than clobbering** if the state moved. Turns a silent loss into a visible, retryable failure. |
| Memory scope | The access level a store is attached at, and the unit of multi-agent memory design. Read-only org-wide stores hold slow-changing conventions; read-write task stores hold what one team's agents are currently learning. |
| Procedural memory | Memory of **how to do things** rather than of facts. S7's ladder names `skills` as exactly this rung, putting skills and memory in one family. |
| Organizational memory | The end state argued toward: per-task notes grown into an org-wide store functioning as the model's understanding of how a whole company works. |
| Test-time compute (applied to memory) | Spending tokens up front to curate, on the bet it pays downstream. The payer completes no user task; every later agent collects. |

## What to distrust in this note

- **A T2 vendor talk about the vendor's own product, at the vendor's own conference.** Split it in two
  when reading: the **mechanism** claims (`n1`-`n12`, `n14`-`n16`, `n19`-`n22`) are transferable and
  stand on their own logic; the **outcome** claims (`n4`, `n17`, `n18`) are vendor-selected customer
  quotes.
- **Every outcome number here is a testimonial, and this source is the softer of the memory pair.**
  S6's figures at least came from the publisher's own chart specs - exact, method undisclosed. S7's
  are pull-quotes on a marketing slide with **no chart, no baseline and no eval set**. A 97% or a 6x
  with no n cannot refute anything. **Never cite them as measured results.**
- **The live demo is the genuinely strong evidence**, and it is worth saying why: a running console
  showing a `content_sha256` field, a version strip, and one agent consuming another's note a minute
  later is **a photograph of the artifact**, not a restatement of the pitch. In two places (`n6`,
  `n20`) it carries detail the narration never states.
- **This was the source that could have settled the topic's headline question, and does not.** It sits
  on the right side of both axes - an agent platform, a maintained rather than append-only memory -
  and supplies **design conviction and testimonials instead of a method.** Whether a *maintained*
  memory helps an *agent* remains unmeasured. See [`memory.md`](../../brain/topics/memory.md).
- **Convergence with S6 is real evidence about the design, and none about efficacy.** Two independent
  vendors reaching the same architecture rules out copying. **It would look identical if both were
  wrong.**
- **The "Background, supplied" blocks are mine** - conflict of interest as a structural rather than
  instructional problem, and optimistic versus pessimistic concurrency. Uncited by construction.

## Open questions

- **What does "verified" mean?** (`d4`) The load-bearing step of the whole design, with no mechanism,
  no slide and no demo behind it. **The highest-value question on this source.**
- **Who arbitrates semantic conflicts?** (`d5`) Write conflicts are solved; two agents learning
  contradictory things is not addressed, and the scope hierarchy guarantees the case arises.
- **What defends a shared memory store?** A background process writing durable, auto-applied
  instructions is a persistent prompt-injection sink, and the demo shows the propagation path working.
  Attribution and version history are forensics; **there is no admission control.** See
  [`agent-security.md`](../../brain/topics/agent-security.md).
- **Is the METR task-horizon claim sound?** The talk rests its motivation on a 2025 study that agent
  task length doubles every ~7 months (`n23`, `single-leg`). It is external, public and checkable -
  **the cheapest external corroboration available to this topic.**
- **Is the sleep analogy load-bearing?** Two vendors independently chose the name "dreaming" and
  **neither cites the memory-consolidation literature.** S8 calls the same operation *lint*, which is
  mild evidence the metaphor is decoration.

## Feeds these topics

- `../../brain/topics/memory.md` - the multi-agent half: memory as a tool-accessible file system,
  scoped stores, optimistic concurrency, attribution, and the objective-conflict rationale for
  decoupling.
- `../../brain/topics/agents.md` - split a loop rather than let it hold two objectives.
- `../../brain/topics/skills.md` - skills as procedural memory (the category name).
- `../../brain/topics/agent-security.md` - shared memory as a prompt-injection sink with a
  demonstrated propagation path.
