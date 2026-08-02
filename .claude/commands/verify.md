---
description: Check one source's LEARNING.md against its own gated evidence - the evaluator the gate lacks
argument-hint: <source id, e.g. 260802_gcp-multi-tenant-agentic-ai>
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# /verify - the source-layer evaluator

**The contract is `AGENTS.md` § "Verifying one source on request".** Read it now and follow it - this
file is only the Claude Code wrapper for that stage. Do not duplicate the contract here; if the two
ever disagree, `AGENTS.md` wins.

Adopt **fact-checker**, alone. This stage has exactly one objective, and composing it with `curator`
would reintroduce the conflict of interest it exists to remove (claim 34).

## Source

`$ARGUMENTS`

A source id under `sources/`. **Required** - there is no whole-repo mode, because reading twelve
sources at once is how a checking pass turns into a skim.

## Run it

1. **Read exactly three files**: that source's `nodes.md`, `LEARNING.md` and `SOURCE.md`. **Do not
   read the topic notes.** What was *promoted* is the dream pass's business; mixing the two gives this
   stage two objectives again.
2. **Work the six checks in the contract's table, in order.** For each, quote the sentence and the
   node it rests on, side by side, so the verdict is inspectable rather than asserted.
3. **Assign one verdict per finding** - `defect`, `judgement`, or `gate-reopen`.
4. **Fix the `defect`s in the same pass.** Propose the rest.
5. **Append to `sources/<id>/verify.md`** with today's date. Never rewrite an earlier entry.
6. Run **`python3 validate.py`** and show the `git diff`.

## Honesty rules (non-negotiable)

- **"Nothing found" is a result.** A clean source gets its entry and says so. Never manufacture
  findings to justify the pass - a checking stage that always finds something is a stage nobody will
  believe.
- **Never re-gate silently.** `gate-reopen` is always a proposal, never an edit. Re-gating changes
  what the brain believes, and that is the human's call.
- **Do not grade prose quality, structure, or whether the ramp works.** Those belong to the curator
  and the human. **A stage that grades everything grades nothing.**
- **Do not run this on a source you wrote in this session.** You do not have an independent vantage
  point on an argument you have been holding for an hour, and saying you will be objective is not a
  mechanism. Use a different session.
