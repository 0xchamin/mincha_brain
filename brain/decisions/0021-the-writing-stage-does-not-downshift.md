# ADR 0021: The writing stage does not downshift, and the line is specifiable vs perceptual

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260806 |
| Deciders | chamin |

## Context

Everything in this kit runs on one strong model - reasoning, gating, distilling, and writing alike.
The proposal was to split that: keep a strong model for reasoning and analysis, and hand **the act
of writing** to a cheaper one, on the intuition that once you know what to say, saying it is
mechanical.

**The motivation was quota, not money.** Nothing here is billed per token, but the subscription has a
usage budget, and on 2026-08-04 the register retrofit exhausted it. Twelve agents were spawned to
rewrite twelve `LEARNING.md` files; **ten died mid-write** when the monthly limit was hit. The two
that reported usage had spent **96,411 and 99,105 tokens each**, so the batch cost somewhere over a
million tokens. That one pass is the most expensive thing the kit has ever done, and it was almost
pure writing. If any stage should downshift, it is that one.

**A first attempt at the answer aimed at the wrong target.** The intuition was to route deterministic
work - `git push`, `validate.py`, `ffmpeg`, shell - to a small model. That saves nothing measurable.
Those calls cost hundreds of tokens against the writing agents' hundred thousand, roughly three
orders of magnitude apart, and **routing granularity in this harness is the agent, not the tool
call**, so moving them would mean spawning a subagent that costs more to brief than the command costs
to run. The expense was never the commands.

## The experiment

Run as an ablation, which is this kit's own instrument for exactly this question
([claim 33](../claims.md)): hold everything constant and change one component.

`260731_chatgpt-memory-dreaming` was retrofitted a second time from its pre-retrofit text, with **the
same prompt, the same contract, the same reference implementation, and Sonnet instead of Opus**. Both
outputs were compared against the original. Nothing was written to the repo; both versions live in a
scratch directory.

| | original | Opus | Sonnet |
|---|---|---|---|
| Words | 3,960 | 6,086 (+53%) | 5,124 (+29%) |
| Discourse markers | 0 | **13** | **2** |
| Median sentence | 20 | 19 | **21** |
| 90th-percentile sentence | 41 | **35** | **42** |
| Bold lead-in labels (rule 3 forbids these) | 5 | **0** | **3** |
| Node IDs, headings, claims, frames | - | all preserved | all preserved |
| `corroborated by` labels | 4 | 4 | **2** |
| Tokens / wall clock | - | ~97k / ~11 min | **112k / 32 min** |

**Sonnet added 29% more words and did not apply the register.** Its sentence rhythm is
indistinguishable from the untouched original, at a median of 21 against 20 and a 90th percentile of
42 against 41. Opus pulled the long tail from 41 to 35, which is the measurable signature of
unrolling stacked subordinate clauses into handoffs. Three forbidden bold lead-in labels survived.

**It also cost an invariant.** It dissolved the structured `- What it teaches:` / `- Corroborated by:`
bullet pairs beneath each figure into italic prose captions, and two of the four `corroborated by`
labels vanished into sentences. Those two lines are the corroboration gate's two legs made greppable,
and [`/verify` check 6](0016-verify-reads-the-frames.md) reads exactly that pair. Note how the change
was reported: as "matching the reference implementation's style", which is a confident rationalisation
for an edit the brief forbade.

**And it was not cheap in the expected way.** More tokens and three times the wall clock. Sonnet costs
fewer quota units per token, so there is still a saving, but it is bought against output that failed
the task.

## Decision

**Keep one strong model for every stage of this kit that spends meaningful quota.** Writing,
distilling, gating, `/verify`, `/dream` and `/conjecture` all stay on the strong model.

**The reason is not "stronger is better". It is that the line runs between specifiable and perceptual,
not between thinking and writing.** Sonnet executed every instruction a script could check. It added
the narrative, kept the table, preserved every heading byte-for-byte and held every node ID. It failed
every instruction requiring a judgement about whether prose reads well, because *"does this paragraph
hand off to the next"* has no mechanical test.

**Which is this brain's own generation-verification gap, arriving from the other side.** A cheap
generator is safe exactly where the verifier is cheap. For the register the verifier is a careful
reader, so the generator has to be strong. That reasoning, rather than the measurement, is what should
survive this ADR.

**The exception class, stated so it is not forgotten:** a transform is a downshift candidate when its
output can be checked **completely** by `diff`, `grep` or `validate.py`, with no residue requiring a
reader. The pending **reference-style citation pass** - moving URL blobs out of the reading path into a
footer - is the clearest current example, because it changes no words at all. **The register retrofit
looked like that class and was not**, which is the whole finding.

**Deterministic work needs no routing decision.** Shell, git and the frozen scripts already cost
nothing worth optimising.

## Alternatives considered

- **Route deterministic execution to a small model.** Rejected on measurement, not principle. Three
  orders of magnitude below the writing agents, and the harness cannot route a single tool call
  without spawning an agent that costs more than the command.
- **Downshift writing but add a strong-model review pass.** Plausible, and rejected for now because it
  reintroduces the full cost it was meant to avoid. Reviewing prose against the register requires
  reading all of it, so the reviewer pays close to what the writer would have. Revisit only if a
  cheap mechanical proxy for the register is found.
- **Give Sonnet the register as a tickable checklist rather than described taste.** Untested, and the
  single most promising follow-up. If the failure is one of operationalisation rather than capability,
  this closes it. Recorded below as a re-test trigger.

## Consequences

**Easier.** No routing machinery, no model matrix in the contract, and no class of note whose quality
depends on which model happened to write it.

**Harder.** Expensive passes stay expensive, and a corpus-wide retrofit remains capable of exhausting
a monthly budget. **The practical mitigation is batch size, not model choice** - twelve concurrent
agents is what hit the limit, and four would not have.

**Revisit when** any of three things happen. A cheap mechanical proxy for prose quality appears. A
purely specifiable transform comes up, in which case use the exception class above rather than
reopening this ADR. Or the checklist variant is tried and works.

> **Confidence: `needs-check`, and deliberately so.** This is **n=1** - one note, one prompt, one run,
> no repeats, and Sonnet's run-to-run variance was not measured. By this kit's own standards that is a
> `single-leg` result, and it is recorded as a decision because a decision was needed, not because the
> evidence is strong. The kit's own claim 115 warns against banking a result whose noise floor was
> never measured. **The result here is one run.**
