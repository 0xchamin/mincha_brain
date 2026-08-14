# Results - agent runtime boundaries

> **Read [`PREDICTIONS.md`](PREDICTIONS.md) first.** It was committed in `f53b44b`, before any code
> in this directory existed, and `git log` is the proof. Nothing below was written before the runs.

| Field | Value |
|---|---|
| Ran | 2026-08-15 |
| Environment | Python 3.12.12, SQLite 3.51.0, macOS 26.5.2, arm64 |
| Under test | a ~230-line reimplementation in [`harness.py`](harness.py) - no model, no network, no key |
| Tests what | whether four **mechanisms** are real and reachable |
| Tests **nothing** about | Hermes, or S24's accuracy. See [ADR-0024](../../brain/decisions/0024-experiments-layer.md) |

## The headline

Two questions S24's `LEARNING.md` recorded as unanswered now have answers, for a system of this
shape. **Two gateway processes sharing one `state.db` keep perfect database integrity and lose
semantic integrity completely**, and **parallel tool results reorder against their side effects in
about one run in eight with no artificial delay at all**.

A third result was not a question anyone had asked, and is the most useful thing here. **The delivery
ledger closes one window and leaves an adjacent one wide open**, so "at-least-once delivery" and
"at-least-once side effects" are two different guarantees and only one of them was purchased.

## Case 01 - transcript order against side-effect order (claim 189)

Two tools dispatched concurrently, each appending one line to a shared file, results restored in
model-call order. N = 200 per condition.

| Condition | Predicted | Observed | Verdict |
|---|---|---|---|
| (a) realistic work, no delay | 5-40%, "genuinely unsure" | **12.0%** (24/200) | hit, but see the self-criticism below |
| (b) jittered work, <= 3ms | ~50% | **49.0%** (98/200) | hit |

**What it establishes.** The reordering is reachable without anybody inserting a sleep. Ordinary file
I/O across two threads diverged once every eight runs, which means `n14`'s disclaimer describes
something a real system meets by accident rather than a theoretical possibility. **A test suite that
ran this case once and saw agreement would have concluded the opposite**, which is the practical
argument for claim 114's noise floor.

**What it does not establish.** Nothing about how often this bites in production, where tools do more
than append a line, and nothing about any real runtime. The 12% is a property of this harness on this
machine.

## Case 02 - two processes, one `state.db` (claim 191)

The case this experiment was built for, because S24 recorded that nobody had reported it. 40 turns per
process, two OS processes, one session key, WAL plus a 10-second busy timeout.

```
rows written .......... 80 / 80 expected
distinct turn numbers . 40
TURN COLLISIONS ....... 40
final sessions.turn ... 40  (would be 80 if no lost updates)
LOST UPDATES .......... 40
worker: proc-A busy=0 blocked=0
worker: proc-B busy=0 blocked=0
```

| Question | Predicted | Observed |
|---|---|---|
| Integrity - does SQLite lose or corrupt rows? | no corruption, zero `SQLITE_BUSY` | **exactly right.** 80/80 rows, 0 busy errors |
| Exclusion - does the in-memory guard exclude across processes? | zero | **zero.** Neither worker blocked once |
| Semantics - do logical turns collide? | "collisions in the majority of concurrent bursts" | **worse. Every single turn collided** - 40 distinct numbers across 80 rows, each written exactly twice, and half the increments lost |

**This is the sharpest result of the four, and the magnitude exceeded the prediction.** The database
did its job flawlessly and the conversation was still corrupted. Both processes read turn *n*, both
wrote turn *n+1*, and SQLite serialised those writes perfectly - which is exactly the behaviour that
makes it invisible. There is no error, no exception, no busy timeout, and no log line. The only
evidence is that the transcript's own numbering is duplicated end to end.

**It settles that `n9`'s distinction has teeth.** S24 insists a database concurrency rule and a
gateway semantic rule are different things. They are, and the gap between them is total: perfect
storage integrity bought exactly zero semantic integrity. A reviewer who reads "SQLite serialises
writers, and we retry on contention" and concludes the conversation is safe has made a real error.

**What it does not establish.** That any shipping system does this. The harness deliberately performs
a naive read-modify-write with a 2ms gap, which is the shape a runtime has when its only mutual
exclusion is the in-memory guard. A runtime using an atomic `UPDATE ... SET turn = turn + 1` or a
conversation-scoped lease would not behave this way, and the experiment says nothing about which
Hermes does.

## Case 03 - crash between the side effect and the reply (claim 190, `n19`)

N = 25 per row. The process is killed with `os._exit(9)`, so nothing unwinds.

| Kill point | Recovery | Predicted | Observed |
|---|---|---|---|
| after commit, before send | naive | 100% duplicate | **100%** (25/25) |
| after commit, before send | ledger | 0% duplicate | **0%** (0/25) |
| **after the side effect, before commit** | ledger | 100% duplicate | **100%** (25/25) |

**The third row is the finding, and it was not in anyone's open questions.** The ledger works exactly
as advertised in the window it covers and is powerless one step earlier. Killed before the transcript
commits, there is no record the tool ever ran, so the only available recovery is to rerun the task,
and the irreversible thing happens twice. The ledger cannot help because **the evidence it reasons
over is written after the effect it is protecting**.

That sharpens `n19` and claim 190 into something more useful than "at-least-once, not exactly-once":

> A delivery ledger converts *an invisible failure* into *a visible ambiguity* for the
> **commit-to-send** window only. The **effect-to-commit** window keeps the original failure mode
> intact, and no amount of delivery bookkeeping touches it. Closing it needs the effect and its
> record to commit together, or the tool to be idempotent.

## Case 04 - resume into a workspace that moved (claim 187)

| Tool layer | Resume | Tool outcome | Loud? |
|---|---|---|---|
| strict (refuses a missing directory) | succeeded | refused | **yes** |
| forgiving (`makedirs(exist_ok=True)`) | succeeded | **wrote to a recreated directory** | **no** |

Exactly as predicted, and the conditional resolves the way the prediction guessed. **Claim 187's
sting - that the failure "presents as success" - is a property of the tool layer's forgiveness, not
of the architecture.** The session resumed correctly in both cases with an intact transcript. What
decided whether the operator ever found out was one `exist_ok=True`.

That makes the mitigation narrower and more actionable than "confirm the workspace before allowing
tools to act". The cheaper version is **do not let tools create their own working directory**, which
converts a silent wrong-place write into a loud refusal at no cost.

## Self-criticism, which matters more than the results

**Every prediction hit, and that is a criticism of the predictions rather than a triumph.** A
prediction set with no misses was probably written safe. Three specific admissions:

1. **The 5-40% band on case 01(a) was too wide to be a real prediction.** `PREDICTIONS.md` says so
   itself in advance, which is honest, but flagging a weak prediction does not make it strong. A
   falsifiable version would have named a point estimate. The genuinely informative half of that case
   is that the answer is not 0%, and I should have predicted *that* and nothing else.
2. **Case 02's magnitude was a partial miss in the direction of understatement.** "Collisions in the
   majority of concurrent bursts" is much weaker than what happened, which was total collision. Being
   wrong by being too cautious is still being wrong, and it is the direction that makes a finding look
   less interesting than it is.
3. **Two of four cases were labelled demonstrations in advance and behaved like demonstrations.**
   They earned their place by quantifying a window (case 03's third row) rather than by discovering a
   mechanism, and a reader should weight them accordingly.

**The deeper limit applies to all four.** I wrote the harness, the predictions and the assertions.
The assertions are deterministic functions over files and rows rather than judgements, which is
claim 164's protection and the reason these numbers are worth anything at all. It is not a substitute
for someone else running it.

## What changed in the brain

- S24's open question *"nobody has reported what actually happens when a second gateway process runs
  against one `state.db`"* - **answered for a system of this shape**, and struck through with a
  pointer here.
- S24's open question *"is transcript order is not side-effect order ever actually observed to
  bite?"* - **answered: yes, 12% of runs with no artificial delay**, struck through with a pointer.
- `n19` and claim 190 gain the **effect-to-commit window**, which no source stated.
- Claim 187 gains the refinement that its silence is a **tool-layer property**.
- **No node's gate verdict changed and no claim's confidence rose.** Per ADR-0024 an experiment
  cannot corroborate the source that suggested it, and nothing here is evidence about Hermes.

## Reproducing

```
cd experiments/260815_runtime-boundaries
python3 cases/01_tool_order.py       # ~2s
python3 cases/02_two_writers.py      # ~4s
python3 cases/03_crash_delivery.py   # ~20s
python3 cases/04_stale_workspace.py  # instant
```

Stdlib only. Case 01 and case 02 are nondeterministic by design and the exact percentages will move;
if case 01(a) ever reports 0/200 or case 02 reports zero collisions, that is a finding worth chasing
rather than a flake.
