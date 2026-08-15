# Stage: `/dream` - the reconciliation pass

> Global coherence over `brain/` itself, into `brain/dreams/`. **Triggered by the user, never automatic.**
>
> **This file is the contract for this stage.** It was extracted verbatim from `AGENTS.md`
> on 2026-08-15 ([ADR-0027](../brain/decisions/0027-stage-specs-leave-the-contract.md)) so that a
> spec needed once a fortnight stops occupying every session's context window. **`AGENTS.md`
> remains the root contract** and this inherits every global rule in it; where the two
> disagree, `AGENTS.md` wins and this file is the bug.

## Dreaming on request (the reconciliation pass)

> **Why this exists, and it is the kit taking its own medicine.** Ingest writes to `brain/` **while
> doing something else** - finishing a source. That write is locally optimal and globally
> unexamined: it merges into the topic note in front of it and never asks whether a claim it just
> added contradicts one promoted three sources ago. This is exactly the diagnosis
> [`brain/topics/memory.md`](../brain/topics/memory.md) records from S6 and S7 - **memory updated
> in a locally optimal way that is not globally optimal, producing duplication and fragmentation**
> (claim 59, `n10`) - pointed at this repo. `validate.py` does not catch it: it checks **form**, and
> this is **drift**. A green validator means the shape is right, not that the thinking is.

**Dreaming is the global reconciliation pass over `brain/` itself.** Not an ingest, not a research
pass, not lint. It reads across every topic note, `claims.md`, `glossary.md` and `INDEX.md` and asks
one question: **is what this brain believes still coherent with itself?**

**Trigger (never automatic).** The user says **"dream"**, or invokes the harness command. Adopt
**architect + fact-checker** - the architect owns merge/split/status calls, the fact-checker owns
claim verdicts.

> **It must never run as part of an ingest, and this is a design rule, not a preference.** An agent
> finishing a source is holding two objectives - land this source, and keep the brain coherent - and
> it will trade the second against the first silently, because the first is the one with a visible
> finish line (claim 59). Curation gets its own invocation and its own objective, or it gets a token
> effort. **Same reason the generator and the evaluator are separate processes (claim 34).**

### What a pass looks for

| Class | The question | Typical finding |
|---|---|---|
| **Contradiction** | Do two claims disagree? Did a later source overturn an earlier one? | Keep both, cite both, flag the conflict - never silently pick a winner |
| **Duplication / fragmentation** | Is one idea stated in two topic notes, or as two claims? | Merge and de-duplicate; the contract already says *don't stack* |
| **Stale confidence** | Is a claim still `emerging` after a second source corroborated it? Is a `needs-check` now resolved? | Promote or demote the confidence, citing what changed |
| **Stale status** | Is a topic `emerging` on two corroborating sources, or `seed` with one? | Advance it, and record an ADR if the call is a judgement |
| **Orphans** | A claim no topic note references; a topic claim with no `claims.md` row; a source feeding nothing | Wire it up or drop it - an unreferenced claim is invisible |
| **Closed open questions** | Did a later source answer an "Open questions" bullet nobody struck through? | Strike it through with the date and the closing source |
| **Superseded framing** | Was a synthesis section written when the brain knew less? | Rewrite it. **This has already happened once** - `memory.md` kept "this topic has zero measurements" after the charts were recovered, and needed a fix commit |
| **Drift from source** | Does the citation still support the claim as written? | Correct the claim, not the citation |

### How a pass runs

1. **Read the whole brain first.** `INDEX.md`, every `brain/topics/*.md`, `claims.md`, `glossary.md`,
   `brain/decisions/`, **every prior note in `brain/dreams/`**, and the tail of `log.md`. **Do not
   sample.** The entire value of being out of band is that you can afford to read everything, which
   is the one thing an ingest cannot.

   > **Prior dream notes are not history, they are the backlog.** Each one ends in "Proposed, not
   > applied (needs a human call)" and "Notes for the next pass" - proposals with their reasoning,
   > written by the only pass that reads everything. **Omitting them from this list meant a pass
   > wrote proposals that the next pass was never told to read**, which is the same defect the stage
   > exists to catch, aimed at the stage itself. Re-reading them is also what makes a fourth backlog
   > file unnecessary: the mechanism already exists and only lacked a guaranteed reader.
2. **Collect findings before changing anything**, each naming the files and claim IDs involved.
3. **Write the pass note** to `brain/dreams/<NNNN>-<YYMMDD>.md`, numbered in order. One note per
   pass, permanent. **Ephemeral output not captured into a kit file did not happen.**
4. **Apply the changes** in the same pass - this is a reconciliation, not a report - then run
   `python3 validate.py` and show the `git diff`.
5. **Propose, do not impose.** Anything that changes what the brain *believes* (dropping a claim,
   splitting a topic, reversing a confidence) goes in the note as a **proposal with its reasoning**
   and is applied only if it is a clear defect. **When it is a judgement call, ask.** The human
   adopts; `git revert` is the undo.

> **Findings are the point, including "nothing found".** A pass that surfaces no drift is a real
> result and gets its note - it is evidence the compounding is holding. **Do not manufacture
> findings to justify the pass.**

> **What dreaming must not do:** re-litigate the gate. Whether a node was corroborated is settled in
> the source's `nodes.md` by the fact-checker at ingest time. Dreaming reconciles what was
> **promoted**; it does not re-open source-local judgements, and it never edits a `nodes.md`.
