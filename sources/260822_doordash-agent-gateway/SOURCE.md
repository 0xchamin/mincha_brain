# Source - How DoorDash Built a Centralized Gateway for AI Agent-Tool Access (S29)

> Persona: **curator** - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | blog |
| URL | https://careersatdoordash.com/blog/how-doordash-built-a-centralized-gateway-for-ai-agent-tool-access/ |
| Title | How DoorDash Built a Centralized Gateway for AI Agent-Tool Access |
| Author / channel | Siddarth Kodwani (Tech Lead Engineer, GenAI Platform) and Vasily Vlasov (Principal Engineer), DoorDash Engineering |
| Published | 2026-07-30 |
| Duration / length | ~2,300 words, 3 figures, 1 table |
| Commit SHA | n/a |
| License | n/a - article read in place, not redistributed; figures captured for citation under the kit's personal-learning use |
| Ingested | 2026-08-22 |
| Access | open (no paywall) - **but Cloudflare-protected**: both `curl` and `WebFetch` return HTTP 403. Captured through the browser instead |
| Topics | mcp, agent-security, agents |
| Visual leg | analysed (3 figures kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/article.md` - the captured ground truth (git-ignored).
3. `nodes.md` - knowledge nodes (gated claims + citations).
4. `LEARNING.md` - the distilled learning document.
5. `visuals/` - the three curated figures.

## Ingest notes

- **Capture method: Chrome, not `web_fetch`.** `curl` and `WebFetch` both return **403** behind
  Cloudflare, and `curl` cheerfully wrote a 284KB challenge page to disk with a `.png` extension.
  The article text came from `get_page_text` on a browser tab; the three figures were captured by
  navigating to each image URL directly and screenshotting it at full viewport width.
  **Worth remembering as a general degrade path** - a source that a headless fetch cannot reach is
  not an inaccessible source when a real browser session is available.
- **Visual pre-filter: not applicable, and there was nothing to filter.** A blog with three
  purpose-drawn figures needs no scene-detect pass; all three were `view`ed and all three earned a
  place, which is unusual and is a fact about the source rather than about the gate. They are
  original diagrams drawn for this article, not screenshots, and each carries content the prose does
  not.
- **Figure-to-file mapping** was verified in the DOM rather than assumed from array order - the
  uploads are named `image-22`, `image-21`, `image-24` and their order on the page is **not** their
  numeric order.

  | Figure | Caption | File |
  |---|---|---|
  | 1 | High Level Architecture of Agent Gateway | `visuals/fig1_gateway-architecture.jpg` |
  | 2 | Elicitation handshake | `visuals/fig2_elicitation-handshake.jpg` |
  | 3 | User experience with bundled MCP pack | `visuals/fig3_bundles-and-filtering.jpg` |

- **Limitation that shapes every number in here: this is a vendor engineering-brand post.** It is
  first-party, unaudited, and published on a careers site with job listings under it. The
  architecture is described in enough detail to be checkable in principle and in no detail that
  could be checked in practice - no latency figures, no failure rates, no cost, no incident, and no
  comparison against the alternative it replaced. Read the adoption block as the strongest claim and
  the least verifiable one.
- **Closest neighbour in this brain is [S27](../260816_scaling-github-for-agents/)** (GitHub's MCP
  server), and the pairing is the most valuable thing about this ingest: S27 is the *server* owner
  solving tool-surface size from the inside, S29 is the *consumer* organisation solving it from the
  outside. They converge on the same answer from opposite ends, which is the independence that
  raises confidence.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
