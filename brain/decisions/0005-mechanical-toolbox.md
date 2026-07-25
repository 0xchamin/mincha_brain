# ADR 0005: Freeze the mechanical ingest steps as `tools/ingest.py` (a toolbox, not a pipeline)

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260725 |
| Deciders | chamin |

## Context

`prd.md` §10 deferred packaging the mechanical pipeline (`yt-dlp` -> `ffmpeg` -> `imagehash`) with an
explicit revisit trigger: **after ~5-10 real ingests**, "only when the Markdown convention actually
hurts". The brain is at **2** ingests, so on that trigger alone this would be premature.

Two things changed:

1. **ADR-0003 created a deterministic contract rule with no canonical implementation.** The visual-leg
   switch turns on "<= 3 distinct frames after scene-detect + phash dedup". Distinctness depends
   entirely on two constants - the ffmpeg scene threshold and the pHash Hamming distance - and both
   lived only in prose. Two agents would compute different verdicts for the same podcast, and a
   verdict computed with different constants is not comparable to any previous source's. **A
   threshold nobody can reproduce is not a rule.**
2. **The same code kept being written and thrown away.** During the 12-factor ingest, `vtt_clean.py`
   and `dedup.py` were both written into a scratch directory and evaporated with the session -
   violating the kit's own rule that ephemeral output not captured into a kit file did not happen.

The underlying principle, which is what makes this narrow rather than a general push toward scripts:
**generate what should vary, freeze what should not.** On-the-fly code is right when variation is a
feature - mid-ingest the phash dedup was abandoned for transcript-anchored extraction, and a rigid
script would have fought that. It is wrong when variation is a bug: VTT parsing has no reason to
differ between videos, and regenerating it re-rolls the dice on a parser whose output still looks
plausible when subtly wrong.

## Decision

Freeze the deterministic steps as **`tools/ingest.py`**, exposing four independent subcommands:
`transcript` (stdlib only), `probe` (the ADR-0003 verdict), `frames`, `sheet`. `AGENTS.md` instructs
agents to use it, and specifically to run `probe` rather than a hand-rolled equivalent.

Three constraints:

- **A toolbox, not a pipeline.** No `--url do-everything` entrypoint. `AGENTS.md`'s "the shell steps
  are reference, not a fixed script" still holds; assembly stays the agent's job, and `yt-dlp`
  invocations stay ad hoc because format selection genuinely varies.
- **Judgement never moves in.** Reading a slide, gating a claim, deciding which frames earn their
  place - those stay in `AGENTS.md` and `personas/`. The same line `validate.py` draws: **form is
  code, judgement is prose.**
- **Pipeline constants are named module-level values** (`SCENE_THRESHOLD`, `PHASH_DISTANCE`,
  `STATIC_FRAME_THRESHOLD`) with a comment saying that changing them makes every past verdict
  incomparable. That is the entire point of freezing them.

## Alternatives considered

- **Wait for 5-10 ingests, per `prd.md` §10** - overridden narrowly, on reason 1 only. The trigger
  was written before ADR-0003 existed; a contract rule that cannot be reproduced is a stronger
  argument than a usage count.
- **One `ingest.py --url <url>` that runs everything** - rejected: it would own the control flow the
  agent is supposed to own, and would have prevented the mid-ingest strategy switch that produced the
  contact-sheet method in the first place.
- **A `pip` package** (as `prd.md` §10 floats) - rejected for now: it hides the code from the agent
  reading the working tree, for no benefit at this size. A file in `tools/` is inspectable and
  editable in place.
- **Leave it in the harness's scratch directory** - rejected; that is precisely the failure being
  fixed.

## Consequences

- **Easier:** the ADR-0003 verdict is now reproducible across agents and sources. The contact-sheet
  triage (17 candidates -> 1-2 `view` calls) is available rather than being re-invented.
- **Harder:** a second frozen artifact to keep in step with the prose. If `AGENTS.md` and the tool
  disagree, `AGENTS.md` wins and the tool is the bug - same precedence as `validate.py`.
- **Verified, not assumed:**
  - `transcript` reproduces the hand-run output from the 12-factor ingest **byte-for-byte** (modulo a
    trailing newline).
  - `probe` was tested against synthetic static and multi-scene videos: 0 distinct -> `STATIC`,
    5 distinct -> `RICH`.
  - **Testing caught a genuine silent-failure bug:** `run_ffmpeg` originally ignored ffmpeg's return
    code, so *any* ffmpeg error produced zero frames and a `STATIC` verdict - the probe would have
    silently skipped the visual leg on error and never said why. It now fails loudly. This is exactly
    the class of bug prose review cannot catch, and the strongest argument for freezing the step.
  - Two of the test videos were themselves wrong before they were right (a full-range YUV artifact,
    then hue-rotated segments with near-identical luma that ffmpeg's luma-based scene detection
    correctly ignored). Recorded because it is the normal shape of this work: the test is as likely
    to be wrong as the code.
- **Revisit when:** a fifth subcommand is wanted, or when `yt-dlp` invocation stabilises enough to be
  worth wrapping (it is not yet).
