# Source - Defending Against Indirect Prompt Injection Attacks With Spotlighting

> Persona: **curator** - re-adopt when working this file.

> Metadata + facts for one ingested source. Single source of truth for this source.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | paper |
| URL | https://arxiv.org/abs/2403.14720 (PDF: https://arxiv.org/pdf/2403.14720) |
| Title | Defending Against Indirect Prompt Injection Attacks With Spotlighting |
| Author / channel | Keegan Hines, Gary Lopez, Matthew Hall, Federico Zarfati, Yonatan Zunger, Emre Kıcıman - **all Microsoft** |
| Published | 2024-03-20 (arXiv v1, the only version) |
| Duration / length | 8 pages (7 pages main paper + a one-page appendix) |
| Commit SHA | n/a (paper). **No code or dataset release is mentioned anywhere in the paper** |
| License | n/a (arXiv preprint; text not redistributed, PDF stays in git-ignored `raw/`) |
| Ingested | 2026-08-05 |
| Access | open |
| Topics | agent-security, context-engineering |
| Visual leg | analysed (4 frames kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/` - the captured PDF + extracted text (git-ignored).
3. `nodes.md` - knowledge nodes.
4. `context/` - external evidence from a deep-research pass (**empty** - none requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the curated figures.

## Ingest notes

- **Capture method:** the established paper flow. At 8 pages the entire paper was read visually,
  including the appendix.
- **Visual pre-filter:** four figures kept, chosen to walk the three techniques in ascending order of
  strength and then to price them - delimiting's modest effect, datamarking's dramatic one,
  datamarking's zero task cost, and encoding's real task cost. A fifth (encoding's ASR) was cropped
  and dropped as redundant with the numbers quoted in prose.
- **Tier: T2/T3, and the vendor position is the thing to record.** An arXiv preprint with **no venue
  and no code release**, authored entirely by **Microsoft** - who ship the products whose compromise
  the related work cites (Bing Chat is named). This is a vendor proposing a defence for its own
  attack surface, which does not make it wrong and does place it in the same evidential class as
  S12's reference architecture rather than alongside S20's peer-reviewed benchmark.
- **Why it was ingested despite being the weakest source in the security set.** It is the **cheap
  defence most teams actually deploy**, S18 measures its cost at 1.06x input tokens against CaMeL's
  2.82x, and S20 evaluates one of its variants. Without it this brain would hold the expensive
  defences and not the common one. **Its intellectual contribution turned out to be larger than its
  evidential one** - see the telecom analogy in `n12`.
- **The evaluation is entirely non-agentic**, which is the most important scoping fact. All tasks are
  document summarization and Q&A - single-turn, no tool calls, no environment state - so this is
  never tested against the threat model S17 describes. See `d3`.
- **Not done:** no deep-research pass. Nothing to clone.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
