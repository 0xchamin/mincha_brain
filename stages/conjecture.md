# Stage: `/conjecture` - the generative pass

> Abduction across the whole brain, into `brain/conjectures.md`. **Triggered by the user, never automatic.**
>
> **This file is the contract for this stage.** It was extracted verbatim from `AGENTS.md`
> on 2026-08-15 ([ADR-0027](../brain/decisions/0027-stage-specs-leave-the-contract.md)) so that a
> spec needed once a fortnight stops occupying every session's context window. **`AGENTS.md`
> remains the root contract** and this inherits every global rule in it; where the two
> disagree, `AGENTS.md` wins and this file is the bug.

## Conjecturing on request (`/conjecture` - the generative pass)

> **Why this exists.** The kit does two of the three moves. It **gathers** (ingest, gate) and it
> **reconciles** (dream). What it has never done deliberately is **abduce** - propose an explanation
> the sources jointly imply and none of them states.
>
> It has happened by luck. Claim 93 exists because an ingesting agent noticed S5, S10 and S11 saying
> the same thing about metadata in three unrelated domains. **Nothing in the kit asks that question
> on purpose**, so the answer arrives only when someone happens to trip over it.
>
> **And dreaming will not do it.** Its eight classes are all coherence - contradiction, duplication,
> stale confidence, orphans. Adding "also invent things" gives that pass two objectives, which is
> claim 59 exactly. Generation gets its own invocation, for the same reason curation did.

**The name is doing work.** A *conjecture* is explicitly unproven. Given that the failure mode here
is confabulation dressed as insight, a word that says "not yet believed" is worth more than one that
sounds like a finding.

**Trigger (never automatic).** The user says **"conjecture"** or runs `/conjecture`, optionally
scoped to a topic. Adopt **synthesizer** (cross-source combination is its job) - **not**
fact-checker, and the reason matters: see "What this pass may not do" below.

### What it reads, and what it looks for

Read **the whole brain** - `brain/claims.md`, every `brain/topics/*.md` including their **Open
questions**, `INDEX.md`, and prior notes in `brain/conjectures.md`. You cannot combine what you have
not seen.

**Generate from tension, not from agreement.** Two agreeing claims usually yield a restatement. The
productive pairs, in rough order of yield:

| Pattern | Why it generates |
|---|---|
| Claims in **different topics sharing a mechanism** | The shape is the finding. Claim 93 came from exactly this |
| A `corroborated` claim against a `needs-check` one **on the same subject** | The gap between what is measured and what is believed |
| A claim plus an **open question from a different topic** | The question may already be half-answered elsewhere in the brain |
| Claims in **quiet tension** that nobody flagged as a contradiction | Dreaming catches flagged conflicts; this catches unflagged ones |
| **A structural gap in the brain's own shape** | Not "the source did not say X" - that is an Open question, inherited. This is *"we hold three claims about identity propagation and none about revocation"*: an absence no source flagged, visible only from above |
| **Cross-domain transfer: import a shape from a dense topic into a thin one** | Does claim 59's objective-conflict argument apply to security review? Does claim 34's producer/grader split? **This generator needs the *other* topics established, not the target one** - so it works best exactly when coverage is uneven |
| A claim plus a **structural feature of this kit** | The brain is a live instance of several of its own claims |

> **Do not wait for coverage to run this.** An earlier version of this section implied the pass gets
> better as the brain broadens, which is breadth-biased and wrong for anyone going *deep* in one
> area. **Depth feeds the last three patterns above harder than breadth does** - two sources that
> disagree about the same thing generate sharper conjectures than two unrelated ones, a thin topic
> beside a dense one is where a structural gap is most visible, and cross-domain transfer needs the
> *source* topic established rather than the target. There is no threshold to wait for.

**Do not enumerate pairs.** At 100+ claims that is 5,000+ combinations and the pass drowns. Follow
the patterns above, follow curiosity, and stop when the yield drops.

### The one hard rule: a conjecture names its own falsifier

**This is the filter that separates the stage from a confabulation engine, and it is not optional.**
Every conjecture states, in this order:

1. **The claim IDs it combines** - checkable, so a reader can reconstruct the leap.
2. **What it asserts that no combined claim states alone.** If you cannot say this in one sentence,
   it is a restatement.
3. **What evidence would prove it wrong.** Concrete enough to look for.
4. **Whether that evidence plausibly exists** - a published study, a benchmark, an ablation someone
   could run. A conjecture nobody could ever test is philosophy, and belongs elsewhere.

> **If it cannot name a falsifier it is not a conjecture, it is an observation** - and observations
> already have homes: a topic note's synthesis, or its Open questions.

### What this pass may **not** do

- **It may not judge whether a conjecture is true.** It cannot: that needs external evidence, and
  fetching it is `/research`'s job. This pass only checks that a conjecture is **well-formed**.
  **That separation is deliberate** - it means the producer never grades its own work (claim 34),
  and the gate that kills a conjecture is always a different invocation.
- **It may not write to `brain/claims.md`.** A conjecture is not a claim and must never be cited as
  one. It lives in its own register until research resolves it.
- **It may not edit a `nodes.md`, a `LEARNING.md`, or a topic note's claims.** It proposes; it does
  not promote.

### Output, and the lifecycle

**One register: `brain/conjectures.md`**, following `claims.md`'s shape - stable IDs (`h1`, `h2`,
never renumbered), a status column, append-only in spirit. Not per-pass notes, because a conjecture
has a *lifecycle* that a dated log handles badly.

| Status | Meaning | Next |
|---|---|---|
| `open` | Well-formed, untested | A `/research` target |
| `supported` | Independent external evidence agrees | **Promote to `brain/claims.md`** with the external citation and tier; retire the conjecture |
| `refuted` | Credible evidence disagrees | **Keep it.** A killed conjecture is a real result and stops it being re-proposed |
| `no-evidence` | Researched, nothing credible either way | Say so. That the field has not asked is itself a finding |

**Discarded at generation** gets its own section in the same file, with the reason - almost always
"no falsifier" or "restates claim N". **A pass that records only its winners is cherry-picking**, and
the audit trail is what makes this scientific rather than decorative. Same discipline `nodes.md`
already applies to dropped candidates.

Then run `python3 validate.py` and show the `git diff`.

### Honesty rules

- **Most conjectures will be wrong, and that is the process working.** Do not optimise for hit rate:
  a pass judged on how many survive will produce safe restatements, which is the one output with no
  value at all.
- **Three good conjectures beat thirty plausible ones.** Volume is the failure mode, not the goal.
- **"Nothing new this pass" is a legitimate result** and gets recorded. It usually means no source
  has arrived since the last pass that could combine with anything.
- **Never launder a conjecture into a claim by citing it.** Prose elsewhere in the brain may
  reference `h3` *as a conjecture*, never as evidence.
