# Grounding and retrieval: the mechanics under RAG

> **Foundation - supplied background, uncited by construction.** Not evidence about any source, and
> never promoted to `brain/claims.md`. See [`README.md`](README.md).

**Covers:** why models hallucinate and why retrieval addresses the cause rather than the symptom;
the five-stage grounding pipeline; dense versus sparse retrieval; chunking and embeddings; why
position inside the window matters; compression; structured versus prose evidence; retrieval as a
decision rather than a step.

**Skip this if** you have built a retrieval pipeline and can say why a reranker exists.

**Why this file exists.** [`brain/topics/rag.md`](../brain/topics/rag.md) is `emerging` and states
its own hole plainly: **chunking, embeddings, vector stores, hybrid search and grounding evals are
at zero.** Its two sources argue *against* retrieval (S8) and retrieve over tool schemas rather than
prose (S10). **So this brain discusses RAG without holding its mechanics.** This is the missing
background, and it is background only - the primaries are on
[`brain/reading-list.md`](../brain/reading-list.md).

**Provenance and status.** Distilled from a personally commissioned research module (2026-07-11),
agent-generated synthesis, roughly **T5**. Definitional content only.

---

## 1. Why models hallucinate, and what grounding actually changes

A model interpolates over its training distribution. Asked for something outside it - a recent
event, a private record, an exact figure - it produces text that is statistically plausible and
anchored to nothing. **The output is not a lie or a bug; it is the same operation that produces
correct answers, run where the distribution has no support.**

The move that retrieval makes is to **change the task**. Instead of asking the model to *recall* a
fact from weights, put the fact in the window and ask it to *read*. Comprehension over supplied text
is something models are heavily trained for; precise recall from parameters is not.

This is why "just fine-tune on your data" is a different and weaker answer. Fine-tuning moves facts
into weights, where they are compressed, unattributable and expensive to update. Retrieval keeps
them **outside**, where they are exact, citable and editable.

> 💡 **The cost is that grounding is now a budget problem.** You cannot inject everything, so you
> must select, rank, compress and position within a finite window. That is not a prompting trick -
> it is an information-selection problem, and it is where all the difficulty moved.

## 2. The pipeline

Five stages. Most systems that "do RAG" implement one and a half of them.

| Stage | What it does | What breaks if you skip it |
|---|---|---|
| **Retrieve** | Fetch candidate chunks for the query, dense or sparse | Nothing to ground on |
| **Rerank** | Reorder candidates by relevance *to the query*, typically with a cross-encoder | Top-k is ordered by embedding proximity, which is not the same as usefulness |
| **Compress** | Prune or summarise chunks to fit the budget | Evidence crowds out instructions, history and reasoning space |
| **Position** | Place the strongest evidence where the model actually attends | Correct evidence present and effectively unread |
| **Assemble** | Order instructions, tools, memory, evidence and history into one input | The layers fight each other, and nobody can say why quality moved |

**The distinction between retrieve and rerank is the one most often collapsed.** A bi-encoder embeds
query and document *separately*, so similarity is computed between two summaries that never met.
A cross-encoder reads the pair *together* and scores the relation. It is far more accurate and far
too slow to run over a corpus - which is exactly why the pipeline has two stages: **retrieve cheaply
and broadly, then rescore a shortlist expensively.**

## 3. Dense, sparse, and why hybrid is the default

**Sparse retrieval** (BM25 and relatives) matches on terms. It is exact, interpretable, needs no
training, and fails when the query and document use different words for the same thing.

**Dense retrieval** embeds text into a vector space where proximity approximates semantic
similarity, then searches by cosine distance. It handles paraphrase, and it fails on the things
lexical matching is best at: rare identifiers, product codes, names, negation.

**Their failure modes are close to complementary, which is the entire argument for hybrid search.**
Run both, fuse the rankings (reciprocal rank fusion is the usual method because it needs no score
calibration between the two systems), then rerank the union.

> 💡 **An embedding is a lossy compression chosen by a model you did not train.** Two texts are
> "similar" according to that model's objective, which may not be your notion of relevance. This is
> why an embedding index that performs badly is often not fixable by swapping vector stores.

**Chunking** is the decision nobody wants to own and everybody regrets. Chunks that are too small
lose the context that made the passage meaningful; too large and a single chunk dilutes its own
embedding across several topics, so it matches everything weakly and nothing strongly. The practical
consequence: **chunk boundaries are a retrieval-quality parameter, not a preprocessing detail.**

## 4. Position inside the window is load-bearing

Attention over a long context is not uniform. Material at the **beginning and end** is used
substantially better than material in the **middle** - the "lost in the middle" effect.

**The practical rule that follows: put the strongest evidence first or last, and the user's actual
question at the very end.** Never assume that because a fact is in the window it has been read.

> **The measurement is not mine to state.** The U-shaped curve was measured by Liu et al. (Stanford,
> 2023, [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)) and that paper is on the reading list
> at `high` priority precisely because this brain holds the *effect* on practitioner assertion alone
> (claim 22, context rot). Treat the shape above as background and the numbers as ungated.

## 5. Compression, and what it costs

Once evidence exceeds the budget, something must go. Three options, in increasing risk:

1. **Truncate** - cheap, and drops whatever happened to be last.
2. **Summarise** - an LLM rewrites the chunk. Preserves meaning, spends a model call, and **removes
   exactly the anomalies a reader needed to see**.
3. **Token-level pruning** - a small model scores tokens by information content and drops the low
   ones (the LLMLingua line of work, Jiang et al., Microsoft, 2023,
   [arXiv:2310.05736](https://arxiv.org/abs/2310.05736)). High ratios, and the output is no longer
   human-readable, so debugging changes character.

**The trade is always the same: compression buys budget and spends the ability to notice something
unexpected.** Which is the right trade depends on whether the pipeline is answering questions or
detecting problems.

## 6. Structured evidence beats prose evidence

Injecting a table, JSON, or a set of triples rather than paragraphs changes what the model has to
do: **extract a value rather than paraphrase a passage.** Extraction has a right answer that is
present verbatim; paraphrase is generation, and generation is where fabrication lives.

The same instinct powers the **cite-then-answer** pattern - require the model to quote the supporting
span before answering. It costs tokens and forces the model to *locate* evidence before committing
to a claim, which is a structurally different operation from recalling one.

## 7. Retrieval as a decision, not a step

The pipeline above retrieves unconditionally. **Sometimes the right number of documents is zero** -
the model already knows, or nothing relevant exists, and injecting weak evidence is worse than
injecting none because it looks authoritative.

**Self-RAG** (Asai et al., UW and IBM, 2023,
[arXiv:2310.11511](https://arxiv.org/abs/2310.11511)) makes this explicit by training the model to
emit reflection tokens: is retrieval needed, is this chunk relevant, is the answer supported by it.
The architectural idea generalises beyond that implementation: **retrieval becomes a decision the
system can get wrong and can be evaluated on**, rather than a fixed stage in a pipeline.

---

## What this file leaves out, and why

| Left out | Why |
|---|---|
| **The skills half of the source module** - registry, lifecycle, governance, progressive disclosure | [`skills.md`](../brain/topics/skills.md) and [`mcp.md`](../brain/topics/mcp.md) hold this ground from **gated** sources (S5, S10). Uncited background restating it would compete with better evidence |
| **Every measured result** - description-quality accuracy drops, compression ratios, structured-vs-prose gains, benchmark numbers | Claims about the world. The papers are on the reading list; the numbers belong to them, gated |
| **Evaluation frameworks and leaderboards** | These are sources to ingest, not fundamentals |
| **Vendor product specifics** | Reference documentation, consulted on demand, and it dates fastest of anything here |

> **What this file does not settle.** `rag.md` stays `emerging`. Reading this does not mean the brain
> holds evidence about retrieval - it means the vocabulary is no longer missing when a real
> retrieval source arrives. **Lewis et al. 2020 is the ingest that would change what the brain
> believes**, and it is on the reading list at `high`.
