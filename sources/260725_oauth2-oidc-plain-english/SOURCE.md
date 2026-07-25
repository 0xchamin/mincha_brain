# Source - OAuth 2.0 and OpenID Connect (in plain English)

> Persona: **curator** (media) / **code-explorer** (code) - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table. The agent fills it on the paste-a-URL trigger
> and keeps it current. Name this folder `YYMMDD_slug` (see `../../AGENTS.md`).

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | video |
| URL | https://www.youtube.com/watch?v=996OiexHze0 |
| Title | OAuth 2.0 and OpenID Connect (in plain English) |
| Author / channel | Nate Barbettini (Okta) / OktaDev |
| Published | 2018-02-05 |
| Duration / length | 62:17 |
| Commit SHA | n/a |
| License | n/a (YouTube, personal-use ingest only) |
| Ingested | 2026-07-25 |
| Access | open |
| Topics | agent-security, mcp |
| Visual leg | analysed (14 frames kept; 40 distinct after dedup - RICH, well above the static threshold) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/` - the captured ground truth (transcript; video git-ignored and discardable).
3. `nodes.md` - knowledge nodes (corroborated claims + visuals + citations).
4. `context/` - **external evidence** from a deep-research pass (empty - not yet requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the curated frames.

## Ingest notes

- **Capture:** `yt-dlp` auto-captions -> `tools/ingest.py transcript` (212 blocks, ~13.1k words).
  Video pulled at <=480p purely as frame source; git-ignored and discardable.
- **Visual pre-filter:** `tools/ingest.py probe` -> `candidates=134 distinct=40 threshold=3 -> RICH`.
  Frames then extracted **transcript-anchored** (24 concept boundaries) rather than from the phash
  set, and triaged via 3 contact sheets in **3 `view` calls instead of 24** - the method carried
  over from `260725_12-factor-agents`, and it worked the same way here: this deck reuses one flow
  diagram as a progressive build, so phash dedup would have kept many near-identical slides while
  collapsing genuinely different ones.
- **Domain note (flagged, then resolved by the owner).** This is a 2018 identity-protocol talk with
  no AI content, so it sits outside the kit's AI/ML guardrail on a literal reading. Flagged before
  ingesting; the owner confirmed it is **deliberate groundwork for a planned identity track**:
  **OAuth 2.1, SPIFFE/SPIRE, and AAuth**. So this is not a detour but **source 1 of a sequence** -
  the last "human clicks Yes in a browser" description of delegated authorization, against which the
  workload-identity and agent-identity models that follow can be read as departures.
- **Age warning (important):** the talk is **8 years old** and one of its recommendations has since
  been reversed by the field - see `n17` and the "What has aged" section of `LEARNING.md`. The
  protocol *mechanics* it teaches are unchanged and remain the best available explanation; the
  *flow-selection advice* for browser apps is stale. This source is a strong candidate for a
  **deep-research pass** to replace commentary with cited current guidance.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
