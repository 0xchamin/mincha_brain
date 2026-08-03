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
| **high** | **Memory poisoning: two 2026 studies** - [arXiv:2601.05504](https://arxiv.org/abs/2601.05504) (attack and defense) and [arXiv:2606.04329](https://arxiv.org/abs/2606.04329) (systematic study), plus **AgentPoison** [arXiv:2407.12784](https://arxiv.org/abs/2407.12784) | T1/T3 | Attacks specifically against agent memory stores, which is where this brain's two vendor memory sources stop | `agent-security.md` records **shared agent memory as the most actionable open threat** and `memory.md` holds three sources that designed memory without attacking it. This closes a gap both notes name |
| **high** | **Lost in the Middle: How Language Models Use Long Contexts** - Liu et al., Stanford, 2023, [arXiv:2307.03172](https://arxiv.org/abs/2307.03172) | T1 | The U-shaped position curve, measured - primacy and recency bias in a filled window | [`context-engineering.md`](topics/context-engineering.md) holds "context rot" and "limiting context beats filling it" (claim 22) from **practitioner assertion**. This is the measured primary underneath, and would be the topic's first T1 |
| **high** | **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** - Lewis et al., FAIR, NeurIPS 2020, [arXiv:2005.11401](https://arxiv.org/abs/2005.11401) | T1 | The original RAG paper: parametric plus non-parametric memory | [`rag.md`](topics/rag.md) is `emerging` and records that **chunking, embeddings, vector stores, hybrid search and grounding evals are at zero**. Its two sources argue *against* retrieval or retrieve over tool schemas. The topic has no foundational paper at all |
| **high** | **ReAct: Synergizing Reasoning and Acting in Language Models** - Yao et al., ICLR 2023, [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) | T1 | The loop, with an ablation against act-only and reason-only baselines | [`agents.md`](topics/agents.md) is `established` across 8 sources and **has no primary behind the agent loop itself** - S2's "prompt + switch + context + loop" is a practitioner framing. A T1 ablation would be the topic's first measured basis |
| **high** | **A-MEM: Agentic Memory for LLM Agents** - Xu et al., NeurIPS 2025, [arXiv:2502.12110](https://arxiv.org/abs/2502.12110), with **Mem0** [arXiv:2504.19413](https://arxiv.org/abs/2504.19413) as the production counterpart | T1/T3 | Memory architectures that were **measured**, not just designed | [`memory.md`](topics/memory.md)'s headline caveat is that **three sources converged on the design and none published an experiment**, and its open question is whether maintained memory helps an agent at all. This is the most direct answer available |
| medium | **Building Effective Agents** - Anthropic Engineering, Dec 2024, [anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents) | T2 | Origin of the five orchestration patterns and the agent-computer interface framing, both circulating here second-hand | S9 supplied the pattern names from a **competing vendor**. Ingesting the origin would test whether S9 reported them faithfully |
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

## How a row leaves this file

Ingest it as a normal source (`sources/<YYMMDD_slug>/`), gate it, compound it, then **delete the
row** - the source's `INDEX.md` entry replaces it. A row left here after ingest is exactly the
bookkeeping drift the dream pass exists to catch.
