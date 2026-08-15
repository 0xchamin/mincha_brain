# Source - LLM Wiki

> Persona: **curator** - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | blog (public GitHub gist - a prose idea document, no code) |
| URL | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f |
| Title | LLM Wiki - "A pattern for building personal knowledge bases using LLMs" |
| Author / channel | Andrej Karpathy (personal gist, no affiliation stated, nothing being sold) |
| Published | 2026-04-04 (single revision, never edited since) |
| Duration / length | ~1,960 words, 8 sections |
| Commit SHA | `ac46de1ad27f92b28ac95459c782c07f6b8c964a` (the only revision - every citation below is pinned to it) |
| License | none declared - a public gist, quoted under fair use, not redistributed |
| Ingested | 2026-07-31 |
| Access | open (public gist; captured via `gist.githubusercontent.com/.../raw/`) |
| Topics | rag, memory, context-engineering |
| Visual leg | n/a (the document contains no figures, diagrams, images or code - there is no second leg to be had) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/llm-wiki.md` - the captured gist verbatim (ground truth, git-ignored).
3. `nodes.md` - knowledge nodes (gated claims + citations). **Read its evidence-class table first.**
4. `context/` - **external evidence** from a deep-research pass.
   [`01_where-the-index-file-ceiling-actually-sits.md`](context/01_where-the-index-file-ceiling-actually-sits.md)
   (2026-08-15) researches `n10`, the source's one quantified claim. Verdict **`refines`**: the
   ceiling is real and measured twice independently, **the unit is wrong** (tokens, not sources), and
   **`n10`'s own design was tested by nobody**.
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - empty; this source has no visual leg and nothing was generated.

## Ingest notes

- **Capture method:** `curl` on the gist's `/raw/` endpoint into `raw/llm-wiki.md`. The GitHub gists
  API returned `502 Server Error` throughout the ingest, so the revision SHA and publication date
  were read off the rendered `/revisions` page instead. `gh` is installed but unauthenticated
  (`gh auth login` not run), so the API path was unavailable twice over.
- **Visual leg `n/a`, and this is not a degrade decision.** It is a plain markdown essay with zero
  images. There was nothing to probe and nothing to skip. The consequence is the same as a skip and
  is recorded in full in `nodes.md`: **every node here is `single-leg`, confidence `needs-check`, and
  this source cannot produce an internally `corroborated` claim.** Not one node claims otherwise.
- **Quotes are reproduced with em dashes normalized to plain dashes.** The gist uses U+2014 heavily;
  the kit forbids it (`validate.py check_style`). Wording is otherwise verbatim. `raw/` is outside
  the validator's scope, so the captured original is untouched.
- **Citation form used here:** `S8 (gist @ac46de1, §Section)`. The gist has no line numbers a reader
  can see and no timestamps, so section headings are the finest addressable unit.
- **This source had a prior claim filed against it before it was ingested.**
  [ADR-0009](../../brain/decisions/0009-dreaming-reconciliation-pass.md) cites this gist as
  "reviewed, not yet ingested" and characterises it in one sentence. That characterisation was
  **re-derived from the text rather than inherited, and it turns out to be wrong** - see `nodes.md`
  `n8` and "Against the prior claim" in `LEARNING.md`. Correcting it is the most valuable thing this
  ingest produced.
- **Gating order was constrained on purpose.** The nodes were gated from the gist text alone, before
  `brain/topics/memory.md` was opened, so that agreement between this source and the brain's existing
  memory synthesis could be *observed* rather than manufactured. Disclosure of what was unavoidably
  already in context at gate time is in `nodes.md` under "What I had already seen".
- **One internal contradiction found** (`d1`), which is notable because a source with a single leg is
  not supposed to yield any: the gist's rhetoric section and its operations section disagree about
  whether LLMs forget cross-references.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
