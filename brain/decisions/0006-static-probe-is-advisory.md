# ADR 0006: The static probe's STATIC verdict is advisory, not dispositive

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260726 |
| Deciders | chamin |

## Context

[ADR-0003](0003-optional-visual-leg.md) made the visual leg skippable and gave the decision a free
mechanical signal: scene-detect plus pHash dedup already run as the first shell step, so a video
yielding `<= 3` distinct frames auto-degrades to transcript-only.
[ADR-0005](0005-mechanical-toolbox.md) then froze that computation in `tools/ingest.py probe`,
precisely so that "distinct" would not vary by agent.

Both were right. Neither anticipated the failure mode.

**Scene detection measures whole-frame delta.** A conference recording is usually a composited
stream: a fixed background, a fixed logo, a fixed speaker-at-podium video inset, a fixed track
footer, and a slide body occupying a minority of the pixels. When the slide changes, most of the
frame does not. The delta never crosses `SCENE_THRESHOLD`, and the probe reports a continuously
changing 20-slide deck as visually static.

**Two occurrences, one root cause, at two different stages:**

| Source | Stage that failed | Symptom |
|---|---|---|
| `260725_12-factor-agents` | pHash dedup | Slides sharing a template collapsed into each other; the ingest switched to transcript-anchored extraction. |
| `260726_dont-ship-skills-without-evals` | scene detection | `candidates=3 distinct=3 -> STATIC` on ~20 dense slides. |

The second is the dangerous one, because ADR-0003 makes STATIC **actionable**: honouring it discards
the entire visual leg and gates every node from the source `single-leg` by construction. On that
source it would have destroyed three specific nodes whose numbers **exist only on the slides** - the
skill-length lift curve (`n11`), "rewriting the description alone fixed 5 of 7 failures" (`n13`), and
the 39.2% -> 91.6% case-study table (`n28`).

**Why this is not just a bad constant.** Lowering `SCENE_THRESHOLD` would trade one false verdict
class for another (webcam noise and cross-fades would start reading as RICH), and worse, it would
break the property ADR-0005 exists to protect: **a verdict computed with different constants is not
comparable to any previous source's.** Five sources have already been measured with the current
values. The metric is wrong for this input class, not mis-tuned.

**The asymmetry that decides it.** The two errors do not cost the same. A false RICH wastes one
`view` call on a contact sheet. A false STATIC silently destroys a source's second leg, and the
contract's own degrade rule says that once you skip the visual leg you must **not** retro-mark nodes
`corroborated` - so the loss is not cheaply recoverable. **An asymmetric error deserves an asymmetric
check.**

## Decision

**A `STATIC` verdict is advisory. It must be confirmed by looking before it is honoured.**

`tools/ingest.py probe`, on `STATIC` only, now samples **9 frames spread evenly across the runtime**,
tiles them into one chronological contact sheet, and prints the path with an instruction to `view` it
before skipping the visual leg. Cost: **one `view` call**, on the branch that would otherwise throw
away the entire visual leg. `RICH` is unchanged and costs nothing new.

**The change is deliberately additive.** The verdict, `STATIC_FRAME_THRESHOLD`, `SCENE_THRESHOLD` and
`PHASH_DISTANCE` are untouched, so every past probe result stays comparable and no source needs
re-measuring. **Confirming a verdict is not the same as recomputing it** - that distinction is what
lets this coexist with ADR-0005 rather than eroding it.

Escape hatches, both explicit:

- `--no-confirm` skips the sheet and prints that you are honouring an advisory verdict unchecked,
  which must then be recorded in `SOURCE.md`.
- If the runtime cannot be read, the tool says the sheet could not be built and instructs the agent
  **not** to record a confirmed STATIC. Failure is never silent - the same rule that caught the
  swallowed `ffmpeg` exit code during ADR-0005's shakedown.

A user opt-out ("transcript only") still skips the probe entirely and therefore this too. Explicit
instruction outranks the mechanism, as in ADR-0003.

## Alternatives considered

- **Lower `SCENE_THRESHOLD`** - rejected. Breaks cross-source comparability (ADR-0005's whole point),
  and trades a false-STATIC class for a false-RICH class without fixing the mismatch between a
  whole-frame metric and a partial-frame change.
- **Add `--crop` to `probe`** so it measures only the slide region - rejected as the default. You
  cannot know the crop region without looking first, which is circular, and a per-source crop
  reintroduces exactly the parameter variance ADR-0005 froze. `frames --crop` already exists for use
  *after* you have looked.
- **Make the agent always eyeball a sheet before any probe** - rejected. That is a token cost on
  every ingest to defend against one branch, and it makes the free signal not free.
- **Leave it to the agent's judgement, documented in prose** - rejected, and this is the ADR-0005
  argument restated: the failure already happened twice with the rule in prose. The check belongs at
  the point of action, in the tool's own output, not in a paragraph the agent may or may not recall.
- **Drop the probe entirely** - rejected. It is right for the case it was built for (podcast, webcam
  interview) and costs nothing. The verdict is useful; its authority was too high.

## Consequences

**Easier.** A false STATIC now costs one `view` instead of a source's second leg. The
`260726_dont-ship-skills-without-evals` override becomes the documented default procedure rather than
an ad-hoc save. Agents get the warning where it is actionable - in the tool's output - rather than in
a contract paragraph.

**Harder.** A genuinely static video now costs one `view` call it did not before. That is the price
of the asymmetry and it is small. `probe` also now depends on `ffprobe` for the runtime, which ships
with `ffmpeg` and is already a hard dependency.

**To revisit.** If a third occurrence appears at a stage neither scene detection nor confirmation
covers, the metric itself should be reconsidered - most likely by measuring delta over a
centre-weighted region rather than the whole frame. That *would* be a constants change and would
need its own ADR plus a re-measurement note.

**Follow-ups completed in this pass:** `tools/ingest.py` (implementation + a reproduction test on a
synthetic templated deck: 9 distinct slides, `candidates=0 -> STATIC`, differences plainly visible on
the confirmation sheet); `AGENTS.md` § "The visual leg"; `prd.md` §5.1 and change log; a dated line in
[`../log.md`](../log.md).
