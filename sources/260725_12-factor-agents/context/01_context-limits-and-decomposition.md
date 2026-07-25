# Research - external evidence for the 12-factor claims

> Persona: **fact-checker + synthesizer**. See `../../../AGENTS.md` § "Deep research on request".

| Field | Value |
|---|---|
| Pass | 01 |
| Date | 2026-07-25 |
| Targets | n4, n13, n14, n17, n18, n22, n23 + the two open questions in `../LEARNING.md` |
| Budget used | 5 searches / 8 fetches (cap: 8 / 12) - stopped early on two independent agreeing sources |

## Why this pass ran

`../LEARNING.md` closed with two open questions that could not be answered from the source:

1. Does anyone **independent** corroborate the 3-10 step micro-agent claim?
2. Is there any **measurement** for "limiting context beats filling it"?

Both are now answered. The second is answered strongly, with peer-reviewed and multi-model
evidence. The first is answered by a preprint that also **qualifies** a neighbouring claim.

## Findings

| Node | External finding | Verdict | Source (tier, independent?) |
|---|---|---|---|
| n4, n22 | **"Lost in the Middle"**: model performance "is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle" - a U-shaped position curve, reproduced across six model families (GPT-3.5/4, Claude 1.3, LongChat-13B, MPT-30B, Cohere Command). | **supports** | [arXiv 2307.03172](https://arxiv.org/abs/2307.03172), **published in TACL** (T1, independent) |
| n4, n22 | **Chroma "Context Rot"**: 18 models (GPT-4.1, Claude 4, Gemini 2.5, Qwen3), input length isolated as the sole variable. "Model performance varies significantly as input length changes, **even on simple tasks**" like retrieval and text replication. A model with a 200K window can degrade materially by 50K. Degradation is **non-uniform** - distractors compound it, and models scored *better* on shuffled haystacks than coherent ones. | **supports** | [trychroma.com/research/context-rot](https://www.trychroma.com/research/context-rot) (T2 vendor research, independent of S2) |
| n9, n20, n22 | **Anthropic** frames context as a finite **"attention budget"**: the transformer requires "every token to attend to every other token", giving "n² pairwise relationships for n tokens", so "as its context length increases, a model's ability to capture these pairwise relationships gets stretched thin". Prescription: find "the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." | **supports** | [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (T2, independent of S2 - but see independence note) |
| n23 | Anthropic names **compaction** (summarising and reinitialising the context window) as one of three core long-task techniques, alongside structured note-taking and sub-agent architectures. S2's "clear pending errors, summarise don't dump" is the same move applied to errors. | **supports** | Anthropic, ibid. (T2) |
| n17 | **Anthropic**: "find the simplest solution possible, and only increasing complexity when needed"; "optimizing single LLM calls with retrieval and in-context examples is usually enough"; agents "often trade latency and cost for better task performance". Same conclusion as S2's 90-second bash script, reached independently. | **supports** | [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (T2, independent) |
| n18 | **Near-verbatim independent match.** Anthropic on frameworks: they "often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug". S2: you end up "seven layers deep in a call stack trying to reverse engineer how does this prompt get built". Two unrelated parties describing the identical failure. | **supports** | Anthropic, ibid. (T2, independent) |
| n13 | **The measurement S2 never provided.** "Beyond pass@1" names **task decomposition the highest-leverage reliability intervention**, quantified across 10 open-source models: **DeepSeek V3 +13.1 pp**, **Qwen3 30B +41.5 pp** reliability gain from decomposing a long task into shorter segments and restarting the agent at each boundary. Mechanism: "decomposing into n independent short segments improves expected completion from pVL toward pS". | **supports** | [arXiv 2603.29231](https://arxiv.org/abs/2603.29231) (T3 **preprint**, independent) |
| n13 | Anthropic independently lists **sub-agent architectures** (delegating focused tasks to specialised agents) as a core technique for extended tasks; and reports the most successful implementations "weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns." | **supports** | Anthropic, both articles (T2, independent) |
| n13 | **Qualifier.** The same decomposition paper finds "the memory scaffold **never improves** long-horizon reliability, and hurts 6 of 10 models" (Kimi K2.5 -0.14 GDS, Mistral 24B -0.13), concluding "naive episodic memory augmentation should not be adopted as a default reliability intervention" - plain ReAct beat it. **Decomposition helps; bolting memory onto a long loop does not.** S2 says nothing about memory either way. | **refines** | arXiv 2603.29231 (T3 preprint) |
| n6, n8 | **Cross-domain: this is Event Sourcing.** S2's `Thread: events: List[Event]` + `thread_to_prompt` replay + "serialize w/ stateID, reload, append, resume" is the pattern Martin Fowler named in **2005**: an append-only event log, current state derived by **replaying** the stream ("rehydration"), with the "Complete Rebuild" property - discard all state and reconstruct purely by re-processing the log. S2 never names it. | **refines** | [Azure Architecture Center, Event Sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) (T1 docs) + Fowler 2005 (T4) |
| n14 | "100 tools, 20 steps, easy" - no external evidence found either way at this budget. | **no-evidence** | - |

## Synthesis

**The context claim is the best-evidenced thing in the source, and S2 undersells it.** Horthy asserts
that limiting tokens beats filling the window; three independent lines of evidence now support it,
and they are stronger than his framing. He argues from "you'll get tighter results"; the literature
shows degradation is **non-uniform and adversarial** - it depends on where in the window the
information sits (Lost in the Middle), on distractors, and on structure, and it shows up at a
quarter of the advertised window. "Use less context" is not a preference. It is a measured property
of the architecture, with a mechanical explanation (n² attention, RoPE decay).

**The micro-agent claim now has a number attached, and it is large.** S2 offers 3-10 steps as
practitioner intuition. "Beyond pass@1" measures the same intervention at **+13 to +41 percentage
points** of reliability. That is not a marginal engineering preference; on some models it is the
difference between a system that works and one that does not.

**But the same paper draws a boundary S2 does not see.** Decomposition helps; *memory scaffolding*
hurts 6 of 10 models. The naive reading of "own your context window" - accumulate a rich thread and
feed it back - is precisely the intervention that measured worse than plain ReAct. The defensible
version of S2's claim is **decompose and keep each segment short**, not **remember more**. Anything
in this brain that drifts toward "give the agent better memory" should be checked against this.

**The convergence with Anthropic is the strongest independence signal in the pass.** Two parties with
no shared interest - a startup founder distilling builder interviews, and a frontier lab writing from
its own deployments - independently reached: start simple, don't reach for an agent by default,
beware framework abstraction that hides the prompt, prefer small composable pieces, and spend the
token budget deliberately. When rivals in different positions agree on the *mechanism*, that is worth
more than either one's confidence.

## Cross-domain framing

**Factors 3, 5, 6 and 12 are Event Sourcing wearing new clothes.** Model the thread as an append-only
list of typed events; derive the prompt by replaying the log; serialise and rehydrate by ID; keep the
processor stateless. Fowler named this in 2005 for enterprise systems, and the mature discipline
carries consequences S2 never mentions: **replay determinism** (the same log must reproduce the same
state - true for an event list, *false* the moment a non-deterministic LLM call is treated as part of
the log), **snapshotting** (don't replay from zero forever - the direct analogue of compaction), and
**event versioning** (what happens to a stored thread when your `Event` schema changes?).

This is the payoff of the cross-domain hop: the older discipline has already found the sharp edges of
this design. **Naming the pattern gives you twenty years of its failure modes for free** - and none of
them appear in the talk.

> 💡 **Event sourcing** - persisting state as an append-only sequence of events rather than as
> current values, and reconstructing state by replaying them. Named by Martin Fowler in 2005.

## Confidence assessment

Assumptions made without asking, per the contract:

- **Anthropic is treated as independent of S2** - different organisation, no shared commercial
  interest with HumanLayer. But it is **T2 and positioned**: Anthropic sells model access, and
  "spend your context budget carefully" is not a neutral position for a company billing per token.
  It is independent of *Horthy*, not disinterested about *the field*. Weighted as support, not proof.
- **"Beyond pass@1" is a T3 preprint**, not peer-reviewed. Its numbers are quoted from the paper's
  own text, verified against the full HTML after the abstract alone did not contain them - the
  initial search summary asserted the figures before I could confirm them, and they were only kept
  after direct verification. Treat as indicative, not settled.
- **The decomposition finding tests coding/web/tool benchmarks** (SWE-bench, WebArena, tau-bench,
  OdysseyBench), not Horthy's deploy-bot scenario. The transfer is plausible, not demonstrated.
- **"Lost in the Middle" (2023) predates the current model generation.** Its position effect is
  reproduced by the newer Chroma work, so the direction holds, but the specific magnitudes are dated.
- **Not attempted at this budget:** independent evidence for n11 (humans as tool calls), n16
  (stateless reducer), n5's four-part decomposition. n14 searched, nothing found.

## Fed back into

- `../nodes.md` - external corroboration table extended (`en2`..`en5`); n13, n22 confidences raised;
  n13 qualifier recorded.
- `../../../brain/claims.md` - external citations appended to claims 11, 14, 17, 22, 23; new claim on
  the memory-scaffold boundary.
- `../../../brain/topics/context-engineering.md` - "no measurements anywhere" open question **closed**.
- `../../../brain/topics/agents.md` - decomposition measurement + memory-scaffold caveat added.
- `../../../brain/glossary.md` - context rot, attention budget, event sourcing, lost in the middle.
