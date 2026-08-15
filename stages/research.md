# Stage: `/research` - deep research on gated claims

> External evidence for specific gated nodes. **Triggered by the user, never automatic.**
>
> **This file is the contract for this stage.** It was extracted verbatim from `AGENTS.md`
> on 2026-08-15 ([ADR-0027](../brain/decisions/0027-stage-specs-leave-the-contract.md)) so that a
> spec needed once a fortnight stops occupying every session's context window. **`AGENTS.md`
> remains the root contract** and this inherits every global rule in it; where the two
> disagree, `AGENTS.md` wins and this file is the bug.

## Deep research on request (external evidence)

> **Why this exists.** The corroboration gate buys *internal* consistency - a slide agrees with the
> narration, code agrees with its docs. That is not truth (see Global rules). Real confidence rises
> only with **external** corroboration. Deep research is the mechanism: it reaches outside the source
> to test what the source claims, and to attach the intellectual context that makes a claim land -
> the prior work, the competing framing, the name the field already has for this thing.

**Trigger (never automatic).** The user says **"deep research"** with the URL, or asks for it on an
already-ingested source, or invokes the harness's research command. Adopt **fact-checker +
synthesizer** (+ **mentor** when the goal is teaching a concept).

**Target the nodes, not the subject.** Open-ended "research <topic>" returns adjacent reading and
makes you a summarizer. Research **specific gated claims by node ID** from `nodes.md`, prioritising:
`single-leg` nodes, anything marked `needs-check`, recorded divergences, and the `LEARNING.md` open
questions. Each finding resolves to one of four verdicts:

| Verdict | Meaning | Effect |
|---|---|---|
| `supports` | An **independent** source agrees | Node confidence may rise; cite the external source in `brain/claims.md` |
| `contradicts` | A credible source disagrees | **A finding, not a failure** - record both, flag the conflict |
| `refines` | Broadly agrees but bounds/qualifies the claim | Rewrite the claim with the qualifier |
| `no-evidence` | Nothing credible found either way | **Also informative** - the claim is one practitioner's experience; say so |

**Read the brain before you read the web.** `grep` the root `INDEX.md`, `brain/topics/*.md` and
`brain/claims.md` first - a prior source may already answer this, and the link between them is worth
more than a fresh fetch.

### Source credibility tiers (record the tier with every citation)

| Tier | What | How to weigh it |
|---|---|---|
| **T1** | Peer-reviewed papers, official specs/standards, official API/product docs | Strongest for *how something works*. |
| **T2** | First-party engineering writing (Anthropic, OpenAI, DeepMind, Cursor, ...) and official repos | Authoritative **about their own system**; **positioned** on the wider field. Flag when a vendor is cited on a topic they sell. |
| **T3** | Preprints (arXiv) | Good for recency and for the field's vocabulary; **not peer-reviewed** - always label as preprint, never treat as settled. |
| **T4** | Practitioner experience: conference talks, engineering blogs, respected individual writers | Same evidential class as most sources in this brain - experience reports, rarely measured. |
| **T5** | Aggregators and directories (Pulse MCP, awesome-lists, doc hubs) | Use for **discovery**; cite the primary source they point to, not them. |

> **The independence rule (hard).** External evidence only counts as corroboration when it is
> **independent** of the original source - not the same author, organisation, or commercial interest.
> A talk's companion repo, a vendor blog restating the vendor's own conference talk, or a paper by
> the same lab is **the same leg wearing a different hat**. Record it, but never let it raise
> confidence. When independence is unclear, say so.

### Calibration: aim one level above the source

The reader already knows the fundamentals of LLMs and agents. **Do not write 101 explainers.** The
target is the concept *one level above* the source - the frame that makes its claim feel inevitable
rather than arbitrary.

> **Take the cross-domain hop.** The most valuable framing is often the established name in an older
> discipline - cognitive science, distributed systems, PL theory, control theory, information
> science. (Example: agent skill design is a rediscovery of **procedural memory**.) Searching only AI
> sources will never surface this, so search for it deliberately.

### Budget, output, and honesty

- **Budget (default):** ≤ 8 searches and ≤ 12 fetches per pass. **Stop early** when two independent
  T1-T3 sources agree, or when a pass surfaces nothing new. Record the budget actually used.
- **Never interrupt with clarifying questions.** Make reasonable assumptions, state them explicitly
  in a **Confidence assessment** section at the end of the note. (Pattern borrowed from Copilot
  CLI's `/research`.)
- **Output is a permanent kit file, not a session artifact:**
  `sources/<id>/context/<NN>_<slug>.md`, one note per pass, numbered in order. Copilot CLI writes
  research to a throwaway session directory; this kit does the opposite - **ephemeral output that is
  not captured into a kit file did not happen.**
- **Feed the findings back** in the same pass: update the affected node's confidence in `nodes.md`
  (pointing at the context note), cite external support in `brain/claims.md`, add new terms to
  `brain/glossary.md`, and let `LEARNING.md` cite the context note rather than absorbing it.

> **Keep research out of `LEARNING.md`'s body.** `LEARNING.md` answers exactly one question - *what
> did this source teach?* Blending external findings into it destroys the distinction between "the
> author claims this" and "the field thinks this", which is the whole point of citing. External
> evidence lives in `context/`; durable cross-source synthesis lives in `brain/topics/*.md`.

### Degrade & failure handling (don't fail silently)

| Situation | Do this |
|---|---|
| Video has no captions | Transcribe audio with `faster-whisper`; if that fails, note it and proceed transcript-light. |
| **`yt-dlp` returns `HTTP 403` on every DASH format** | **A missing JavaScript runtime, not a blocked video.** YouTube's n-challenge needs one, and without it the *only* downloadable format is usually `18` - **progressive 360p**. Fix with **`brew install deno` AND `pip install yt-dlp-ejs`**: **both are required**, and deno alone still fails the challenge with `n challenge solving failed`. Then `-f 299` (1080p) downloads normally. |
| **The only format that downloads is 360p** | **Do not gate a slide-heavy source at 360p.** Dense screens - a rendered document, a `SKILL.md`, a saved prompt - are **illegible** at that resolution, so the frames will look contentless and the source will degrade to transcript-only *for a reason that is not true*. **This is the false-`STATIC` failure arriving from a different direction** (ADR-0006) and it has the same asymmetry: the cost of re-extracting at 1080p is one download, and the cost of a wrong degrade is the source's entire second leg, which the degrade rule forbids you to reinstate later. Fix the runtime (row above) and re-extract **before** viewing anything. It happened on S26, where the whole payload was on screen. |
| Talking-head video, no useful frames | The static probe catches this: <= 3 distinct frames after dedup -> **`view` the confirmation sheet it writes (ADR-0006)**, then auto-degrade to transcript-only and record `Visual leg: skipped (static probe)`. Nodes are `single-leg` (needs-check), never `corroborated`. |
| **Probe says `STATIC` but the sheet shows changing slides** | A **false STATIC** - a templated deck defeating whole-frame scene detection (ADR-0006). **Override**: extract transcript-anchored frames, record `Visual leg: analysed (N frames kept) - static probe overridden` in `SOURCE.md`, and say why. Do **not** file a bug against the constants; the metric is wrong for this input class, not mis-tuned. |
| User says "don't analyze video" / "transcript only" | Skip frame extraction **and the probe**; record `Visual leg: skipped (user)`; gate every node `single-leg`; say in one line that internal corroboration is now unavailable and deep research is the way back to two legs. |
| Visual leg skipped but the source turns out to matter | Do **not** retro-mark nodes `corroborated`. Either re-run the visual leg and re-gate, or get the second leg externally via deep research. |
| Paywalled / login-required article or paper | Ingest only what you can legitimately access; set `SOURCE.md` Access + Status `blocked` or `partial`; do not bypass. |
| Repo private / huge / has submodules or Git-LFS | Prefer `gh` shallow clone; for huge repos orient from the README + a sparse checkout; never read it all. Non-GitHub git URL: clone by URL, skip `gh`. |
| Repo has no/shallow/stale docs | Code is the primary leg; nodes are `single-leg`; a docs↔code gap is a `divergence` finding, not a drop. |
| License missing/unclear (code) | Record `License: unknown` in `SOURCE.md`; keep the clone git-ignored; do not redistribute source. |
| Symlink not permitted (Windows, no Dev Mode) | `link-agents.ps1` writes a marked one-line pointer instead; the harness still reads `AGENTS.md`. |
| Ingest interrupted | Leave `SOURCE.md` Status at the last safe stage; resume from there next session. **If it stopped at `capture` (nothing gated, `SOURCE.md` still template) - and `ls -la` shows no recent writes, because an unfilled template does not mean no live process - move the folder to git-ignored [`staging/`](../staging/README.md) instead of leaving it in `sources/`** - `sources/<id>/` is `validate.py`'s namespace and every folder there is checked as a *finished* source, so a bare capture can only be silenced by faking an INDEX row or deleting the download. **A capture becomes a source when it is distilled, not when it is downloaded.** Move it back when you intend to finish it. |
| Deep research finds nothing credible | Record `no-evidence` in the context note - that the claim rests on one practitioner's experience **is** the finding. Do not pad with weak T4/T5 hits. |
| Deep research finds only non-independent sources | Record them, cite them, but **do not raise confidence** (independence rule). Say plainly that corroboration is still missing. |
| Sources conflict | Keep **both**, cite both with tiers, flag the conflict in the context note and in the topic note's "Open questions / conflicts". Do not silently pick a winner. |
| No web access / search unavailable | Say so, skip the research step, leave `SOURCE.md` Status at `distill`; do not fabricate citations or work from memory. |
