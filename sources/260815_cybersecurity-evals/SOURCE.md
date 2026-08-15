# Source - Patterns for Building Cybersecurity Evals

> Persona: **curator** - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | blog |
| URL | https://eugeneyan.com/writing/cybersecurity-evals/ |
| Title | Patterns for Building Cybersecurity Evals |
| Author / channel | Eugene Yan (Ziyou Yan), eugeneyan.com |
| Published | 2026-06 (self-cited "Jun 2026"; stated read time 19 min) |
| Duration / length | ~3,960 words, 11 meaningful figures |
| Commit SHA | n/a |
| License | n/a (personal blog, read-only ingest) |
| Ingested | 2026-08-15 |
| Access | open |
| Topics | evals, agent-security, agents |
| Visual leg | analysed (8 frames kept, of 11 meaningful figures downloaded) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/article.md` - the captured article text; `raw/figures/` - all 11 downloaded figures.
3. `nodes.md` - knowledge nodes (gated claims + citations).
4. `context/` - external evidence (empty; no deep-research pass requested).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the 8 curated figures.

## Ingest notes

- **Capture method:** `curl` the article HTML to `raw/article.html`, then a per-source Python
  extractor to `raw/article.md` (no `pandoc` on this machine). All 11 content figures downloaded as
  `.webp` to `raw/figures/` and converted to `.png` with Pillow for viewing.
- **Visual pre-filter:** not applicable in the video sense - a blog's figures are already a curated
  set. 18 `<img>` tags found, 7 discarded as site chrome (icons, share buttons), leaving **11
  meaningful figures**, all of which were `view`ed. **8 kept**, each carrying one teaching step in
  `LEARNING.md`.
- **Dropped figures:** `cybench-table1` (a subtask worked example - the outcome ladder in
  `fig2` teaches the same idea more generally) and `cybergym-figure3` (a model leaderboard whose
  lesson `fig5` carries better, with cost and harness attached).

### The thing to know before reading anything else here

**This is a secondary source.** Every number in it belongs to one of seven other artifacts - six
arXiv preprints and one vendor research page - and Yan is summarising them, not running them. That
has two consequences the rest of this folder is built around:

1. **The corroboration gate works unusually well on it and means unusually little.** The second leg
   is a figure lifted verbatim from the primary paper, so "the prose agrees with the figure" tests
   whether *Yan read the paper correctly* - which is worth testing and is not evidence about the
   world. Nodes here are gated on that reading, and the confidence column says so.
2. **Where the two legs disagree, the figure wins**, because the figure is the primary artifact and
   the prose is the summary. That asymmetry does not exist on a normal single-author source, and it
   is why five of the eight divergences below (`d1`-`d5`) are recorded as *the article understating its own
   figures* rather than as an internal contradiction.

**No primary was read.** The seven papers were not fetched, so every `d` finding is a statement about
this article against the figure it chose to embed, never about the paper as a whole.

### Compound pass, completed 2026-08-15

Promoted **claims 197-205**, and **amended claim 132** with a fourth instance rather than stacking a
duplicate - the attempt-budget variant, where three benchmarks report at single-shot, best-of-three
and best-of-eight and the article discloses none of them.

Merged into [`evals.md`](../../brain/topics/evals.md) (primary home, new synthesis section, four
Key-claims rows, one Key visual, three Open questions),
[`agent-security.md`](../../brain/topics/agent-security.md) (new synthesis section on offensive
capability, three Key-claims rows) and [`agents.md`](../../brain/topics/agents.md) (two Key-claims
rows). Nine terms added to [`glossary.md`](../../brain/glossary.md). `INDEX.md` Sources row plus all
three Topics rows updated. Dated entry in [`log.md`](../../brain/log.md).

**[ADR-0025](../../brain/decisions/0025-a-secondary-source-corroborates-its-own-reading.md) written
in the same pass** - *a secondary source corroborates its own reading, not the world* - the structural
call this source forced, and the sibling of ADR-0022 from the opposite direction.

`python3 validate.py` passes: 25 sources, 11 topics, 13 checks, nothing to report. All 8 kept frames
verified cited by this source's own `LEARNING.md`.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
