---
description: Check one source's LEARNING.md against its own gated evidence - the evaluator the gate lacks
argument-hint: <source id, e.g. 260802_gcp-multi-tenant-agentic-ai>
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# /verify - the source-layer evaluator

**The contract is [`stages/verify.md`](../../stages/verify.md).** Read it now and follow it - this
file is only the Claude Code wrapper for that stage. Do not duplicate the contract here; if the two
ever disagree, `AGENTS.md` wins.

Adopt **fact-checker**, alone. This stage has exactly one objective, and composing it with `curator`
would reintroduce the conflict of interest it exists to remove (claim 34).

## Source

`$ARGUMENTS`

A source id under `sources/`. **Required** - there is no whole-repo mode, because reading twelve
sources at once is how a checking pass turns into a skim.

## Run it

1. **Read three text files plus the frames**: that source's `nodes.md`, `LEARNING.md`, `SOURCE.md`,
   and every image in its `visuals/`. **Nothing else - and in particular, do not read the topic
   notes.** What was *promoted* is the dream pass's business; mixing the two gives this stage two
   objectives again.
2. **Work the six checks in the contract's table, in order.** For each, quote the sentence and the
   node it rests on, side by side, so the verdict is inspectable rather than asserted.
3. **Check 6 needs the images open** ([ADR-0016](../../brain/decisions/0016-verify-reads-the-frames.md)).
   Read each frame and compare it against its own `what it teaches` line. If the source has no
   `visuals/`, the check is `n/a` and costs nothing.
4. **Assign one verdict per finding** - `defect`, `judgement`, or `gate-reopen`.
5. **Fix the `defect`s in the same pass.** Propose the rest.
6. **Append to `sources/<id>/verify.md`** with today's date, opening with a field table that records
   `Read`, **`Frames`** (`checked (N)` / `n/a (visual leg skipped)` / `skipped (user)`),
   `Independence` and `Findings`. Never rewrite an earlier entry.
7. Run **`python3 validate.py`** and show the `git diff`.

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
- **Never skip check 6 silently.** If the frames were not read, the entry says so in the `Frames`
  field and gives the reason. A pass that quietly checks five of six and reports six is the S7 `d4`
  failure - a verification step with no stated mechanism - which is the defect this whole stage was
  built out of.
