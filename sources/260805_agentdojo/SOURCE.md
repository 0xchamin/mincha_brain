# Source - AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents

> Persona: **curator** - re-adopt when working this file.

> Metadata + facts for one ingested source. Single source of truth for this source.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | paper |
| URL | https://arxiv.org/abs/2406.13352 (PDF: https://arxiv.org/pdf/2406.13352) |
| Title | AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents |
| Author / channel | Edoardo Debenedetti (ETH Zurich), Jie Zhang (ETH), Mislav Balunović (ETH + Invariant Labs), Luca Beurer-Kellner (ETH + Invariant Labs), Marc Fischer (ETH + Invariant Labs), Florian Tramèr (ETH) |
| Published | 2024-06-19 (v1); 2024-11-24 (v3, ingested) |
| Duration / length | 26 pages (9 pages main paper + appendices A-D) |
| Commit SHA | n/a (paper). Code: `github.com/ethz-spylab/agentdojo`; leaderboard and docs at `agentdojo.spylab.ai` - **neither cloned nor gated** |
| License | n/a (arXiv preprint; text not redistributed, PDF stays in git-ignored `raw/`) |
| Ingested | 2026-08-05 |
| Access | open |
| Topics | agent-security, evals, agents |
| Visual leg | analysed (5 frames kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/` - the captured PDF + extracted text (git-ignored).
3. `nodes.md` - knowledge nodes.
4. `context/` - external evidence from a deep-research pass (**empty** - none requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the curated figures and tables.

## Ingest notes

- **Capture method:** the established paper flow. Read tool over pages 1-9 (the whole main paper),
  `pdftotext -layout` for grepping the appendices.
- **Visual pre-filter:** five artifacts, chosen to walk framework -> environments -> the headline
  finding -> attack variance -> defences. One crop landed on Figure 7 rather than the intended
  attacker-knowledge ablation and **Figure 7 was kept instead**, because the spread of attack success
  across applications teaches more than the ablation table.
- **Tier: this is the strongest venue in the security set so far.** Published at
  **NeurIPS 2024, Datasets and Benchmarks Track** - a main-conference peer-reviewed track, not a
  workshop and not a bare preprint. Recorded as **T1-adjacent**; the kit's tier table has no exact
  slot for a benchmark paper, and the review standard here is the highest of S16-S20.
- **⚠️ The independence fact that decided the ingest order.** AgentDojo shares two authors with
  **S18 (CaMeL)** - Debenedetti first-authors both, Tramèr co-authors both. **This source therefore
  cannot validate CaMeL**, which is exactly what was recorded as an open question when S18 was
  ingested, and it is why S19 was prioritised ahead of this one. What AgentDojo *can* do is stand on
  its own as the field's reference benchmark and as a source of findings independent of S16, S17 and
  S19.
- **A second affiliation worth naming:** three authors are also at **Invariant Labs**, a startup in
  agent security. No product is evaluated here and the benchmark is open source, so the conflict is
  mild and recorded rather than weighted.
- **What this source is *for*, in this brain.** It is the first **eval harness** for agent security,
  and it is the closest thing available to the verifier the owner's build needs - the S14/S15
  frame says a self-improving loop improves at the rate its verifier can distinguish good from bad,
  and this is a verifier for the security half.
- **Not done:** the repository was not cloned and no deep-research pass was run.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
