# Source - Multi-tenant agentic AI system (Google Cloud reference architecture)

> Persona: **curator** - re-adopt when working this file.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | blog (vendor reference architecture) |
| URL | https://docs.cloud.google.com/architecture/multi-tenant-agentic-ai-system |
| Title | Multi-tenant agentic AI system |
| Author / channel | Shivank Awasthi (Field Solutions Architect) + Utkarsh Bhardwaj (Technical Solutions Consultant, Agentic AI), Google Cloud Architecture Center - **21 further contributors listed** |
| Published | Last reviewed 2026-06-18 UTC |
| Duration / length | ~5,000 words, **1 figure** |
| Commit SHA | n/a |
| License | page text CC BY 4.0; code samples Apache 2.0 (stated in the page footer) |
| Ingested | 2026-08-02 |
| Access | open |
| Topics | agent-security, mcp, agents, context-engineering |
| Visual leg | analysed (1 figure kept, presented as 3 views - the full diagram plus 2 crops) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/article.md` - the captured article text (git-ignored).
3. `nodes.md` - knowledge nodes (gated claims + citations).
4. `context/` - empty; no deep-research pass has been run on this source.
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the kept figure and its two crops.

## Ingest notes

- **Capture method:** `curl` of the rendered devsite page, HTML stripped to `raw/article.md` with a
  throwaway Python script. `WebFetch` was tried first and returned a *summary*, not the text - useful
  as a sanity check, useless as a citable leg, so it was discarded.
- **Visual pre-filter:** the page has exactly **one** content image
  (`/static/architecture/images/multi-tenant-agentic-ai-system.svg`); every other image is site chrome
  (logos, favicons, a video placeholder). Nothing to triage. The SVG was rendered at 2374x2740 with
  headless Chrome - `qlmanage` squashed a 1188x1370 viewBox into a square thumbnail and cropped half
  the diagram away, which would have silently cost the tenant half of the visual leg - then cropped
  into the two views used as teaching steps in `LEARNING.md`.
- **Both legs share one author team.** For a media source the legs are prose and figure; here they
  were produced by the same people for the same page, so `corroborated` means *the diagram and the
  text agree* and nothing more. Read every `corroborated` verdict in `nodes.md` with that in mind: it
  is weaker here than on a source whose figure came from a benchmark or a console.
- **Tier: T2**, first-party vendor writing about its own products. Authoritative on what those
  products do, **positioned** on whether this is the right shape. There is **no measurement anywhere
  in the document** - no latency number, no cost number, no incident data, no named deployment.
- **Genre limitation, stated up front:** a reference architecture documents a *shape*, not a result.
  This one reports no deployment of itself.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
