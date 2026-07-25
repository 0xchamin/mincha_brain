# Source - <TITLE>

> Persona: **curator** (media) / **code-explorer** (code) - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table. The agent fills it on the paste-a-URL trigger
> and keeps it current. Name this folder `YYMMDD_slug` (see `../../AGENTS.md`).

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | video / blog / paper / code |
| URL | <url> |
| Title | <title> |
| Author / channel | <name> |
| Published | <date, if known> |
| Duration / length | <mm:ss for video, page/word count, or repo LOC> |
| Commit SHA | <for code: pin the snapshot, e.g. a1b2c3d> |
| License | <for code: the repo license, e.g. MIT> |
| Ingested | <date> |
| Access | open / paywalled-accessible / limited (note any restriction) |
| Topics | <agents, mcp, skills, rag, agent-security, inferencing, ...> |
| Status | capture / understand / researched (optional) / distill / awaiting-promotion / compounded / blocked / partial |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. For **code**: `MAP.md` - repo orientation (what it demonstrates, module map, key flow).
3. `raw/` (media) or `repo/` (code, git-ignored) - the captured ground truth.
4. `nodes.md` - knowledge nodes (corroborated claims + visuals/diagrams + citations).
5. `context/` - **external evidence** from a deep-research pass (empty unless requested).
6. `LEARNING.md` - the distilled learning document.
7. `visuals/` - the curated frames/figures/generated diagrams.

## Ingest notes

- Capture method used (yt-dlp captions / Whisper / web_fetch / PDF / git clone): ...
- Visual pre-filter result (candidates after scene-detect + dedup) / code orientation summary: ...
- Anything notable / limitations: ...

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
