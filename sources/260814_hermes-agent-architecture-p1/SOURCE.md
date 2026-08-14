# Source - Hermes Agent Architecture Part 1: Gateway, Sessions, and the Agent Loop

> Persona: **curator** (media) - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | blog |
| URL | https://theagentstack.substack.com/p/hermes-agent-architecture-part-1 |
| Title | Hermes Agent Architecture - Part 1: Gateway, Sessions, and the Agent Loop |
| Author / channel | Vinoth Govindarajan ("The Agent Stack", Substack) |
| Published | 2026-08-10 |
| Duration / length | ~6,350 words, 4 figures |
| Commit SHA | n/a (the *subject* is pinned by the author: Hermes Agent v0.19.1, tag `v2026.7.30`, commit `cc4cab2`) |
| License | n/a (article, all rights reserved - quoted under fair use, not redistributed) |
| Ingested | 2026-08-14 |
| Access | open |
| Topics | agents, context-engineering, agent-security, evals |
| Visual leg | analysed (4 figures kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/article.txt` - the captured body text (git-ignored).
3. `nodes.md` - knowledge nodes (corroborated claims + figures + citations).
4. `context/` - **external evidence** from a deep-research pass (empty - not requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the four curated figures.

## Ingest notes

- **Capture method:** `curl` for the page HTML, then a scripted tag-strip into `raw/article.txt`;
  `WebFetch` for the structured read. The four content figures were downloaded from
  `substack-post-media.s3.amazonaws.com` and downscaled to 1600px with `sips` before `view`.
- **Visual pre-filter:** the article carries five images. One is the publication logo and was
  dropped without viewing. The remaining four are all substantive (two rendered mermaid diagrams,
  two rendered tables), so **all four were `view`ed and all four were kept** - the pre-filter step
  that matters for video does not bind here, because a hand-authored figure count of four is
  already below the triage threshold.
- **Figure order in the body** (established by byte offset in the captured HTML, since Substack
  lazy-loads images out of the DOM): `fig1` architecture overview -> `fig2` ownership split ->
  `fig3` gateway message flow -> `fig4` six failure cases.
- **What makes this source unusual for its tier.** It is a T4 practitioner blog, and the author
  pins a version, a git tag and a commit, states the platform, and says architecture claims were
  checked against source, official docs and regression tests. That is a **claim about method**
  which this brain could not verify - the Hermes repository was **not cloned** and no line was
  read. Every node here is gated on the article and its own figures only.
- **Limitation that shapes every node:** the article describes **one system**. Its transferable
  content is the set of **boundaries** it names, not the fact that Hermes places them where it
  does. Nodes are written to the boundary wherever the boundary survives losing the product name,
  and nodes that cannot survive that are marked as product-specific.
- **Nothing here is measured.** No latency, no throughput, no failure rate, no incident, no
  comparison against another design. It is an architecture description.
- **The subject is the same artifact S19 attacked, verified rather than assumed.**
  [S19](../260805_memory-poisoning-systematic/LEARNING.md) names HERMES as one of its two evaluated
  agent systems and attributes it to Nous Research in its own bibliography. This is the first artifact
  in this brain covered by both an independent measured attack and an independent architecture
  description. **The use restriction is `d5` in [`nodes.md`](nodes.md)** - Part 1 is not about memory,
  so it moves neither claim 160 nor claim 161.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
