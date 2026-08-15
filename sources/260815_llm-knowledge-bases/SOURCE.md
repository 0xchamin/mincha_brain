# Source - LLM Knowledge Bases: a practical guide

> Persona: **curator** (media) - re-adopt when working this file.

> Metadata + facts for one ingested source. Single source of truth for this source; other docs here
> link to this table.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | video (conference talk, AI Engineer World's Fair 2026, Track 3 "Memory & Continual Learning") |
| URL | https://www.youtube.com/watch?v=I3bpdgFJCUY |
| Title | LLM Knowledge Bases: a practical guide |
| Author / channel | Ben Holmes (developer relations lead, **Warp**) - channel: AI Engineer |
| Published | 2026-08-12 (talk delivered 2026-07-01) |
| Duration / length | 21:17 (1,277s) |
| Commit SHA | n/a (not a code source) |
| License | n/a - YouTube ToS; transcript and frames derived for personal study, video not redistributed |
| Ingested | 2026-08-15 |
| Access | open |
| Topics | memory, rag, skills, agents |
| Visual leg | analysed (8 frames kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/transcript.txt` - the captured ground truth (git-ignored).
3. `nodes.md` - knowledge nodes. **Read its independence section first** - it is the whole story of
   this gate.
4. `context/` - external evidence from a deep-research pass (empty - not requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the 8 curated frames.

## The one thing to know before reading any of it

**This is a talk about [S8](../260731_llm-wiki/LEARNING.md), which this brain already holds.** Ben
Holmes builds on Andrej Karpathy's `llm-wiki` gist, names it on stage and displays it. **Showing a
source is not corroborating it** - under the independence rule those frames are the same leg wearing
a different hat, and **no S8 node was moved by this ingest.** What is genuinely independent is the
*implementation*: a different person at a different organisation built the pattern and ran it on a
real corpus. That is evidence about **instantiability**, not efficacy - the source measures nothing
(`n16`).

## Ingest notes

- **Capture method:** `yt-dlp` auto-captions -> `tools/ingest.py transcript` (82 blocks, ~4,682
  words). Video via `yt-dlp`.
- **Capture hazard worth recording, because it nearly cost the source its second leg.** All DASH
  formats returned `HTTP 403` - yt-dlp could not solve YouTube's n-challenge with **no JavaScript
  runtime on this machine**. The only format that downloaded was `18` (progressive, **360p**), and at
  360p the talk's dense screens - the gist, the `SKILL.md`, the scheduled prompt - are **illegible**.
  A transcript-only degrade was one decision away. Fixed by installing **deno** (`brew install deno`)
  *and* **`yt-dlp-ejs`** (`pip install yt-dlp-ejs`) - **both are required**; deno alone still failed
  the challenge. Format `299` (1080p) then downloaded normally and every node was gated against that.
  **For any future video ingest in this kit: if DASH 403s, this is the fix.**
- **Visual pre-filter:** `tools/ingest.py probe` -> `candidates=39 distinct=14 threshold=3` ->
  **`RICH`**, so the visual leg was analysed with no override needed. 32 transcript-anchored
  candidates were extracted and triaged as **4 contact sheets in 4 `view` calls** rather than 32;
  9 were then re-extracted at 1080p and viewed individually; **8 kept**.
- **Frames dropped after viewing at full resolution:** the on-disk folder-tree diagram (`t=110`,
  restated in the mental-model diagram and in `frame_728`'s text), the whiteboard sync sketch
  (`t=940` - an empty rectangle labelled "ob sync" twice, teaching nothing a sentence does not), the
  graph view (`t=1150`) and the burndown chart (`t=1185`) under the frame budget. `n15` records what
  the graph frame showed and marks it **not citable**, since it is not kept.
- **Limitations:** T4 practitioner demo with a **T2 commercial position on its most novel section**
  (`d2` - the scheduled-automation mechanism is demonstrated exclusively on the speaker's employer's
  product). **Nothing in the talk is measured** (`n16`). Three of the most interesting mechanisms
  (`n11`, `n12`, `n15`) are **figure-only** - visible in a screenshot, never spoken.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
