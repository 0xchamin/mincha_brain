# Source - Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection

> Persona: **curator** - re-adopt when working this file.

> Metadata + facts for one ingested source. Single source of truth for this source; other docs here
> link to this table.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | paper |
| URL | https://arxiv.org/abs/2302.12173 (PDF: https://arxiv.org/pdf/2302.12173) |
| Title | Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection |
| Author / channel | Kai Greshake (Saarland University + sequire technology GmbH), Sahar Abdelnabi (CISPA), Shailesh Mishra (Saarland), Christoph Endres (sequire), Thorsten Holz (CISPA), Mario Fritz (CISPA). **Greshake and Abdelnabi contributed equally** |
| Published | 2023-05-05 (arXiv v2; v1 2023-02-23) |
| Duration / length | 33 pages, 28 figures (13 pages main paper + appendix of prompts and screenshots) |
| Commit SHA | n/a (paper). Companion code: `github.com/greshake/lm-safety` - **not cloned, not gated** |
| License | n/a (arXiv preprint; text not redistributed, PDF stays in git-ignored `raw/`) |
| Ingested | 2026-08-04 |
| Access | open |
| Topics | agent-security, memory, agents |
| Visual leg | analysed (6 frames kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/` - the captured PDF + extracted text (git-ignored).
3. `nodes.md` - knowledge nodes (corroborated claims + figures + citations).
4. `context/` - external evidence from a deep-research pass (**empty** - none requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the curated figures.

## Ingest notes

- **Capture method:** the paper flow established by S16 the same day. `curl` the arXiv PDF into
  git-ignored `raw/`, the **Read tool rendered pages 1-10 visually**, and `pdftotext -layout`
  produced `raw/greshake.txt` so the discussion, ethics and mitigation sections could be read as text
  without spending tokens on twenty more pages of appendix prompts.
- **Visual pre-filter:** six figures selected by argument role from a 28-figure paper, cropped from
  `pdftoppm` renders at 130 DPI and `view`ed to confirm framing. **Four were re-cut** after viewing
  showed them truncated or catching an adjacent float, which is now the expected rate for two-column
  ACM layouts rather than a surprise.
- **Tier: T3 (preprint).** The arXiv listing carries **no journal reference and no venue comment** as
  of ingest, so this note is written to T3. *(This paper is widely cited as the origin of the term
  "indirect prompt injection" and may well have been published at a workshop; that was not verified
  here and the artifact does not say so.)*
- **Independence: strong, and it matters more than usual.** Six authors across Saarland University,
  CISPA and a small security firm, with **no overlap of any kind with S16's authors** (Chicago /
  UIUC / Wisconsin / Berkeley). Different institutions, different countries, different years, and
  different attack mechanisms converging on the same target. **This is what makes S17 the first
  source in `agent-security.md` to corroborate another** - see
  [ADR-0019](../../brain/decisions/0019-agent-security-established.md).
- **What the paper does and does not do.** It is a **taxonomy and demonstration** paper. It
  establishes *feasibility* across six threat classes on real deployed systems (Bing Chat on GPT-4,
  GitHub Copilot), and it reports **no attack success rates, no sample sizes and no statistics
  anywhere** - see `d1`, which is the single most important thing to know before citing it.
- **Ethics:** responsible disclosure to OpenAI and Microsoft is stated, and the authors say they did
  not inject prompts into any public source retrievable by other users (§5.1).
- **Not done:** the companion repo was not cloned and no deep-research pass was run, so every
  citation points inside one paper.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
