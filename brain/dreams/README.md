# Dreams - the reconciliation passes

> Persona: **architect + fact-checker** - re-adopt when working these files.

One note per **dreaming** pass: the global reconciliation of `brain/` against itself. The contract is
[`AGENTS.md`](../../AGENTS.md) § "Dreaming on request"; the Claude Code wrapper is
[`.claude/commands/dream.md`](../../.claude/commands/dream.md).

**Why these notes are permanent.** A pass changes what the brain believes - a confidence raised, a
framing rewritten, a claim merged away. Without a record, the *reasoning* for those edits lives only
in a `git` diff, and a diff shows what changed but not why it was wrong. **Ephemeral output not
captured into a kit file did not happen.**

Name them `<NNNN>-<YYMMDD>.md`, numbered in order: `0001-260731.md`.

## Structure of a pass note

```markdown
# Dream 0001 - 2026-07-31

| Field | Value |
|---|---|
| Scope | whole brain / <topic> |
| Read | N topic notes, claims 1-64, M ADRs |
| Findings | N applied, M proposed, K none |
| Validator | OK / N errors fixed |

## Findings applied

| # | Class | Where | What was wrong | What changed |
|---|---|---|---|---|

## Proposed, not applied (needs a human call)

| # | Proposal | Reasoning | Why it is a judgement call |
|---|---|---|---|

## Checked and clean

<Which classes were examined and found sound - so the next pass knows what was
already looked at, and a clean result is recorded rather than implied by silence.>

## Notes for the next pass

<Anything watched but not yet actionable - a topic approaching a split, a claim
one source away from corroborated.>
```

## The eight classes a pass works

Contradiction, duplication / fragmentation, stale confidence, stale status, orphans, closed open
questions, superseded framing, drift from source. The table in `AGENTS.md` defines each.

> **"Nothing found" is a result.** A clean pass still gets its note. It is evidence the compounding
> is holding, and it is the baseline the next pass reads. Never manufacture findings to justify a
> pass.
