# Deep research 01 - where the index-file ceiling actually sits

> Persona: **fact-checker + synthesizer**. External evidence for gated nodes. **This note is not
> `LEARNING.md` material** - it answers "what does the field think?", not "what did this source
> teach?", and the two must stay separable (`AGENTS.md`).

| Field | Value |
|---|---|
| Date | 2026-08-15 |
| Target node | **`n10`** - "This works surprisingly well at moderate scale (**~100 sources, ~hundreds of pages**) and **avoids the need for embedding-based RAG infrastructure**" [S8 gist @ac46de1, §Indexing and logging] |
| Why this node | The source's **one falsifiable, quantified claim**, gated `needs-check` with nothing attached, and named the best research target by `nodes.md`, `LEARNING.md`, `rag.md` and the `/verify` pass |
| Verdict | **`refines`** - the ceiling is real and independently measured, and **"~100 sources" is the wrong unit at roughly the right magnitude, for reasons that are luck rather than insight** |
| Budget used | **4 searches, 3 fetches** (of ≤8 / ≤12). Stopped early: two independent sources agree on the ceiling and the fourth search closed the framing question |
| Brain read first | `INDEX.md`, `rag.md` (full), `memory.md`, `claims.md` tail. `rag.md` already records that S10's "you don't need embeddings" result and `n10` **only superficially agree** - different designs, three orders of magnitude apart in scale. That reading survives this pass and is sharpened by F1 |

## The short version

**The ceiling `n10` asserts is real, has been measured twice independently, and the measurements
agree with each other.** They do not measure what `n10` measures. Both denominate the limit in
**tokens the navigation must range over**, and `n10` denominates it in **sources** - which tracks the
same quantity only if your sources are all about the size of an academic paper. They were, in the one
benchmark that tested this regime, which is why the number looks right.

**And the design `n10` actually describes has still not been tested by anyone**, because it has a
compression step neither measured alternative has. That is a genuine `no-evidence` sitting inside a
`refines`, and it is the useful part of this pass.

## Findings

### F1 - the ceiling is measured, and it is measured in tokens (T3)

**[Can Long-Context Language Models Subsume Retrieval, RAG, SQL, and More?](https://arxiv.org/abs/2406.13121)**
(Lee et al., **Google DeepMind** + affiliates, 19 authors, arXiv:2406.13121, June 2024; the LOFT
benchmark). **T3 - preprint, not peer-reviewed, and label it as such.**

Six tasks, 35 datasets, three corpus sizes: **32k, 128k and 1M tokens**. Models: Gemini 1.5 Pro,
GPT-4o, Claude 3 Opus, against specialised retrievers (Gecko, CLIP, PaLM 2 DE).

**The result that bears on `n10`:** long-context models **match** RAG pipelines at **128k** and
**drop at 1M**. The mechanism is stated and is the part worth carrying - *"performance drops as the
gold documents of the test queries are moved towards the end of the corpus, suggesting reduced
attention in later sections."* The failure is **positional**, not capacity: the model is not refusing
the corpus, it is failing to attend to the far end of it.

**Verdict: `refines`.** It establishes that a no-retrieval-infrastructure approach has a real,
measured ceiling and gives its magnitude in tokens. **It does not test an index file** - LOFT places
the whole corpus in context, which is a different design from navigating a catalog.

### F2 - an independent benchmark crossed over at ~100 documents (T2, conflicted)

**[Did filesystem tools kill vector search?](https://www.llamaindex.ai/blog/did-filesystem-tools-kill-vector-search)**
(LlamaIndex, 2026). **T2 vendor engineering post, and the conflict runs *toward* the RAG result** -
LlamaIndex sells RAG framework tooling, and the post asks whether filesystem tools kill the category
it sells. Weigh accordingly; the direction of the bias is the one that would inflate the RAG side.

Agentic file search (Gemini 3 Flash with `read_file`, `grep_file_content`, `parse_file`) against
hybrid RAG (OpenAI dense embeddings + BM25 via FastEmbed, Reciprocal Rank Fusion). Corpora of
**5, 100 and 1,000 arXiv papers** of 22-52 pages each.

| Scale | Filesystem tools | RAG |
|---|---|---|
| **5 papers** | correctness **8.4**, relevance **9.6**, 11.17s | correctness 6.4, relevance 8.0, **7.36s** |
| **100 papers** | slower, slightly lower | **faster, higher**, relevance similar |
| **1,000 papers** | substantially slower | **substantially faster**, slightly higher |

**Two things here, and the second is the one people quote wrongly.** At small scale the
no-embeddings approach **wins on quality and loses on latency** - it is 2 points better on
correctness and 1.6 on relevance, and 52% slower. **The crossover is around 100 documents**, and what
flips there is primarily **speed**, with quality converging rather than collapsing.

**Verdict: `refines`.** The number in `n10` survives contact with the one benchmark that tested that
exact regime. What it marks is not what `n10` says - not "works well up to ~100, then stops working"
but "**is better up to a point, then becomes the expensive way to get the same answer**".

> **The sample is tiny and this is the load-bearing caveat: five questions per scale.** Three scales,
> five questions each, one model, one judge. That is an existence demonstration, not a measurement of
> a threshold, and nobody should quote "100 documents" from it as a constant.

### F3 - the strongest practitioner evidence is for the direction, and it is badly non-independent (T2/T5)

**Anthropic removed the vector database from Claude Code (May 2025)** and replaced it with `Glob`,
`Grep` and `Read`. Boris Cherny, its creator, is quoted as saying agentic search *"outperformed
everything. By a lot."* The reasons given are staleness, security, privacy and reliability, plus the
disappearance of an index to keep in sync.

**Tier and independence, both bad, both worth stating precisely.** The **primary** is a Latent Space
podcast appearance (May 2025); everything reachable in writing is **T4/T5 secondary** restating it,
and the T5 rule says cite the primary rather than the aggregator - **which I could not fetch, so this
finding is recorded as reported and not as read.** Beyond tier: Anthropic is a vendor describing its
own product, **and Claude Code is the harness this brain is running in**, which is about as
conflicted as a source can be for this particular reader.

**And the corpus is wrong for the question.** Code has symbols, imports, call graphs and exact
identifiers, so `grep` is a near-perfect retriever for it in a way it is not for prose. `n10` is a
claim about **documents**.

**Verdict: `supports` the design direction, and contributes nothing to the ceiling.** Recorded mainly
so a future reader does not mistake the industry's enthusiasm for evidence about `n10`.

### F4 - the cross-domain hop: this experiment ran once already, at web scale, and lost

Searching only AI sources will never surface this, so it was searched for deliberately.

**`n10` describes a curated catalog with human-authored one-line summaries, read first to decide where
to go.** That is the **Yahoo Directory** (1994) and **DMOZ** - a hierarchical, human-vetted taxonomy of
the web, browseable and searchable, explicitly the design a library catalog uses. It lost to
crawler-based search engines, and **the recorded reason is precise: by late 1999 Yahoo had roughly
100 editors, the web was doubling every few months, and by 1998 the directory model was visibly
failing.** Human curation bought quality and could not keep pace with corpus growth.

**The constraint that killed it is exactly the constraint S8 names.** `n15` places this pattern as
Vannevar Bush's Memex, *"blocked for eighty years on who does the maintenance"*, and `n13` says LLM
bookkeeping removes it. The Yahoo Directory is that argument's natural experiment, and it ran to
completion.

**Which produces the finding this pass exists for. A curated catalog has two independent ceilings and
the LLM removes exactly one of them.**

| Ceiling | Binds when | Did the LLM remove it? |
|---|---|---|
| **Curation labour** - somebody must summarise and file every source | corpus growth outruns editor capacity | **Yes.** This is `n13`/`n15`, and it is the one S8 argues about |
| **Attention over the catalog** - somebody must read the index and pick correctly | the index outgrows what the reader can attend to | **No.** F1 measures it degrading positionally at 1M tokens |

Yahoo's editors never hit the second ceiling - a human reading a directory page does not suffer
positional decay across a million tokens. **An LLM does.** So the pattern trades a limit that scaled
with *human hours* for one that scales with *context attention*, and `n10` reports a single number as
if there were only ever one ceiling.

## The refinement, stated as a replacement for `n10`

**Two independent measurements land in the same place, and neither of them noticed the other.** F2's
crossover sits at ~100 papers of 22-52 pages. At a conservative ~15k tokens per paper that is roughly
**1.5M tokens** - which is where F1 measures long-context retrieval degrading, having matched RAG at
128k. **Different teams, different methods, different units, same neighbourhood.** That convergence is
this brain's arithmetic and neither source states it, so treat it as a synthesis rather than a
reported result.

The consequence is that **`n10`'s unit is wrong and its magnitude is a coincidence of its author's
corpus.** What binds is the **token volume the navigation must range over**, and "sources" tracks that
only when sources are uniform and paper-sized. The same ~100 becomes badly wrong in both directions -
a corpus of short meeting notes should hold thousands before anything degrades, and a corpus of books
should break in the low tens.

> **The honest replacement: an index-navigated store stops beating retrieval infrastructure when the
> material the navigation ranges over approaches the model's usable attention, which is a token
> budget and not a source count - and what fails first is cost and latency, not correctness.**

## What nobody has tested, which is S8's actual design

**Neither measured alternative implements `n10`.** F1 puts the entire corpus in context. F2 gives an
agent `grep` and `read_file` over raw documents. **`n10` describes a third thing: a maintained
`index.md` of one-line summaries, read first, used to choose which pages to open** (`n9`).

**That difference is a compression step, and it changes the arithmetic by three orders of magnitude.**
An index of 100 one-line summaries is on the order of **2k tokens**, not 1.5M. The agent attends to
the catalog, not the corpus, and only then opens two or three pages. On F1's own mechanism - failure
is positional over the attended span - **that design should push the ceiling far past where either
measurement puts it**, because the attended span is the index rather than the library.

**Nobody has measured this. `no-evidence`, and it is the sharpest thing in this pass**, because it
means the two studies that appear to bound `n10` are bounding its neighbours. It also relocates the
question: the failure mode of a summary-index design is not attention, it is **whether a one-line
summary is a sufficient discriminator** - a *precision* problem in the catalog, which is the failure
Yahoo's editors actually had.

## Confidence assessment

**Assumptions made, stated rather than hidden** (the contract forbids interrupting to ask):

- **"~100 sources" was read as a claim about a prose/document corpus**, matching the gist's own
  examples. If it was meant to include code, F3 is more relevant and the ceiling is higher.
- **The ~15k-tokens-per-paper estimate in the refinement is mine**, from F2's stated 22-52 pages. It
  is an order-of-magnitude figure used to show two results coincide, not a measurement, and the
  convergence argument survives anything in the 8k-25k range.
- **F3's primary was not read.** It is a podcast; every written source is secondary. Recorded as
  reported.

**What would change the verdict:** a benchmark that implements the actual design - a maintained
summary index over N sources, agent reads index first, opens k pages - and sweeps N. That experiment
does not appear to exist and is cheap to run, which makes it the most attractive open item this pass
produces.

**Independence summary.** F1 and F2 are independent of S8 and of each other (Google DeepMind; a RAG
tooling vendor), and their agreement is what carries the verdict. F2's commercial interest points
toward RAG and therefore *against* `n10`, which is the useful direction for a claim we are trying not
to over-credit. **F3 is not independent of this brain's own harness and raises nobody's confidence.**
F4 is historical background, correctly sourced but general-knowledge tier, and it supplies framing
rather than evidence.

**Net effect on `n10`: stays `needs-check`, and is now `needs-check` for a better reason.** It was
unmeasured assertion; it is now a claim whose neighbours are measured, whose unit is wrong, and whose
own mechanism is untested. **Do not cite `n10` as a result. The refined statement above may be cited,
with F1 and F2.**

> Inherits the global rules in `../../AGENTS.md`.
