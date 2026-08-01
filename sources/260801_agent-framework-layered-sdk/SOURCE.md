# Source - Inside the Microsoft Agent Framework: How we designed a layered SDK

> Persona: **curator** (media) - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table. The agent fills it on the paste-a-URL trigger
> and keeps it current. Name this folder `YYMMDD_slug` (see `../../AGENTS.md`).

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | blog |
| URL | https://commandline.microsoft.com/agent-framework-layered-sdk-loops-workflows-harnesses/ |
| Title | Inside the Microsoft Agent Framework: How we designed a layered SDK |
| Author / channel | Shawn Henry, Principal Group Product Manager (the `commandline` engineering blog) |
| Published | 2026-05-28 |
| Duration / length | ~1,150 words, 4 architecture figures, 1 pseudocode block |
| Commit SHA | n/a (not a code source) |
| License | n/a - article read in place; only paraphrase and short quotes are stored here |
| Ingested | 2026-08-01 |
| Access | open |
| Topics | agents, context-engineering, skills |
| Visual leg | analysed (4 figures kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/article.txt` - the captured article text (git-ignored).
3. `nodes.md` - knowledge nodes (gated claims + visuals + citations).
4. `context/` - **external evidence** from a deep-research pass (empty - not requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the four kept figures.

## Ingest notes

- **Capture method:** `curl` for the article HTML, then a stdlib `html.parser` extraction to
  `raw/article.txt`; the four `wp-content/uploads` figures downloaded at their 1536px variants into
  `visuals/`. No paywall, no login, nothing blocked.
- **Visual pre-filter:** not applicable. A blog post has four authored figures, not hundreds of video
  frames, so there is nothing to scene-detect or dedup. All four were `view`ed and all four are cited
  by a node, which is why the count did not drop at the prune step.
- **The figures are not decoration, and that is the notable thing here.** Three of the four carry
  material the prose never states: the model/tool/provider inventory (`n3`), the preset harness
  archetypes plus `Skills` and `Todo` as named first-class primitives (`n7`), and the fact that the
  three layers are *not* stacked (`n9`). That makes this a genuine two-leg source - uncommon for a
  vendor announcement post, where figures are usually logo grids.
- **Evidence class: T2** - first-party engineering writing about the vendor's own product.
  Authoritative on *what this framework is*; **positioned** on everything else. No measurement, no
  benchmark, no comparison against any other framework, and six lines of pseudocode as the only code.
- **The limitation to carry forward:** this is a *design* article about an SDK. Its claims are about
  how a framework is organised, not about what happens when you use one. On the "does this help?"
  axis everything here is `emerging` at best, and the brain already holds measured claims (24, 32)
  that bear on it which the article does not engage with.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
