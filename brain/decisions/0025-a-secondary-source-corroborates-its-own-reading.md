# ADR 0025: A secondary source corroborates its own reading, not the world

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260815 |
| Deciders | chamin |

## Context

S25 ([Patterns for Building Cybersecurity Evals](../../sources/260815_cybersecurity-evals/LEARNING.md),
Eugene Yan, 2026-06) is **the first survey this brain has ingested**. Every previous source was a
primary: someone describing a system they built, a paper reporting an experiment they ran, a repo
whose code is the artifact. Yan ran none of the seven experiments he writes about. He is summarising
six arXiv preprints and one vendor research page, and embedding those papers' own figures alongside
his summary.

That breaks the corroboration gate in a way the contract did not anticipate. The gate asks for **two
legs that agree** - a visual against the surrounding text for media, code against its docs. Both legs
are nominally present here and they are unusually easy to obtain, because the article embeds eleven
figures and discusses each one in the adjacent paragraph. Running the gate mechanically would have
produced a page of `corroborated / OK` verdicts on a source where **not one number is first-hand**.

The specific thing being tested needs naming precisely, because getting it slightly wrong is what
would launder the source. When Yan's prose agrees with a figure lifted from CyberGym's paper, what has
been established is that **Yan read CyberGym correctly**. That is genuinely worth establishing and it
is worth recording. It is not evidence that CyberGym's method is sound, that its numbers replicate,
or that the benchmark measures what it claims. **Two legs agreeing proves internal consistency and
never truth** is already the global rule; on a secondary source the "internal" shrinks from *the
subject* to *the summary*, and nothing in the contract said so.

The gate then produced a second surprise that forced the rest of this decision. **Six of the eight
divergences found in S25 run the same direction**: the embedded figure carries something the prose
does not, and the prose consistently states the more conservative or more comfortable version. The
largest is `d2`, where a chart annotated with a **1.3-month doubling time** for offensive capability
sits inside an article whose text reports two endpoints from it and never mentions the trend. Others
include a total safety-filter block summarised as partial refusals (`d5`), an entire experimental arm
that appears in half a table's rows and nowhere in the text (`n17`), and a difficulty ceiling stated
without the guidance regime it belongs to (`d1`).

On a normal single-author source a prose-versus-figure divergence is **symmetric** - the author made
both legs, either could be the error, and you record the conflict without picking a winner. That is
what S24's `d1` did. **Here the legs have different provenance and different authority.** The figure
was made by the researchers who ran the experiment; the sentence beside it was written by someone
compressing their paper into a paragraph.

## Decision

**A secondary source is gated normally, with two amendments that must be stated in its `nodes.md`
gate note rather than left implicit.**

1. **`corroborated` degrades to `OK (faithful summary)`.** The verdict word stays, because the check
   really did run and really did pass, and inventing a fourth gate verdict would ripple into
   `validate.py`, the topic notes and every downstream count. What changes is the **confidence
   cell**, which must say what was actually verified. A node reading `corroborated / OK` on a
   secondary source is a bug in the gate note, not a strong claim.
2. **Where prose and figure disagree, the figure wins and the prose is recorded as the defect.** The
   divergence is written as *the article understating its own figure*, not as an unresolved internal
   conflict. This is a deliberate asymmetry and it applies **only** where the figure is demonstrably
   lifted from the primary rather than drawn by the summarizer. Author-drawn diagrams in a secondary
   source are ordinary second legs and stay symmetric.

**Neither amendment upgrades or downgrades the source's tier.** S25 is T4 practitioner writing about
T3 preprints, and it stays there. What this ADR governs is the *gate*, which is a separate axis from
the tier and was the one with no rule.

This is **not a one-way door**. It changes how future survey sources are gated and adds a required
paragraph to their `nodes.md`; nothing already promoted depends on it.

## Alternatives considered

- **Refuse to ingest secondary sources at all, and ingest the primaries instead.** Cleanest in
  principle and wrong in practice. The seven primaries here are a very large amount of reading, and
  the survey's actual contribution - that all seven share one four-primitive structure (claim 198,
  claim 199) - **exists in none of them**. A synthesis across artifacts is a real thing to learn from,
  and this brain would be poorer for a rule that excluded the genre. The correct response is to gate
  it honestly and put the primaries on the reading list, which S25's open questions do.
- **Add a fourth gate verdict, `secondary`, beside `corroborated` / `single-leg` / `divergence`.**
  Attractive and rejected on cost. It would need `validate.py` changes, a new legal value in the
  contract, and a decision about what it means for promotion eligibility - and it would still not
  say *what* was verified, which is the actual information a later reader needs. **A sentence in the
  gate note carries more than a keyword and costs nothing to the toolchain.**
- **Treat every node from a secondary source as `single-leg`.** Superficially the conservative
  option, and it destroys real information. The prose-versus-figure check **does** catch things - it
  caught six divergences in this source - and collapsing a passed check and an absent check into one
  verdict would mean the gate that found `d2` reports the same value as a gate that never ran.
- **Keep divergences symmetric, as on a primary source.** Rejected because it is false here. Treating
  "the paper's own figure" and "a summarizer's sentence about it" as equally authoritative would have
  recorded `d2` as *"the article and its chart disagree about whether there is a trend"*, which is not
  what happened. **The chart is right and the summary is incomplete**, and the note should say so.

## Consequences

**Easier.** Survey and review articles become ingestable without either overstating them or wasting
the check that does work. The gate note now has a stated job on this source class - say what
agreement establishes - which is the same discipline `SOURCE.md`'s `Visual leg` row applies to a
skipped visual leg: **the limitation is recorded rather than discovered.**

**Harder.** Every secondary ingest now owes a paragraph of reasoning before its first node, and the
`Confidence` column stops being a single word. That is the intended cost.

**What to watch.** The asymmetry in amendment 2 depends on correctly telling a lifted figure from an
author-drawn one, and S25 contains both - `fig1` and `fig2` are Yan's own diagrams and were gated
symmetrically, while `fig3` through `fig8` are crops of the primaries. **If that distinction is ever
unclear, gate symmetrically**, because the asymmetry is a privilege extended to the primary artifact
and not to the figure format.

**Revisit if** this brain ever gates a secondary source *and* its primary. At that point the primary's
own nodes supersede the summary's, and this ADR should say what happens to the secondary's promoted
claims - most likely that they are re-cited to the primary and the summary's node retained only as
provenance. Nothing here settles that, because it has not happened yet.

**Follow-ups applied in the same pass.** S25's gate note in
[`nodes.md`](../../sources/260815_cybersecurity-evals/nodes.md) states both amendments and was written
before this ADR; claims 198, 202 and 203 carry the `OK (faithful summary)` qualifier or an explicit
"figure wins" note; and [`evals.md`](../topics/evals.md) records the reading rule in its synthesis.
