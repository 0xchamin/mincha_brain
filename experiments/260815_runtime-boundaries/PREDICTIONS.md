# Predictions - agent runtime boundaries

> **Written and committed before any code in this directory existed.** `git log` is the proof. See
> [ADR-0024](../../brain/decisions/0024-experiments-layer.md) for why that ordering is mandatory
> rather than stylistic.

**What is under test.** A minimal agent runtime written for this experiment - SQLite, a session
table, a transcript table, a delivery ledger, a tool runtime that can dispatch concurrently. **No
model, no network, no API key**, which is possible because the claims being tested are all about the
runtime rather than about inference. That is itself claim 194 taken at its word.

**What this cannot establish, restated so it cannot be forgotten.** Nothing here is evidence about
Hermes or about S24's accuracy. A reimplementation tests whether a **mechanism** is real and
reachable. If a case fires, the finding is "this failure mode is reachable in a system shaped this
way", never "Hermes has this bug".

**Honesty about case strength.** Two of the four below are genuine tests whose outcome I cannot
predict. Two are closer to demonstrations, where the mechanism is near-certain and the *quantity* is
the only open part. They are labelled, because presenting a demonstration as a test is the exact
dishonesty this layer was created to avoid.

---

## Case 01 - transcript order against side-effect order (claim 189)

**Strength: genuine test.** The interesting variant has an outcome I do not know.

Two tools are dispatched concurrently. Each appends a line to one shared external file, which stands
for a side effect on the world. Their results are then restored into the transcript in **model-call
order**, as S24 describes. The question is whether the file order and the transcript order agree.

Run in two conditions, N = 200 each:

- **(a) realistic work, no artificial delay.** Each tool does ordinary file I/O and returns.
- **(b) jittered work**, a random sleep up to a few milliseconds inside each tool.

| | Prediction | What would falsify it |
|---|---|---|
| (a) | Divergence occurs but is **uncommon**, somewhere in **5-40%** of runs. I am genuinely unsure; thread scheduling around I/O is nondeterministic, and it is equally plausible that dispatch order dominates and it is near 0% | **0 divergences in 200 runs.** That would mean the concern is unreachable without deliberate delay, which weakens claim 189's practical bite while leaving its logic intact |
| (b) | Divergence approaches **50%**, because jitter swamps dispatch order | Anything below 20% would mean something is serialising the tools that I did not intend, and the harness is wrong rather than the claim |

**Why (a) is the one that matters.** A claim that only fires when you insert sleeps is a claim about
sleeps. If ordinary I/O reorders, the disclaimer in `n14` is describing something a real system meets
by accident.

## Case 02 - two processes, one `state.db` (claim 191)

**Strength: genuine test, and the reason this experiment exists.** S24's `LEARNING.md` records
directly that *"nobody has reported what actually happens when a second gateway process runs against
one `state.db`"*.

Two **separate OS processes** each run a gateway holding an in-memory active-run guard, and both
handle messages for the **same session key** against one SQLite file in WAL mode with a busy timeout.
Each turn does a read-modify-write: read the current turn number, do a little work, append a
transcript row.

| | Prediction | What would falsify it |
|---|---|---|
| Mutual exclusion | The in-memory guard provides **exactly zero** cross-process exclusion. Certain, since it is per-process state, and it is stated only so the run is complete | Any observed exclusion, which would mean the harness accidentally shares state |
| Database integrity | **No corruption and no lost rows.** SQLite serialises writers, and with a busy timeout I expect **zero** `SQLITE_BUSY` failures | Corruption, or dropped rows, would be a finding about SQLite rather than about agents |
| **Semantic integrity** | **This is the real question and I predict it breaks.** Turn numbers collide or interleave, because SQLite serialises the *write* and not the *logical turn* - two processes both read turn 5 and both write turn 6. I expect **collisions in the majority of concurrent bursts** | **A perfectly ordered, collision-free transcript.** That would mean SQLite's serialisation incidentally supplies the semantic guarantee, and claim 191's practical risk is materially lower than its logic suggests |

**Why the outcome is not obvious.** The article's `n9` insists a database concurrency rule and a
semantic concurrency rule are different things. This case is a direct test of whether that
distinction has teeth or is a distinction without a difference at this scale.

## Case 03 - crash between the side effect and the reply (claim 190, `n19`)

**Strength: demonstration for the first window, genuine test for the second.**

A tool performs an external side effect (append to a file), the transcript commits, and the process
is then killed before delivery completes. Recovery runs in two modes, and the kill point moves.

| Kill point | Recovery | Prediction | What would falsify it |
|---|---|---|---|
| After commit, before send | **naive** ("no reply recorded, so rerun the task") | Side effect duplicated in **100%** of runs. Near-certain; the value is quantifying it | Any run that does not duplicate |
| After commit, before send | **ledger** ("an obligation exists, so retry delivery only") | Duplicated in **0%** of runs | Any duplicate would mean the ledger does not do its job |
| **After the side effect, before the transcript commits** | **ledger** | **The ledger also duplicates, in 100% of runs.** There is no record the tool ever ran, so recovery cannot know | **0% duplication**, which would mean the ledger closes a window I believe it structurally cannot |

**The third row is the point of this case.** If it holds, the finding sharpens `n19` and claim 190:
the delivery ledger closes the **commit-to-send** window and leaves the **effect-to-commit** window
wide open, so "at-least-once delivery" and "at-least-once side effects" are two different
guarantees and only one of them was bought.

## Case 04 - resume into a workspace that moved (claim 187)

**Strength: demonstration, with one conditional worth resolving.**

A session is bound to a working directory, the directory is moved away, and the session is resumed
and asked to run a tool.

| | Prediction | What would falsify it |
|---|---|---|
| Resume | Succeeds. The transcript is intact and the conversation continues normally | Failure to resume, which would mean workspace and session are coupled |
| The tool | **Depends on the runtime's forgiveness, and that is the finding.** A strict tool raises and the failure is loud. A tool that creates missing directories, or falls back to the process working directory, writes to the wrong place **silently** | If a strict implementation also failed silently, the claim would be stronger than stated |

**The refinement being tested** is that claim 187's sting - "presents as success" - is **not a
property of the architecture** but of how forgiving the tool layer is. If that holds, the mitigation
is narrower and more actionable than "confirm the workspace": it is *do not let tools create their
own working directory*.

---

## What I expect to be wrong about

Recording this in advance, because a prediction set with no expected misses is a prediction set
written to be safe. **My least confident number is Case 01(a)**, where I have given a range so wide
it is nearly unfalsifiable in one direction, and I expect the true answer to sit outside 5-40% rather
than inside it. **My most likely outright miss is Case 02's database-integrity row**, where I may be
wrong about `SQLITE_BUSY` under a busy timeout with two writers hammering one file.
