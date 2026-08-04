# Reading list - ingest candidates

> Persona: **architect** - re-adopt when working this file. Contract:
> [`AGENTS.md`](../AGENTS.md) § "`foundations/` - supplied background, uncited by construction".

> **What this is.** Primary sources this brain has decided are worth gating but has not ingested
> yet. It is the destination the contract names when staged material turns out to be *making claims
> about the world* rather than *teaching a fundamental*: **the primary it cites is what to ingest,
> and this is where that pointer lives** so it is not lost when `staging/` is cleared.
>
> **Nothing here is evidence.** A row is a pointer and an intention. A claim enters this brain only
> through `sources/<id>/`, the corroboration gate, and `claims.md` - never from this file.
>
> **Priority is about what a source would close, not about how good it is.** `high` means it closes a
> gap a topic note names, or answers a recorded open question. Re-read the topic note before
> promoting a row: a gap may have closed since.

> **Specifications are not on this list, deliberately.** The MCP spec, the OpenAI and Anthropic tool
> use guides, RDF/OWL, the EU AI Act - these are **reference, looked up on demand**, not material to
> learn *from*. This kit exists to turn things you learn from into durable cited knowledge, and a
> normative document is consulted at the moment you need the exact answer. Ingesting one would
> produce a worse copy of something authoritative and permanently online.

## Candidates

| Priority | Source | Tier | Why it earns an ingest | Gap it closes |
|---|---|---|---|---|
| **high** | **Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection** - Greshake et al., CISPA/Bosch, 2023, [arXiv:2302.12173](https://arxiv.org/abs/2302.12173) | T1 | The paper that defined indirect prompt injection as a class, with working attacks against real deployed applications | [`agent-security.md`](topics/agent-security.md) is `emerging` on three sources of which **only one studies threats at all**; the rest are the auth substrate. This is the field's foundational threat paper and the topic's most obvious hole |
| **high** | **Memory poisoning: two 2026 studies** - [arXiv:2601.05504](https://arxiv.org/abs/2601.05504) (attack and defense) and [arXiv:2606.04329](https://arxiv.org/abs/2606.04329) (systematic study) | T3 (**titles unverified** - the IDs came from a prior pass and the listings have not been opened) | Attacks specifically against agent memory stores, and **the first of the two claims to carry defenses**, which is now the gap rather than the attack | **AgentPoison was ingested as S16 on 2026-08-04 and is removed from this row.** It closed the attack half decisively and left the defence half wide open: claims 138-141 rule out volume detection, embedder privacy, perplexity filtering and isolate-then-aggregate, and `agent-security.md`'s restated open question is now simply *what defends a retrieval store*. **Ingest these for the defence, not the attack** |
| **high** | **Lost in the Middle: How Language Models Use Long Contexts** - Liu et al., Stanford, 2023, [arXiv:2307.03172](https://arxiv.org/abs/2307.03172) | T1 | The U-shaped position curve, measured - primacy and recency bias in a filled window | [`context-engineering.md`](topics/context-engineering.md) holds "context rot" and "limiting context beats filling it" (claim 22) from **practitioner assertion**. This is the measured primary underneath, and would be the topic's first T1 |
| **high** | **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** - Lewis et al., FAIR, NeurIPS 2020, [arXiv:2005.11401](https://arxiv.org/abs/2005.11401) | T1 | The original RAG paper: parametric plus non-parametric memory | [`rag.md`](topics/rag.md) is `emerging` and records that **chunking, embeddings, vector stores, hybrid search and grounding evals are at zero**. Its two sources argue *against* retrieval or retrieve over tool schemas. The topic has no foundational paper at all |
| **high** | **ReAct: Synergizing Reasoning and Acting in Language Models** - Yao et al., ICLR 2023, [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) | T1 | The loop, with an ablation against act-only and reason-only baselines | [`agents.md`](topics/agents.md) is `established` across 8 sources and **has no primary behind the agent loop itself** - S2's "prompt + switch + context + loop" is a practitioner framing. A T1 ablation would be the topic's first measured basis |
| **high** | **A-MEM: Agentic Memory for LLM Agents** - Xu et al., NeurIPS 2025, [arXiv:2502.12110](https://arxiv.org/abs/2502.12110), with **Mem0** [arXiv:2504.19413](https://arxiv.org/abs/2504.19413) as the production counterpart | T1/T3 | Memory architectures that were **measured**, not just designed | [`memory.md`](topics/memory.md)'s headline caveat is that **three sources converged on the design and none published an experiment**, and its open question is whether maintained memory helps an agent at all. This is the most direct answer available |
| **high** | **Large Language Monkeys: Scaling Inference Compute with Repeated Sampling** - Brown, Juravsky, Ehrlich, Clark, Le, Re, Mirhoseini, 2024, [arXiv:2407.21787](https://arxiv.org/abs/2407.21787) | T3 | The primary behind S14's headline chart, and the source of the coverage/precision decomposition | S14 is a **lecture narrated by this paper's senior author**, so claims 120 and 121 currently rest on a non-independent secondary. [`self-improvement.md`](topics/self-improvement.md) is `emerging` on one source and this is its founding primary. Would also settle what the "(Oracle Verifier)" panels actually measure (`d1`) |
| **high** | **The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery** - Lu et al., Sakana AI, 2024, [arXiv:2408.06292](https://arxiv.org/abs/2408.06292) | T3 | A full research loop that generates ideas, runs experiments, writes the paper, **and reviews it with an LLM** | [`autonomous-research-loops.md`](topics/autonomous-research-loops.md) is `emerging` on **one primary** (S13) and names a second primary as its merge-back trigger. This is the obvious candidate: same shape, different domain, and its terminal LLM-review step is claim 34's prohibition installed as architecture. S14 only mentions it (`n10`, ADR-0012) |
| **high** | **Shrinking the Generation-Verification Gap with Weak Verifiers (Weaver)** - Saad-Falcon, Buchanan, Chen, Huang, McLaughlin, Bhathal, Zhu, Athiwaratkun, Sala, Linderman, **Mirhoseini**, Ré, 2025, [arXiv:2506.18203](https://arxiv.org/abs/2506.18203) (CS329A lecture 3) | T3 | The field's direct attack on the gap S15 only measured. Combines many weak, imperfect verifiers into one strong verifier using weak supervision to estimate each one's accuracy, reporting 87.7% average with Llama-3.3-70B as generator, and distils the ensemble into a 400M cross-encoder to cut its cost | Answers [`self-improvement.md`](topics/self-improvement.md)'s named open question, **"What actually closes the generation-verification gap?"** - and it is one of the two suggestions recorded from S15's own room (ensembling many weak verifiers). **⚠️ NOT independent: Mirhoseini is a co-author**, so under the independence rule it may supply mechanism and may **not** advance the topic's independent source count, which stays at 1. Ingest it for how a verifier ensemble is actually built, never for confidence |
| **high** | **Let's Verify Step by Step** - Lightman et al., OpenAI, 2023, [arXiv:2305.20050](https://arxiv.org/abs/2305.20050) (CS329A lecture 3) | T3 (preprint, OpenAI authors) | Process supervision against outcome supervision, **measured** rather than asserted, with the PRM800K label set released | This brain holds the ORM/PRM distinction from **S15's narration alone** (`n16`, `n17`) with nothing measured behind it, and `frame_1000`'s reward-model curves are the thing that plateaus. The primary underneath the single most important design choice in a verifier: score the answer, or score each step |
| **high** | **Darwin Gödel Machine (DGM): Open-Ended Evolution of Self-Improving Agents** - Zhang, Hu, Lu, Lange, Clune, 2025, [arXiv:2505.22954](https://arxiv.org/abs/2505.22954) (CS329A lecture 7, where the syllabus lists it under the older title "Automated design of agentic systems") | T3 | An agent that iteratively **rewrites its own code**, empirically validating each change against coding benchmarks rather than proving it beneficial, and keeping an **archive** of agents instead of a single lineage. SWE-bench 20.0% -> 50.0%, Polyglot 14.2% -> 30.7%, with ablations against no-self-improvement and no-open-endedness baselines | [`autonomous-research-loops.md`](topics/autonomous-research-loops.md) is `emerging` on **one primary** (S13) and names a second primary as its merge-back trigger. This is the strongest candidate: S13's loop edits one training script under four freezes, and this one edits **the agent itself**, so it tests whether the four freezes generalise or were specific to a fixed harness. **Independent of both S13 and the CS329A lecturers.** Also the only paper on that syllabus touching the threat question `self-improvement.md` records as absent, via its sandboxing and human-oversight precautions |
| medium | **Building Effective Agents** - Anthropic Engineering, Dec 2024, [anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents) | T2 | Origin of the five orchestration patterns and the agent-computer interface framing, both circulating here second-hand | S9 supplied the pattern names from a **competing vendor**. Ingesting the origin would test whether S9 reported them faithfully. **S14 cites this page on three separate slides** (`frame_2640` among them), making it the most-referenced un-ingested source in this brain |
| medium | **Cognitive Architectures for Language Agents (CoALA)** - Sumers et al., Princeton, 2023, [arXiv:2309.02427](https://arxiv.org/abs/2309.02427) | T1 | An explicit working/episodic/semantic/procedural taxonomy for agents, drawn from cognitive science | `memory.md` and `skills.md` both lean on "**a skill is procedural memory**" as a borrowed label with **no primary behind it**. The cross-domain hop the research calibration asks for |
| medium | **Gorilla: LLM Connected with Massive APIs** - Patil et al., Berkeley, 2023, [arXiv:2305.15334](https://arxiv.org/abs/2305.15334) | T1 | Measures API hallucination with and without schema grounding | S10's retrieval findings are **uncorroborated**; this is an independent second leg for `mcp.md` and `rag.md` |
| medium | **tau-bench** - Sierra/Princeton, 2024, [arXiv:2406.12045](https://arxiv.org/abs/2406.12045), and **SWE-bench** - Jimenez et al., ICLR 2024, [arXiv:2310.06770](https://arxiv.org/abs/2310.06770) | T1 | pass^k reliability under repetition, and outcome-graded real-world tasks | `evals.md` is `established` but every source is a practitioner pipeline. These are the field's reference benchmarks and would give the topic a measured spine |
| medium | **Self-RAG: Learning to Retrieve, Generate, and Critique** - Asai et al., 2023, [arXiv:2310.11511](https://arxiv.org/abs/2310.11511) | T1 | Reflection tokens deciding retrieval on demand - retrieval as a decision rather than a step | `rag.md` has nothing on adaptive or conditional retrieval |
| medium | **Toolformer** - Schick et al., Meta AI, 2023, [arXiv:2302.04761](https://arxiv.org/abs/2302.04761) | T1 | Establishes that *when* to call a tool is learnable, not only promptable | `agents.md` treats tool selection as a prompting problem throughout. This is the counter-position |
| low | **Reflexion** - Shinn et al., NeurIPS 2023, [arXiv:2303.11366](https://arxiv.org/abs/2303.11366) | T1 | Self-critique as a loop stage; finds hallucination dominates inefficient planning | Bears on claim 34 (do not let the producer grade its own work), but the brain already holds that well |
| low | **Universal and Transferable Adversarial Attacks on Aligned LLMs (GCG)** - Zou et al., CMU, 2023, [arXiv:2307.15043](https://arxiv.org/abs/2307.15043) | T1 | Automated transferable jailbreaks - attacks on the model rather than on the agent | Real, but `agent-security.md` needs **agent-layer** threats first. Queue behind Greshake |
| low | **Sleeper Agents** - Hubinger et al., Anthropic, 2024, [arXiv:2401.05566](https://arxiv.org/abs/2401.05566) | T2 | Backdoors surviving safety training | Adjacent to this brain's scope - a training-time property, not an agent-architecture one |
| low | **Tree of Thoughts** - Yao et al., 2023, [arXiv:2305.10601](https://arxiv.org/abs/2305.10601) | T1 | Search over reasoning states rather than a linear trace | `agents.md` has nothing on search or backtracking |
| low | **ToolLLM** - Qin et al., ICLR 2024, [arXiv:2307.16789](https://arxiv.org/abs/2307.16789) | T1 | Tool retrieval at 16,000 APIs, beyond S10's 1,180 | Extends S10's curve rather than corroborating it |
| low | **MRKL Systems** - Karpas et al., AI21, 2022, [arXiv:2205.00445](https://arxiv.org/abs/2205.00445) | T1 | Identified routing as the hard part before ReAct named the loop | Historical framing; S10 carries the modern statement |
| low | **The Entity-Relationship Model** - Chen, ACM TODS 1976, [dl.acm.org/doi/10.1145/320434.320440](https://dl.acm.org/doi/10.1145/320434.320440), and **Knowledge Graphs** - Hogan et al., ACM CSUR 2021, [arXiv:2003.02320](https://arxiv.org/abs/2003.02320) | T1 | The domain-modelling classics behind every schema an agent reads | Only relevant if this brain goes toward structured knowledge representation. **Parked, not queued** |

## Not promoted, and why

- **Specifications and official guides** - MCP spec, OpenAI/Anthropic tool-use docs, W3C RDF and OWL,
  NIST AI RMF, EU AI Act. **Reference, consulted on demand.** See the note at the top.
- **Surveys and aggregators** - Wang et al. 2023, Xi et al. 2023, the RAG survey, the agent-evaluation
  surveys, OWASP's Top 10. **T5 by the aggregator rule: use for discovery, cite the primary they
  point at.** OWASP is the marginal case, since ASI06 is the field's shared vocabulary for memory
  poisoning - if the poisoning papers above get ingested, cite them and mention OWASP as the label.
- **Framework and tool repositories** - LangGraph, DSPy, MemGPT/Letta, Mem0, Zep, promptfoo, Inspect,
  lm-evaluation-harness, OpenAI Evals. These are **code sources** needing the code-explorer flow, not
  a paper ingest. Worth doing deliberately, not from this list.
- **Product documentation** - Dataverse, Azure AI Search, and the ERP data-entity documentation that
  arrived with the staged modules. Vendor reference for a specific platform, off this brain's domain.
- **Community artifacts** - AutoGPT, BabyAGI. Interesting as failure-mode history, no stable text to
  gate.
- **The rest of the CS329A syllabus - checked in full on 2026-08-04, and deliberately left here.**
  [cs329a.stanford.edu](https://cs329a.stanford.edu/) assigns roughly **34 papers across 20
  lectures**, and three were already on this list before the syllabus was read (ReAct, Large Language
  Monkeys, The AI Scientist). Three more are promoted above. **The remaining ~28 are not, and the
  reason is scope rather than quality**: the bulk is math and code RL scaling (STaR, DeepSeekMath,
  DAPO), tree search (LATS, AlphaCode, Search-o1) and inference-time architecture (Archon, Snell), all
  of which change **weights or a search procedure**, where this brain's live interest is the artifact
  layer. **The survey's own finding is what is worth recording: across all 20 lectures and all 34
  papers there is no security material and no MCP material at all** - no threat modelling, no prompt
  injection, no protocol. That confirms from the syllabus what S14 `n11` only suggested from a slide,
  and it is why the security rows at the top of this table are not displaced by anything here.
  **Re-read this bullet before ingesting further CS329A lectures**, because the independence ceiling
  applies to the papers too wherever Mirhoseini is an author (see the Weaver row).

## How a row leaves this file

Ingest it as a normal source (`sources/<YYMMDD_slug>/`), gate it, compound it, then **delete the
row** - the source's `INDEX.md` entry replaces it. A row left here after ingest is exactly the
bookkeeping drift the dream pass exists to catch.
