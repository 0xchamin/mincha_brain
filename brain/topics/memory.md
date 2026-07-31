# Topic: Memory

**Status:** emerging (1 source - S6 "Dreaming: Better memory for a more helpful ChatGPT", OpenAI,
2026-06-04).
**Basis:** first source on this topic, created under [ADR-0007](../decisions/0007-memory-topic.md).
**Read the evidence limit first:** S6 is a **T2 vendor post about the vendor's own consumer product**.
Its three eval charts are recovered (see "What the numbers say"), so this topic **does** carry
measurements - but they are the vendor's own, with **no sample size, eval-set description, method or
confidence interval published**. Precise numbers, opaque provenance. `established` needs a
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

### What the numbers say

Each objective has a published chart. They never render in a static capture, but they are Vega-Lite
components and their specs were recovered from the page payload [S6, `n12`,
`sources/260731_chatgpt-memory-dreaming/chart_data.json`]. Task success, in percent:

| Objective | 2024 saved memories | 2025 + Dreaming V0 | 2026 Dreaming V3 | Total gain |
|---|---|---|---|---|
| Factual recall | 41.5 | 67.9 | 82.8 | +41.3 |
| Preference adherence | 31.4 | 55.3 | 71.3 | +39.9 |
| Staying correct over time | **9.4** | 52.2 | 75.1 | **+65.7** |

Three readings the source never states:

- **Staleness was catastrophic, not suboptimal** [`n13`]. A 9.4% baseline is a system wrong about
  time-sensitive facts nine times in ten. This is the quantitative backing for the write-once
  diagnosis above, and the only claim in this topic that has any.
- **Introducing dreaming beat improving it** [`n14`]. The 2024 -> 2025 step wins on every objective
  (+26.4 vs +14.9, +23.9 vs +16.0, +42.8 vs +22.9). The architectural move carries the value; V0 -> V3
  is refinement.
- **The ceiling is low.** 2026 tops out at 71-83%, so memory still fails **roughly one task in five**
  on the vendor's own measure. Any design that assumes memory is reliable should carry that number.

> ⚠️ **Precise extraction, opaque method.** These come from the publisher's own chart specs, so the
> figures are exact. But "task success" is never defined and **no sample size, eval set, methodology
> or confidence interval is published anywhere.** They are a vendor's directional self-report about
> its own product, not a benchmark result, and nothing here is independently replicated.

### The tension this topic must not paper over

[`context-engineering.md`](context-engineering.md) records, from R1's measured evidence, that **naive
episodic memory scaffolding never improved long-horizon reliability and hurt 6 of 10 models**, losing
to plain ReAct - the measured win was *decomposition*, not *remembering more* (claim 24, T3 preprint,
10 models).

S6 is best read as an argument that the thing measured there is the wrong design - append-everything
episodic memory is precisely what `n1` and `n4` diagnose as broken - and that a **maintained,
synthesized** memory is a different object. **S6 now has numbers of its own** (`n12`), so the shape of
the disagreement has changed, but it has not gone away.

**Sharpened after recovering the charts: these two results do not measure the same construct, and
that is the actual resolution.**

| | Claim 24 (R1, T3 preprint, 10 models) | S6 (`n12`, T2 vendor self-report) |
|---|---|---|
| System under test | An **agent loop** on long-horizon tasks | A **chat assistant** serving one human |
| Memory design | Naive **episodic append + retrieve** | **Maintained synthesized** user model |
| Metric | Task **reliability** over many steps | **Recall / adherence / freshness** about the user |
| Verdict | Scaffold **hurt 6 of 10 models** | All three objectives improve |

So the honest position is **not** "one says memory helps, the other says it hurts". It is:

> **Nothing in this brain yet measures the same memory design on the same kind of task.** Claim 24
> retires the naive episodic scaffold on agent loops - and S6 agrees with that much, since its whole
> argument is that write-once append-only memory is broken. **Whether a *maintained* memory helps an
> *agent* is measured by neither**, and S6's numbers - vendor-run, methodologically undisclosed, on a
> different system class - cannot be borrowed to answer it.

**This is the highest-value thing an agent-platform memory source could settle**, which is another
reason the second source below matters.

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
| **Staleness was the worst of the three failures by far** - "staying correct over time" starts at **9.4%** against 41.5% and 31.4%, and gains the most (+65.7 pts). The quantitative backing for the write-once diagnosis. | S6 `n13` (recovered chart specs) | needs-check (vendor self-report, no method published) |
| **Introducing memory synthesis beat refining it**, on every objective (2024 -> 2025 gains exceed 2025 -> 2026). **And the ceiling is low: 71-83% in 2026, so memory still fails ~1 task in 5** on the vendor's own measure. | S6 `n14` (deltas computed from the same specs) | needs-check (arithmetic on a self-report; the article states neither) |

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

- ~~**This topic has no measurements at all.**~~ **Closed 2026-07-31** by recovering the chart specs
  (`n12`-`n14`). What replaced it is narrower and sharper: **"task success" is never defined**, and no
  sample size, eval set, method or confidence interval is published. The numbers are exact and their
  meaning is unknown. **Highest-value deep-research target on this topic.**
- **Claim 24 is not actually contradicted** - see the table above. The two results measure different
  memory designs on different system classes. **What no source here measures is whether a *maintained*
  memory helps an *agent*,** which is the question this brain actually needs answered.
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
  shipped. Its eval numbers were recovered from the page's own Vega-Lite chart specs, so **extraction
  is exact and methodology is undisclosed**: treat every performance figure as the vendor's
  directional self-report, never as a benchmark result.
