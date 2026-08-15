# ADR 0027: The four stage specs leave `AGENTS.md`, and reserved terms enter it

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260815 |
| Deciders | chamin |
| Persona | architect |

## Context

**`AGENTS.md` reached 1,408 lines and 17,164 words, roughly 23,000 tokens, and every one of them is
loaded into every session's context window.** That is the cost side. The evidence side is that it had
started to fail, and the failures are recent and specific.

**Four of them happened on one day, 2026-08-15, all in the same session, all the same shape.** The
word **`movement`** was given two meanings in one document - the roadmap's groups of walkthrough
sections and the units of a presentation - and nobody noticed until a reader said the presentation
read wrong. **Two contradictory rules ran live for hours**, the diagram rule demanding "direction of
flow" against a new persona banning exactly that. **`sources/_TEMPLATE/LEARNING.md` went stale** and
was only caught because the human asked whether the rules had propagated. And a register carve-out
was written and voided within hours. A fifth was found while implementing this decision:
**`personas/presenter.md` was never added to `BUILD.md`'s embed list**, so a clone built from the
bundle would carry a contract citing a persona that does not exist.

**None of these is a contradiction git could catch.** They are a specification that has outgrown one
reader's working memory, including the agent's - and the file already recorded that this happens:
*"two sessions editing different sections of `AGENTS.md` merge cleanly and can still produce two
competing definitions of the same thing... a clean merge is the dangerous case here."*

**And the brain had already measured the answer without applying it.**
[X2](../../experiments/260815_summary-index-ceiling/RESULTS.md) found discriminability decaying
log-linearly with the volume attended over. **Claim 209**, promoted the same week from S26, says to
*scope an agent's behaviour with a schema file placed in the thing being managed, discovered at run
time, overriding the worker's generic instructions.* The kit adopted that as a finding while running
the opposite design.

## Decision

**Extract the four user-triggered stage specs to [`stages/`](../../stages/)** - `verify`, `research`,
`conjecture`, `dream` - **386 lines, 27% of the file.** `AGENTS.md` keeps a short section per stage
naming the trigger, the persona and the output, and pointing at the spec.

**Add a `Reserved terms` registry near the top of `AGENTS.md`** - twelve words that each mean exactly
one thing, with a `Not` column. This is claim 207 (a controlled vocabulary, read first, extended
reluctantly) applied to the contract itself, and it attacks the cause of the `movement` collision
rather than the instance.

**Three choices worth recording because each could have gone otherwise:**

1. **`stages/`, not `.claude/commands/`.** The wrappers already exist and already fire lazily, so
   folding the specs into them looks tidier. **It would break harness portability**, which this kit
   explicitly holds - Copilot CLI, Codex and Cursor read the repo and not Claude Code's command
   folder. The specs are neutral; the wrappers point at them.
2. **The `LEARNING.md` shape stays**, though at 383 lines it is the single largest block and the
   obvious extraction. **The test that decides it is whether the extracted content has a guaranteed
   loader**, because a rule in a file nobody loads is worse than a rule in a long file. Each stage has
   one - the command fires and reads its spec. The shape's would be a template that had **gone stale
   that same day**, and it is needed on the most common operation rather than a fortnightly one.
   Revisit if the collision rate does not fall.
3. **`validate.py` gains one check and only one**: every `stages/*.md` must be linked from
   `AGENTS.md`. That is the single genuinely new failure a split introduces - an orphaned spec that is
   correct and unrouted - and it is pure form, so it belongs in the validator. **The terms registry
   gets no check**, because whether a word is being used in two senses is a reading judgement, and
   encoding it would launder judgement as a green check ([ADR-0004](0004-validator-as-type-checker.md)).

## Consequences

**`AGENTS.md` goes from 1,408 to roughly 1,090 lines** - the stage extraction removes 346 and the
terms registry adds 28. Every session pays about 25% less for the contract, and the four specs arrive
exactly when their stage fires.

**Costs, accepted.**

- **Propagation surface grows.** The stale-template incident hours earlier is precisely this failure,
  and this decision creates four more files that can drift from the root contract. Mitigated by the
  precedence rule (`AGENTS.md` wins, the stage file is the bug), by the routing check, and by adding
  `stages/` to `BUILD.md`'s embed list - which is where `presenter.md` was just found missing.
- **Coherence is harder to see.** "A specification needs one author to stay coherent" still holds and
  is now spread over five files.
- **This is scaffolding and claim 31 applies.** It encodes an assumption - that stage specs are read
  rarely - which expires if a stage becomes routine.

**Revisit when:** the next few contract changes are done, to see whether the collision rate actually
falls. If it does, the `LEARNING.md` shape is the next candidate. **If it does not, this was tidying
rather than a fix**, and the honest move is to say so and stop.
