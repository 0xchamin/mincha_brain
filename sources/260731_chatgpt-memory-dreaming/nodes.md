# Knowledge nodes - Dreaming: Better memory for a more helpful ChatGPT

> Persona: **fact-checker** - re-adopt when working this file.

> The atomic units of knowledge extracted from this source. Each node has a **stable ID** (`n1`,
> `n2`, ... - never renumber; topic notes reference these), a claim, **both legs each with its own
> citation** (or one leg marked `single-leg`), a gate verdict, and a confidence. Only
> `corroborated`/`single-leg` nodes (and recorded `divergence` findings) feed `LEARNING.md` and get
> promoted to `../../brain/`. The **fact-checker** persona owns the verdicts; see `../../AGENTS.md`
> and `prd.md` §6.

## What counts as a second leg here

This is a **blog with product screenshots**, so the two legs are the **article prose** and **the
shipped UI in the figures**. That pairing is stronger than the usual blog case, and worth naming:

- A screenshot is **not** the author restating himself in a second rendering (the weakness recorded
  for `260725_harness-design-long-running-apps`, where a table agreed with its own prose). It is a
  **photograph of the artifact the prose describes.** When the text says memory is reviewable and
  correctable and the figure shows a `Make a correction` control, the UI is genuine independent
  evidence that the described mechanism shipped.
- **What it cannot do is show the mechanism works, or how well.** A screenshot proves the affordance
  exists, not that dreaming keeps memory fresh. **Every claim about *quality* in this source is
  single-leg by construction** - and the charts that would have carried them did not survive capture
  (`d1`).

**Nothing here is externally corroborated.** This is a **T2 vendor** writing about its own consumer
product, and the one quantitative claim in the article (`n9`) has no supporting artifact at all.

## Nodes

| ID | Claim (crux) | Evidence leg + citation | Corroborating leg + citation | Gate | Confidence |
|---|---|---|---|---|---|
| n1 | **Write-once memory goes stale as a structural property, not as a bug.** Saved memories were written only during the conversation and never revisited, so they "tend to go stale over time and eventually become incorrect or irrelevant". | prose, S6 §How memory has evolved | `visuals/fig_saved_memories.png` - a flat append-only list of 14 atomic assertions ("Marine biologist in coastal Maine", "Studies whale migration patterns") with **no timestamp, no expiry and no revision affordance** on any row | corroborated | OK |
| n2 | **Explicit-cue memory under-captures.** Saved memories "relied on strong cues to decide when to trigger memory, such as an instruction to 'remember I'm traveling to Singapore in July'", which felt "like talking to someone who took a few notes, but still forgot everything that wasn't written down". | prose, S6 §How memory has evolved | `visuals/fig_saved_memories.png` - every row reads as a discrete user-dictatable fact; none reads as ambient context picked up in passing | corroborated | OK |
| n3 | **Dreaming decouples the memory write from the conversation turn.** It is "a background process that allows ChatGPT to learn from many conversations and synthesize ChatGPT's memory state", rather than writing during the chat. | prose, S6 §How memory has evolved | `visuals/fig_memory_summary.png` - the header reads **"Memory summary - Updated 2h ago"**: an update timestamp with no user action attached to it | corroborated | OK |
| n4 | **The representation changes from a list of facts to a maintained narrative.** The synthesized state is presented as prose sections a reader can "quickly glean the highlights of", not as rows. | prose, S6 §How memory has evolved | the **figure pair over the same persona**: `visuals/fig_saved_memories.png` (14 flat bullets) vs `visuals/fig_memory_summary.png` (4 narrative sections - Overview / Hobbies and Lifestyle / Travel and Culture / Community and Education) | corroborated | OK |
| n5 | **Staleness is handled by rewriting the memory, not by expiring it.** "With dreaming, memories are automatically updated as time passes, allowing ChatGPT to revise its memory from 'You're going to Singapore in July' to 'You went to Singapore in July 2026' when the trip ends." | prose, S6 §Staying current over time | the worked example pair in the same section: the stale-memory answer opens "It's about 5:19 AM Sunday **in Singapore**"; the with-memory answer opens "I'll use **Portola Valley / Ladera** as the starting point" | corroborated | OK |
| n6 | **Correction is offered on the synthesized artifact, not on the raw notes.** The user reviews and repairs the *summary* - the thing the background process wrote - rather than editing underlying memory rows. | prose, S6 §How memory has evolved ("reviewable through a summary... you can... add or update information about yourself, and provide instructions on what topics ChatGPT should bring up and when") | `visuals/fig_memory_summary.png` - selecting a sentence raises **`Make a correction`** and **`Don't mention this again`**; the modal foot carries an **`Add or update`** composer | corroborated | OK |
| n7 | **"Good memory" is decomposed into three separately-evaluable objectives**: carry forward useful context, follow preferences and constraints, and stay current over time - then measured across three system generations (2024 saved memories, 2025 saved + Dreaming V0, 2026 Dreaming V3). | prose, S6 §How we evaluate memory (explicit three-item list + explicit generation ladder) | the article's own structure - three dedicated sections (§Carrying forward context, §Following preferences, §Staying current over time), each closing with an evaluation statement | corroborated (structure) | OK |
| n8 | **Preferences are a three-way category, not one thing**: response instructions ("don't bring up Stan again"), stated personal constraints ("I'm vegetarian"), and **implicit** preferences that shape relevance ("I live near San Francisco" -> local options should be tailored). The third is precisely what explicit-cue memory cannot capture. | prose, S6 §Following preferences | (none - no figure for this taxonomy) | single-leg | needs-check |
| n9 | **Serving cost, not answer quality, was the gate on universal rollout.** "Recent improvements reduced the compute required to serve dreaming to Free users by approximately **5x**, making it possible to begin rolling out dreaming to Free users." | prose, S6 §A more scalable foundation for the future | (none - no chart, no baseline, no methodology) | single-leg | needs-check (vendor self-report, unreplicated, no method given) |
| n10 | **Dreaming was not standalone-viable for a year.** It "supplemented saved memories" from 2025 and "historically was never sufficient as a standalone memory system"; only the 2026 architecture is "built on top of dreaming" as the foundation. | prose, S6 §How memory has evolved | `visuals/fig_memory_settings.png` - `Reference chat history` and `Reference saved memories` are still **two independent toggles**, i.e. the older store is still shipped and separately switchable | corroborated | OK |
| n11 | **Memory is exposed as user-governable surface, not as an implementation detail.** Five separate switches govern it, including one controlling *proactive* use ("Reference memory in suggestions... turning this off will disable Pulse"). | `visuals/fig_memory_settings.png` - Memory section (3 controls) + Pulse section (2 controls) | prose, S6 §How memory has evolved (the summary is reviewable and instructable) plus the closing pointer to a "Memory FAQ... memory user controls" | corroborated | OK |

## Dropped / divergences (audit trail)

| Candidate | Verdict | Note |
|---|---|---|
| The three eval charts - **the entire quantitative case of the article** (`d1`) | **gap, recorded** | The charts are **client-rendered components** and appear as `Loading…` placeholders in every static capture attempted. The recoverable text gives only unquantified direction: "the new dreaming-based system **improves** the model's ability to recall relevant facts"; "Dreaming provides a **substantial lift** in this area". **This means the source contributes mechanism to the brain and no measurement whatsoever.** Do not let "improves" harden into a number later. |
| The two long worked examples - underwater TTL camera gear, Singapore itinerary (`d2`) | dropped | Product demonstrations, not transferable claims. Their *structure* serves as the second leg for `n5`; their content is source-specific trivia and is not promoted. |
| Rollout scope - "Plus and Pro users in the US today", Free/Go "over the coming weeks" (`d3`) | dropped | True but perishable product-release detail with no transferable content. Stays in `raw/` only. |

## Divergence worth naming

**`n10` against the article's own framing.** The prose presents this as a new architecture "built on
top of dreaming" that finally serves as a **shared memory foundation for all users** - the language of
a replacement. The shipped settings panel (`visuals/fig_memory_settings.png`) still exposes
`Reference saved memories` as its own toggle alongside `Reference chat history`.

**This is not a contradiction and must not be filed as one** - the article never claims saved memories
were removed. It is a **completeness gap**: the article does not say what the saved-memories store is
still *for* once a background process maintains a synthesized picture, nor which one wins when the two
disagree. Recorded as an open question in
[`../../brain/topics/memory.md`](../../brain/topics/memory.md), not as a claim.

> **Citations - cite BOTH legs.** Video -> `<youtube-url>&t=<seconds>s`; blog -> `source, <section
> heading>`; paper -> `source, Figure/Table N, §`; **code -> an immutable GitHub blob permalink
> containing the SHA**. A `single-leg` node cites its one leg and leaves the other cell `(none)`.
