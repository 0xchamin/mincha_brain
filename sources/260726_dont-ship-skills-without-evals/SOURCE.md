# Source - Don't Ship Skills Without Evals

> Persona: **curator** (media) - re-adopt when working this file. This ingest was run with
> **architect + mentor** on the analysis leg by request, and **fact-checker** at the gate.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | video |
| URL | https://www.youtube.com/watch?v=0vphxNt4wyk |
| Title | Don't Ship Skills Without Evals |
| Author / channel | Philipp Schmid (Google DeepMind) - AI Engineer World's Fair, Track 5 (Evals) |
| Published | 2026-07-14 |
| Duration / length | 21m45s (1305s), ~20 slides, ~4,100 transcript words |
| Commit SHA | n/a |
| License | n/a (conference talk; learned from, not redistributed) |
| Ingested | 2026-07-26 |
| Access | open |
| Topics | skills, evals, agents |
| Visual leg | analysed (11 frames kept) - **static probe overridden, see below** |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/transcript.txt` - de-duplicated timestamped transcript (`tools/ingest.py transcript`).
3. `nodes.md` - 29 knowledge nodes (claims + both legs + gate verdicts).
4. `context/` - external evidence from a deep-research pass (empty - not requested).
5. `LEARNING.md` - the distilled learning document.

## Ingest notes

### The static probe returned a false STATIC - overridden deliberately

`python3 tools/ingest.py probe` reported **`candidates=3 distinct=3 -> STATIC`** and recommended
skipping the visual leg. **That verdict was wrong and was overridden.** The talk is ~20
information-dense slides, several carrying numbers the narration never speaks.

**Why the probe failed.** The deck is heavily templated: every slide carries the same starfield
background, the same World's Fair logo, the same speaker-at-podium video inset, and the same
"TRACK 5 / Evals" footer. Scene-detect measures **whole-frame** delta; the constant chrome dominates
the frame and the changing slide body never crosses the scene threshold. **Only 3 scene changes
fired across 21 minutes of continuously changing slides.**

**This is the second occurrence of this class of failure in this repo.** On
`260725_12-factor-agents`, phash dedup **over-collapsed slides sharing a template** and that ingest
switched to transcript-anchored extraction. Same root cause at a different stage: **a shared
template suppresses whole-frame change metrics.** Recorded as a defect against the toolbox rather
than as a one-off - see `../../brain/log.md`.

**The override cost 1 `view` call.** Nine frames spread across the runtime, tiled into one contact
sheet: nine different dense slides, verdict obvious. That is the cheap check that should probably
precede any STATIC verdict on a conference talk.

**What the override bought.** `n11` (the skill-length lift curve), `n13` (5 of 7 failures fixed by a
description rewrite) and `n28` (the 39.2% -> 91.6% case-study table) exist **only on the slides**.
Honouring the probe would have lost them and gated every remaining node `single-leg`.

### Capture and extraction

- **Transcript:** `yt-dlp` auto-captions -> `tools/ingest.py transcript` (74 timestamped blocks).
- **Frames:** transcript-anchored extraction at topic-shift timestamps (the `260725_12-factor-agents`
  method), triaged as two contact sheets in **2 `view` calls for 17 candidates**.
- **Frame ordering caveat:** `tools/ingest.py sheet` tiles in *filename string* order, so
  `frame_1100` precedes `frame_60`. Every frame in both sheets was re-verified against its
  transcript timestamp before any claim was attached.
- **11 frames kept of ~20 slides**, above the usual 3-8. Justified by an explicit rule recorded in
  `nodes.md`: a frame is kept only when it **adds** data the transcript lacks. Six slides that merely
  render the narration were pruned and are cited by title instead. `LEARNING.md` features 8; the
  other 3 are cited in `nodes.md`.

### Evidence quality

- **Tier: T4** (conference talk) delivered by a **T2** vendor employee (Google DeepMind), presenting
  a mix of third-party benchmark data and his own team's internal numbers.
- **The split matters.** SkillsBench (`n1`, `n9`, `n10`, `n11`) is a **public third-party benchmark**
  with a leaderboard and open contributions - the strongest evidence in the talk. The DeepMind
  internal figures (`n26`, `n28`) are **self-reported, single-case, unreplicated**, and `n28` is a
  vendor measuring a skill for its own API.
- **Not independently verified.** No deep-research pass has been run on this source.
