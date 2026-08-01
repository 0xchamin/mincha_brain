# Source - Tool search: Finding the right tool at the right time

> Persona: **curator** - re-adopt when working this file.

> Metadata + facts for one ingested source. Single source of truth for this source; other docs here
> link to this table.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | blog |
| URL | https://commandline.microsoft.com/tool-search-toolboxes-foundry/ |
| Title | Tool search: Finding the right tool at the right time |
| Author / channel | Lisa Brown Jaloza - Command Line (Microsoft) |
| Published | 2026-07-29 |
| Duration / length | ~1,900 words, 3 figures, 1 results table, 1 Python snippet |
| Commit SHA | n/a |
| License | n/a (article, read-only ingest) |
| Ingested | 2026-08-01 |
| Access | open |
| Topics | mcp, rag, context-engineering, agents |
| Visual leg | analysed (3 figures kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/article.txt` - the captured article text (ground truth).
3. `nodes.md` - knowledge nodes (gated claims + citations).
4. `context/` - external evidence (empty; no deep-research pass requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the three curated figures.

## Ingest notes

- **Capture method:** `curl` for the article HTML, then a small extraction of the `article-content`
  block to `raw/article.txt`. The three figures were downloaded at full resolution from
  `wp-content/uploads/2026/07/` and `view`ed individually.
- **Visual pre-filter:** not needed. A blog post ships a fixed, small set of figures, so the
  candidate set was three and all three were `view`ed. All three were kept - unusual, and earned:
  Figure 1 corroborates the architecture prose, Figure 2 carries the headline measurement, and
  Figure 3 (a portal screenshot shipped with an empty `alt`) turned out to carry the load-bearing
  **MCP** mechanic the prose never states (`n7`).
- **The second leg is unusually real here.** Unlike a text-only post, this source has figures, a
  results table **and** a code snippet, so most nodes are genuinely two-legged. The snippet supports
  the same docs-vs-code check the contract applies to repositories, and it caught a defect (`d1`).
- **Limitations:** T2 vendor post about its own preview product. The token measurement runs on a
  public benchmark (ToolRet) and is the strongest evidence here; the metadata-tuning figures (`n14`)
  are self-reported on an unnamed eval with no absolute baselines, and the retrieval comparison mixes
  self-run with borrowed numbers (`d2`).

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
