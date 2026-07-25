---
description: Deep research on a source's gated claims - external evidence into sources/<id>/context/
argument-hint: <source-id or topic> [| specific question]
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, WebSearch, WebFetch
---

# /research - deep research (external evidence)

**The contract is `AGENTS.md` § "Deep research on request".** Read it now and follow it - this file
is only the Claude Code wrapper for that stage. Do not duplicate the contract here; if the two ever
disagree, `AGENTS.md` wins.

Adopt **fact-checker + synthesizer** (+ **mentor** if the goal is teaching the concept).

## Target

`$ARGUMENTS`

If that names a source folder, research **that source's gated nodes**. If it names a topic or a bare
question, research that - but still land the output in a `context/` note under the most relevant
source, or in `reports/` if it spans several.

## Run it

1. **Orient.** Read the source's `SOURCE.md` and `nodes.md`. Pick the research targets by ID:
   `single-leg` nodes, anything `needs-check`, recorded divergences, and the `LEARNING.md` open
   questions. **Target claims, not the subject** - open-ended topic research makes you a summarizer.
2. **Read the brain before the web.** `grep` the root `INDEX.md`, `brain/topics/*.md` and
   `brain/claims.md`. A prior source may already answer this; that link beats a fresh fetch.
3. **Search and fetch,** favouring T1-T3 (see the tier table in `AGENTS.md`). Deliberately attempt
   the **cross-domain hop** - the established name for this idea in an older discipline. Respect the
   budget: **≤ 8 searches, ≤ 12 fetches**; stop early on two independent agreeing sources, or when a
   pass surfaces nothing new.
4. **Apply the independence rule.** A companion repo, a vendor blog restating that vendor's own
   talk, or same-lab work is *the same leg wearing a different hat*: record it, cite it, but **do not
   raise confidence**.
5. **Write** `sources/<id>/context/<NN>_<slug>.md` using the structure in
   `sources/_TEMPLATE/context/README.md`. Every finding gets a verdict
   (`supports` / `contradicts` / `refines` / `no-evidence`), a tier, and an independence call. End
   with a **Confidence assessment** - never interrupt with clarifying questions; state assumptions
   there instead.
6. **Feed it back in the same pass:** update node confidences in `nodes.md` (pointing at the context
   note), cite external support in `brain/claims.md`, add terms to `brain/glossary.md`, set
   `SOURCE.md` Status, and append to `brain/log.md`. Keep external findings **out of `LEARNING.md`'s
   body** - it may cite the note, never absorb it.
7. **Report back:** one paragraph on what changed - which claims got stronger, which got weaker,
   which found nothing - then `git diff`.

## Calibration

The reader knows LLM and agent fundamentals. **No 101 explainers.** Aim one level above the source:
the frame that makes its claim feel inevitable rather than arbitrary.

## Honesty rules (non-negotiable)

- `no-evidence` is a **result**, not a failure - "this rests on one practitioner's experience" is
  exactly the kind of thing this brain exists to record. Never pad with weak T4/T5 hits.
- `contradicts` is a **finding**. Keep both sides, cite both, flag the conflict.
- If web access is unavailable, say so and stop. **Never fabricate a citation or work from memory.**
