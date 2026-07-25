# ADR 0004: Add `validate.py` as the type checker for the prose contract

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260725 |
| Deciders | chamin |

## Context

Brain is a convention, not an application (`prd.md` §0): the pipeline, the corroboration gate and
the file schema live as English in `AGENTS.md`, and the agent is the runtime. The upside is that new
capabilities ship as paragraphs - ADR-0002 and ADR-0003 both added real behaviour without a line of
code. The structural weakness is the mirror of that: **prose has no compiler.** Nothing enforces the
rules but the agent's willingness to follow them, and drift does not fail loudly - it accumulates.

`prd.md` §10 already anticipates **volume** pressure (grep slowing down at a few hundred sources,
answered by a vector index). It does not anticipate **consistency** pressure, which arrives far
earlier. Evidence from a single working day at **two** sources:

- `brain/log.md` was left non-chronological **twice** and hand-corrected both times.
- ADR-0002 nearly stayed marked "untested" after it had been tested.
- The `claims.md` footnote asserting "the only cross-source claim" went stale within one pass.
- INDEX integrity and frame-citation pruning were verified by throwaway shell loops written on the
  spot, then discarded - violating the kit's own rule that ephemeral output not captured into a kit
  file did not happen.

Every one of those is a *form* error a machine can catch.

## Decision

Add **`validate.py` at the repo root**, run before the `git diff` at the end of any compound,
research or close-the-loop pass, and in CI on every push and PR.

Constraints that shaped it:

- **Stdlib only.** CI must not need a venv to check a folder of Markdown. The kit's `requirements.txt`
  exists for the *ingest* pipeline; validation must not inherit it.
- **It enforces the contract, it does not define it.** If a check and `AGENTS.md` disagree,
  `AGENTS.md` wins and the check is the bug. Stated in both files so the precedence never drifts.
- **Form, never judgement.** It cannot decide whether a claim is corroborated, whether a frame earns
  its place, whether a topic should split, or whether a source is genuinely independent. Encoding
  those would be worse than useless - it would launder judgement as a green check. They stay with the
  fact-checker and architect personas.
- **Mutation-tested.** Each of the ten checks was verified against a deliberately corrupted copy of
  the repo. A validator that passes because it is broken is worse than no validator, and the first
  run of that test caught a bad *test* (see Consequences).

## Alternatives considered

- **Do nothing; rely on the agent following `AGENTS.md`** - rejected on the evidence above. The
  contract was violated repeatedly in the same session that wrote it, by an agent that had it in
  context the whole time.
- **A pre-commit hook instead of CI** - rejected as the primary mechanism: hooks are per-clone and
  easy to bypass, and the repo is headed for a public release where contributors' PRs must be
  checked. A hook is a fine optional addition later.
- **Encode judgement too** (score corroboration, flag "weak" claims) - firmly rejected. A green check
  on a judgement call would manufacture false confidence, which is the exact failure mode
  `prd.md`'s confidence semantics were written to prevent.
- **Wait for more sources before building it** - rejected: the failures are already happening, and
  every check written now is one that stops being re-derived ad hoc each session.

## Consequences

- **Easier:** drift fails loudly instead of accumulating. Contributors get the conventions enforced
  automatically rather than by review. Three checks that were being hand-written each session are now
  captured.
- **Harder:** one more thing to keep honest. A check that disagrees with `AGENTS.md` must be fixed,
  not worked around, or the contract quietly becomes whatever the script happens to accept.
- **Known limitation, deliberately accepted:** the `log.md` check compares dates only, so it **cannot**
  catch an entry misordered *within a single day* - which is precisely the mistake that occurred twice.
  Per-entry timestamps would catch it and are not worth the ceremony. Documented in the code and in
  `AGENTS.md` rather than left as a silent gap.
- **Found on the first run:** three genuine defects, all in the validator rather than the repo - two
  false positives from following the git-ignored `AGENTS.md` symlinks, and one from counting raw
  substring matches instead of table rows. Worth recording because it is the expected shape of early
  validator bugs: a checker's first job is to be more correct than the thing it checks.
- **Revisit when:** checks start needing repo state a regex cannot see (e.g. verifying a citation's
  timestamp against a transcript), or if false positives make people add ignore-comments - the point
  at which a validator starts costing more trust than it earns.
