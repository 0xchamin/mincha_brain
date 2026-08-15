# Stage: `/verify` - verifying one source

> The source-layer evaluator the corroboration gate lacks. **Triggered by the user, never automatic.**
>
> **This file is the contract for this stage.** It was extracted verbatim from `AGENTS.md`
> on 2026-08-15 ([ADR-0027](../brain/decisions/0027-stage-specs-leave-the-contract.md)) so that a
> spec needed once a fortnight stops occupying every session's context window. **`AGENTS.md`
> remains the root contract** and this inherits every global rule in it; where the two
> disagree, `AGENTS.md` wins and this file is the bug.

## Verifying one source on request (`/verify`)

> **Why this exists.** This kit violates its own best-supported eval claim. **Claim 34: do not let
> the producer grade its own work** - an agent asked to judge its own output confidently praises it,
> and that is not promptable-away, because the generator has no independent vantage point on itself.
> Yet the agent that distils a source is also the agent that runs its corroboration gate, decides
> whether a node is really two-leg, and writes the prose built on those decisions. **One invocation,
> two objectives - finish the source, and gate it honestly - which is claim 59's untunable trade.**
>
> `validate.py` does not close this: it checks **form**. Whether a cited node actually supports the
> sentence citing it is a **reading judgement**, and the one time that failed in this repo it took a
> human asking "where did that come from" to find it.
>
> Note the asymmetry this fixes. The **`brain/` layer has a reconciler** - the dream pass, decoupled,
> one objective. The **`sources/<id>/` layer had none**: the gate fired once, at ingest, by the agent
> doing the ingest, and was never revisited.

**Trigger (never automatic).** The user says **"verify \<source>"** or runs `/verify`. Adopt
**fact-checker**, alone - this stage has exactly one objective and composing it with `curator` would
reintroduce the conflict it exists to remove.

> **The stage's own coverage is the thing to watch, and it went badly wrong once already.** `/verify`
> shipped on 2026-08-03. Over the next twelve days **fourteen sources were ingested and one was
> verified.** The corpus nearly doubled and the evaluator ran once. **Nothing was broken** - the stage
> works, and the design decision that it never fires automatically is correct, because an agent that
> has held a source's argument for an hour has no independent vantage point on it. What was missing is
> that **the coverage number appeared nowhere**, so nobody could notice it was 1 in 26 without running
> `ls sources/*/verify.md`. That is this kit reproducing the defect it records against S7 (`d4`) and
> S26 (`n13`): **the load-bearing step with no mechanism behind it.**
>
> **`python3 validate.py` now prints `/verify` coverage on every run** (see "Validating the
> contract"). It is informational and **never fails the run**, because *how many sources should be
> verified* is a judgement and encoding a threshold would launder judgement as a green check.
> **100% is the wrong target** - verification costs a separate session and most sources will never
> earn one. **The right reading is comparative**: a number that has not moved while ten sources landed
> means the stage has quietly stopped existing, and the sources worth spending it on are the ones
> whose claims are **most reused** (check `brain/claims.md`) rather than the most recent.

**Scope: one source's distilled layer against its own gated evidence.** Read that source's
`nodes.md`, `LEARNING.md`, `SOURCE.md` **and its `visuals/` frames** - and nothing else. Do not read
the topic notes - what was *promoted* is the dream pass's business, and mixing the two gives this
stage two objectives again.

> **The frames are in the read list because check 6 cannot run without them**
> ([ADR-0016](../brain/decisions/0016-verify-reads-the-frames.md)). The stage's first run found this
> against itself: it asked whether a caption matches the image while being forbidden from opening the
> image. **The set needs no selecting** - `validate.py` already pins `visuals/` to exactly the frames
> that source's own `LEARNING.md` cites. It is a bounded cost: **median 4 frames per source, maximum
> 15**, and zero on a source whose visual leg was skipped.

> **This is the one pass that MAY re-open the gate**, and the only one. Dreaming is explicitly
> forbidden from re-opening source-local judgements or editing a `nodes.md` (see below); that rule
> stands, because this stage exists to do it instead.

### What it checks, exactly

**Stating this precisely is not pedantry, it is the point.** This brain's sharpest criticism of S7 is
`d4`: the vendor says dreaming produces "a **verified**, better organized snapshot" and never says
what verification means, who performs it, or what happens on failure - **the load-bearing step with
no mechanism behind it.** A stage of this kit called `/verify` that did the same thing would be
reproducing the defect it was built from.

| # | The question | Failure it catches |
|---|---|---|
| 1 | Does each cited node **actually support the sentence citing it**? | Citation drift - the `claim 33` class, at source level |
| 2 | Is anything the prose presents as settled gated `single-leg` or `needs-check` in `nodes.md`? | **Label drift between the gate and the prose** |
| 3 | Is anything outside a `Background, supplied` block **uncited**? | The scaffolding rule leaking - supplied context laundered as evidence |
| 4 | Are weak-evidence labels **at the point of use**, or deferred to the end? | Caveats parked where nobody reading the claim will meet them |
| 5 | Does "What to distrust" carry the **gate note's** trust facts, or a softer version? | The source-level caveat quietly improving in translation |
| 6 | Does a kept frame's `what it teaches` **match what the frame shows**? | A frame embedded rather than taught |

**Nothing else.** Not prose quality, not structure, not whether the ramp works - those are the
curator's and the human's. **A stage that grades everything grades nothing**, and its verdicts stop
being trustworthy the moment they include taste.

**Check 6 runs by default, and a skip is recorded rather than discovered.** Record it in the pass
entry's `Frames` field: `checked (N)` / `n/a (visual leg skipped)` / `skipped (user)`. This is
deliberately the same shape as `SOURCE.md`'s `Visual leg` row - the kit already knows how to make an
expensive visual step optional without letting the omission go quiet, and a second mechanism for the
same problem would be machinery.

> **Why it is not opt-in, having been proposed as opt-in and withdrawn.** A default-off check is a
> check that never runs, because **nobody asks about frames they have not seen.** And note who wrote
> the caption: the `what it teaches` line comes from the ingesting **curator** - same agent, same
> session, same argument - after which **nobody ever looks at that image and that sentence together
> again.** `validate.py` proves a frame is *cited*; only a reader with the image open can tell
> whether the citation is *true*. Dropping the check would leave the visual half of every source with
> no independent reader at all, which is the exact asymmetry this stage exists to close (claim 34).

### Verdicts, and what happens on failure

Each finding is one of:

| Verdict | Meaning | Action |
|---|---|---|
| `defect` | Unambiguous - the citation does not support the sentence, an uncited claim sits outside scaffolding | **Fix it in the same pass** |
| `judgement` | Arguable - a label that may be too strong, a caveat that may belong closer | **Propose with reasoning and ask.** The human adopts |
| `gate-reopen` | The evidence itself looks mis-gated | **Never fix silently.** Record it, state the reasoning, ask. Re-gating changes what the brain believes |

**Output goes to `sources/<id>/verify.md`** - one file per source, **appended** per pass with a date,
never rewritten. It is a log, not an index: the point is that a later reader can see what was checked
and when. Each entry opens with a field table carrying **`Read`**, **`Frames`**, **`Independence`**
and **`Findings`**. **Ephemeral output not captured into a kit file did not happen.**

Then run `python3 validate.py` and show the `git diff`, as with every other stage.

> **What this stage cannot do.** It reads a source against *itself*, so it inherits the gate's own
> ceiling: **two legs agreeing proves internal consistency, never truth** (Global rules). It cannot
> tell you a source is wrong about the world - only that this brain has represented it honestly.
> External evidence is deep research's job; cross-source coherence is dreaming's.

> **Do not run it on a source you just wrote in the same session.** The whole point is an independent
> vantage point, and an agent that has been holding the source's argument for an hour does not have
> one. **A different session, or at minimum a different invocation, is the mechanism** - not a
> promise to be objective.
