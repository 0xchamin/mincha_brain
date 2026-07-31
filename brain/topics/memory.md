# Topic: Memory

**Status:** emerging (1 source - S6 "Dreaming: Better memory for a more helpful ChatGPT", OpenAI,
2026-06-04).
**Basis:** first source on this topic, created under [ADR-0007](../decisions/0007-memory-topic.md).
**Read the evidence limit first:** S6 is a **T2 vendor post about the vendor's own consumer product**,
and its three eval charts did not survive capture, so **this topic currently contains mechanism and
zero measurement.** Every claim below is a design argument, not a result. `established` needs a
genuinely independent second source - the parked
`sources/260731_agent-memory-and-dreaming/` capture (Anthropic, in flight under another agent) is the
obvious candidate - **merge into this note, do not create a second one.**

> Living, cross-source synthesis on agent and assistant memory. Many sources feed this note; **merge
> and de-duplicate** as they arrive (architect persona). Every claim cited.

## What this covers

How a system remembers **across sessions**: what gets written and when, how the stored thing is
represented, how it is kept true as the world changes, how the human inspects and corrects it, and
how you evaluate whether any of it works.

**Boundary with the neighbours** - the reason this is its own note (ADR-0007):

- [`context-engineering.md`](context-engineering.md) owns **which tokens reach the model in one
  call**. This note owns **what persists between calls and who maintains it.** Memory is an *input*
  to context engineering; the maintenance problem is not a context problem.
- [`rag.md`](rag.md) owns **retrieval over a corpus someone else authored**. Memory is a corpus **the
  system authors about its user**, which is why it can be wrong in a way a document store cannot: a
  retrieved document is stale *as a document*, a memory is stale *as a belief*.

## Synthesis

### The failure that motivates everything: staleness is not irrelevance

Memory written **during** a conversation is written in that conversation's tense. Nothing revisits it,
so it decays into **confident wrongness** rather than into uselessness [S6 §How memory has evolved,
`n1`; corroborated by the saved-memories UI, which carries no timestamp, expiry or revision affordance
on any row].

> **Keep the distinction sharp: a missing fact degrades an answer; a stale fact poisons it.** The
> system acts on a stale fact with full confidence. "I'm going to Singapore in July" is true in June
> and actively harmful in August, and a store with no revision mechanism has nowhere to put the
> difference.

This is the diagnosis worth carrying to any memory design, and it is independent of the product.

### The second failure: explicit-cue capture under-collects

A memory that fires only on "remember that..." collects what a user thinks to dictate and nothing
else - "like talking to someone who took a few notes, but still forgot everything that wasn't written
down" [S6 §How memory has evolved, `n2`].

The category it misses is named, and is the useful part [S6 §Following preferences, `n8`,
single-leg]:

| Kind of preference | Example | How it is stated |
|---|---|---|
| Response instruction | "don't bring up Stan again" | Explicit, imperative - easy |
| Stated constraint | "I'm vegetarian" | Explicit, declarative - easy |
| **Implicit preference** | "I live near San Francisco" | **Never stated as a preference at all** |

The third row is where explicit capture structurally fails, and it is also the row that does the most
work in practice, because it governs relevance rather than a single answer.

### The architecture: a second loop on a second clock

**Dreaming** is a background process that reads across many past conversations and **synthesizes** the
memory state, rather than appending to it during a chat [S6 §How memory has evolved, `n3`;
corroborated by a "Memory summary - Updated 2h ago" header, a write with no user action attached].

> 💡 **Dreaming** - memory maintenance as a scheduled process between sessions, decoupled from the
> conversation turn. Named for sleep-time memory consolidation; the source does not cite that
> literature, so the analogy is framing, not evidence.

**The transferable claim is the decoupling, not the name.** A write that only happens while the user
is talking can only ever record the present tense of that talk; giving some process the standing *job*
of revisiting is the only way revision happens at all.

### Revision over expiry

The maintenance operation is a **rewrite**, not a TTL: "You're going to Singapore in July" becomes
"You went to Singapore in July 2026" when the trip ends [S6 §Staying current over time, `n5`;
corroborated by the paired worked example, where the stale answer assumes Singapore local time and
the maintained answer uses the user's home location].

This is a real design choice with a real alternative. Expiry deletes and loses the fact; revision
preserves it with an updated tense, so "went to Singapore in July 2026" remains usable context
afterwards. **Expiry treats age as invalidity; revision treats age as information.**

### Representation is a maintenance decision, not a storage one

The shipped change is visible as a before/after over the same persona [S6 §How memory has evolved,
`n4`]:

| | Saved memories | Memory summary |
|---|---|---|
| Shape | 14 flat atomic assertions | 4 narrative prose sections |
| Written | during the conversation, on an explicit cue | by a background pass, on its own clock |
| Revisable | no affordance exists | the whole artifact is rewritten each pass |

**The generalisable rule: pick the representation whose edits you can express.** You cannot rewrite
row 7 of an append-only list into the past tense when nothing owns that list; you can rewrite a clause
in a paragraph that a process is responsible for maintaining. The list form is not merely less
readable - it makes the required operation inexpressible.

### Put the human on the synthesized artifact

Correction is offered on the **summary** - the thing the process wrote - not on the underlying records
[S6 §How memory has evolved, `n6`; corroborated by the UI, where selecting a sentence raises
`Make a correction` / `Don't mention this again` and the modal carries an `Add or update` composer].

This is the only tractable choice once a background process is authoring: asking a user to hand-curate
an append-only fact table is asking them to do the job you just automated. **But note the unresolved
consequence** - nothing in the source says a correction is a durable override rather than another
input to the next synthesis pass. That difference is the difference between user control and the
appearance of it, and it is an open question below.

Memory also ships as **governable surface** rather than as an implementation detail: five separate
switches, including one governing *proactive* use [S6, `n11`].

### Evaluating memory: three objectives, not one metric

The most portable frame in the topic [S6 §How we evaluate memory, `n7`]:

| Objective | The question it asks | The failure it catches |
|---|---|---|
| Carry forward useful context | Told once, is it still known later? | Under-capture |
| Follow preferences and constraints | Does **behaviour** change to match? | Capture without application |
| Stay current over time | Does the answer change when the world does? | **Staleness** |

Two things make this worth keeping. **Row two separates recall from compliance** - a system can
retrieve "I'm vegetarian" and still recommend a steak house, and a single "memory accuracy" number
hides that entirely. **Row three is the one most memory evaluations omit**, because it is the only one
that requires constructing a case where the correct answer changes with the passage of time while the
stored fact does not.

This is a memory-specific instance of the pattern in [`evals.md`](evals.md): making a subjective
quality gradable by fixing the *question* rather than by finding a better judge.

### The tension this topic must not paper over

[`context-engineering.md`](context-engineering.md) records, from R1's measured evidence, that **naive
episodic memory scaffolding never improved long-horizon reliability and hurt 6 of 10 models**, losing
to plain ReAct - the measured win was *decomposition*, not *remembering more* (claim 24, T3 preprint,
10 models).

S6 is best read as an argument that the thing measured there is the wrong design - append-everything
episodic memory is precisely what `n1` and `n4` diagnose as broken - and that a **maintained,
synthesized** memory is a different object. **That argument is entirely unmeasured.** The honest
position for now:

> **The one measured result in this brain about agent memory says memory scaffolds hurt. The one
> source advocating memory offers no measurement.** Do not resolve this in favour of the vendor. Any
> future claim that maintained memory beats decomposition needs evidence that S6 does not supply.

## Key claims

| Claim | Sources (cited) | Confidence |
|---|---|---|
| Write-once memory goes stale as a structural property: written in the conversation's tense, never revisited, it decays into confident wrongness rather than irrelevance. | S6 §How memory has evolved (prose + `fig_saved_memories`) | emerging |
| Explicit-cue capture under-collects; **implicit preferences** (never uttered as instructions) are the category it structurally misses. | S6 §How memory has evolved, §Following preferences | emerging (the taxonomy is single-leg) |
| Decouple the memory write from the conversation turn - synthesis is a background process on its own clock, which is what makes revision possible at all. | S6 §How memory has evolved (prose + "Updated 2h ago") | emerging |
| **Revision, not expiry:** rewrite a stale memory into a new tense rather than deleting it. Expiry treats age as invalidity; revision treats age as information. | S6 §Staying current over time (prose + paired worked example) | emerging |
| Representation is a maintenance decision - pick the shape whose edits you can express. A flat append-only list makes revision inexpressible; a maintained narrative does not. | S6 §How memory has evolved (`fig_saved_memories` vs `fig_memory_summary`, same persona) | emerging |
| Offer correction on the **synthesized artifact**, not on the raw records - once a process authors memory, hand-curating its inputs is the job you just automated. | S6 §How memory has evolved (prose + `fig_memory_summary`) | emerging |
| "Good memory" decomposes into three separately-evaluable objectives - carry forward, follow preferences, stay current - and only the third can fail purely through the passage of time. | S6 §How we evaluate memory | emerging |
| Memory synthesis is expensive enough to gate rollout: **cost, not answer quality**, was the stated constraint on serving it universally (a claimed ~5x compute reduction unlocked it). | S6 §A more scalable foundation for the future | needs-check (single-leg, vendor self-report, no method) |

## Key visuals

![Saved memories: a flat, append-only list of atomic assertions](../../sources/260731_chatgpt-memory-dreaming/visuals/fig_saved_memories.png)
> The old representation: 14 atomic rows, no timestamp, no expiry, no revision affordance. The data
> model has nowhere to put the information that a fact has aged. S6 §How memory has evolved.

![Memory summary: the same person as a maintained narrative, with correction affordances](../../sources/260731_chatgpt-memory-dreaming/visuals/fig_memory_summary.png)
> The same persona as four prose sections. Two details carry the meaning: "Updated 2h ago" (a write
> with no user action) and `Make a correction` / `Don't mention this again` on any selected sentence.
> S6 §How memory has evolved.

![Memory settings: five switches, including one for proactive use](../../sources/260731_chatgpt-memory-dreaming/visuals/fig_memory_settings.png)
> Memory as governable surface. Also the evidence that the older saved-memories store still ships as
> its own toggle, despite the article's replacement framing. S6 §How memory has evolved.

## Open questions / conflicts

- **This topic has no measurements at all.** S6's three eval charts are client-rendered and did not
  survive capture (`nodes.md` `d1`), so every claim above is a design argument. **The highest-value
  next step for this topic is any source that measures memory quality.**
- **Unresolved against claim 24** - see "The tension this topic must not paper over". Measured
  evidence says naive memory scaffolds hurt; the advocate offers no numbers. Not resolved here.
- **Does a user correction survive the next synthesis pass?** `n6` establishes the affordance;
  nothing establishes whether it is a durable override or another input. This is the difference
  between control and its appearance.
- **What is the write-once store still for?** Both `Reference chat history` and `Reference saved
  memories` still ship as separate toggles (`n10`), and the source never says which wins on
  disagreement, or whether saved memories feed dreaming or run parallel to it.
- **Consumer assistant, not agent platform.** One user, one assistant. Nothing here addresses memory
  **shared across agents**, memory as a tool-accessible file system, or who arbitrates when two agents
  learn contradictory things. The in-flight `sources/260731_agent-memory-and-dreaming/` capture
  covers exactly that case.
- **Memory is an unexamined attack surface.** A background process that ingests conversation content
  and writes durable, automatically-applied instructions about a user is a **persistent
  prompt-injection sink** - inject once, and the instruction is re-applied in every future session
  with no further access needed. No source in this brain touches this. See
  [`agent-security.md`](agent-security.md).
- **The sleep analogy is unexamined.** "Dreaming" invokes memory consolidation, and cognitive science
  has an established literature on offline replay and schema formation that would predict which parts
  of this design generalise. S6 cites none of it; the cross-domain hop is unmade and is a good deep
  research target (`AGENTS.md`: "take the cross-domain hop").

## Sources feeding this topic

- **S6** - [Dreaming: Better memory for a more helpful ChatGPT](../../sources/260731_chatgpt-memory-dreaming/LEARNING.md)
  (OpenAI, 2026-06-04). **T2 vendor post about its own consumer product.** Mechanism claims are
  corroborated by product screenshots - real second-leg evidence that the described affordances
  shipped. **No quantitative claim survives capture**; treat every performance statement as
  unevidenced direction.
