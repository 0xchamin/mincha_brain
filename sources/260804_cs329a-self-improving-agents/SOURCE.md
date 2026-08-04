# Source - Stanford CS329A: Self-Improving AI Agents (Lecture 1, Course Overview)

> Persona: **curator** - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table. The agent fills it on the paste-a-URL trigger
> and keeps it current. Name this folder `YYMMDD_slug` (see `../../AGENTS.md`).

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | video |
| URL | https://www.youtube.com/watch?v=6YnLB0XbTnI |
| Title | Stanford CS329A Self-Improving AI Agents - Part 1 - Course Overview |
| Author / channel | Azalia Mirhoseini (Assistant Professor, Stanford CS) + Akanksha Chowdhery (Adjunct Professor, Stanford; research at Reflection AI). Published on the Stanford Online channel |
| Published | 2026-08-03 (recorded Fall quarter; the second time the course has run) |
| Duration / length | 69:42 (4,182s); ~12,100 words of transcript across 262 timestamped blocks |
| Commit SHA | n/a |
| License | n/a (personal-use ingest of a publicly posted lecture; no material redistributed) |
| Ingested | 2026-08-04 |
| Access | open (public YouTube, human-authored English captions - no Whisper fallback needed) |
| Topics | self-improvement, evals, agents, autonomous-research-loops |
| Visual leg | analysed (8 frames kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/` - the captured ground truth (git-ignored: `cs329a.en.vtt`, `cs329a.webm`, `transcript.txt`).
3. `nodes.md` - knowledge nodes (corroborated claims + visuals + citations).
4. `context/` - **external evidence** from a deep-research pass (empty - not requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the curated frames.

## Ingest notes

- **Capture:** `yt-dlp --write-sub --sub-lang en` returned **human-authored** captions rather than
  auto-generated ones, de-duplicated to 262 timestamped blocks by `tools/ingest.py transcript`. The
  video was pulled at 720p for the visual leg.
- **Visual pre-filter:** `tools/ingest.py probe` reported `candidates=154 distinct=44 threshold=3
  -> RICH` - **the richest visual leg this brain has measured**, against 19 distinct for S1 and a
  `STATIC` threshold of 3. No ADR-0006 override question arose. 32 transcript-anchored candidates
  were extracted and triaged through four contact sheets, which cost 4 `view` calls rather than 32,
  and 8 frames were kept.
- **The recording alternates between two camera cuts, and that matters for frame quality.** One cut
  is a clean full-screen slide capture and the other is a wide room shot. Six kept frames come from
  the clean cut. Two of them (`frame_1712`, `frame_2098`) exist only as room shots and were cropped
  to the screen region (`crop=780:475:10:30`); both are fully legible, and the crop removes the
  lectern and the back wall.
- **The first ~20 minutes are field 101 for this brain's reader.** They cover scaling laws, few-shot
  prompting, chain-of-thought, and the pre-train / fine-tune / instruction-tune / RLHF ladder. That
  stretch was gated but deliberately not promoted, because the `AGENTS.md` calibration is "enough
  fundamentals, never 101" and every claim in it is either already held here or is textbook. The
  source's payload starts at `t=1169`, where inference is named as a third scaling frontier, and the
  argument is complete by `t=3070`.
- **Course logistics occupy the last ~11 minutes**, from `t=3686` onward: homeworks, grading, the
  poster session, the late policy. No knowledge nodes were taken from it. The one slide worth
  keeping from that stretch is the syllabus (`frame_3645`), because the course's own decomposition
  of "self-improvement techniques" is the taxonomy this note is organised around.
- **One limitation belongs up front, because it colours everything else: this is lecture 1 of a
  course.** It is a map of a field delivered at survey depth, and it defers nearly every mechanism
  to a later session - "we have a lecture just dedicated to verifiers" @ `t=1624`. Treat it as a
  reliable taxonomy and an unreliable measurement, and see the trust section of `LEARNING.md` for
  what that costs.
- **Conflict of interest, recorded because it is load-bearing.** The two strongest empirical slides
  (`frame_1206`, `frame_1355`) present *Large Language Monkeys*, on which the lecturer is the senior
  author, and the Q&A leans on *Code Monkeys* from the same lab. The presenter is not an independent
  voice on that result. Both are arXiv preprints (**T3**) and the lecture itself is **T4**.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
