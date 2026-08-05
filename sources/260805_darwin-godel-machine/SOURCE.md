# Source - Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents

> Persona: **curator** - re-adopt when working this file.

> Metadata + facts for one ingested source. Single source of truth for this source.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | paper |
| URL | https://arxiv.org/abs/2505.22954 (PDF: https://arxiv.org/pdf/2505.22954) |
| Title | Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents |
| Author / channel | Jenny Zhang (UBC + Vector Institute), Shengran Hu (UBC + Vector + Sakana AI), Cong Lu (UBC + Vector + Sakana), Robert Lange (Sakana AI), Jeff Clune (UBC + Vector + Sakana + Canada CIFAR AI Chair). **Zhang and Hu are co-first authors; Lange and Clune co-senior** |
| Published | 2025-05-29 (v1); 2026-03-12 (v3, ingested) |
| Duration / length | 72 pages (**9 pages of main paper**, the rest appendices A-I: ablations, prompts, per-modification diffs, safety discussion) |
| Commit SHA | n/a (paper). Code open-sourced at `github.com/jennyzzt/dgm` - **not cloned, not gated** |
| License | n/a (arXiv preprint of a published paper; text not redistributed, PDF stays in git-ignored `raw/`) |
| Ingested | 2026-08-05 |
| Access | open |
| Topics | self-improvement, autonomous-research-loops, agent-security |
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

- **Capture method:** the established paper flow. Read tool over pages 1-9 (the entire main paper,
  including the safety discussion), `pdftotext -layout` for locating sections in the 63 pages of
  appendix. The appendices are ablations, prompts and per-modification code diffs - replication
  material, deliberately not read.
- **Visual pre-filter:** four figures, chosen to carry the loop, the ablation, the search behaviour
  and the generalisation. Three crops were shifted after viewing caught body text above the figure,
  which is now the routine correction on ICLR two-column layouts.
- **Tier: the strongest venue in this brain.** The PDF header reads **"Published as a conference paper
  at ICLR 2026"** - a top-tier peer-reviewed main track, above S20's NeurIPS Datasets and Benchmarks
  track and well above the preprints. **Code is open-sourced**, which none of S16-S19 managed.
- **Independence:** UBC, Vector Institute, Sakana AI. **No overlap with any prior source in this
  brain.** Sakana AI is a commercial lab and also the publisher of *The AI Scientist*, which S14
  cites and which this brain declined to ingest - so there is a mild commercial position in
  self-improving systems being a promising research direction.
- **Why it was ingested last, and why it still earned a place.** It is the only non-security source of
  the five, and it is the artifact-layer counterpart to S13 (`karpathy/autoresearch`) that
  [`autonomous-research-loops.md`](../../brain/topics/autonomous-research-loops.md) named as its
  merge-back trigger. **What was not anticipated is that its §5 Safety Discussion supplies the
  builders' own statement of S19's V-S5** - see `n12`.
- **Not done:** the repository was not cloned and no deep-research pass was run. Given that the code
  is public and the whole claim is about code that rewrites itself, **a docs-versus-code pass here
  would be unusually informative** and was not taken.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
