# Source - Scaling GitHub for your Agents (Sam Morrow, GitHub)

> Persona: **curator** (media) - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | video |
| URL | https://www.youtube.com/watch?v=0n3MKk7r60w |
| Title | Scaling GitHub for your Agents |
| Author / channel | Sam Morrow (leads development of GitHub's MCP server) - AI Engineer, recorded at AI Engineer Europe, London |
| Published | 2026-04-27 (upload); talk given ~April 2026, one year after the server's first release on 2025-04-04 |
| Duration / length | 20:34 |
| Commit SHA | n/a |
| License | n/a |
| Ingested | 2026-08-16 |
| Access | open |
| Topics | mcp, agents, context-engineering, agent-security, evals |
| Visual leg | analysed (17 frames kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/` - the captured ground truth (`transcript.txt`, timestamped; `video.mp4` and captions are git-ignored).
3. `nodes.md` - knowledge nodes (corroborated claims + visuals + citations).
4. `context/` - **external evidence** from a deep-research pass (empty; not requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the curated frames.

## Ingest notes

- **Capture method:** `yt-dlp` auto-captions -> `tools/ingest.py transcript` (78 blocks, ~3,600 words).
  The plain download 403'd; `--extractor-args "youtube:player_client=web_safari,default"` with `deno`
  present recovered the video stream.
- **Visual pre-filter:** `tools/ingest.py probe` reported `candidates=27 distinct=16 -> RICH`, so the
  visual leg ran without a confirmation sheet. 35 transcript-anchored frames extracted, triaged in 4
  contact sheets, pruned to 17 that `LEARNING.md` cites.
- **Two dense frames were unreadable at native resolution** and were cropped and upscaled before
  reading (`frame_345`, the before/after tool-and-token table, and `frame_370`, the PR token-reduction
  table). **That step changed a number**: at contact-sheet resolution the LangChain slide read as
  "60%+" and at full resolution it reads **50%+**. Zoom before quoting a figure off a slide.
- **Limitation:** this is a **vendor talk about the vendor's own product**, with no external
  evaluation, no baseline against another MCP server, and every efficacy figure self-reported. The
  one measured artifact shown is an internal PR. Read `## What to distrust in this note`.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
