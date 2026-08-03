# Agent memory: the taxonomy, the lifecycle, and the retrieval problem

> **Foundation - supplied background, uncited by construction.** Not evidence about any source, and
> never promoted to `brain/claims.md`. See [`README.md`](README.md).

**Covers:** why statelessness forces external memory; the episodic / semantic / procedural
distinction and where it comes from; the four-stage memory lifecycle; why retrieval over memory is
harder than retrieval over documents; the memory-as-virtual-memory framing.

**Skip this if** you can already say what distinguishes episodic from semantic memory and why a
recency-weighted retrieval score exists.

**Why this file and not the topic note.** [`brain/topics/memory.md`](../brain/topics/memory.md) is
`established` and covers what three sources *taught*: staleness as a structural property, decoupled
curation, revision over expiry, memory as a tool-accessible file system. **None of them taught the
vocabulary they were using.** This supplies that, and nothing more.

**Provenance and status.** Distilled from a personally commissioned research module (2026-07-11),
which is agent-generated synthesis and therefore roughly **T5**. Definitional content only - see
"What this file leaves out".

---

## 1. Why memory is external, and why a bigger window does not fix it

A transformer has no state between calls. At inference it sees exactly two things: **parametric
knowledge** frozen into weights at training time, and the **context window** it was handed, which is
discarded afterwards.

So the context window is **the only pathway by which information reaches the model during
inference**. That is not an implementation limit to route around; it is what inference *is*. It
follows that every memory system, however it is described, is ultimately answering one question:
**what goes in the window this time?**

The obvious objection is to make the window bigger. It mitigates and does not solve, for four
separate reasons that do not share a fix:

1. **Attention cost is quadratic** in sequence length for full attention. Doubling the window
   roughly quadruples the compute.
2. **Position matters.** Models attend poorly to material buried mid-context - the "lost in the
   middle" effect (Liu et al., Stanford, 2023,
   [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)).
3. **Agent output is unbounded.** An agent running for weeks produces arbitrarily more text than any
   finite window holds. This is a growth-rate argument, so no constant factor answers it.
4. **Sessions have boundaries.** A new call starts empty regardless of how large the window is.

> 💡 **The useful framing is virtual memory.** Keep everything in durable external storage, inject
> only the relevant subset at inference. As in an operating system, **the scarce resource is not
> storage capacity but bandwidth between tiers** - which is why the interesting design questions are
> all about what gets promoted into the window and when, never about how much you can keep.

## 2. The taxonomy, and where it actually comes from

The episodic / semantic split is not an AI invention. It is **Endel Tulving's** distinction from
cognitive psychology (1972, elaborated 1985), imported wholesale.

| | **Episodic** | **Semantic** |
|---|---|---|
| Binding | To a specific time and place | Decontextualised |
| Source | Personal experience | Generalised knowledge |
| Volatility | Higher - events go stale | Lower - facts persist |
| Formation | Captured from traces | Distilled from episodes, or ingested directly |
| Example | "On 2026-07-10 a migration failed because the column type was wrong" | "This project prefers TypeScript over Python" |

**Procedural memory** is the third member of the family: knowing *how*, rather than knowing *that*
or knowing *when*. It is the category an agent skill occupies, which is why
[`skills.md`](../brain/topics/skills.md) uses the label.

**The distinction earns its keep because it predicts different failure modes.** An agent with only
episodic memory has a diary: it can tell you what happened and cannot tell you what is true. An
agent with only semantic memory has a style guide: it knows preferences and cannot learn from a
specific mistake. **Semantic memory is what learning produces; episodic memory is its raw material.**

The taxonomy is stated formally for agents in **CoALA** (Sumers et al., Princeton, 2023,
[arXiv:2309.02427](https://arxiv.org/abs/2309.02427)), which separates memory by *function*
(factual, experiential, working) from *storage medium* (token-level, parametric, latent). The second
axis is the one people forget: **the same fact can live in weights, in a retrievable document, or in
the window, and those are three different systems with three different update costs.**

## 3. The lifecycle

Four stages, and naming them is what stops a memory system from silently becoming a log file.

| Stage | Input | Output | Mechanism |
|---|---|---|---|
| **Capture** | Raw interaction - tool calls, messages, observations | Event record | Logging hooks, trace collectors |
| **Distil** | Event record | Compact unit plus metadata | Summarisation, importance scoring, entity extraction |
| **Store** | Memory unit | Indexed durable record | Vector store, key-value, graph, files |
| **Retrieve** | Current query and context | Ranked relevant memories | Hybrid search over several signals |

**Distillation is the stage that is skipped, and skipping it is what turns memory into logging.**
Raw traces are verbose (mostly scaffolding), addressable only by exact similarity ("we discussed
authentication on turn 47" is unretrievable unless you already know it was turn 47), and expensive
to re-read. Distillation converts them into **compact, semantically addressable units**: *"the user
confirmed they prefer TypeScript."* Small, retrievable, immediately usable.

**Reflection is distillation applied to its own output.** In *Generative Agents* (Park et al.,
Stanford, 2023, [arXiv:2304.03442](https://arxiv.org/abs/2304.03442)), when the accumulated
importance of recent memories crosses a threshold, the agent is prompted to synthesise abstract
insights from them, which are stored as new higher-importance memories. That gives two levels: raw
observation, then reflected insight. **The threshold matters more than the prompt** - it is what
makes synthesis periodic rather than constant, and periodic-and-out-of-band is the shape this brain
already recognises from elsewhere.

## 4. Why retrieval over memory is harder than retrieval over documents

Given a store of N items and a query, returning the right k requires satisfying four objectives at
once:

- **Semantic match** - "what I ate" must reach a memory tagged "lunch".
- **Temporal recency** - recent memories are usually, not always, more relevant.
- **Importance** - a repeated preference outweighs a one-off remark.
- **Scope isolation** - one user's memories must never surface in another's context.

**No single ranking function optimises all four**, which is why production systems combine signals.
*Generative Agents* makes the combination explicit as a weighted sum over normalised components:

```
score(m) = a * recency(m) + b * importance(m) + c * relevance(m, query)
```

The formula is less interesting than what it concedes: **the weights are hand-set, and nobody
knows the right values.** That is the honest state of the art, and it is worth holding onto when a
system presents its retrieval as solved.

> 💡 **This is categorically not RAG, though it uses the same machinery.** RAG retrieves from a
> static corpus someone else wrote. Memory retrieval reads **the agent's own accumulated
> experience**, which the agent also writes. A store you both read and write has failure modes a
> read-only corpus cannot have: it can poison itself, it can compound its own errors, and it drifts
> as the world moves under it.

## 5. Tiering, made concrete

**MemGPT** (Packer et al., Berkeley, 2023, [arXiv:2310.08560](https://arxiv.org/abs/2310.08560))
takes the virtual-memory analogy literally: the context window is main memory, external storage is
disk, and **the agent itself calls the paging functions** (`core_memory_replace`,
`archival_memory_search`) to move information between tiers.

The design choice worth extracting is *who decides*. Three options exist, and they are not
equivalent:

| Grounding pattern | Trade-off |
|---|---|
| **Prepend to the system prompt** | Reliable, and spends tokens on it whether relevant or not |
| **Dynamic retrieval, top-k at query time** | Token-efficient, and now retrieval quality is load-bearing |
| **Core plus archival tiers** | Both, at the cost of deciding what is core |
| **Memory as a tool the model calls** | Most flexible, and the model now spends reasoning on memory management |

**Handing paging to the model is a real architectural commitment, not an implementation detail.** It
makes memory management legible and debuggable, and it spends the model's attention on bookkeeping
that a deterministic policy could have done for free.

---

## What this file leaves out, and why

| Left out | Why |
|---|---|
| **Best practices and failure modes** | Claims about the world, not fundamentals. `memory.md` holds this ground already, from gated sources |
| **Measured results** - the memory-tool benchmark improvements, A-MEM's and Mem0's numbers | **Deliberately excluded.** These are exactly the measurements `memory.md` records as missing, and an uncited file is the wrong place for them to appear. **The papers are on [`brain/reading-list.md`](../brain/reading-list.md) at `high` priority** for that reason |
| **Memory poisoning and privacy attacks** | Real, on the reading list, and they belong to `agent-security.md` as **gated** evidence. Background here would understate them |
| **Exercises and framework catalogues** | Not kit material |

> **What this file does not settle.** `memory.md`'s headline caveat stands: **three sources converged
> on the design and none published an experiment**, and nobody here has measured whether maintained
> memory helps an agent. Nothing above changes that. This file supplies vocabulary, not evidence.
