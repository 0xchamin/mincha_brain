# Knowledge nodes - Harness Design for Long-Running Application Development

> Persona: **fact-checker** - re-adopt when working this file.

> The atomic units of knowledge extracted from this source. Each node has a **stable ID** (`n1`,
> `n2`, ... - never renumber; topic notes reference these), a claim, **both legs each with its own
> citation** (or one leg marked `single-leg`), a gate verdict, and a confidence. Only
> `corroborated`/`single-leg` nodes (and recorded `divergence` findings) feed `LEARNING.md` and get
> promoted to `../../brain/`. The **fact-checker** persona owns the verdicts; see `../../AGENTS.md`
> and `prd.md` §6.

Citations are `S4, §N <section name>` against the original article (URL in `SOURCE.md`), **not**
against the derived outline in `raw/`.

## Gate note - read before trusting a verdict here

**The visual leg was skipped** (see `SOURCE.md`), so this source cannot produce a figure-vs-text
corroboration. Two verdicts are therefore in play:

- **`single-leg`** - the prose asserts it and nothing else in the article checks it. This is most of
  the file, and it is the honest verdict for every *conceptual* claim.
- **`corroborated (table)`** - a **numeric** claim where the article's own table states the same
  figure as the prose. This is a real second leg in the blog sense (`prd.md` §5.2: keep a figure when
  the surrounding text agrees) and it catches misreading - **but it is one author agreeing with
  himself in two renderings**, far weaker than a slide matching independent narration. It raises
  confidence in *extraction*, not in the number's truth.

**Nothing here is externally corroborated.** All figures are self-reported, n=1 per configuration,
from a **T2 vendor source** writing about its own models.

## Nodes

| ID | Claim (crux) | Evidence leg + citation | Corroborating leg + citation | Gate | Confidence |
|---|---|---|---|---|---|
| n1 | **Prompt engineering has a ceiling that architecture breaks.** Prior long-running-agent work plateaued despite continued prompt improvement; splitting one agent into a generator and a separate evaluator moved the ceiling. | prose, S4 §1 Introduction | (none - no figure) | single-leg | needs-check |
| n2 | **Separating creation from evaluation is more tractable than making one agent self-critical**, and the gap is widest on subjective work where no binary check exists. Borrowed from GAN architecture. | prose, S4 §1 | (none) | single-leg | needs-check |
| n3 | **Self-evaluation bias is the mechanism:** agents asked to judge their own output confidently praise it even when a human sees the quality as obviously mediocre. | prose, S4 §2 Why naive implementations fall short | (none) | single-leg | needs-check |
| n4 | **The fix for subjectivity is question design, not model capability.** "Is this design beautiful?" grades inconsistently; "does this follow our design principles?" supplies concrete criteria. Rubrics beat taste. | prose, S4 §2 | criteria table, S4 §3 (four named criteria with definitions) | corroborated (table) | OK |
| n5 | **"Context anxiety":** during long tasks a model may prematurely wrap up work as it approaches its *perceived* context limit - a behavioural failure, distinct from actually exhausting the window. | prose, S4 §2 | (none) | single-leg | needs-check |
| n6 | **Compaction and context reset are not interchangeable.** Compaction summarises in place and preserves continuity but does **not** remove context anxiety; a reset clears the window and does, at the cost of orchestration and a handoff artifact carrying enough state to resume cleanly. | prose, S4 §2 | (none) | single-leg | needs-check |
| n7 | **The remedy is model-dependent and therefore dated.** Sonnet 4.5 required resets; Opus 4.5 largely eliminated the behaviour natively. | prose, S4 §2 | (none) | single-leg | **needs-check - model-version-bound** |
| n8 | **Giving the evaluator a browser changes what it can grade.** With Playwright MCP the evaluator navigated, screenshotted and interacted with the live page before scoring, rather than reading source code. | prose, S4 §3 and §4a | (none) | single-leg | needs-check |
| n9 | **Prompt wording steers aesthetics more than expected** - a phrase like "museum quality" pulled an entire run toward one look. | prose, S4 §3 | (none) | single-leg | needs-check |
| n10 | **Iterative improvement is real but non-monotonic:** scores rose across 5-15 iterations, yet a middle iteration was sometimes preferred over the last. Complexity grew as the generator became more ambitious. | prose, S4 §3 | (none) | single-leg | needs-check |
| n11 | **The three-agent split is planner / generator / evaluator**, communicating **through files** so state survives handoffs. The planner expands a 1-4 sentence prompt into ~16 features across 10 sprints and stays at deliverable level rather than implementation detail. | prose, S4 §4a Architecture | (none - **the article has no architecture diagram**) | single-leg | needs-check |
| n12 | **Sprint contract negotiation:** generator and evaluator agree what "done" means *before* coding - the bridge from a high-level spec to a testable implementation. | prose, S4 §4a | (none) | single-leg | needs-check |
| n13 | **Hard thresholds, not weighted averages:** any criterion below threshold fails the sprint, so a strong score elsewhere cannot mask a specific failure. | prose, S4 §4a | (none) | single-leg | needs-check |
| n14 | **Out-of-the-box Claude is a poor QA engineer.** It took several tuning rounds, driven by reading logs, to make the evaluator catch subtle bugs, probe edge cases, and stop being lenient toward AI-generated output. | prose, S4 §4a | QA examples table, S4 §4a (three worked sprint failures with root causes) | corroborated (table) | OK |
| n15 | **The measured baseline: solo 20 min / $9 vs full harness 6 hr / $200** on the same 2D game-maker prompt - roughly **18x wall clock and 22x cost**. | prose, S4 §4b Baseline comparison | comparison table, S4 §4b | corroborated (table) | OK (extraction); **needs-check (n=1)** |
| n16 | **The solo run's failure was categorical, not cosmetic:** the game was fundamentally broken - entities rendered but did not respond to input, the entity-to-runtime wiring disconnected, with nothing on screen indicating it. The harness run had a working core loop. | prose, S4 §4b | (screenshots exist but were **not** analysed - see `SOURCE.md`) | single-leg | needs-check |
| n17 | **Every harness component encodes an assumption about what the model cannot do on its own, and those assumptions are worth stress-testing.** The article's most transferable line. | prose, S4 §4c Iterating on the harness | (none) | single-leg | needs-check |
| n18 | **On a stronger model, scaffolding was removed rather than added.** With Opus 4.6 the **sprint construct was deleted entirely** and the evaluator moved from per-sprint to a single end-of-run pass; the model then ran coherently for **2+ hours** unscaffolded. | prose, S4 §4c | (none) | single-leg | needs-check |
| n19 | **Whether a component is load-bearing depends on where the task sits relative to the model's capability boundary** - not on the component's merit. As the boundary moved outward, the evaluator became optional overhead on simple tasks while retaining value on complex ones. | prose, S4 §4c | (none) | single-leg | needs-check |
| n20 | **Method finding: remove one component at a time.** Radical simultaneous cuts failed; methodical single-component removal worked. | prose, S4 §4c | (none) | single-leg | needs-check |
| n21 | **The evaluator kept earning its place even on the improved model:** QA rounds on the DAW build found core features shipped as display-only stubs (R1) and audio recording still stubbed (R2) - genuine last-mile gaps the self-grading generator had missed. | prose, S4 §5 Updated harness results | cost/duration table, S4 §5 (three build+QA rounds) | corroborated (table) | OK |
| n22 | **The V2 harness run: 3 hr 50 min / $124.70 total**, of which the planner was 4.7 min / $0.46 and QA across three rounds ~25 min / ~$10 - i.e. **QA was roughly 8% of cost and caught the stub failures.** | prose, S4 §5 | full phase-by-phase table, S4 §5 | corroborated (table) | OK (extraction); **needs-check (n=1)** |
| n23 | **A modality gap bounds what QA can grade: Claude cannot hear**, so the DAW's musical quality could not be evaluated - the harness could verify that audio *ran*, not that it *sounded* good. | prose, S4 §5 | (none) | single-leg | needs-check |
| n24 | **Improving models move the harness problem rather than dissolving it.** Better models unlock longer and more complex tasks, which opens new harness combinations - so the space of useful designs shifts rather than shrinking. | prose, S4 §6 What comes next | (none) | single-leg | needs-check |

## Dropped / divergences (audit trail)

| Candidate | Verdict | Note |
|---|---|---|
| All 8 screenshots | **not analysed** | Outcome screenshots of generated apps; no explanatory diagram exists in the article. Skipped per `SOURCE.md` - the blog analogue of ADR-0003. This is what makes nearly every node above `single-leg`. |
| Decorative header SVG | dropped | Branding. |
| Dutch-museum "3D room" example (§3) | kept in `LEARNING.md`, **not a node** | One vivid qualitative anecdote (an iteration 9 -> 10 creative leap). Illustrative, not a claim that can be gated or promoted - and exactly the kind of n=1 story that reads as evidence without being any. |
| Tech stack (React, Vite, FastAPI, SQLite/PostgreSQL) | **not promoted** | Source-specific trivia. The kit promotes transferable concepts, not one team's stack choice. |

## Tension worth recording (not a divergence within this source)

**`n18`/`n19` sit against `brain/claims.md` claim 24**, which holds - from a T3 preprint measuring 10
models - that decomposition delivers **+13.1 to +41.5 pp** reliability on long-horizon tasks. This
source *removed* decomposition (sprints) on a stronger model and reports improved efficiency with
maintained performance.

**They do not actually contradict, and the reconciliation is the interesting part:** claim 24 measures
decomposition *at a fixed model capability*, while `n19` says the value of any scaffold is a function
of where the task sits relative to that capability. **Decomposition helps until the boundary moves
past your task.** Recorded in `brain/topics/agents.md` as a refinement rather than a conflict - but
note the asymmetry of evidence: one side is a 10-model measured study, the other a vendor's n=1
report. If they *did* conflict, claim 24 would carry more weight.
