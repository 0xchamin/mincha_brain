# Source - Dreaming: Better memory for a more helpful ChatGPT

> Persona: **curator** (media) - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | blog |
| URL | https://openai.com/index/chatgpt-memory-dreaming/ |
| Title | Dreaming: Better memory for a more helpful ChatGPT |
| Author / channel | OpenAI (no individual byline - the article credits "OpenAI") |
| Published | 2026-06-04 |
| Duration / length | ~1,800 words + 3 product screenshots + 3 eval charts (chart data recovered, see below) |
| Commit SHA | n/a |
| License | n/a - copyrighted vendor post, quoted under fair use, not redistributed |
| Ingested | 2026-07-31 |
| Access | open (free, no paywall) but **bot-blocked**: the live URL returns HTTP 403 to the harness fetch tool and to `curl` with a browser UA. Captured from the Internet Archive snapshot instead. |
| Topics | memory, context-engineering, evals |
| Visual leg | analysed (3 frames kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/article.md` - the captured article text (ground truth, git-ignored).
3. `nodes.md` - knowledge nodes (gated claims + citations).
4. `context/` - **external evidence** from a deep-research pass (empty - not requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the 3 curated product figures.

## Ingest notes

- **Capture method:** `web.archive.org/web/2026id_/<url>` -> gunzip -> HTML -> text extraction to
  `raw/article.md`. The archive snapshot is a verbatim copy of the publisher's own page, so the text
  leg is trustworthy. **Section headings are the citation anchor** (`S6 §Staying current over
  time`), because the capture preserves no stable paragraph index.
- **Visual pre-filter:** the page carries 6 content images. **3 product screenshots** (saved-memories
  list, memory summary modal, memory settings) were downloaded and viewed - all 3 kept, all 3 cited.
- **The eval charts, and the technique that recovered them.** The other 3 images are the eval charts
  for the article's three objectives. They are **client-rendered and show `Loading…` in any static
  capture** - initially recorded as an unrecoverable gap. They are **Vega-Lite** components
  (`reactComponent: "VegaChart"`), and a Vega-Lite spec **carries its own data inline**, so the full
  `data.values` arrays sit in the Next.js **RSC flight payload** (`self.__next_f`) of the same HTML.
  Extracted to [`chart_data.json`](chart_data.json) -> `nodes.md` `n12`-`n14`.
  > **Reusable rule:** when a chart will not render in a static capture, grep the payload for the
  > charting library before declaring the numbers lost. Vega/Vega-Lite, Plotly and Chart.js all embed
  > their data in the spec. `view`ing a rendered chart is *lossier* than this - you read values off
  > pixels; here the publisher's own numbers are exact.
- **Notable limitation:** a **T2 vendor post about the vendor's own consumer product.** The numbers
  are now exact, but **"task success" is never defined and no sample size, eval-set description,
  methodology or confidence interval is published anywhere** in the page or the specs. The
  *mechanism* claims are well corroborated by the screenshots; the *magnitude* claims are a vendor's
  directional self-report and must never be cited as a benchmark result.
- **Related source in flight, not ingested:** `sources/260731_agent-memory-and-dreaming/` (untracked,
  **another agent is working it**) holds a captured Anthropic conference talk on memory and dreaming
  in Claude Managed Agents. It is the natural **independent** second leg for this topic - different
  org, different
  commercial interest, agent platform rather than consumer product. Until it is distilled, `memory`
  stays `emerging`.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
