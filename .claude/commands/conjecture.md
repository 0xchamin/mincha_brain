---
description: Generate falsifiable conjectures by combining claims across topics - the abductive pass
argument-hint: [topic to scope to, e.g. "evals" | blank for the whole brain]
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# /conjecture - the generative pass

**The contract is [`stages/conjecture.md`](../../stages/conjecture.md).** Read it now and follow it - this file is
only the Claude Code wrapper for that stage. Do not duplicate the contract here; if the two ever
disagree, `AGENTS.md` wins.

Adopt **synthesizer**. Deliberately **not** fact-checker: this pass does not judge whether a
conjecture is true, only whether it is well-formed. Truth-judging is `/research`'s job and is a
separate invocation, which is what keeps the producer from grading its own work (claim 34).

## Scope

`$ARGUMENTS`

Blank means **the whole brain**, which is the intended use - the best combinations cross topics, and
scoping to one topic removes most of them. A topic name is for when a fresh ingest has just landed
there and you want to see what it now touches.

## Run it

1. **Read the whole brain first** - `claims.md`, every topic note *including its Open questions*,
   `INDEX.md`, and the existing `brain/conjectures.md`. You cannot combine what you have not seen.
2. **Hunt the five patterns in the contract's table.** Do **not** enumerate pairs; at 100+ claims
   that is thousands of combinations and the pass drowns. Follow the patterns, follow curiosity, stop
   when the yield drops.
3. **For each candidate, write the four required fields** - claims combined, what it asserts that
   none of them states, what would falsify it, whether that evidence plausibly exists.
4. **Kill anything without a falsifier**, and record it under "Discarded at generation" with the
   reason. This is not optional bookkeeping; it is what stops the stage becoming a confabulation
   engine.
5. **Append to `brain/conjectures.md`** with stable IDs (`h1`, `h2`, ...), never renumbering.
6. Run **`python3 validate.py`** and show the `git diff`.

## Honesty rules (non-negotiable)

- **Three good conjectures beat thirty plausible ones.** Volume is the failure mode.
- **Most of these will be refuted, and that is the process working.** Do not optimise for survival
  rate - a pass judged on how many hold up produces safe restatements, which are worthless.
- **"Nothing new this pass" is a result.** Record it. It usually means nothing has arrived since the
  last pass that could combine with anything.
- **Never write to `brain/claims.md`.** A conjecture is not a claim. It reaches `claims.md` only
  after `/research` returns `supports` with an independent external citation.
- **Never cite a conjecture as evidence** anywhere in the brain. Reference `h3` *as a conjecture*, or
  not at all.
