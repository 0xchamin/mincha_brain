# Source - Harness Design for Long-Running Application Development

> Persona: **curator** (media) / **code-explorer** (code) - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table. The agent fills it on the paste-a-URL trigger
> and keeps it current. Name this folder `YYMMDD_slug` (see `../../AGENTS.md`).

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | blog |
| URL | https://www.anthropic.com/engineering/harness-design-long-running-apps |
| Title | Harness Design for Long-Running Application Development |
| Author / channel | Prithvi Rajasekaran (Anthropic Labs) |
| Published | 2026-03-24 |
| Duration / length | ~4,000 words, 6 sections, 8 screenshots, 4 tables |
| Commit SHA | n/a |
| License | n/a (copyrighted first-party engineering writing; learned from, not redistributed) |
| Ingested | 2026-07-25 |
| Access | open |
| Topics | agents, context-engineering, evals |
| Visual leg | skipped (figures are outcome screenshots, no explanatory diagram - see below) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/article-outline.md` - the **derived** structural outline (not a copy of the article).
3. `nodes.md` - knowledge nodes (claims + citations + gate verdicts).
4. `context/` - **external evidence** from a deep-research pass (empty - not requested).
5. `LEARNING.md` - the distilled learning document.

## Ingest notes

- **Capture:** `web_fetch` structural extraction into `raw/article-outline.md`. **Verbatim
  reproduction was declined and not pursued** - the article is copyrighted first-party writing, and
  this kit learns from sources rather than redistributing them. The outline is the agent's own
  restatement plus short attributed quotes where exact wording carries meaning. **Cite the original
  by section**, not the outline.
- **Visual leg: skipped, deliberately.** The article carries **eight images and they are all outcome
  screenshots** of the generated apps (game maker, DAW), plus a decorative header. Confirmed by a
  second fetch asking specifically whether an architecture diagram exists: **it does not**; the
  three-agent system is described in prose only. Skipped for two reasons:
  1. **They are not explanatory.** A screenshot of a nicer sprite editor illustrates a conclusion the
     prose already states; looking at it cannot corroborate *why* the harness worked. This is the blog
     analogue of ADR-0003's static probe - the pixels carry no second leg.
  2. **They are Anthropic's product screenshots.** Copying them into the repo is the kind of
     redistribution this kit's license rule discourages.
- **Consequence, recorded not discovered (ADR-0003):** most nodes here are **`single-leg`**. The
  exception is the numeric claims, where the article's **tables** act as a real second leg against the
  prose - see the gate note in `nodes.md`. That is weaker than slide-vs-narration and is labelled so.
- **Tier and independence (`AGENTS.md` research tiers): this is T2** - first-party engineering
  writing. Authoritative about *its own* harness and models, **positioned** on the wider field. It is
  Anthropic reporting how to get more out of Claude, including dollar costs of Claude usage. Treat the
  mechanisms as well-evidenced and the framing as interested.
- **No independent verification.** Every figure here (durations, costs, iteration counts) is
  self-reported from internal runs, **n=1 per configuration**, with no released harness code.
- **This is the kit's first blog ingest** - it exercises `prd.md` §5.2, previously unrun prose (R10).
  Findings from the shakedown are recorded in `brain/log.md`.
