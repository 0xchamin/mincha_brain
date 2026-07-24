# Source - Building Closed-Loop Evals for a Multimodal Agent at Scale

> Persona: **curator** (media) - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table. The agent fills it on the paste-a-URL trigger
> and keeps it current. Name this folder `YYMMDD_slug` (see `../../AGENTS.md`).

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | video |
| URL | https://www.youtube.com/watch?v=31GUkCBD-Uc |
| Title | Building Closed-Loop Evals for a Multimodal Agent at Scale |
| Author / channel | Soumya Gupta & Jai Chopra (Uber, Computer Vision team) - AI Engineer (World's Fair) |
| Published | 2026-07-24 |
| Duration / length | 21:38 (1298s) |
| Commit SHA | n/a |
| License | n/a (YouTube ToS; personal-use captions + sampled frames only) |
| Ingested | 2026-07-25 |
| Access | open |
| Topics | evals, agents |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/` (media, git-ignored) - the captured ground truth (auto-captions + low-res video).
3. `nodes.md` - knowledge nodes (corroborated claims + visuals + citations).
4. `LEARNING.md` - the distilled learning document.
5. `visuals/` - the curated frames.

## Ingest notes

- Capture method: `yt-dlp` English auto-captions (`en.vtt`) + low-res (`<=480p`) video for frames.
  Whisper not needed (captions present).
- Visual pre-filter: `ffmpeg` scene-detect (threshold 0.12) -> 14 candidates -> `imagehash` phash
  dedup -> 13 distinct; dropped 2 non-content (title/podium) + 4 uncited setup slides after distill
  -> **7 kept frames** (only those cited by a node or the report; signal, not archive).
- Transcript caveat: auto-captions mangle proper nouns - "Uber" -> "Aruba/Rue Ba", "Soumya" ->
  "Sonya/Somya". Corrected from the title/slides; slides read "Uber Eats" and carry the real terms.
- Speakers: Jai Chopra (routing/orchestration/generation evals) + Soumya Gupta (golden dataset,
  online tuning, auto-tuning loop).

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
