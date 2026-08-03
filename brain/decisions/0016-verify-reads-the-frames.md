# ADR 0016: `/verify` reads the frames, and a skipped check 6 is recorded not discovered

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260803 |
| Deciders | chamin |

## Context

The `/verify` stage shipped on 2026-08-03 with six checks. **On its first run anywhere it found a
defect in itself.**

Check 6 asks whether a kept frame's `what it teaches` matches **what the frame actually shows** - the
failure it catches is *a frame embedded rather than taught*. Answering that requires looking at the
image. But the stage's scope rule was **"read that source's `nodes.md`, `LEARNING.md` and `SOURCE.md`,
and nothing else"** - three text files and no images.

**So the stage as written could not run one of its own six checks.** That is not a small
inconsistency for this stage in particular: `/verify` exists because this brain's sharpest criticism
of S7 is `d4` - a vendor calling a step "verified" while never saying what verification means or who
performs it. A stage of this kit reproducing that defect is the one outcome it was built to avoid.

The finding was logged, undecided, in
[`sources/260802_gcp-multi-tenant-agentic-ai/verify.md`](../../sources/260802_gcp-multi-tenant-agentic-ai/verify.md)
with three options, none free.

**The cost was measured before deciding**, because the original objection to reading images was a
guess about expense. Across the 12 sources: **81 kept frames, median 4 per source, maximum 15**
(`260725_oauth2-oidc-plain-english`). Two sources have 1. Sources whose visual leg was skipped have
none at all.

## Decision

**Check 6 runs by default, and the read list gains the frames that `LEARNING.md` cites** - so the
stage reads three text files **plus that source's own `visuals/`**, and nothing else. The
anti-scope-creep rule is unchanged in force: still no topic notes, still no other sources.

**The frame set is already bounded and already pinned.** `validate.py` enforces that every file in
`visuals/` is cited by its **own** `LEARNING.md`, so "the frames it cites" and "the contents of
`visuals/`" are the same set by construction. There is nothing to select and no judgement to make
about which frames to look at.

**A skipped check 6 is recorded, not discovered.** Every `verify.md` entry carries a `Frames` field:

| Value | When |
|---|---|
| `checked (N)` | the default |
| `n/a (visual leg skipped)` | the source has no frames - **free, and the common case will grow** |
| `skipped (user)` | the human asked for text-only |

**This is deliberately the same shape as `SOURCE.md`'s `Visual leg` row**, and reusing that pattern
is most of the argument for this option. The kit already knows how to make an expensive visual step
optional without letting the omission go silent; inventing a second mechanism for the same problem
would be the machinery this repo keeps declining to build.

Not a one-way door. Reverting means deleting a row from a log format and a clause from a read list.

## Alternatives considered

- **Opt-in behind an explicit flag** (the default pass stays three text files). Cheaper per pass and
  it was the initial recommendation, **withdrawn once the cost was measured**. The objection that
  killed it: the visual half would then be checked only when someone remembers to ask, and **nobody
  asks about frames they have not seen.** A default-off check is a check that never runs.
- **Run check 6 only when a caption "looks unusually load-bearing"** (option 3 as originally logged).
  **Partly circular.** You cannot tell from the text which captions are *wrong* - that is exactly
  what needs the image. You can only tell which are *consequential*. It works as risk-weighting and
  not at all as error-detection, and it sites the trigger in the one place that carries no signal.
- **Drop check 6 and go to five checks.** The smallest possible contract, and honest in the sense
  that matters here: it would not claim a mechanism it lacks. Rejected because of **who wrote the
  caption**. The `what it teaches` line is written by the ingesting curator - the same agent, in the
  same session, holding the same argument - and after ingest **nobody ever looks at that image and
  that sentence together again.** Dropping the check leaves the visual half of every source with no
  independent reader, which is the precise asymmetry this stage was created to close (claim 34).
  `validate.py` proves a frame is *cited*; it cannot prove the citation is *true*.

## Consequences

**Easier.** The stage can now run all six of its checks, so its verdicts mean what they say. The
visual leg gets an independent reader for the first time - it previously had exactly one reviewer
ever, at ingest, with a conflict of interest.

**Harder.** A `/verify` pass on a frame-heavy source now costs up to 15 image reads on top of three
text files. That is the real price and it is not hidden. The asymmetry that justifies paying it is
[ADR-0006](0006-static-probe-is-advisory.md)'s: **a spent `view` costs one call, and a wrong caption
is durable** - it survives into `LEARNING.md`, into the topic notes that quote it, and onto the phone
reader that `build_site.py` publishes.

**Revisit if** a frame-heavy source makes a pass genuinely unaffordable, or if several passes in a
row return check 6 clean. The second is the more likely retirement trigger and it is the right one -
[claim 33](../claims.md) says ablation is the test for whether a bet has expired, and this check is a
bet that curators mis-caption. **It has zero recorded instances so far**, which is a reason to run it
and watch, not a reason to skip it.

**Follow-ups applied in the same pass:** `AGENTS.md` § "Verifying one source on request" (scope, the
check table's note, the `Frames` field), `.claude/commands/verify.md`, a resolution entry appended to
S12's `verify.md`, and `BUILD.md` regenerated.
