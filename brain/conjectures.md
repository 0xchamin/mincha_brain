# Brain - conjectures (generated, unproven)

> Persona: **synthesizer** - re-adopt when working this file. Contract:
> [`AGENTS.md`](../AGENTS.md) § "Conjecturing on request".

> **These are not claims and must never be cited as evidence.** A conjecture is a proposition this
> brain's existing claims jointly suggest and **no source states**. It reaches
> [`claims.md`](claims.md) only after a `/research` pass returns `supports` with an **independent**
> external citation - at which point it stops being a conjecture and starts being a claim.
>
> **Every entry names its own falsifier.** That is the rule that separates this file from a
> confabulation engine: if a proposition cannot say what would prove it wrong, it is an observation
> and belongs in a topic note's synthesis or its Open questions, not here.
>
> IDs (`h1`, `h2`, ...) are stable and never renumbered. Status: `open` -> `supported` (promote and
> retire) / `refuted` (**keep** - a killed conjecture is a result) / `no-evidence`.

## Open conjectures

| ID | Conjecture | Combines | What no source states | What would falsify it | Status |
|---|---|---|---|---|---|
| h1 | **Evaluator independence requires a different model family, not merely a different invocation.** A separate evaluator drawn from the same family as the generator retains a substantial share of self-evaluation bias, because the leniency is a shared prior about what good output looks like rather than a property of grading one's own tokens. | claim 34 (do not let the producer grade its own work) + claim 36 (out-of-the-box graders are lenient QA, **biased toward AI-generated output**) | Claim 34 argues for a separate *process*. Claim 36 observes leniency toward AI output generally. **Neither asks whether separation across *families* differs from separation within one** - yet 36's bias would survive 34's fix | Run one eval suite over outputs of known quality with (a) a same-family evaluator and (b) a different-family evaluator. If the leniency gap is negligible, refuted. If (b) is materially harsher on AI-generated output, supported | `open` |
| h2 | **Prompt caching indirectly degrades output quality**, by removing the cost signal that previously constrained resident context. Teams that adopt caching will grow their context, because the thing that made them prune it was the invoice. | S10's caching finding (a price cut, **never** an attention cut) + claim 22 (limiting context beats filling it; degradation is non-uniform and starts early) | S10 says cached tokens still cost attention. Claim 22 says more context degrades quality. **Neither states the behavioural consequence**: that removing the price removes the discipline, so caching makes the quality problem *worse* by making the cost problem better | Measure resident context length in real systems before and after cache adoption. If context does not grow, refuted. Stronger test: hold context fixed and vary only caching - if quality is unchanged, the mechanism is confirmed but the behavioural claim still needs the first measurement | `open` |
| h3 | **The measured harm of episodic memory is attributable to the write being in-band, not to memory itself.** A maintained, out-of-band curated store would not show the same degradation - so claim 24 retires a *write discipline*, not a capability. | claim 24 (naive episodic scaffolding **hurt 6 of 10 models**, measured) + claim 59 (decouple curation from the work loop; one loop optimising two things trades them off silently) | Claim 24 measured append-and-retrieve. Claim 59 argues in-band curation is structurally compromised. **Nobody has connected them**: `memory.md` records the two as measuring different constructs and leaves it there. This names the mechanism that would explain 24's result | Run claim 24's benchmark with an out-of-band curated store in place of the episodic scaffold. If it still hurts 6 of 10, refuted and memory itself is the problem. If harm disappears, supported. **This is `memory.md`'s headline open question stated as something testable** | `open` |
| h4 | **The dominant failure of any model-read metadata field is vocabulary mismatch between author and consumer, and is therefore reducible editorially without changing any algorithm.** The effect size of an editorial pass should exceed that of algorithmic tuning across all three known domains. | claim 93 (metadata becomes a control surface; incumbent human vocabulary is the dominant failure) + claim 88 (retrieval quality is editorial before algorithmic) + claim 43 (a skill's description is its trigger and causes 50%+ of failures) | Claim 93 unifies three domains descriptively. Claim 88 states the editorial-first finding **for tool retrieval only**. **No source claims the editorial lever dominates the algorithmic one as a general property of model-read metadata** | Any domain where rewriting descriptions in consumer vocabulary yields materially *less* improvement than algorithmic tuning refutes it. S10 half-measured this and blended two eval regimes (`n15`); a clean single-regime comparison would settle it | `open` |

## Discarded at generation

Recorded because a pass that keeps only its winners is cherry-picking, and because a discarded
candidate stops being re-proposed next pass.

| Candidate | Why discarded |
|---|---|
| "Contract documents are the load-bearing artifact of LLM knowledge systems" (claims 68 + 93) | **Restates claim 68.** Combining it with 93 adds emphasis, not a proposition - no new assertion, so nothing to falsify |
| "Multi-agent systems need versioned stores" (claim 61 + S12's tenant isolation) | **No falsifier.** As stated it is a design preference; every plausible test collapses into "did a bad thing happen", which is unfalsifiable in the absence of an incident |
| "Ablation generalises to any expiring scaffold" (claims 31 + 44) | **Already a claim.** Claim 44 says the delta is the verdict and claim 31 names the retirement question; the union is what `skills.md` already asserts |
| "Agents will converge on filesystem-shaped interfaces" (claim 60 + S7's memory-as-files bet) | **Not researchable on any horizon.** A prediction about where the field goes, with no evidence that could arrive in time to be useful. Interesting; not a conjecture |

## Passes

| # | Date | Scope | Generated | Discarded | Note |
|---|---|---|---|---|---|
| 1 | 2026-08-03 | whole brain, **partial** | 4 | 4 | First pass, and the stage's first run. **Scope caveat: generated from `claims.md` plus the topic notes read in that session, not a fresh read of all nine.** A full pass should re-run over every topic note's Open questions, which is where the richest unclaimed material sits. Incidentally surfaced a mis-citation (claim 44 cited for the skill-description trigger in four places; the claim is 43), fixed separately |
