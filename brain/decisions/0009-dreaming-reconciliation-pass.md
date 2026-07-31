# ADR 0009: Add a dreaming pass - the kit applying its own sources to itself

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260731 |
| Deciders | chamin |

## Context

Ingesting the memory pair (S6 OpenAI, S7 Anthropic) produced a diagnosis that turned out to describe
**this repo**, not just the products the sources were selling.

Both sources independently found that memory written **during** work is *locally optimal and
globally suboptimal*: each individual write is defensible, the aggregate duplicates, fragments and
drifts, and nothing ever reconciles it because the writer was busy doing something else
([`../topics/memory.md`](../topics/memory.md), S7 `n10`; claim 59).

That is exactly how `brain/` is written. **Ingest updates topic notes while finishing a source** -
it merges into the note in front of it and never asks whether the claim it just added contradicts
one promoted three sources ago.

Two things already exist and neither covers it:

- **`validate.py` checks form, not drift.** Broken links, missing INDEX rows, uncited frames. It
  says so itself: *"a green validator means the shape is right, not that the thinking is."* A topic
  note can be perfectly well-formed and quietly wrong.
- **Deep research (ADR-0002) looks outward.** It tests a source's claims against external evidence.
  It never asks whether the brain is coherent with itself.

**The gap is not hypothetical - it has already produced a defect.** `memory.md` shipped carrying
"this topic has no measurements at all", which became false when S6's eval charts were recovered
hours later. It survived one full ingest and needed a dedicated `fix:` commit
(`51dcb23`). Nothing in the kit was looking for it, because nothing in the kit reads across the
brain asking whether what it says is still true.

A third source sharpened the framing. Karpathy's *LLM Wiki* gist describes this same pattern
(raw sources / maintained wiki / schema) and names three operations: **ingest, query, lint**. The
kit has all three. **What it does not have is what S6 and S7 both argue is the load-bearing one** -
a maintenance pass that runs on its own clock rather than inside the ingest.

> ⚠️ **The last sentence of that paragraph is wrong, and is corrected by
> [ADR-0010](0010-lint-is-the-dream-pass.md).** The gist was cited here from a review, not an ingest.
> Once ingested as S8 (2026-07-31), §Lint turns out to *be* the out-of-band maintenance pass - four of
> its six defect classes are verbatim members of the eight below. The error was matching the word
> "lint" to `validate.py`. **The decision below stands and is better supported than it appears here**;
> only this reading of the third source changes. Left in place rather than edited: an ADR records what
> was decided and why *at the time*.

## Decision

**Add a `dream` stage: a global reconciliation pass over `brain/` itself, triggered on request,
writing a permanent note to `brain/dreams/<NNNN>-<YYMMDD>.md`.**

Contract in `AGENTS.md` § "Dreaming on request"; Claude Code wrapper in `.claude/commands/dream.md`;
note structure in `brain/dreams/README.md`. Persona: **architect + fact-checker**.

It works eight classes: contradiction, duplication, stale confidence, stale status, orphans, closed
open questions, superseded framing, drift from source.

**The design follows what the sources actually established, point for point:**

| S6 / S7 finding | How the stage implements it |
|---|---|
| Curation must be **decoupled** from the work loop (claim 59 - objective conflict) | Never runs as part of an ingest. Separate invocation, own objective. |
| Out of band means it can **afford to be expensive** (S7 `n12`) | Reads the *whole* brain, no sampling. That is the one thing an ingest cannot do. |
| Output is a **reviewable diff** agents "can choose to adopt" (S7 `n11`, `n21`) | Applies clear defects; **proposes** judgement calls and asks. `git revert` is the undo. |
| The pass must be **recorded**, not ephemeral | One permanent note per pass, numbered. |

**The decoupling is the whole point and is worth stating as a rule rather than a preference.** An
agent finishing a source holds two objectives - land this source, keep the brain coherent - and it
will trade the second against the first silently, because only the first has a visible finish line.
This is the same argument that separates the generator from the evaluator (claim 33), and the same
one S7 gives for putting dreaming outside the agent loop.

## Alternatives considered

- **Extend `validate.py` to catch drift.** Rejected, and this is the important rejection. It would
  cross the line ADR-0004 drew and the kit repeats everywhere: **form is code, judgement is prose.**
  Whether two claims contradict, whether a topic should split, whether a framing is superseded - none
  of that is decidable by a checker, and encoding a guess would **launder judgement as a green
  check**, which is worse than not checking. The validator stays a type checker.
- **Run reconciliation at the end of every compound.** Rejected on the sources' own finding - it
  recreates the objective conflict the stage exists to remove, and would be done badly and
  invisibly. It would also make every ingest dramatically more expensive for a payoff that is
  usually nil, since most single ingests introduce no global drift.
- **Run it on a schedule (cron / `/loop`).** Rejected **for now**, deliberately. S7's dreaming is
  scheduled because it serves a fleet of agents generating transcripts continuously; this brain gains
  a source every few days and is written by a human-triggered agent. A nightly pass would mostly
  produce "nothing found" notes and train the reader to ignore them. **Revisit if ingest rate rises.**
- **Wait for more sources before building it.** Rejected on evidence: the drift defect already
  happened once at 7 sources, and the failure is silent, so waiting means accumulating unfound
  errors rather than gathering data about whether they occur.

## Consequences

- **Easier:** contradictions and stale statuses have somewhere to be found and something that looks
  for them. `INDEX.md` status rows, claim confidences and topic notes now have a maintenance owner
  that is not "whoever happens to be ingesting".
- **The kit now practises what it records.** `memory.md` argues that write-once memory decays into
  confident wrongness and that the fix is a maintainer on a separate clock. Until now the kit made
  that argument while being a write-once memory itself.
- **Harder:** a new stage is new surface. The pass can be run badly - manufacturing findings to look
  productive, or re-litigating gate decisions that belong to a source's `nodes.md`. Both are
  explicitly forbidden in the contract, and "nothing found" is defined as a valid result to remove
  the incentive.
- **Cost is real and deliberately unbudgeted.** Unlike deep research (≤ 8 searches, ≤ 12 fetches),
  dreaming has no budget cap, because its value comes precisely from reading everything. It is
  local reads only - no network - so the cost is context, not time or money.
- **Revisit when:** the brain outgrows a single pass (the point at which "read everything" stops
  fitting, which is the same signal that a topic note needs splitting); or ingest rate rises enough
  that scheduling beats on-request; or two consecutive passes find nothing, which would suggest the
  trigger is too eager rather than that the kit is clean.
- **Follow-up edits:** `AGENTS.md` § "Dreaming on request"; `.claude/commands/dream.md`;
  `brain/dreams/README.md`; a "Deeper layers" pointer in the root [`INDEX.md`](../../INDEX.md).

> **Not yet run.** This ADR records the decision to add the stage. The first pass will be
> `brain/dreams/0001-*.md`, and it should be expected to find real drift - seven sources have been
> compounded with no reconciliation, and one defect is already known to have slipped through.
