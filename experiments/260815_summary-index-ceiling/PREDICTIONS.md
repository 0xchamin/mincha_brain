# Predictions - the summary-index ceiling

> **Written and committed before any code in this directory existed.** `git log` is the proof. See
> [ADR-0024](../../brain/decisions/0024-experiments-layer.md) for why that ordering is mandatory
> rather than stylistic.

## What is under test, and why it is this

[R4](../../sources/260731_llm-wiki/context/01_where-the-index-file-ceiling-actually-sits.md) researched
S8's `n10` - *"works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and
avoids the need for embedding-based RAG infrastructure"* - and found the ceiling **measured twice
independently and in agreement**, and then found that **neither measurement tested the design `n10`
describes.** LOFT places the whole corpus in context. The LlamaIndex benchmark greps raw documents.
**Neither reads a maintained index of one-line summaries and uses it to choose which pages to open**,
which is `n10`'s actual mechanism and attends to roughly 2k tokens where those studies made the model
attend to 1.5M.

R4 therefore relocated the question rather than closing it: the failure mode of a summary-index design
is probably **not attention** but **whether a one-line summary discriminates well enough to pick the
right page.** That is a property of the index, it is measurable, and R4 recorded that the experiment
appears not to exist and is cheap.

**This experiment measures index discriminability as the item count grows.**

## What it is measured on, which is the reason it is cheap

**This brain is a live instance of the design**, and it carries mechanical ground truth. Two arms:

| Arm | Items (the "index") | Ground truth |
|---|---|---|
| **A** | the **26 source rows of `INDEX.md`** - the real, running summary index | a query drawn from a source's `LEARNING.md` belongs to that source |
| **B** | the **~470 gated nodes** across all `nodes.md` files, each carrying a bolded one-line crux | a `LEARNING.md` sentence citing `` `n7` `` belongs to node `n7` of that source |

Arm B exists because **Arm A cannot answer the question**: 26 items is an order of magnitude below
`n10`'s ~100, and no sweep over 26 items tells you where anything breaks. Arm B reaches **N = 478**,
comfortably past the claimed ceiling, using a corpus of genuine one-line summaries with 2,126
available citations to draw queries from.

## Scoring - deterministic, no model, per rule 2

Ranking is **lexical only**: tokenise, drop stopwords, score candidates by TF-IDF cosine against the
query, rank. No embeddings, no model, no judgement. For each query the true item is placed among
`N-1` distractors sampled from the same pool; `Recall@1`, `Recall@3` and `MRR` are recorded, averaged
over repeated distractor draws. `N` sweeps by doubling.

> **This measures a floor, not the system.** A real agent reading an index can match semantically
> where a lexical scorer cannot, and can also be distracted in ways a scorer is not. **What transfers
> is the shape of the curve** - how discriminability responds to N - not the absolute level. Stated
> here rather than discovered later.

## Honesty about case strength

- **Arm A is a demonstration.** N is capped at 26 by the corpus. Its outcome is close to
  predetermined and it is included because it is the live instance, not because it tests anything.
- **Arm B is a genuine test.** I do not know the shape of the curve, and P3 and P4 below are the
  predictions I would most expect to get wrong.

## The known confound, predicted rather than excused

**Queries and index entries were written by the same agents from the same material**, so they share
distinctive vocabulary that an independent query would not. **This inflates every absolute number**,
and it makes this a **best-case** measurement: whatever discriminability decay appears here is a
*lower bound* on the decay a real, differently-worded query would suffer. If it degrades even under
favourable conditions, that is a strong result. If it does not degrade, that is weak evidence,
because the confound points that way.

---

## P1 - Arm A, full index rows, N = 26

**Recall@1 between 60% and 85%.**

*Falsified by:* anything below 50%, which would mean this brain's own index cannot find its own
sources and the harness is more likely wrong than the index.

## P2 - Arm A, summary richness ablation

**Ordering `full > oneline > title` on Recall@1** (near-certain, a demonstration), with the **full
minus oneline gap between 10 and 25 points** at N = 26.

*Falsified by:* a gap under 5 points, which would say the extra 200 words in a row buy nothing and
this brain's annotated rows are waste; or `oneline` beating `full`, which would say the extra words
actively distract a lexical matcher.

## P3 - Arm B, the shape of the decay **(the one that matters)**

**Recall@1 decays smoothly and approximately log-linearly in N - a roughly constant loss per doubling
- with no knee.**

*Falsified by:* any adjacent doubling whose drop exceeds **twice the median per-doubling drop**. That
would be a scale-specific breakdown, and would mean "~100 sources" names a real threshold rather than
a point on a smooth curve.

**Why this is the prediction worth making.** `n10`, R4 and claim 213 all use the word *ceiling*, which
implies a knee. **I predict there is no knee**, and that what actually happens at ~100 is that cost
and latency dominate while quality is still declining gently - which is exactly what the LlamaIndex
crossover showed and nobody framed that way. If I am right, "the ceiling" is a **budget decision, not
a capability limit**, and claim 213 should be sharpened to say so.

## P4 - Arm B, does summary richness buy scale or only accuracy?

**The gap between rich and one-line summaries stays roughly constant as N grows** - richness shifts
the curve down without changing its slope.

*Falsified by:* the gap at N >= 256 being **more than double** the gap at N <= 16.

**This is the actionable one.** If the gap is constant, richer summaries are a fixed accuracy
purchase and the index scales the same either way. **If the gap widens, then summary richness buys
scalability**, and every knowledge base built on one-line summaries has a lower ceiling than one built
on paragraphs - which would be a direct, practical correction to `n10`'s design and to this brain's
own `INDEX.md`.

## P5 - Arm B at `n10`'s claimed scale

**At N = 100, one-line-summary Recall@1 lands between 25% and 55%.**

*Falsified by:* falling outside that band. Deliberately wide because I have no basis for a tighter
one, and a band this wide is weak - noted as a criticism of the prediction, not a hedge to hide behind.

---

## What this experiment cannot establish

- **It is not evidence about S8.** Per ADR-0024 an experiment tests a mechanism and **never
  corroborates the source that suggested it**. `n10` stays `needs-check` whatever happens here, and
  no claim about Karpathy's system may move.
- **It is not evidence about agents.** A lexical scorer is not an LLM reading an index. It bounds the
  **information available in the summary**, which is the half R4 identified as untested.
- **n = 1 corpus.** One knowledge base, in one domain, written by one pipeline. A curve measured here
  is this corpus's curve.
