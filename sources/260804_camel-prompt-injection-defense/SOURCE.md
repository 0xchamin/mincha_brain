# Source - Defeating Prompt Injections by Design (CaMeL)

> Persona: **curator** - re-adopt when working this file.

> Metadata + facts for one ingested source. Single source of truth for this source.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | paper |
| URL | https://arxiv.org/abs/2503.18813 (PDF: https://arxiv.org/pdf/2503.18813) |
| Title | Defeating Prompt Injections by Design |
| Author / channel | Edoardo Debenedetti (Google + ETH Zurich), Ilia Shumailov (Google DeepMind), Tianqi Fan (Google), Jamie Hayes (DeepMind), Nicholas Carlini (DeepMind), Daniel Fabian (Google), Christoph Kern (Google), Chongyang Shi (DeepMind), Andreas Terzis (DeepMind), Florian Tramèr (ETH Zurich) |
| Published | 2025-03-24 (v1); 2025-06-24 (v2, ingested) |
| Duration / length | 125 pages - **25 pages of main paper, 100 pages of appendix** (prompts, full result tables, generated-code transcripts) |
| Commit SHA | n/a (paper). Companion code: `github.com/google-research/camel-prompt-injection` - **not cloned, not gated** |
| License | n/a (arXiv preprint; text not redistributed, PDF stays in git-ignored `raw/`) |
| Ingested | 2026-08-04 |
| Access | open |
| Topics | agent-security, agents, context-engineering |
| Visual leg | analysed (6 frames kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/` - the captured PDF + extracted text (git-ignored).
3. `nodes.md` - knowledge nodes.
4. `context/` - external evidence from a deep-research pass (**empty** - none requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the curated figures.

## Ingest notes

- **Capture method:** the established paper flow. `curl` the PDF into git-ignored `raw/`, Read tool
  over the design pages (3-10) visually, and `pdftotext -layout` for the evaluation, overheads and
  discussion sections. **The appendix is 100 of the 125 pages** and was deliberately not read: it is
  system prompts, per-suite result tables and transcripts of generated code, which is replication
  material rather than teaching material.
- **Visual pre-filter:** six figures chosen to walk problem -> design -> mechanism -> results ->
  limitation -> cost. Cropped from `pdftoppm` renders at 130 DPI and `view`ed. Note that `pdftoppm`
  zero-pads to **three digits** on a 125-page PDF, which broke the first crop script - worth knowing
  before the next long paper. One crop landed on Figure 12 (data flow becoming control flow) rather
  than the intended baseline chart, and **Figure 12 was kept instead** because the paper's own
  demonstration of its limits teaches more than another bar chart.
- **Tier: T3 (preprint).** No journal reference on the arXiv listing at ingest.
- **⚠️ Independence: the headline number is measured on the authors' own benchmark.** CaMeL reports
  77% of **AgentDojo** tasks solved with provable security. **Debenedetti is first author of both
  CaMeL and AgentDojo, and Tramèr is a co-author of both.** This is not concealed - the paper cites
  AgentDojo normally - and under this kit's independence rule it means the evaluation cannot be
  treated as third-party validation. **This is the single most important gate fact about the source**
  and it is why S19 (AgentDojo) is being ingested separately rather than taken on trust from here.
- **Vendor position:** Google and Google DeepMind, plus ETH Zurich. Google sells agent infrastructure,
  so a Google defence paper is **T2-adjacent on the question of whether agent security is tractable**,
  even though the artifact is an academic preprint. Recorded because the paper's thesis - that
  scaffolding beats model training - happens to favour a platform provider.
- **Unusually honest, and this is worth recording positively.** §3.1 lists explicit non-goals, §6.4
  demonstrates an attack that defeats the design's core isolation, §7 concedes side channels, and
  §9.3 is titled "So, Are Prompt Injections Solved Now?" and answers "No". The authors volunteer the
  Control Flow Integrity / return-oriented-programming analogy **against their own work**.
- **Not done:** the companion repo was not cloned and no deep-research pass was run.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
