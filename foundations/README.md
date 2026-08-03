# Foundations - supplied background, uncited by construction

> **Read this before using anything in this folder.**

These files hold **background a reader needs and that no ingested source taught**. They are the
repo-level home for the `> **Background, supplied.**` blocks that appear inside every
`LEARNING.md` - written once and kept, instead of re-derived by whichever agent happens to be
writing.

**They are not evidence.** Nothing here is gated, nothing here produces knowledge nodes, and
**nothing here may be promoted to [`brain/claims.md`](../brain/claims.md)**. A foundation is
background you are supplying so the rest reads; it is not a finding.

> **Why the line is drawn this hard.** The entire value of `brain/` is that every claim carries a
> citation and a gate verdict. Material that arrives already synthesised - especially
> agent-generated research notes - is roughly **T5** on this kit's scale, and the T5 rule is *"use
> for discovery; cite the primary source they point to, not them."* Filing something here does not
> upgrade it. It puts it where its status is **declared** rather than assumed.

## Required header

Every file in this folder starts with a status line `validate.py` checks for:

```markdown
> **Foundation - supplied background, uncited by construction.** Not evidence about any source, and
> never promoted to `brain/claims.md`. See [`README.md`](README.md).
```

## How to use one

- **A `LEARNING.md` may cite a foundation as background, never as evidence** - the same way a
  `Background, supplied` block is treated today. The sentence leaning on it says so.
- **Keep any citations the material already carries.** A foundation pointing at an arXiv paper or a
  vendor engineering post is far more useful than one that does not, and the pointer is what makes a
  later proper ingest cheap. Those citations do **not** change its status.
- **If a foundation turns out to be load-bearing for something the brain wants to assert, ingest the
  primary it points at.** The claim comes from the gated source, not from here.
- **Promote reusable terms** to [`brain/glossary.md`](../brain/glossary.md), which is the
  one-or-two-sentence version of the same material.

## Bringing material in

Drop markdown into git-ignored [`staging/`](../staging/README.md) first. There is no `_inputs/` -
`staging/` already exists for this, and the rule is the same one it was written for: **material
becomes part of the kit when it is filed, not when it is copied in.**

Then read it and make the call:

| What it is | Where it goes |
|---|---|
| Teaching a fundamental the reader needs | **`foundations/<slug>.md`**, with the status header |
| Making claims about the world, with citations | **Not here.** The *primary it cites* is what to ingest |
| Both | Split it. Neither half improves by travelling with the other |

## Contents

| File | Covers | Notable citations | Gap it backfills |
|---|---|---|---|
| [`tool-use-and-mcp.md`](tool-use-and-mcp.md) | Why a model needs tools; function calling; MCP primitives, transports and handshake; the reason-act-observe loop; orchestrator plus sub-agents; intent to execution; the agent-computer interface | ReAct (Yao 2022), Reflexion, Tree of Thoughts, MRKL, Toolformer, Anthropic *Building Effective Agents* | `mcp.md` holds nothing on primitives, transports or the handshake |
| [`memory-taxonomy-and-lifecycle.md`](memory-taxonomy-and-lifecycle.md) | Statelessness; episodic / semantic / procedural and where the distinction comes from; the capture-distil-store-retrieve lifecycle; why memory retrieval is harder than document retrieval; tiering | Tulving (1972/85), CoALA, *Generative Agents*, MemGPT | `memory.md` and `skills.md` use "procedural memory" as a borrowed label with no primary |
| [`grounding-and-retrieval.md`](grounding-and-retrieval.md) | Why grounding changes the task from recall to reading; retrieve / rerank / compress / position / assemble; dense vs sparse vs hybrid; chunking; position effects; retrieval as a decision | Lewis et al. (2020), Liu et al. *Lost in the Middle*, LLMLingua, Self-RAG | `rag.md` records chunking, embeddings, vector stores and hybrid search as **at zero** |
| [`agent-threat-model.md`](agent-threat-model.md) | Why LLM reliability differs from software reliability; direct and indirect prompt injection and why neither is patchable at the model layer; memory poisoning; excessive agency; the operator/user/environment trust hierarchy; audit logging | Greshake et al. (2023), Zou et al. (GCG), Constitutional AI | `agent-security.md` is `emerging` on three sources of which **only one studies threats** |

> **Where the rest of that material went.** Each staged module also carried prescriptive "best
> practices", "common pitfalls", exercises, and a bibliography. **Only the definitional half becomes
> a foundation.** Prescriptions are claims about the world and do not belong in an uncited file; the
> bibliography becomes ingest candidates in [`brain/reading-list.md`](../brain/reading-list.md). Each
> foundation ends with a table stating exactly what was dropped, so the omission is visible rather
> than silent.
