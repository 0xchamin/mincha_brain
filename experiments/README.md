# `experiments/` - first-party observation

> **What this layer is.** Things **this brain ran itself**, to find out what actually happens. Not a
> source (nobody else made it), not background (it makes claims), not synthesis (it produces new
> observations rather than combining old ones). See
> [ADR-0024](../brain/decisions/0024-experiments-layer.md).

**It exists because in twenty-four sources this brain had never once executed anything.** Four
separate `INDEX.md` rows record the gap in its own words: *"ran none of the code (no GPU)"*, *"repo
not cloned"*, *"the cheapest un-taken second leg"*. Every claim here rests on somebody else's report
of their own system. This layer is the first place that is not true.

## The evidential status, which is narrower than it looks

| Layer | Holds | Evidence status |
|---|---|---|
| `sources/<id>/` | artifacts someone else made | **gated** - two legs, cited, promoted to `brain/` |
| `foundations/` | background no source taught | **uncited by construction** - never promoted |
| `reports/` | synthesis written *out* of the brain | cited to the nodes it draws on |
| **`experiments/<id>/`** | **what this brain observed when it ran something** | **first-party** - tests whether a *mechanism* is real and reachable, and **never** corroborates the source that suggested it |

**An experiment on a reimplementation says nothing about the system that inspired it.** If this brain
writes its own runtime and observes that parallel tool results reorder, that is evidence the
mechanism is real and reachable in general. It is **not** evidence that Hermes does it, and no
experiment here may raise confidence in a claim *about a source*. Where an experiment bears on a
claim, it bears on the claim's **general mechanism**, and the distinction is recorded in the claim
row rather than assumed.

## The three rules that stop this becoming a puppet show

**A harness built to demonstrate what you already believe proves nothing**, because you designed the
thing that produced the green checks. Three disciplines, each borrowed from a claim this brain
already holds:

1. **Predictions are written and committed *before* the first run.** `PREDICTIONS.md` lands in its
   own commit, and `git log` is the proof it was not edited afterwards. This is **claim 34** - the
   producer must not grade its own work - applied to the one agent that would otherwise mark its own
   homework.
2. **Every check is a deterministic function**, never a judgement and never a model. This is
   **claim 164**: an evaluator that can be influenced by the thing it evaluates is unsound, so the
   assertions read files and database rows and compare integers.
3. **Anything nondeterministic is reported as a distribution over N runs, never as pass or fail.**
   This is **claim 114** and **claim 177** - an accept rule with no notion of variance banks noise as
   signal. A race that fires once in fifty runs is the finding, and a single green run would have
   hidden it.

> **A missed prediction is the most valuable output here and is never quietly corrected.**
> `RESULTS.md` records what was predicted, what happened, and which predictions were wrong. A pass
> that records only its successes is cherry-picking, which is the discipline `nodes.md` already
> applies to dropped candidates and `brain/conjectures.md` to discarded conjectures.

## Layout

```
experiments/<YYMMDD_slug>/
  PREDICTIONS.md   committed before any code runs
  harness.py       the minimal system under test
  cases/           one file per case, deterministic assertions
  RESULTS.md       observed, including misses; written after
```

Same naming as `sources/` - `YYMMDD_slug`, big-endian, `_` divides date from name.
