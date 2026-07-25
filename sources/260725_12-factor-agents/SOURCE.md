# Source - 12-Factor Agents: Patterns of reliable LLM applications

> Persona: **curator** (media) - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table. The agent fills it on the paste-a-URL trigger
> and keeps it current. Name this folder `YYMMDD_slug` (see `../../AGENTS.md`).

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | video |
| URL | https://www.youtube.com/watch?v=8kMaTybvDUw |
| Title | 12-Factor Agents: Patterns of reliable LLM applications |
| Author / channel | Dex Horthy (HumanLayer) - AI Engineer (World's Fair 2025) |
| Published | 2025-07-03 |
| Duration / length | 17:05 (1025s) |
| Commit SHA | n/a (video). Companion repo `github.com/humanlayer/12-factor-agents` not cloned - README fetched only |
| License | n/a (YouTube ToS; personal-use captions + sampled frames only). Companion repo: code Apache-2.0, content CC BY-SA 4.0 |
| Ingested | 2026-07-25 |
| Access | open |
| Topics | agents, context-engineering |
| Visual leg | analysed (9 frames kept; 19 distinct after dedup - well above the static threshold) |
| Status | compounded (+ researched 2026-07-25) |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/` (media, git-ignored) - the captured ground truth (English captions + low-res video).
3. `nodes.md` - knowledge nodes (18 claims + 5 external corroborations + 3 divergences, cited).
4. `context/01_context-limits-and-decomposition.md` - **external evidence** (deep-research pass,
   2026-07-25): closes both of `LEARNING.md`'s open questions, adds the Event Sourcing framing.
5. `LEARNING.md` - the distilled learning document (written as a ramp-up read).
6. `visuals/` - the 9 curated frames.
7. `../../reports/260725_agent-fundamentals-ramp-up.md` - the cross-source report this fed.

## Ingest notes

- **Capture method:** `yt-dlp` English captions (`en.vtt` - human-quality here; proper nouns and code
  identifiers survived intact, unlike the auto-captions on the previous source) plus a 480p video
  (format 397, 9.6MB) for frames. Whisper not needed. `yt-dlp` warns about a missing JS runtime;
  extraction still succeeded.
- **Transcript:** de-duplicated the rolling VTT cues and merged them into ~15s blocks ->
  `raw/transcript.txt`, 58 blocks / ~3,970 words, timestamps preserved for deep-links (527 unique
  cues in).
- **Visual pre-filter (two passes, first one failed):** scene-detect gave 154 candidates at threshold
  0.12 and 135 at 0.30 - too many, because the talk cuts constantly between speaker and slide.
  `imagehash` phash dedup (distance <= 10) collapsed those to 19, **but it also collapsed genuinely
  distinct slides sharing one template**, dropping several key diagrams. Changed approach: read the
  transcript first, then extract **17 frames anchored to the transcript beats**, tile them into two
  3x3 contact sheets, and `view` the sheets (2 calls instead of 17) to triage. Pulled the 6 dense
  ones at full resolution cropped to the slide area, then cut **9 final frames**.
- **Why 9 and not 8:** the kit guideline is 3-8 visuals. This talk covers 12 distinct factors, and
  every kept frame is cited by a node *and* by the report; 8 title-card / redundant candidates were
  dropped instead (see `nodes.md` "Dropped"). Recording the deviation rather than padding it or
  trimming a cited frame.
- **Second leg for the factor numbering:** the talk delivers the factors **out of order and bundled**
  (`&t=211s`), so the canonical README at `github.com/humanlayer/12-factor-agents` was fetched with
  `web_fetch` to verify the mapping of spoken content onto factor numbers. It matched exactly - see
  `nodes.md` `en1`.
- **Limitation to carry forward:** the repo and the talk share one author, so that external leg
  corroborates *the framework as stated*, not that it works. The talk contains no benchmarks,
  ablations or failure rates; its empirical basis ("100+ founders, builders, engineers" `&t=105s`) is
  not checkable from here.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
