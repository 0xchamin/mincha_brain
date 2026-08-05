# Topic: Autonomous research loops

**Status:** **emerging (2 primary sources, and no longer a merge-back candidate)** - **S13**
`karpathy/autoresearch` and **S22** the Darwin Godel Machine. Created 2026-08-03 by
[ADR-0017](../decisions/0017-autonomous-research-loops-topic.md); **merge-back trigger resolved
2026-08-05 by [ADR-0020](../decisions/0020-autonomous-research-loops-second-primary.md)**.
**Basis, and the two sources are almost opposites evidentially.** S13 is a **T4 personal repository**
whose design is fully inspectable and whose *results* are a single unreproducible PNG - strong design
claims, weak empirical ones, labelled so throughout. S22 is **ICLR 2026 main track with open-sourced
code and two ablations that isolate its claimed components**, which makes it the best-evidenced source
in this brain on any subject. ~~This note is a candidate for merge back into `agents.md` if no second
primary source arrives.~~ **It arrived.**

> **What the pairing buys, beyond a source count.** S13 supplies a *practitioner's* freezes, stated as
> design and unmeasured. S22 supplies **ablations** - remove the archive and progress plateaus lower,
> remove self-improvement and it plateaus earlier - so for the first time this note can say a
> structural choice was *tested* rather than merely reasoned. And the two disagree productively on the
> one thing they both got wrong-adjacent: S13's accept rule had **no notion of variance** and banked a
> random-seed change (claim 114), while S22 built a staged evaluation with a promotion threshold
> "chosen based on the noise observed in preliminary runs". **One loop ignored noise and one designed
> around it, and the second is the one that worked.**

> Living, cross-source synthesis on **agents that iterate on an artifact unattended**, accepting or
> rejecting each change against an automated metric. Many sources feed this note; **merge and
> de-duplicate** as they arrive (architect persona). Every claim cited.
>
> **Not literature-search agents.** In this kit "research" as a *verb* means the `/research` stage -
> gathering external evidence into `sources/<id>/context/`. This note is about the other thing: a
> loop that runs experiments. The name is deliberately long to keep the two apart (ADR-0017).

## What this covers

The **setup** an unattended improvement loop needs before it can be trusted to run for hours with
nobody watching: what must be frozen and what may move; which resource is held constant so that
heterogeneous changes stay comparable; how the metric is made invariant to what the agent may
change; where the loop's state and audit trail live; the accept/reject rule and its statistical
behaviour; the per-iteration cost of running a loop hundreds of times; and how to read the results
of such a loop honestly.

**Adjacent, and deliberately not re-homed here** - these live in `agents` and `evals` and are
cross-referenced, not restated: claim 7 (closed-loop auto-tuning on production data), claim 10
(self-tuning via a prompt optimizer), claim 31 (scaffolding as an expiring bet, tested by ablation),
claim 34 (do not let the producer grade its own work), claim 59 (one loop, one objective).

## Synthesis

### The engineering happens before the loop starts

The single organising finding from S13, and the reason the topic exists. An autonomous loop is nine
steps of shell commands and needs no framework - `karpathy/autoresearch` contains **no agent code at
all**, because the agent is whatever coding harness you point at a markdown file [S13 `n16`,
`README.md:44`]. What the repository actually is, is a set of decisions taken *before* the agent
starts, after which the loop is trivial.

Four things are frozen, and each answers a question the previous one leaves open. **The derivation
matters more than the list** - it is what transfers to a domain that is not model training:

1. **The editable surface.** Exactly one file; everything defining the experiment is read-only
   [S13 `n1`]. In S13 the hyperparameters are module-level constants with no CLI, which makes an
   experiment **a diff** rather than a command line - and that is what lets the next three decisions
   work.
2. **The resource held constant.** If the agent may change model size and shape, two runs are not
   naturally comparable. S13 holds **wall-clock time** (300 seconds), not steps and not tokens
   [S13 `n3`]. Fixing steps rewards shrinking the model; fixing tokens makes efficiency invisible.
   Fixing time puts a faster kernel, a better optimizer and a longer schedule on one axis - so
   **efficiency becomes part of the objective without being part of the metric**.
3. **The metric's units.** Bits-per-byte rather than per-token loss, and evaluation always at a
   fixed sequence length whatever the model trained at [S13 `n4`]. Any degree of freedom that
   changes the metric's *units* is a way to improve the number without improving the thing, and an
   optimizer finds it with no intent to cheat.
4. **The holdout.** One validation shard pinned inside the read-only file and excluded from both the
   tokenizer corpus and the training dataloader [S13 `n2`].

**Where the defence lives is the transferable part: in the code layout, not in the prompt.** None of
the four is an instruction to the agent; all four are properties of a module the agent has been told
not to open. Generalised: if you point an agent at a scored artifact, the score's definition, its
input data and its units belong in a module the agent has no reason to import.

### The freeze is usually a declaration, and it is worth knowing which of yours are enforced

S13's read-only boundary is a banner comment and a line of markdown - **no sandbox, no import hook,
no checksum, no permission bit** [S13 `n1`]. Exactly one invariant is structurally enforced (the
pinned holdout, `n2`), and it is the one whose violation would be most damaging and most greppable.

This is not a flaw to fix reflexively - an enforced version costs a container or a git hook, and a
non-adversarial agent respects the declaration. **The lesson is that under this design an enforced
invariant and a written-down one look identical in the source tree**, and you should know which is
which before you rely on one.

### The accept rule is where these designs spend the least, and it is where they leak

Two independent weaknesses in S13 sit on the **decision** path rather than the computation path, and
the pattern is worth carrying:

**The producer prints its own grade.** `evaluate_bpb` is frozen, but the editable file imports it,
calls it, formats the result and prints it - and the agent reads its score by grepping that print
[S13 `n5`]. Nothing compares the number in the log to what the frozen function returned. This is
**claim 34 arriving as a plumbing fact rather than a prompting one**, and that is the more useful
form: you can separate generator from evaluator perfectly at the level of functions and still route
the evaluator's output through the generator's hands on the way to the decision. The fix is one
`open()` in the frozen module.

**The rule has no notion of variance.** "If val_bpb improved (lower), advance the branch; if equal
or worse, git reset" - no repetition, no seed averaging, no threshold, no error bar [S13 `n11`].
**The consequence is visible in the source's own published run: the fifteenth and final kept
improvement of 83 experiments is a change of random seed.** That is not a failure of the agent's
judgement; it is the rule executing correctly on an input it cannot recognise.

That experiment also **measures the loop's noise floor for free** - reseeding changes nothing real,
so whatever it "improved" is a lower bound on how much the score moves for no reason. Read off the
chart it is roughly 0.0005 bpb, and at least three other accepted changes appear smaller than that
[S13 `n12`, **needs-check - deltas read off a rendered PNG, and the floor rests on n=1**].

The compounding is the part to carry: every accepted change permanently moves the baseline all later
experiments are judged against, and **nothing ever re-tests a kept change** [S13 `g3`]. So a lucky
accept does not merely add a spurious row - it raises the bar for every subsequent real improvement.

### Version control is a sufficient experiment database, if an experiment is a diff

Branch per run, commit per experiment, `git reset` as the discard operation, branch tip as
current-best [S13 `n6`]. No tracker, no registry. This works *because* of the first freeze: with
hyperparameters as in-file constants, the thing being tracked is a sequence of diffs and the
operation needed most is "undo the last one".

The sharpest small idea: **the ledger is deliberately untracked** [S13 `n7`]. Discard is `git reset`,
so anything committed is inside the thing that gets rewound, and the row you most want to keep is
the one describing the experiment that just failed. Stated generally - **in any loop whose failure
mode is rollback, the audit trail must not be rollback-able.** (The instruction is the source's; the
derivation is this brain's - the source gives no reason.)

The price is paid in the same breath: because the ledger was never committed, **the author's own
published results cannot be reproduced from the repository**.

### Running a loop hundreds of times is a context problem before it is a compute problem

The scarce resource is not the GPU - that is busy exactly 300 seconds per iteration whatever
happens. It is the agent's context, and S13 spends three separate mechanisms on it: the training log
is a single carriage-returned line, `tee` is forbidden, and the result is read with `grep` rather
than by opening the file - roughly **two lines per five-minute experiment** [S13 `n8`]. The artifact
is given a machine-readable reporting interface (nine `key: value` lines) so the driver never parses
prose.

**The cost is per-iteration and therefore multiplied by the iteration count**, which is the number to
design against; 500 wasted tokens per experiment is 50,000 across a night. Related: **empty output is
the error signal** - "if the grep output is empty, the run crashed" - which costs zero tokens in the
common case, paired with a fast-fail in the artifact that kills a NaN run rather than spending the
remaining budget [S13 `n17`].

### Autonomy is a suppressed default, and the freezes are what earn it

S13 instructs the agent in capitals never to check in: "do NOT pause to ask the human if you should
continue... The human might be asleep" [S13 `n9`]. This is not a capability added but **the default
that most agent guidance works to install, deliberately removed**.

Two properties make it defensible here, and they are the test to apply elsewhere: **the check-in has
no information to offer** (the decision is a scalar comparison against a protected metric, so a human
woken at 3am adds nothing the rule does not encode), and **the blast radius is a branch** - nothing
deployed, nothing sent, nothing irreversible, with the holdout structurally out of reach. The freezes
above are what make "disable all permissions" a defensible instruction here and an alarming one
almost anywhere else.

The instruction carries a second half that is easy to skim and is load-bearing: an **idea-generation
fallback ladder** for when the agent runs out of ideas (think harder, read the papers cited in the
code, re-read the in-scope files, combine previous near-misses, try radical changes). Without it
"never stop" degrades into re-trying variations of the last success. Whether it works is untestable
from this source, because **the reasoning behind each experiment is never recorded** [S13 `g1`].

### When the loop carries a second objective, publish the exchange rate

S13 gives the agent simplicity as a second goal beside the metric, and resolves the conflict not with
a preference but with **four worked numeric trades** - a 0.001 improvement costing 20 lines of hacky
code is refused, a 0.001 improvement from *deleting* code is kept, a ~0 improvement that simplifies
is kept [S13 `n10`, `single-leg`]. Claim 59 says a loop holding two objectives trades them off
untunably; this is a partial answer to it that does not require splitting the loop - **specify the
rate rather than the preference**. Note the limit: the ledger has no complexity column, so the trade
is made in the agent's head and is never recorded or audited.

### What the results actually look like, and how to read them

From S13's single published run, all `needs-check` [S13 `n13`, `n14`, `n15`]:

- **Yield is low and that is fine.** 15 keeps in 83 experiments (~18%). The loop's advantage is not
  intelligence, it is **indifference to rejection**.
- **Gains are front-loaded** - four of fifteen in the first eight experiments, and they are schedule
  and sizing knobs, which is the wall-clock budget choice showing up directly in the results.
- **The search is greedy coordinate descent and nothing else was available.** Three consecutive kept
  experiments walk one hyperparameter monotonically. Each experiment is judged against the current
  tip, so there is no way to evaluate a combination, compare two directions, or escape a local
  optimum other than a "rewind, very very sparingly" escape hatch with no stated criterion.
- **A ~22-experiment plateau** in the middle, escaped for reasons the design did not record.
- **Read the chart's code before the chart.** The shipped figure filters out crashes and everything
  scoring worse than `baseline + 0.0005`, while its title counts all 83 - so the visible near-miss
  cloud is not the failure population [S13 `n15`].

### The artifact you iterate on is the prose

The author's own framing: "you're not touching any of the Python files like you normally would as a
researcher. Instead, you are programming the `program.md`" - and he calls that file "essentially a
super lightweight 'skill'" [S13 `n16`]. 115 lines of markdown hold the setup ritual, the rules, the
output contract, the ledger schema, the loop and the autonomy policy. **Every gap identified in this
note is a markdown edit rather than an engineering project**, which is the strongest argument that
the inversion is real and not a slogan. See [`skills.md`](skills.md), which records this as the
second instance in this brain of the pattern outside a coding-assistant context.

### An archive beats a lineage, and it is the first ablated claim this note holds

**S13 froze rollback-as-discard: any change that did not improve the metric was reverted with
`git reset`. S22 measures what that costs**
([S22](../../sources/260805_darwin-godel-machine/LEARNING.md) `n8`, claim 174).

Take the obvious search first. Hold the current best agent, ask it to modify itself, keep the child if
it scores better. Now ask what happens the first time a self-modification is bad: **you have damaged
the only agent you have**, and every later improvement starts from the worse version. The failure
compounds, because an agent degraded at editing code is degraded at exactly the capability it needs to
repair itself. S22 runs that configuration as an ablation and it plateaus **lowest of three**.

The alternative is to keep everything. S22 maintains an **archive** of every agent ever produced and
selects the next parent from the whole archive, weighting selection **proportionally to score and
inversely to how many children an agent already has**, with every agent retaining non-zero probability
(claim 175). One bad child then costs one iteration rather than the run.

**The payoff is visible and it is the argument for the whole design.** At iterations 4 and 56 the
agent scored *below* its parent. A hill-climber discards that branch; the archive let the search
continue down it and produce an agent that outperformed every predecessor. **An accept rule that only
moves forward cannot cross a valley** - which is a plain statement of what S13's rollback-as-discard
freeze buys and what it costs.

> **Both S22 ablations matter and they separate cleanly.** Freeze the meta-agent so it never improves
> at improving - the prior ADAS approach - and gains "taper off quickly", plateauing in the middle.
> Keep only the latest agent and it plateaus lowest. **Neither component is decoration**, and this is
> the only ablation-backed claim about self-improving architecture anywhere in this brain.

### What must not be modifiable, now stated by two sources

S13 gave this note its organising idea: **the four things you freeze before letting an agent change
everything else.** S22 freezes two, for stated reasons, and one of them is sharper than anything S13
had (claim 176).

**The viability gate.** Only agents that compile **and retain the ability to edit a codebase** are
admitted to the archive; everything else is discarded, because only those can continue self-modifying.
Note what kind of check that is - **not a quality bar**, since an agent much worse than its parent is
still archived. It is a **liveness invariant, deliberately separate from the performance metric**, and
it is the only thing standing between the system and a self-modification that ends the run by breaking
the tool it needs to modify itself.

**The meta-level.** Archive maintenance and parent selection are "fixed and not modifiable by the
DGM". Ask what lifting that restriction would do and the reason is immediate: **a system that can
rewrite its own selection criteria can rewrite them to prefer itself**, and the empirical evidence that
was supposed to discipline the search is then produced under rules the search chose.

> **This is claim 113 avoided by construction, and the contrast with S13 is exact.** S13's autoresearch
> had a *protected* metric whose value nonetheless reached the decision through code the agent could
> rewrite - separation at the level of functions did not deliver separation in fact. S22 puts the
> deciding machinery **outside the modifiable surface entirely**. The principle both sources point at:
> **the thing that decides what counts as improvement must not be inside what improves.**

It also bounds S22's own framing. The search is open-ended **within a human-designed search
procedure**, which is the same concession S18's authors made about their architecture search, and the
paper records it as future work.

### The loop amplifies whatever its verifier cannot see, and three sources now say so

**The most important thing this note holds, and it is now stated from three independent directions**
(claim 177).

S22's Safety Discussion says it plainly of their own system: if evaluation benchmarks "do not fully
capture all desired agent properties (e.g., safety and robustness), **the self-improvement loop could
amplify misalignment over successive generations**".

| Source | Form | What it says |
|---|---|---|
| **S13**, claim 114 | **Observed** | A loop with a real, cheap, automatic verifier banked a **change of random seed** as its final improvement, because the accept rule had no notion of variance |
| **S19**, claim 162 | **Predicted, adversarially** | An attacker's step in a self-refining skill runs without error, the loop treats "no error" as validation, and the procedure is optimised **around** the adversarial step |
| **S22**, claim 177 | **Predicted, by the builders** | If the benchmark misses a property, successive generations **compound** the miss |

**All three are one statement**: a self-improving loop optimises what it can measure and compounds what
it cannot. **And claim 124 is the frame that explains all three** - verification, not generation, is
the rate limit, so a loop improves at the rate its verifier can discriminate and degrades at the rate
its verifier is blind.

S22's safeguards follow from taking that seriously, and what they are *not* is the instructive part:
sandboxed execution, a strict per-execution time limit, a modifiable scope confined to the agent's own
codebase, and a **traceable lineage** of every modification for human review. **Every one is
containment.** None is a check that a modification is *good* - consistent with the paper's own premise,
since the impossibility of that check is why it swapped proof for evidence in the first place.

The authors then name the shape of a real answer as future work: incentivising a self-improving system
to retain safety directives is hard, and "an option worth exploring is to create an **unmodifiable part
of the system to be able to evaluate at halt the rest**". **That is this note's freeze pattern proposed
for the safety layer, and nobody has built it.**

## Key claims

| # | Claim | Confidence |
|---|---|---|
| 110 | Hold a **resource** constant, not the work: wall-clock time makes architecture, model-size and efficiency changes directly comparable in a way fixed steps or fixed tokens do not. | corroborated (S13, docs+code) |
| 111 | Make the metric invariant to everything the agent may change - normalise by a physical unit, evaluate under fixed conditions, pin the holdout in read-only code. **Anti-Goodhart is a code-layout problem, not a prompt problem.** | corroborated (S13, docs+code) |
| 112 | Splitting the workspace into an editable file and a read-only file is the containment boundary of an unattended loop - and it is typically a **declaration, not an enforcement**. | corroborated (S13, docs+code) |
| 113 | A protected metric can still reach the decision through agent-editable code; separating generator from evaluator at the function level does not separate them on the **reporting path**. | corroborated (S13, code) |
| 114 | **A bare improve-or-regress accept rule with no variance handling will bank noise** - S13's own run kept a change of random seed as one of fifteen improvements. | corroborated (S13, rule + figure) |
| 115 | Re-running one configuration with a different seed measures the loop's noise floor for free; any accepted improvement smaller than it is unresolved. | needs-check (S13, n=1, chart-read) |
| 116 | In a loop whose discard operation is a rollback, **the audit trail must live outside the rolled-back state**. | corroborated (S13, docs + repo state) |
| 117 | Version control is a sufficient experiment database when an experiment is a diff: branch per run, commit per experiment, reset as discard. | needs-check (S13, single-leg) |
| 118 | The **per-iteration** context budget is a first-class design parameter of an unattended loop, because its cost is multiplied by the iteration count. | corroborated (S13, docs+code) |
| 119 | Autonomy requires explicitly suppressing the agent's check-in default, and is earned by two conditions: the check-in has no information to offer, and the blast radius is bounded. | needs-check (S13, single-leg + this brain's reading of the conditions) |

Full rows and citations in [`../claims.md`](../claims.md). **The `Topic` column there distributes
these across four notes** - 110, 112, 116 and 117 are filed here; 111, 113, 114 and 115 under
[`evals.md`](evals.md) because they are measurement claims reusable well outside a research loop;
118 under [`context-engineering.md`](context-engineering.md); 119 under [`agents.md`](agents.md).
They are all listed above because they are all key to *this* argument, and are cross-referenced
rather than restated in the other notes.

## Key visuals

- [`progress_endgame.png`](../../sources/260803_autoresearch/visuals/progress_endgame.png) - **the
  most important image in this topic.** The end of S13's run: a long plateau, a three-step
  coordinate-descent staircase, and a final accepted improvement labelled `random seed 42->137`. The
  whole variance argument is legible in one crop.
- [`progress_full.png`](../../sources/260803_autoresearch/visuals/progress_full.png) - the complete
  83-experiment frontier. Yield, front-loading and the plateau in one view. Read `n15` before
  quoting it - the figure is filtered by the notebook that draws it.
- [`progress_early.png`](../../sources/260803_autoresearch/visuals/progress_early.png) - the first
  ten experiments, where four of the fifteen wins land, all of them schedule and sizing knobs.

## Open questions / conflicts

- **What is the actual noise floor of a loop like this?** The cheapest unrun experiment in the area:
  run an unmodified baseline five times with different seeds and report the spread. It would settle
  how many of S13's 15 improvements are real (claim 115).
- **Does recording *why* an experiment was tried improve the next hundred?** S13 records only what
  changed and what happened [S13 `g1`]. The addition costs one column; the effect is unmeasured
  anywhere this brain has seen.
- **How do you parallelise a git-as-database loop?** Two agents on two GPUs produce two branch tips
  editing the same constants, which do not merge [S13 `g2`]. S13 hints at one-agent-per-GPU in a
  branch name and designs nothing.
- **Does the reporting-path leak (claim 113) matter empirically**, or only as a principle? No source
  here has observed an agent exploiting it.
- ~~**Where does this shape stop working?** Everything in S13 depends on "better" being one number a
  frozen function computes. Most research questions worth automating do not have that, and this
  brain holds nothing on the case where the accept decision is a judgement.~~ **Partly closed
  2026-08-04 by S14**, which names the constraint and generalises it: the loop runs at exactly the
  rate its verifier can distinguish good output from bad, so where the accept decision is a
  judgement rather than a number, the loop stalls on human attention (claim 124,
  [`self-improvement.md`](self-improvement.md)). **Still open is the interesting remainder** - what a
  loop should *do* in that case, since "wait for a human" is a description of the problem rather than
  a design.
- **Conflict to watch, not yet a contradiction:** claim 119 (suppress the check-in) sits against
  claim 16 from S2 (make contacting a human a tool call among the others). They are reconcilable -
  S2's agents act in the world, S13's acts on a branch - but the *condition* that separates them is
  this brain's reading, not either source's, and a second source on unattended loops should be
  checked against it.

## Sources feeding this topic

- **S13** - [`karpathy/autoresearch`](../../sources/260803_autoresearch/LEARNING.md) (Andrej
  Karpathy, code, snapshot `228791f`, 2026-03-26). The primary and currently only source. An agent
  is given one editable training script, a five-minute budget, a protected metric and an instruction
  never to stop; it hill-climbs overnight. Contributes the four freezes, the git-as-database
  pattern, the untracked-ledger rule, the per-iteration context budget, and the noise finding.
  **⚠️ T4 personal repository. The design is fully inspectable and the docs-versus-code gate passes
  on every design claim; the results are one PNG whose underlying ledger is untracked by design and
  absent from the repo, so nothing empirical here is reproducible. No code was executed by this
  brain (no GPU). No deep-research pass has been run - this note contains no external evidence at
  all.**
- **S14** - [Stanford CS329A: Self-Improving AI Agents, lecture 1](../../sources/260804_cs329a-self-improving-agents/LEARNING.md)
  (video, 2026-08-03). **Cross-reference, not counted as a primary source for this note** - it works
  a different layer (a model improving its own weights, not an agent improving an artifact), and its
  claims are filed in [`self-improvement.md`](self-improvement.md) under
  [ADR-0018](../decisions/0018-self-improvement-topic.md). Two things reach here.
  **First, the frame that explains claim 114**: verification sets a loop's ceiling, so S13's accept
  rule banking a random-seed change is not a quirk of that repository but the general failure of a
  verifier with no notion of variance. **Second, a second instance of the shape** - the AI Scientist
  pipeline (Lu et al, 2024) runs idea generation, an experiment iteration loop, and paper write-up,
  and terminates in a box reading "LLM Paper Reviewing" [S14 `n10`, `frame_3420`]. That is
  **mention-level evidence under [ADR-0012](../decisions/0012-a-mention-is-not-a-source.md)** - a
  lecture slide about someone else's paper, not an ingest of it - and the paper itself is on
  [`reading-list.md`](../reading-list.md) as the obvious second primary for this note.
