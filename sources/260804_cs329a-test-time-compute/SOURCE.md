# Source - Stanford CS329A: Self-Improving AI Agents (Lecture 2, Test-Time Compute Scaling)

> Persona: **curator** - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table. The agent fills it on the paste-a-URL trigger
> and keeps it current. Name this folder `YYMMDD_slug` (see `../../AGENTS.md`).

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | video |
| URL | https://www.youtube.com/watch?v=-Ggc37xLj_Y |
| Title | Stanford CS329A Self-Improving AI Agents - Part 2 - Test-Time Compute Scaling |
| Author / channel | Azalia Mirhoseini (Assistant Professor, Stanford CS), with Akanksha Chowdhery co-teaching. Published on the Stanford Online channel |
| Published | 2026-08-03 |
| Duration / length | 63:20 (3,800s); ~9,900 words of transcript across 237 timestamped blocks |
| Commit SHA | n/a |
| License | n/a (personal-use ingest of a publicly posted lecture; no material redistributed) |
| Ingested | 2026-08-04 |
| Access | open (public YouTube, human-authored English captions - no Whisper fallback needed) |
| Topics | self-improvement, evals, inferencing, agents |
| Visual leg | analysed (9 frames kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/` - the captured ground truth (git-ignored: `cs329a-l2.en.vtt`, `cs329a-l2-720.mp4`, `transcript.txt`).
3. `nodes.md` - knowledge nodes (corroborated claims + visuals + citations).
4. `context/` - **external evidence** from a deep-research pass (empty - not requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the curated frames.

## Relationship to S14, and why this is a separate source

This is **lecture 2 of the same course** as [S14](../260804_cs329a-self-improving-agents/SOURCE.md).
It is tracked separately at the owner's request, and that is also what
[`self-improvement.md`](../../brain/topics/self-improvement.md) already required in writing: further
CS329A lectures get their own `S<n>` and **must not advance the topic's confidence**, because every
one of them is the same two lecturers, the same course and the same commercial position - **the same
leg wearing a different hat** under the independence rule.

**Read the two in the intended direction.** Lecture 1 is a map that defers nearly every mechanism to
a later session, and this is one of the sessions it was deferring to. So S15's job in this brain is
**mechanism, never corroboration**. Where it appears to confirm S14, that is one person repeating
herself eight days apart.

**It does something worth more than corroboration: it supplies the evidence against S14's own
recorded defect.** S14's gate caught `d1` - the headline slide says "Models Improve Drastically" and
plots *coverage*, with an oracle verifier on half its panels. S15 reproduces that framing twice
(`d1`, `d2` below) **and then, sixteen minutes later, presents the slide that proves why it is not
allowed** (`frame_1000`, the generation-verification gap). The source refutes its own headline. That
is not corroboration between sources; it is a single source being internally inconsistent, and it is
the most useful thing in the ingest.

## Ingest notes

- **Capture:** `yt-dlp --write-sub --sub-lang en` returned **human-authored** captions, de-duplicated
  to 237 timestamped blocks by `tools/ingest.py transcript`.
- **The video had to be pulled twice, and the first pull would have silently degraded the visual
  leg.** The 720p AV1 stream returned HTTP 403, and the fallback format 18 downloaded cleanly at
  **640x360** - fine as video, useless for slides carrying eight-panel charts and per-fit error bars.
  Caught by `ffprobe`, not by eye. The kept frames come from a second pull of the **video-only** 720p
  H.264 stream (format 136); audio was never needed, since the transcript is the text leg.
- **Visual pre-filter:** `tools/ingest.py probe` reported `candidates=83 distinct=33 threshold=3
  -> RICH`. No ADR-0006 override question arose. 35 transcript-anchored candidates were extracted and
  triaged through four contact sheets - **4 `view` calls rather than 35** - and 9 frames were kept.
- **All 9 kept frames come from the clean full-screen slide cut**, so unlike S14 no cropping was
  needed. The recording alternates between that cut and a wide room shot; room-shot candidates were
  dropped in triage because a clean duplicate of the same slide existed nearby.
- **9 frames slightly exceeds the contract's "3-8 visuals" guidance, deliberately and for a stated
  reason.** The lecture has three distinct movements (the scaling law, the verification gap, the
  Archon architecture search) and the ninth frame is not decoration - it is the **second leg** for
  `n9`, the compute-reallocation node. Dropping it to hit the range would have converted a
  `corroborated` node into a `single-leg` one, trading a hard rule for a soft one.
- **A citation convention this ingest needed, and why it is the honest option.** Many nodes cite a
  slide that was `view`ed during triage and **not kept** in `visuals/`. Those cite it by **title plus
  timestamp** rather than by file path. The gate is about what the evidence *is*, not about what the
  repo *stores* - the slide genuinely exists at that point in the video and anyone can check it -
  while the prune rule (signal, not archive) governs what is kept. Inflating `visuals/` to twenty
  frames so every citation resolved to a local file would have honoured the letter of the citation
  rule by breaking the rule that actually matters.
- **The payload is the whole lecture, which is unlike S14.** There is no 101 stretch to skip and no
  logistics tail; the first minute recaps the pre-train / fine-tune / inference split and the last
  minute runs out of time on discussion questions. Two student-discussion blocks (`t=1165-1608`,
  `t=2561-2726`) are conversation rather than content, and nothing was gated from them except two
  exchanges the lecturer answers factually (`n13`, `n17`).
- **Conflict of interest, and it is heavier here than in S14.** The lecturer is **senior author of
  three of the four papers taught**: *Large Language Monkeys*, *How Do Large Language Monkeys Get
  Their Power (Laws)?* and *Archon*. The fourth (Snell et al. on compute-optimal scaling) is the only
  one she is not on, and it is also the one presented with the most qualification. The Archon segment
  is a lab result presented by its senior author to students, with the course TA named as a
  co-author. **Nothing in this lecture is independent of its presenter.** Tiers: the lecture is
  **T4**, the papers behind it **T3** preprints - except the power-laws paper, which is **ICML 2025**
  and therefore peer-reviewed, making it the strongest single citation in the ingest.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
