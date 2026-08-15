# `stages/` - the user-triggered stage contracts

**Four passes that fire on request and never automatically**, each with its own spec. They were
extracted verbatim from `AGENTS.md` on 2026-08-15
([ADR-0027](../brain/decisions/0027-stage-specs-leave-the-contract.md)).

| Stage | Trigger | Spec | Writes |
|---|---|---|---|
| **verify** | "verify \<source>" | [`verify.md`](verify.md) | `sources/<id>/verify.md` |
| **research** | "deep research" | [`research.md`](research.md) | `sources/<id>/context/<NN>_<slug>.md` |
| **conjecture** | "conjecture" | [`conjecture.md`](conjecture.md) | `brain/conjectures.md` |
| **dream** | "dream" | [`dream.md`](dream.md) | `brain/dreams/<NNNN>-<YYMMDD>.md` |

## Why these left the root contract

`AGENTS.md` was 1,408 lines and **every one of them was loaded into every session's context**, while
these four specs are needed **once a fortnight between them**. They are 27% of the file, and the cost
of carrying them everywhere is not only tokens: this brain measured in
[X2](../experiments/260815_summary-index-ceiling/RESULTS.md) that discriminability decays with the
volume attended over, and it holds claim 209 - **scope behaviour with a schema file placed in the
thing being managed, discovered when needed, overriding the generic instruction**. The kit adopted
that as a finding while running the opposite design.

**The test that made this safe rather than merely tidy: each of these has a guaranteed loader.** The
`.claude/commands/<stage>.md` wrapper fires and reads its spec, so a rule here is not a rule nobody
loads - which is the one way a split is worse than a long file. **The `LEARNING.md` shape stayed in
`AGENTS.md` for exactly the opposite reason**: it is needed on the most common operation, and its only
guaranteed loader would be a template that had already gone stale once that same day.

## The rules that still bind

- **`AGENTS.md` is the root contract and these inherit every global rule in it.** Where the two
  disagree, **`AGENTS.md` wins and the stage file is the bug.**
- **Harness-neutral on purpose.** These live here rather than in `.claude/commands/` because Copilot
  CLI, Codex and Cursor read the repo and not Claude Code's command folder. The wrappers point here;
  the specs are portable.
- **Single-writer, like the rest of the contract layer.** A specification needs one author to stay
  coherent, and a clean merge is the dangerous case rather than the conflicting one.
- **Every stage file must be linked from `AGENTS.md`.** `validate.py` enforces it, because the failure
  a split introduces is an orphaned spec nobody is routed to.
