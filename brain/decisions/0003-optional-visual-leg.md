# ADR 0003: Make the visual leg optional (opt-out), with a free static-video probe

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260725 |
| Deciders | chamin |

## Context

Frame extraction and `view`ing are the most token-expensive steps in a media ingest. On a slide-heavy
conference talk that cost is the entire point - the slides *are* the second leg, and the two ingests
so far both depended on them. On a **podcast, webcam interview, or fireside chat the picture never
changes**, so the same spend buys nothing: the agent looks at ten near-identical stills of a person
talking and extracts no crux from any of them.

The kit already handled this as an *accident* - the degrade table said "talking-head video, no useful
frames -> transcript-only, `single-leg`". It had no way to make it a *decision* taken up front,
before the tokens are spent.

Two asymmetries shaped the design:

- **Opposite default from deep research (ADR-0002).** Research is opt-**in** because it is expensive
  and rarely needed. The visual leg is opt-**out** because it is usually the whole reason the source
  is a video rather than an article.
- **The probe is already free.** Scene-detect + `imagehash` dedup is the *first* step of the existing
  pipeline and is pure shell work - no tokens. It therefore doubles as a static-video detector at
  zero marginal cost, which means the default can be made smart rather than merely obedient.

## Decision

**Analyse the visual leg by default. Skip it in three cases**, in priority order:

1. **User opt-out** - "don't analyze video", "transcript only", or similar. Explicit instruction wins
   and skips even the probe.
2. **Static-video probe** - if the whole video yields **<= 3 distinct frames** after scene-detect +
   phash dedup, treat it as visually static, auto-degrade to transcript-only, and say so in one line.
   (Calibration: `260725_12-factor-agents`, a slide-heavy talk, yielded 19 distinct.)
3. **Capture failure** - no video stream or download blocked.

**The consequence is recorded, never discovered.** Dropping the visual leg means every node from that
source is **`single-leg` by construction** - there is no second leg left to corroborate against, and
a transcript agreeing with itself is not two legs. So `SOURCE.md` gains a **Visual leg** field
(`analysed (N frames kept)` / `skipped (user)` / `skipped (static probe: N distinct)` / `n/a (code)`),
every such node is gated `single-leg` / `needs-check`, and the agent states the trade-off in one line
when it happens.

**Deep research is the designated complement.** With the visual leg gone the only route back to two
legs is **external** evidence, not a harder look at the video. The two switches from ADR-0002 and
this one compose deliberately: skip the cheap internal leg, buy an expensive external one *only if
the source turns out to matter*.

The rule generalises to blogs with decorative-only images and papers with unreadable figures. Code
sources are unaffected - their visual leg is *generated* from the code and generating a diagram is
cheap.

## Alternatives considered

- **A pure manual flag, no probe** (the literal request) - rejected as strictly worse: the probe is
  free, already the first pipeline step, and catches the podcast the user forgot to flag. The manual
  switch is kept and takes priority; the probe just makes the default competent.
- **Auto-detect only, no manual switch** - rejected: the user knows "this is a podcast" before any
  shell command runs, and skipping the download entirely is cheaper than probing it. Explicit
  instruction should never be second-guessed by a heuristic.
- **Make it opt-in like deep research** - rejected: it would silently degrade the common case
  (slide-heavy talks), where the visual leg is the source's main value.
- **Let transcript-only nodes count as `corroborated`** when the narration is internally consistent -
  **firmly rejected.** A transcript agreeing with itself is one leg. Allowing this would quietly
  destroy the meaning of `corroborated` across the whole brain, which is the kit's core asset.

## Consequences

- **Easier:** podcasts and interviews become cheap to ingest instead of wasteful, which lowers the
  bar for ingesting them at all.
- **Harder:** a second thing to record honestly. The temptation on a skipped-visual source will be to
  mark a well-argued claim `corroborated`; the contract forbids it.
- **Watch:** the `<= 3 distinct frames` threshold is a heuristic from a sample of one calibration
  point. Revisit after a few podcast ingests - screen-shares and demo-heavy streams are the likely
  false negatives, and a video that *starts* static but shares a screen at minute 40 could be
  mis-classified. If that happens, consider probing in windows rather than over the whole video.
- **Untested.** No podcast or interview has been ingested yet, so neither the switch nor the
  threshold has run in anger.
