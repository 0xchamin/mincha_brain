# ADR 0010: Karpathy's "lint" *is* the dreaming pass - correcting ADR-0009's reading of S8

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260731 |
| Deciders | chamin |

## Context

[ADR-0009](0009-dreaming-reconciliation-pass.md) added the `dream` stage and cited three sources.
Two of them - S6 (OpenAI) and S7 (Anthropic) - had been ingested. The third had not:

> A third source sharpened the framing. Karpathy's *LLM Wiki* gist describes this same pattern
> (raw sources / maintained wiki / schema) and names three operations: **ingest, query, lint**. The
> kit has all three. **What it does not have is what S6 and S7 both argue is the load-bearing one** -
> a maintenance pass that runs on its own clock rather than inside the ingest.

That gist has now been ingested as **S8** ([`sources/260731_llm-wiki/`](../../sources/260731_llm-wiki/LEARNING.md)),
with its nodes gated **before** `topics/memory.md` was reopened, specifically so the prior conclusion
would be re-derived rather than inherited. It does not survive.

**The first two assertions hold** - the three-layer architecture (S8 `n4`) and the three operations
(S8 `n6`) are both accurate readings.

**The third is wrong.** §Lint reads in full:

> "Periodically, ask the LLM to health-check the wiki. Look for: **contradictions between pages,
> stale claims that newer sources have superseded, orphan pages with no inbound links, important
> concepts mentioned but lacking their own page, missing cross-references, data gaps that could be
> filled with a web search.** The LLM is good at suggesting new questions to investigate and new
> sources to look for."

Against the eight classes the `dream` stage works:

| Karpathy's §Lint (S8 `n8`) | The `dream` stage |
|---|---|
| contradictions between pages | **Contradiction** |
| stale claims that newer sources have superseded | **Stale confidence** / **Superseded framing** |
| orphan pages with no inbound links | **Orphans** |
| missing cross-references | **Orphans** / **Drift from source** |
| important concepts mentioned but lacking their own page | the architect's create-vs-merge call |
| data gaps that could be filled with a web search | the deep-research trigger ([ADR-0002](0002-deep-research-stage.md)) |
| - | **Duplication / fragmentation**, **Stale status**, **Closed open questions** (the kit's own additions) |

"**Periodically**" and "ask the LLM to" place it outside the ingest, on its own trigger. **It is the
maintenance pass, described eight weeks before either vendor published.**

**How the error was made, which is the part worth keeping.** The prior reading matched the *word*
"lint" to `validate.py`, concluded the kit already had that operation, and stopped. The two share
nothing but the name: `validate.py` checks **form** ([ADR-0004](0004-validator-as-type-checker.md)),
and **every item on Karpathy's list is a judgement**. The kit's own contract says exactly this, one
sentence from where ADR-0009 reasons: *"a green validator means the shape is right, not that the
thinking is."*

## Decision

**Record that S8's §Lint is an independent third statement of the decoupled maintenance pass, and
correct ADR-0009's characterisation of it. ADR-0009's decision stands unchanged; only its reading of
one source changes.**

Nothing about the `dream` stage is altered - not its trigger, its classes, its output, or its
prohibition on running inside an ingest. What changes is what the brain believes about the evidence
behind it.

**What the third source is worth, stated precisely, because it is easy to overclaim:**

| | Bought | Not bought |
|---|---|---|
| **Independence** | S8 is dated **2026-04-04** - seven weeks before S7 (2026-05-21), two months before S6 (2026-06-04) - and sells nothing. **It cannot be restating either vendor.** This removes "two marketing departments reached for the same metaphor" as the explanation of S6/S7's convergence. | The author is a former OpenAI researcher, so "wholly disconnected" would overstate it. The **publication order** carries the argument, not the biography. |
| **Generality** | The same operation over a **document wiki** with no agents in it. That makes the pattern a property of maintained knowledge stores, not of agent memory - which is why it now sits in both [`memory.md`](../topics/memory.md) and [`rag.md`](../topics/rag.md). | Nothing about agents, multi-agent stores, or memory specifically. |
| **The practice** | Corroborated: reconcile the whole store, periodically, out of band. | - |
| **The rationale** | Nothing. **S8 never says why periodic beats at-ingest.** The objective-conflict argument (claim 59) remains **S7's alone**, and this ADR does not raise its confidence. | - |
| **Evidence it works** | **None.** S8 is T4 and unmeasured - no eval, no baseline, no cost figure. | Three unmeasured sources are not more measured than two. |

**The closest S8 comes to the rationale is by accident, and it is recorded as a divergence** (S8
`d1`): §Why this works claims LLMs "don't forget to update a cross-reference" while §Lint instructs
you to hunt for missing ones. Both cannot be true. **Believe §Lint** - it is the operational section,
and the six-item list is an admission that integrate-on-ingest leaves defects behind. The usable form:
**LLM bookkeeping is cheap enough to be worth doing repeatedly, not so reliable that doing it once is
enough.** That is the observation underneath claim 59, not an argument for it.

## Alternatives considered

- **Silently fix the sentence in ADR-0009.** Rejected. An ADR is a dated record of what was decided
  and why; editing the reasoning after the fact destroys the thing it exists to preserve. The
  correction gets its own numbered entry and ADR-0009 gets a pointer.
- **Reopen the decision itself.** Rejected, and it was considered seriously: if one of three cited
  sources was misread, was the stage justified? **Yes, and more strongly than before.** The
  misreading understated the support - S8 argues *for* the pass, not for its absence. The stage would
  stand on S6 and S7 alone, and on the concrete defect that motivated it (the stale
  "no measurements" claim in `memory.md`).
- **Treat S8 as raising confidence in claim 59.** Rejected under the independence rule's sibling
  principle: **S8 corroborates the practice and is silent on the reason.** Recording it as support
  for the rationale would launder a coincidence into evidence. `memory.md` now splits the claim's
  confidence explicitly - practice: three sources, one non-vendor; rationale: still S7 alone.
- **Rename the kit's stage to "lint" for consistency with the earliest source.** Rejected. The kit
  already has a `validate.py`, and "lint" in every engineer's usage means a **form checker** - which
  is precisely the confusion that produced this error. `dream` is a worse metaphor (S6 and S7 borrow
  it from sleep without citing any of that literature) but an unambiguous name in this repo. **Pick
  the name that cannot be mistaken for something you already have.**

## Consequences

- **`memory.md` gains a third source and an explicit split**: the decoupled-curation *practice* now
  has three sources including one non-vendor and earliest; the *rationale* still has one.
- **`rag.md` goes `seed` -> `emerging` on S8**, its first source in the brain's history, and the
  topic's scope widens to cover maintained knowledge layers as the alternative to query-time
  retrieval - rather than spawning a `knowledge-bases` note that would put two halves of one argument
  in two places.
- **The `rag` / `memory` boundary drawn in [ADR-0007](0007-memory-topic.md) needed a qualifier**, and
  got one in both notes. "Who authored the corpus" does not separate them: an LLM Wiki is
  system-authored *about someone else's documents*. **The refined line is what the knowledge is
  about** - external sources (`rag`) versus the system's own experience (`memory`). Recorded here
  rather than as its own ADR: it is one qualifying sentence in two notes and creates no new structure.
  **If a second source straddles the line, that earns an ADR.**
- **A named failure mode for this kit, and the real lesson.** The defect was **a claim made about a
  source that had not been ingested**. It was wrong the day it was written, it lived in a file nothing
  re-reads, and **a dream pass could not have caught it** - reading all of `brain/` would show a
  perfectly coherent story, because the contradicting evidence was outside the brain. The general
  rule: **citing a source you have only skimmed creates a claim with no gate behind it.** Prefer
  "reviewed, not yet ingested - claims about it are ungated" over a confident one-line summary, or
  ingest it first.
- **Revisit when:** a source straddles the `rag`/`memory` boundary a second time; or S8's `n10`
  (index-file navigation replacing embedding retrieval at ~100 sources) is externally tested, which
  is the highest-value deep-research target either topic now carries.
