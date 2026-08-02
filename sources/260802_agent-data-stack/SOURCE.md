# Source - How we built LangChain's agent-first data stack

> Persona: **curator** (media) / **code-explorer** (code) - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table. The agent fills it on the paste-a-URL trigger
> and keeps it current. Name this folder `YYMMDD_slug` (see `../../AGENTS.md`).

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | blog |
| URL | https://www.langchain.com/blog/agent-data-stack |
| Title | How we built LangChain's agent-first data stack |
| Author / channel | Emily Hawkins (data team, LangChain) |
| Published | 2026-07-27 |
| Duration / length | ~2,890 words, 14 min read, 2 substantive figures |
| Commit SHA | n/a |
| License | n/a (article, read in place; not redistributed) |
| Ingested | 2026-08-02 |
| Access | open |
| Topics | context-engineering, rag, evals, skills |
| Visual leg | analysed (2 frames kept) |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/article.md` - the captured article text (converted from `raw/page.html`).
3. `nodes.md` - knowledge nodes (corroborated claims + visuals + citations).
4. `context/01_data-agent-accuracy-and-prior-art.md` - **external evidence** (deep-research pass).
5. `LEARNING.md` - the distilled learning document.
6. `visuals/` - the two curated figures.

## Ingest notes

- **Capture method:** `curl` the article HTML to `raw/page.html`, then a per-source Python
  converter to `raw/article.md` (headings, lists, captions and image placeholders preserved). The
  "Related content" trailer was trimmed - site chrome, not the article.
- **Visual pre-filter:** 26 `<img>` tags on the page, of which **23 are chrome** (nav icons, author
  avatars, related-post thumbnails). Three sit in the article body; one of those is a decorative
  title card carrying only the headline, and was **deleted after viewing** per the prune rule.
  **2 figures kept and `view`ed**, both carrying claims the prose does not make.
- **The figures are load-bearing here**, which is unusual for a company-blog post. `fig2` is the
  only statement of the underlying pipeline, and `fig3` is the only place the five context stores
  appear as one bounded object. Both produced findings the prose does not state (`d1`, `d2`).
- **Legs for this source:** Leg A is the article prose; Leg B is one of the two figures. Two prose
  passages agreeing with each other are **one** leg - and this article repeats itself deliberately
  (a "How we think about context" section and a "What we've learned" section restating the same
  lessons), so that rule does real work here.
- **Deep research:** requested by the user at ingest time. One pass,
  `context/01_data-agent-accuracy-and-prior-art.md`, targeting the measurement gap (`n9`) and the
  prior art behind endorsements (`n6`).

## Trust caveats (read before citing anything here)

- **T4 practitioner experience published on a T2 vendor blog.** The author is LangChain's data lead
  writing about LangChain's own internal migration - an experience report, the same evidential class
  as most of this brain. But it is hosted by a company that sells LangSmith, and it names LangSmith
  and LangSmith Fleet inline as the observability and access path "if their data agent is built
  in-house".
- **It is also, functionally, a customer testimonial for Hex** - the vendor chosen in the evaluation
  the post describes. No commercial relationship is disclosed either way. Weigh the
  vendor-selection narrative accordingly; the **context-layer design is tool-independent** and is
  the part worth taking.
- **Every number is adoption; none is accuracy.** Conversation volume, user coverage and migration
  speed are all reported. Answer correctness is **never measured** - the article says so itself and
  files evals under "Where we're going next". See `n9`, `d3` and the deep-research note.
- **n = 1 company, ~290 people, 3-person data team.** Nothing here is a controlled comparison.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
