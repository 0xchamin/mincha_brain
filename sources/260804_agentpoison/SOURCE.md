# Source - AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases

> Persona: **curator** - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | paper |
| URL | https://arxiv.org/abs/2407.12784 (PDF: https://arxiv.org/pdf/2407.12784) |
| Title | AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases |
| Author / channel | Zhaorun Chen (U Chicago), Zhen Xiang (UIUC), Chaowei Xiao (U Wisconsin-Madison), Dawn Song (UC Berkeley), Bo Li (U Chicago + UIUC) |
| Published | 2024-07-17 (arXiv v1) |
| Duration / length | 22 pages, 13 figures, 7 tables (10 pages main paper + appendix) |
| Commit SHA | n/a (paper). Companion code: `github.com/BillChan226/AgentPoison` - **not cloned, not gated** |
| License | n/a (arXiv preprint; text not redistributed, PDF stays in git-ignored `raw/`) |
| Ingested | 2026-08-04 |
| Access | open |
| Topics | agent-security, memory, rag |
| Visual leg | analysed (7 frames kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/` - the captured PDF + extracted text (git-ignored).
3. `nodes.md` - knowledge nodes (corroborated claims + figures + citations).
4. `context/` - external evidence from a deep-research pass (**empty** - none requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the curated figures and tables.

## Ingest notes

- **Capture method:** `curl` the arXiv PDF into `raw/`, then two complementary reads. The **Read
  tool rendered pages 1-10 visually** (this kit's `view` capability *is* the vision model, so a
  paper's figures are read in place rather than extracted blind), and `pdftotext -layout` produced
  `raw/agentpoison.txt` so the appendix could be grepped for citations without spending tokens on
  twelve more pages. **`pdftotext` was installed for this ingest** (`brew install poppler`) - this is
  the brain's **first paper source**, and the flow had never been run.
- **Visual pre-filter:** a paper needs no scene-detect. Figures were selected by argument role, then
  cropped from `pdftoppm` page renders at 130 DPI and `view`ed to confirm framing. Four crops were
  re-cut after viewing showed them truncated or catching the wrong float - notably the perplexity
  figure, where the p9 version was **replaced** by Figure 10 on p17 (the same measurement across all
  three agents rather than two).
- **Tier: T3 (preprint).** The PDF footer reads "Preprint. Under review." and the arXiv listing
  carries **no journal reference** as of ingest. `reading-list.md` listed this row as "T1/T3"; the
  ingested artifact is **T3**, and the note is written to that.
- **Independence:** five authors across four universities, no vendor. **The first source in this
  brain with no commercial position in what it claims** - it sells nothing, and its headline result
  is an attack rather than a product.
- **Limitations the paper states about itself:** the attack requires **white-box access to the
  embedder** for trigger optimization. The transferability result (Figure 3) is the paper's own
  answer to that, and it is argued rather than closed.
- **Not done:** the companion repo was not cloned, so nothing here is corroborated against running
  code. No deep-research pass was run, so **every citation points inside one paper**.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
