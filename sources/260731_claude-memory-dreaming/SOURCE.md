# Source - Memory and dreaming for self learning agents

> Persona: **curator** (media) - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | video |
| URL | https://www.youtube.com/watch?v=IGo225tfF2I |
| Title | Memory and dreaming for self learning agents |
| Author / channel | Ravi (API knowledge team, Anthropic) - "Code w/ Claude" conference, Claude channel |
| Published | 2026-05-21 |
| Duration / length | 21:34 (1294s) |
| Commit SHA | n/a |
| License | n/a - conference talk, quoted under fair use, not redistributed |
| Ingested | 2026-07-31 |
| Access | open (public YouTube, auto-captions available) |
| Topics | memory, agents, agent-security |
| Visual leg | analysed (13 frames kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/transcript.txt` - de-duplicated timestamped transcript (ground truth, git-ignored).
3. `nodes.md` - knowledge nodes (gated claims + citations).
4. `context/` - **external evidence** from a deep-research pass (empty - not requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the 13 curated slide and demo frames.

## Ingest notes

- **Capture method:** `yt-dlp` auto-captions (`en-orig`) -> `tools/ingest.py transcript` -> 81 blocks,
  ~2,959 words. Video pulled at 720p for frame extraction only; `raw/video.webm` is git-ignored and
  discardable.
- **Static probe (ADR-0003):** `candidates=85 distinct=45 -> RICH`. Far above the `<= 3` threshold, so
  no confirmation sheet was needed and the visual leg ran by default. The richest visual source
  ingested so far.
- **Visual pre-filter:** transcript-anchored extraction (the method adopted in
  `260725_12-factor-agents` after phash over-collapsed a templated deck), 50 candidates across three
  batches, triaged in **7 `view` calls via contact sheets** rather than 50. **13 kept**, all cited in
  `nodes.md`; 37 pruned.
- **Two frames carry disproportionate weight.** `frame_1030` and `frame_1188` are the live demo, not
  slides: a running console showing a `content_sha256` write precondition, a `v1..v6 head` version
  strip, per-agent attribution, and one agent consuming another's note one minute later. **A
  photograph of the artifact beats a bullet describing it**, and in two places the demo supplies
  mechanism the narration never states (`n6`, `n20`).
- **Notable limitation - read `nodes.md`'s evidence-class table before citing anything.** This is a
  **T2 vendor talk about the vendor's own product at the vendor's own conference**. Mechanism claims
  gate cleanly and transfer. **Outcome claims (`n4`, `n17`, `n18`) are vendor-curated customer quotes
  with no methodology, no baseline and no published benchmark** - weaker evidence than the sibling
  source's recovered chart numbers, which are themselves methodologically undisclosed.
- **Sibling source, deliberately paired:**
  [`../260731_chatgpt-memory-dreaming/`](../260731_chatgpt-memory-dreaming/LEARNING.md) (S6, OpenAI,
  2026-06-04) is the same concept from the other vendor. This source (S7) is the **independent**
  second leg: different organisation, different commercial interest, **agent platform rather than
  consumer chat assistant**. Their convergence is why `memory` reaches `established`
  ([ADR-0008](../../brain/decisions/0008-memory-established.md)).
- **Re-captured clean.** An earlier capture of this URL was disrupted by a concurrent session; this
  folder is a fresh run of the pipeline from the URL. The transcript reproduces the earlier one
  **byte-for-byte**, and all 13 frames were re-extracted at the same timestamps.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
