# Topic: Autonomous research loops

**Status:** emerging (1 primary source - **S13** `karpathy/autoresearch`), created 2026-08-03 by
[ADR-0017](../decisions/0017-autonomous-research-loops-topic.md).
**Basis:** one source, and it is a **T4 personal repository** whose design is fully inspectable and
whose *results* are a single unreproducible PNG. The design claims are strong (code read against its
own docs, gate passing on every one); the empirical claims are weak by construction and are labelled
so throughout. **This note is a candidate for merge back into [`agents.md`](agents.md) if no second
primary source arrives** - the trigger is recorded in ADR-0017 rather than left to be re-derived.

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
- **Where does this shape stop working?** Everything in S13 depends on "better" being one number a
  frozen function computes. Most research questions worth automating do not have that, and this
  brain holds nothing on the case where the accept decision is a judgement.
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
