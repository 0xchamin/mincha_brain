# Verification log - LLM Wiki (S8)

> Persona: **fact-checker**, alone. Appended per pass, never rewritten. See `../../AGENTS.md`
> § "Verifying one source on request" for what the six checks are and what the verdicts mean.

---

## Pass 1 - 2026-08-15

| Field | Value |
|---|---|
| Read | `nodes.md` (n1-n18, `d1`, the gate note, the dropped-candidates table, the ADR-0009 post-mortem), `LEARNING.md` (535 lines), `SOURCE.md`. **No topic notes read.** |
| Frames | **`n/a` (no visual leg)** - `visuals/` contains only its `README.md`. The source is ~1,960 words of prose with no figures, diagrams, code, data or worked example, so check 6 has nothing to run against and costs nothing. |
| Independence | **Compromised, and this is the honest reason to weigh this pass lower than a clean one.** This ran in the **same session** that ingested S26 (`260815_llm-knowledge-bases`), a talk *about* this gist. That session read **all of S8's `nodes.md` in full** before writing S26's gate, and disclosed it there. Two specific biases follow. **First**, I arrived holding a prior position on `n4`: S26's `d1` was derived by holding `n4`'s immutability rule against S26's frames, so I have already argued about what `n4` means and cannot claim a fresh reading of the sentences citing it. **Second**, the S26 gate re-read `n1`, `n2`, `n8` and `n13` closely for the same reason. `LEARNING.md` and `SOURCE.md` were **not** read in that session and were read fresh here, which is the one thing working in this pass's favour. **The kit's own rule says use a different session and I recommended exactly that**; the human invoked it here anyway, which is their call to make. **Treat the `n4`, `n1`, `n2`, `n8` and `n13` verdicts below as the weakest in this entry**, and a re-run from a cold session is worth more than it would normally be. |
| Findings | **2** - 1 `defect` (fixed in this pass), 1 `judgement` (proposed, not applied). Checks 1, 2, 4 and 5 clean; check 6 `n/a`. |

### Check 1 - does each cited node actually support the sentence citing it?

**Clean.** Every node ID in `LEARNING.md` was traced to its row in `nodes.md`: `n1`-`n5`, `n7`-`n11`,
`n13`-`n17` and `d1` across the TL;DR, the 1-minute version and its table, Key claims, the ten
walkthrough sections, the mental-model provenance line, "What to distrust" and Open questions. No
citation drift found - this is the `claim 33` class of failure and it does not occur here.

Two that were checked closely rather than waved through, because they are the two doing the most
inferential work:

| Sentence | Node | Verdict |
|---|---|---|
| §5: "an ingest may *weaken* the existing synthesis" | `n3` | **Supported.** `n3` quotes "noting where new data contradicts old claims, **strengthening or challenging** the evolving synthesis". "Weaken" is a fair reading of "challenging", and the note does not overstate it into "will weaken". |
| Key claims: "An index file **replaces** embedding RAG at ~100 sources" | `n10` | **Supported and correctly flagged.** `n10` says "avoids the need for embedding-based RAG infrastructure". "Replaces" is marginally stronger than "avoids the need for", and the bullet carries a ⚠️ and "unmeasured, do not cite as a result" in the same breath, so no reader takes it as settled. Not filed. |

The §7 ADR-0009 post-mortem table in `LEARNING.md` reproduces `nodes.md`'s own verdict table
(`n4` holds, `n6` holds, `n8` does not hold) **without alteration**, including the direction of the
overturn. That is the highest-consequence citation in the file and it is exact.

### Check 2 - is anything the prose presents as settled gated `single-leg` or `needs-check`?

**Clean, and unusually well handled.** Every node in this source is `single-leg`/`needs-check` with no
exceptions, which is the hardest configuration to write honestly, because a note where *everything* is
weak invites the writer to stop saying so. This one states it three times at increasing depth - the
preamble ("**Every node here is `single-leg`, `needs-check`, without exception** - and nothing may be
retro-marked `corroborated` later"), the trust-summary bullet, and the ⚠️ blocks at the point of use.

The one paragraph worth naming as *not* a finding: §6's second-order effect about two people producing
different wikis from the same hundred sources. It could have been slipped in as the source's, and
instead it opens "**And there is a second-order effect the document does not draw out**", which marks
it as the note's own inference in the sentence that makes it. That is the scaffolding rule working
rather than failing.

### Check 3 - is anything outside a `Background, supplied` block uncited?

**One `defect`, fixed in this pass.**

| Verdict | Location | Finding |
|---|---|---|
| **`defect`** | "What to distrust", the live-instance bullet | The sentence asserted this brain runs the pattern "at **11 sources**, an order of magnitude below the claimed ceiling". **Uncited, outside any `Background, supplied` block, and now factually wrong** - the brain is at **26 sources**, which is roughly 4x below `n10`'s ~100 ceiling, not an order of magnitude. **Both halves of the sentence had gone stale.** |

**Why this one is worth more than its size.** The identical bullet exists in
[`rag.md`](../../brain/topics/rag.md), where it **went stale twice** - caught at dream 0001 and again
at dream 0002 - and was then converted to a pointer at `INDEX.md` with a note recording the repeat
failure. **The topic note learned the lesson and the source note was never updated**, so the same
hard-coded number was left to rot one directory away from its own fix. That is a drift class the dream
pass structurally cannot catch, because dreaming reconciles what was **promoted** and never re-opens a
source's own files.

**Fixed** by replacing the hard-coded count with a pointer to `INDEX.md`, mirroring the wording already
adopted in `rag.md` so the two now fail or survive together.

| Verdict | Location | Finding |
|---|---|---|
| **`judgement`** | Open questions, the human-grip bullet | "...and **the generation effect in learning** suggests the answer is 'less than they think'." This names a real body of psychological literature and asserts its direction, uncited and outside any `Background, supplied` block. It is hedged ("suggests") and sits in an open question rather than in the argument, which is why it is `judgement` and not `defect`. **Proposed**: mark it as supplied background in line, or drop the attribution and keep the question, which loses nothing. **Not applied - the human adopts.** |

### Check 4 - are weak-evidence labels at the point of use, or deferred to the end?

**Clean.** Four ⚠️ blocks, each in the sentence that leans on the weak claim rather than parked in the
trust summary: on `n5` immediately after the schema-document quote ("Unmeasured, and
self-descriptive"), on `n10` in Key claims *and* again at full length in §9 ("Do not cite this as a
result"), and on `n13`/`d1` in §10 where the contradiction is laid out. The source-level summary
carries the source-level facts and does not absorb any claim-level caveat.

### Check 5 - does "What to distrust" carry the gate note's trust facts, or a softer version?

**Clean, and this is the check this note passes most convincingly.** `nodes.md`'s evidence-class table
splits the source into a **pattern** half (`n1`-`n9`, `n11`-`n12`, `n14`-`n18`) and an **efficacy**
half (`n10`, `n13`). `LEARNING.md` reproduces that split **with the same node lists and the same
verdict** ("Never cite the efficacy claims as results").

The sentence most likely to soften in translation did not. `nodes.md` gives the source two credits -
nothing is being sold, and it declares its own abstractness - and then immediately withdraws any
evidential value from them: "**An unmeasured claim from a disinterested expert is still an unmeasured
claim** - it just fails differently from a vendor's." `LEARNING.md` carries that sentence at full
force. A note that kept the two credits and dropped the withdrawal would read as a mild endorsement,
and that is exactly the failure this check exists to catch.

### Check 6 - does a kept frame's `what it teaches` match what the frame shows?

**`n/a`.** No frames exist. Recorded rather than skipped silently, per the contract.

### Considered and not filed

Stated so the pass is auditable rather than cherry-picked, and because each was a candidate I decided
was out of this stage's scope:

- **`n12` (an LLM cannot read markdown and its inline images in one pass) is gated, listed in the
  pattern half, and cited in "Feeds these topics" - but never taught anywhere in the walkthrough.**
  Real, and **not one of the six checks**: whether a gated node earns a section is the curator's call
  and the human's, and a stage that grades coverage is grading structure. Noted here for whoever next
  works the file, not filed as a finding.
- **The prose quality, the ramp, the roadmap's four movements and the mental model's shape** were all
  deliberately not assessed. A stage that grades everything grades nothing.
- **No `gate-reopen` was raised.** Every node's `single-leg` verdict is forced by the source having no
  second leg, which is a fact about the artifact and not a judgement that could go the other way.

### What this pass cannot tell you

It read this source against itself, so it inherits the gate's ceiling: **it establishes that the brain
has represented S8 honestly, never that S8 is right about the world.** S8's two efficacy claims
(`n10`, `n13`) remain unmeasured after this pass exactly as they were before it - `n10`'s ~100-source
ceiling is still the best deep-research target in the source, and **`/research` is the stage that
moves it, not this one.**

> Inherits the global rules in `../../AGENTS.md`.

---

## Pass 1 - addendum, 2026-08-15 (same day)

**The `judgement` finding was adopted by the human and applied.** Pass 1's entry above is left
exactly as written - it is a log, and rewriting the record of what was proposed would destroy the
thing the log is for.

**What changed.** The Open questions bullet on whether a human keeps their grip on knowledge they
never wrote no longer asserts a direction in passing. The generation effect is **kept**, because
deleting it would have removed the reason the question is sharp rather than rhetorical, and is now
carried in a marked `> **Background, supplied.**` block that states it is uncited by construction and
that **the direction is deliberately not asserted**. The claim it makes is now the conditional one -
*if* the effect transfers, `n14`'s division of labour trades retention for throughput and the trade is
invisible to the person making it - followed by the plain statement that nobody has tested whether it
transfers to reviewing LLM-written prose.

**One consequential knock-on, worth recording because it is the kind of thing a fix creates.** Adding
a third `Background, supplied` block made "What to distrust" wrong: it **enumerates the blocks by
name** and listed two. That enumeration is itself an uncited factual assertion about the file, so
leaving it stale would have opened a fresh check-3 inconsistency while closing another one. Updated to
name all three. **A fix that satisfies a checker and breaks a neighbouring sentence is not a fix**, and
this file's honesty rests on that enumeration being complete.

No other finding was re-opened, no gate was touched, and no node changed.
