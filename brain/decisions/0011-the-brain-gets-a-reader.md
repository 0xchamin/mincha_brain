# ADR 0011: The brain gets a reader - a third frozen script that renders, and never authors

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260731 |
| Deciders | chamin |

## Context

The kit's premise is that knowledge compounds if you keep promoting it into one place. Eight
sources in, that place is ~340 KB of markdown across `brain/topics/`, `brain/claims.md` and eight
`LEARNING.md` files, and it is only legible at a desk. GitHub's mobile markdown view renders a
74-row five-column claims table and citations like `` `&t=616s` `` that cannot be tapped or
retyped. The practical effect is that **the brain is only read while it is being written** - during
an ingest, at a laptop - which is the opposite of a compounding store's value, since the payoff of
promotion is being able to *re-read* it cheaply, later, in a different context.

Nothing about the notes needed changing to fix this. The reading surface was already specified by
the contract and already written:

- every `LEARNING.md` opens with `## TL;DR` and `## Key claims` - **that is the per-source lesson**;
- `brain/topics/*.md` carry a `**Status:**` line and a `## What this covers` - **that is the meta
  lesson**;
- `INDEX.md` already annotates every source with a summary and a "when to read".

So the gap was a renderer, not an authoring stage.

## Decision

**Add `tools/build_site.py` as a third frozen script.** It renders `INDEX.md`, `brain/` and
`sources/*/LEARNING.md` into `site/` - a static, offline-capable, phone-first reader - and
`.github/workflows/pages.yml` publishes it to GitHub Pages on every push to `main`.

**The hard constraint is that it is a renderer.** Every word it emits comes from a file already in
this repo. It adds no claims, drops no citations, resolves no judgement, and `site/` is git-ignored
and reproducible from scratch. This is the same line [ADR-0004](0004-validator-as-type-checker.md)
and [ADR-0005](0005-mechanical-toolbox.md) already drew - **form is code, judgement is prose** -
applied a third time. `validate.py` checks form; `ingest.py` performs mechanics; `build_site.py`
presents. None of the three is allowed an opinion about what is true.

Four transformations earn their place by being *presentation* decisions that markdown cannot make:

| Transformation | Why it is presentation, not authoring |
|---|---|
| `&t=NNNs` -> tappable YouTube deep link | the citation is unchanged; only its affordance changes, and it is the one citation form you cannot retype on a phone |
| `claims.md`'s table -> filterable cards | all 74 claims survive with topic, sources and confidence; a five-column table is simply unreadable at 390px |
| Landing page = TL;DR + Key claims per source | a *selection* of existing sections, in the order `AGENTS.md` already puts them |
| Each note's agent-directed preamble collapsed | see below |

## The one judgement call, and why it went the way it did

The preamble of every note ("Persona: **curator** + **mentor**. Re-adopt when working this file.")
is written **to the agent**, not to a reader, and on a phone it pushes the TL;DR below the fold.
The obvious move is to strip it.

**Stripping is wrong**, and the skills source is the counterexample: its preamble carries "the two
things that bound how far to trust this: it is a conference talk (T4) by a vendor employee, and its
strongest numbers come from a third-party benchmark while its most dramatic ones are self-reported
and unreplicated." That is evidence about evidence, and a renderer that silently deletes it is
authoring by omission - exactly what this ADR forbids.

**So it is collapsed, never dropped**, behind an "About this note" disclosure. When a renderer is
tempted to remove something, the answer is to demote it, because removal is a claim about
importance and this script does not get to make claims.

## Consequences

- **Every ingest reaches the phone with no extra step.** The compound pass already ends in a push;
  the deploy hangs off that, and nothing new is added to the pipeline an agent must remember.
- **`validate.py` gates the deploy.** A contract violation now blocks publication as well as CI.
- **The reader is a second, weaker contract check.** A source without a `## TL;DR`, a topic note
  without a `**Status:**` line, or a source missing its `INDEX.md` row renders as a visible hole.
  That is the note being wrong, not the renderer - fix the note. It is weaker than `validate.py`
  because it reports by looking odd rather than by exiting 1.
- **A new failure mode: reading a claim without its gate.** The reader shows claims with their
  confidence pill, but a phone reader skims. `corroborated` still means *internally consistent*,
  never *true* - the Global rule is unchanged and the reader does not soften it.
- **BUILD.md grows.** The open-source bundle now ships `build_site.py` and its three assets, because
  `AGENTS.md` travels verbatim and promises a reader; a bundle that described one without shipping
  it would be stale by construction.
- **One manual step this cannot self-serve:** GitHub Pages must be switched to the "GitHub Actions"
  source once, in repo settings, before the first deploy succeeds.

## Alternatives considered

- **Obsidian / an existing markdown mobile app.** Reads the vault with zero build, but renders the
  files as-authored: the agent preamble, the wide claims table and the dead `&t=` citations all
  survive, so it solves access without solving legibility. It also puts a third-party app between
  the human and a repo whose whole point is that it is plain files.
- **A generated digest file committed to the repo** (`LESSONS.md`). Cheapest option, but it is a
  derived artifact inside the namespace `validate.py` treats as source of truth, and a second place
  where a claim lives - which is the duplication that
  [`brain/topics/memory.md`](../topics/memory.md) records as the characteristic failure of
  locally-optimal memory writes (claim 59).
- **Publishing to a Claude Artifact or similar.** Immediate and private, but it does not update
  itself from git, so it drifts the moment the next source lands - the exact staleness this kit
  exists to avoid.
