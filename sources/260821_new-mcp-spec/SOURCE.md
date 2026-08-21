# Source - Here's how the new MCP spec works (Kent C. Dodds)

> Persona: **curator** (media) - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | video |
| URL | https://www.youtube.com/watch?v=1B9H6RTAGmE |
| Title | Here's how the new MCP spec works |
| Author / channel | Kent C. Dodds - "Better with Kent". Long-time JavaScript educator, former TC39 participant; here as the author of **Kody**, his own MCP server and client, which he migrated to this spec revision |
| Published | 2026-08-20 (upload). Covers specification revision **`2026-07-28`**, released ~3 weeks earlier |
| Duration / length | 24:55 |
| Commit SHA | n/a |
| License | n/a |
| Ingested | 2026-08-21 |
| Access | open |
| Topics | mcp, agent-security, agents |
| Visual leg | analysed (8 frames kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/` - the captured ground truth (git-ignored: video, captions, transcript, candidate frames).
3. `nodes.md` - knowledge nodes (corroborated claims + visuals + citations).
4. `context/` - **external evidence** from a deep-research pass (empty - not requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the curated frames.

## What the visual leg is on this source, and why it is unusually strong

This is a **screencast**, not a talk. The speaker has no slides. What is on screen is a sequence of
**third-party and first-party artifacts**: the official MCP blog post announcing the release, four
sequence diagrams the speaker drew in Excalidraw, his own merged pull request, and his own public
GitHub issue carrying a production dashboard readout.

That makes the second leg **better than a slide deck would have been** on the specification claims,
because the artifact on screen is the primary document rather than a summary somebody made of it.
On the adoption claims it makes the two legs genuinely independent: the narration is the speaker's
recollection, and the visual is an aggregate query he did not compute by hand.

It also means the frames are dense text rather than diagrams-with-labels. Every kept frame was read
at full resolution before gating, not at contact-sheet resolution.

## Ingest notes

- **Capture:** `yt-dlp` auto-captions (`en`), de-duplicated to 96 timestamped blocks / ~4,873 words
  via `tools/ingest.py transcript`.
- **Video capture degraded, and it constrains nothing that mattered.** The default and `web_safari`
  player clients returned HTTP 403 on the media data, and only the `tv` client served a downloadable
  stream - format 18, **640x360**. Every frame kept was checked for legibility at full resolution
  before curation; the on-screen text is a browser at a large zoom level throughout, so it reads
  cleanly at 360p. Had it not, the fallback was to fetch the blog post directly.
- **Visual pre-filter:** `tools/ingest.py probe` -> `candidates=13 distinct=7 threshold=3` -> **RICH**.
  Frames were then extracted **transcript-anchored** rather than from the probe's scene cuts, because
  the argument's structure is known from the transcript and the interesting moments are document
  scroll positions, which scene detection does not find. 23 candidates extracted, triaged in
  2 contact sheets, 8 kept.
- **Frame prune:** 2 frames were viewed, gated and dropped for budget (`frame_1395`, `frame_580`) -
  reasons recorded in `nodes.md`. They are not in `visuals/`.
- **Terminology warning:** the auto-captions render **CIMD** as "SIMD" everywhere. `grep`ping the
  transcript for the real term returns nothing. See `d1` in `nodes.md`.
- **Limitations:** one server's adoption data, from a self-selected client population, over a window
  the source itself says is ~6 to ~13 days rather than the 30 it is labelled. No deep-research pass
  was requested, so nothing here is externally corroborated.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
