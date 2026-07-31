---
description: Reconcile the brain against itself - global drift pass into brain/dreams/
argument-hint: [topic or scope, e.g. "memory" | blank for the whole brain]
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# /dream - the reconciliation pass

**The contract is `AGENTS.md` § "Dreaming on request".** Read it now and follow it - this file is
only the Claude Code wrapper for that stage. Do not duplicate the contract here; if the two ever
disagree, `AGENTS.md` wins.

Adopt **architect + fact-checker**. The architect owns merge / split / status calls; the
fact-checker owns claim verdicts and citations.

## Scope

`$ARGUMENTS`

Blank means **the whole brain** - the default and the intended use. A topic name narrows the pass to
that note and everything cross-linking it, which is worth doing after a big ingest but is **not** a
substitute for a full pass.

## Run it

1. **Read everything in scope before changing anything.** `INDEX.md`, every `brain/topics/*.md`,
   `brain/claims.md`, `brain/glossary.md`, `brain/decisions/`, the tail of `brain/log.md`. **Do not
   sample.** Reading it all is the entire advantage of being out of band; an ingest cannot afford it
   and that is why drift accumulates.
2. **Collect findings first**, in a scratch list, each naming the files and claim IDs involved.
   Work the eight classes in the `AGENTS.md` table: contradiction, duplication, stale confidence,
   stale status, orphans, closed open questions, superseded framing, drift from source.
3. **Check the cheap structural things with `grep`, not by eye** - a claim number that appears in
   `claims.md` and in no topic note, a topic note whose Status disagrees with its INDEX row, a
   source in `INDEX.md` feeding no claims. These are the findings most likely to be real and least
   likely to be noticed.
4. **Write the pass note** to `brain/dreams/<NNNN>-<YYMMDD>.md` (next number, today's date), using
   the structure in `brain/dreams/README.md`. One note per pass, permanent.
5. **Apply the clear defects** in the same pass - a stale status, an orphan link, a superseded
   sentence, a confidence that a second source already earned. This is a reconciliation, not a
   report.
6. **Ask before applying judgement calls** - dropping a claim, splitting or merging a topic,
   reversing a confidence, retiring a source. Put the proposal and its reasoning in the note, then
   ask. **The human adopts.**
7. **Append one dated line to `brain/log.md`**, run **`python3 validate.py`**, and show the
   `git diff`.

## Honesty rules (non-negotiable)

- **"Nothing found" is a result.** A clean pass gets its note and says so. It is evidence the
  compounding is holding. **Never manufacture findings to justify the pass.**
- **A contradiction is a finding, not a failure.** Keep both sides, cite both, flag the conflict in
  the topic note's "Open questions / conflicts". Do not silently pick a winner.
- **Never re-litigate the gate.** Whether a node was `corroborated` is settled in that source's
  `nodes.md` at ingest time. Dreaming reconciles what was **promoted** and never edits a `nodes.md`.
- **Never raise confidence without a citation to point at.** "It feels well established now" is how
  a brain drifts into confident wrongness - the exact failure this topic exists to record.
