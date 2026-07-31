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
  exists, not that dreaming keeps memory fresh.

**The numeric leg was recovered late in the pass (`d1`).** The three eval charts never render in a
static capture, but they are **Vega-Lite** components and their specs - including the full data
arrays - are embedded in the page's RSC flight payload. Extracted to
[`chart_data.json`](chart_data.json), which makes `n12`-`n14` possible. Their second leg is
**the article's own prose direction** ("improves", "a substantial lift"), which is the weak
same-author-twice pairing, so they are gated `corroborated (spec + prose)` for *extraction* accuracy
only.

**Nothing here is externally corroborated.** This is a **T2 vendor** publishing evals of its own
consumer product with **no sample size, eval-set description, methodology or confidence intervals**
anywhere in the page or the specs. The numbers are real and precisely extracted; what they measure is
undisclosed.

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
| n12 | **All three memory objectives improve across both generations, on the vendor's own evals.** Task success, by chart: **Factual recall 41.5 -> 67.9 -> 82.8%**; **Preference adherence 31.4 -> 55.3 -> 71.3%**; **Staying correct over time 9.4 -> 52.2 -> 75.1%** (2024 saved memories -> 2025 saved + Dreaming V0 -> 2026 Dreaming V3). | Vega-Lite specs in the RSC payload -> [`chart_data.json`](chart_data.json) | prose, S6 §§Carrying forward context / Following preferences / Staying current over time ("improves", "a substantial lift") - direction only | corroborated (spec + prose) | needs-check (T2 self-report, **no n, no eval-set description, no method, no CIs**) |
| n13 | **Staleness was the worst failure by a wide margin, and this is the number that carries the article's thesis.** "Staying correct over time" starts at **9.4%** - near-total failure - against 41.5% and 31.4% for the other two objectives, and gains the most (**+65.7 points**). The write-once diagnosis (`n1`) is the only claim here with quantitative support. | `chart_data.json` (9.4% baseline, lowest of three) | prose, S6 §Staying current over time - the worked example where the model still believes the user is in Singapore | corroborated (spec + prose) | needs-check (same T2 limits as `n12`) |
| n14 | **Introducing dreaming at all mattered more than improving it.** The 2024 -> 2025 step (adding Dreaming V0 alongside saved memories) beats the 2025 -> 2026 step (V0 -> V3) on **every** objective: +26.4 vs +14.9, +23.9 vs +16.0, +42.8 vs +22.9. **And the ceiling is low** - even 2026 tops out at 71-83%, so memory still fails roughly **1 task in 5** on the vendor's own measure. | `chart_data.json` (computed deltas across all three charts) | (none - the article never presents deltas, and never mentions the residual failure rate) | single-leg | needs-check (arithmetic on `n12`, so it inherits every limit above) |

## Dropped / divergences (audit trail)

| Candidate | Verdict | Note |
|---|---|---|
| The three eval charts - **the entire quantitative case of the article** (`d1`) | **RESOLVED - recovered 2026-07-31** | Originally recorded as an unrecoverable gap: the charts are client-rendered and show `Loading…` in every static capture, leaving only "improves" / "a substantial lift". **They are Vega-Lite components, and the specs - data arrays included - are embedded in the Next.js RSC flight payload.** Extracted to [`chart_data.json`](chart_data.json); now `n12`-`n14`. **The original warning stands in modified form:** the numbers are precise and the methodology is entirely undisclosed. |
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
