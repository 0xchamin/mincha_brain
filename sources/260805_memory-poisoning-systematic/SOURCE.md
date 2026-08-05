# Source - From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning Attacks in LLM Agents

> Persona: **curator** - re-adopt when working this file.

> Metadata + facts for one ingested source. Single source of truth for this source.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | paper |
| URL | https://arxiv.org/abs/2606.04329 (PDF: https://arxiv.org/pdf/2606.04329) |
| Title | From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning Attacks in LLM Agents |
| Author / channel | Pritam Dash (Huawei Canada), Tongyu Ge (Huawei Canada), Aditi Jain (Huawei Canada), Tanmay Shah (University of Waterloo; work done during an internship at Huawei), Zhiwei Shang (Huawei Canada) |
| Published | 2026-06-03 (v1); 2026-06-18 (v2, ingested) |
| Duration / length | 14 pages (9 pages main paper + appendices A-C) |
| Commit SHA | n/a (paper). **MPBench is described but no repository URL appears in the main paper** |
| License | n/a (arXiv preprint; text not redistributed, PDF stays in git-ignored `raw/`) |
| Ingested | 2026-08-05 |
| Access | open |
| Topics | agent-security, memory, skills |
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
  `pdftotext -layout` for grepping. At 14 pages this is the smallest paper ingested so far and the
  whole argument fits in the visual read.
- **Visual pre-filter:** five artifacts chosen to carry the argument - the attack surface, the
  vulnerability-to-channel map, the attack results, the defence results, and the signal-strength
  breakdown. Two crops were extended after viewing cut off their final rows.
- **Tier: T3, and slightly better than a bare preprint.** The PDF states it was **published at the
  Second Workshop on Agents in the Wild (AIWILD) at ICML 2026**, so it has had workshop-level review.
  That is lighter than a main-conference track and it is more than none. Recorded as T3 with the
  venue noted rather than promoted to T1.
- **⚠️ Vendor position: four of five authors are Huawei Canada.** Huawei sells cloud and AI
  infrastructure. The paper sells no product and its findings are unflattering to agent vendors
  generally, so the conflict is mild - but it is a corporate lab publishing on agent security, and
  the "aggressive memory design is more exploitable" finding is one a platform vendor benefits from
  being seen to raise.
- **Independence: strong, and it is the reason this source was prioritised.** No author or
  institutional overlap with S16 (Chicago/UIUC/Wisconsin/Berkeley), S17 (Saarland/CISPA), or S18
  (Google/DeepMind/ETH). **This is the third independent source in this brain on agent memory as an
  attack surface**, after S16 and S17.
- **The limitation the authors state and that governs the numbers:** MPBench delivers the adversarial
  payload as a **labelled context block alongside the user query**, not through the agent's real tool
  call and retrieval pipeline. They call it "a controlled emulation of real deployment" and note it
  follows prior agent-security benchmarks. See `d1`.
- **Not done:** no deep-research pass; MPBench was not located or run.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
