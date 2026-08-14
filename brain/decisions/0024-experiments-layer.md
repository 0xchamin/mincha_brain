# ADR 0024: An `experiments/` layer - first-party observation gets a home and a ceiling

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260815 |
| Deciders | chamin |
| Persona | architect |

## Context

Twenty-four sources in, **this brain has never executed anything**. It records the gap about itself
four times, in `INDEX.md`, in its own words: *"this brain ran none of the code (no GPU)"* for S13,
*"repo not cloned"* for S16 and S20, *"the cheapest un-taken second leg of the five ingested"* for
S22. Every claim rests on somebody reporting on their own system.

S24 sharpened that into something specific. Its gate found `d3`: the article opens by constructing a
deterministic task **specifically so the architecture can be traced through it**, and never shows the
trace running. And `n24`: the author states a verification method - checked against source,
documentation and regression tests - that the article gives no way to check. So S24's twenty-two
`corroborated` nodes are one author's prose against the same author's diagrams, and nothing in them
was witnessed by anyone.

Its `LEARNING.md` then records two open questions that are **answerable by running something**, which
is a category the kit has no stage for:

- *"Nobody has reported what actually happens when a second gateway process runs against one
  `state.db`"* - and whether SQLite's serialisation incidentally supplies the semantic guarantee that
  the in-memory guard does not is simply unknown.
- *"Is 'transcript order is not side-effect order' ever actually observed to bite?"* - which the note
  itself calls **the single most testable claim in the source**.

Neither is answerable by deep research, because nobody has published on them. Both are answerable in
an afternoon with SQLite and no model at all.

**The problem is that there is nowhere to put the answer.** `sources/<id>/` is `validate.py`'s
namespace and means "an artifact someone else made". `foundations/` is background that is uncited by
construction and explicitly produces no claims. `reports/` is synthesis cited back to nodes that
already exist. **First-party observation - "this brain ran something and saw X" - fits none of them**,
and filing it in any of the three would blur the line the whole kit exists to protect.

## Decision

**Create `experiments/<YYMMDD_slug>/` as a fourth layer**, with its evidential status declared in its
own README exactly as `foundations/` declares its own.

**The ceiling is the load-bearing half of this decision.** An experiment on a reimplementation tests
whether a **mechanism** is real and reachable. It says nothing whatever about the system that
inspired it. Concretely, and this is the rule that must not erode: **no experiment may raise
confidence in a claim about a source.** If this brain writes its own runtime and watches tool results
reorder, that is evidence about concurrency and not evidence about Hermes. Where an experiment bears
on a claim, it bears on the claim's general mechanism, and the claim row says which.

**Three disciplines are mandatory**, because the obvious failure mode is a harness built to
demonstrate what its author already believes, which produces green checks that prove nothing:

1. **`PREDICTIONS.md` is committed before any code runs**, in its own commit. `git log` is the proof.
   This is claim 34 applied to the one agent that would otherwise grade its own work.
2. **Every assertion is a deterministic function** over files and database rows. Never a judgement,
   never a model. This is claim 164 - an evaluator the subject can influence is unsound.
3. **Nondeterministic behaviour is reported as a distribution over N runs**, never as pass or fail.
   This is claims 114 and 177 - an accept rule with no noise floor banks randomness as signal.

**Misses are recorded, never quietly corrected.** `RESULTS.md` carries predictions that were wrong,
on the same principle that `nodes.md` records dropped candidates and `brain/conjectures.md` records
discarded conjectures.

## Consequences

**What it buys.** Two open questions become answerable rather than permanently parked. More
generally, the kit gains a second way to resolve a `/conjecture`: today a conjecture can only be
settled by `/research` and external evidence, and some could be settled by running them. That is a
real capability the kit was missing and did not know it was missing.

**What it costs.** A fourth layer is a fourth thing to keep coherent, and the taxonomy has been
deliberately conservative - [ADR-0014](0014-no-topic-for-organisational-context.md) and
[ADR-0023](0023-no-topic-for-agent-runtime-operations.md) both declined new homes on thinner grounds
than this. The distinguishing fact is that those were *topics*, which are a taxonomy over existing
evidence, while this is a **new evidence class** with no existing home at all.

**The risk worth naming.** Running code feels more authoritative than reading a paper, and it is not.
An experiment answers exactly the question it was built to ask, on exactly the machine it ran on, and
a green result on a 250-line reimplementation is weaker evidence than a peer-reviewed measurement of
a real system. **The ceiling above is what keeps that honest, and the first sign of erosion will be
an experiment cited as though it settled something about a source.**

**What is deliberately not built.** No validator checks. Whether a prediction was honest, whether a
harness tests what it claims, and whether a result generalises are all judgement, and encoding them
would launder judgement as a green check - the line [ADR-0004](0004-validator-as-type-checker.md)
draws. The one mechanical guarantee here is `git log` proving `PREDICTIONS.md` predates the run, and
that is a property of the commit history rather than of a checker.

## Related

- [ADR-0004](0004-validator-as-type-checker.md) - form is code, judgement is prose.
- [ADR-0002](0002-deep-research-stage.md) - the other stage that reaches outside the source for
  evidence. Deep research reaches for **someone else's** evidence; this produces **our own**.
- [ADR-0023](0023-no-topic-for-agent-runtime-operations.md) - the S24 material this experiment tests.
