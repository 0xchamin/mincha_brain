# Source - Scaling AI Agent Infrastructure with the MCP Stateless updates

> Persona: **curator** - re-adopt when working this file.

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | blog |
| URL | https://developers.googleblog.com/scaling-ai-agent-infrastructure-with-the-mcp-stateless-updates/ |
| Title | Scaling AI Agent Infrastructure with the MCP Stateless updates |
| Author / channel | Kurtis Van Gent (Senior Staff Software Engineer, Google Cloud Data) + Alan Blount (Technical Product Manager, Google Cloud AI) - Google Developers Blog |
| Published | 2026-08-05 |
| Duration / length | ~2,030 words, 6 code blocks |
| Commit SHA | n/a |
| License | n/a (article, read in place; not redistributed) |
| Ingested | 2026-08-07 |
| Access | open |
| Topics | mcp, agent-security, agents |
| Visual leg | skipped (no article figures - the only two images on the page are related-post thumbnails). **Second leg is the protocol artifacts** - see below |
| Status | compounded |

## The gate on this source, stated before any verdict is read

**Leg A is the article prose. Leg B is the six verbatim protocol artifacts** it prints: the legacy
`initialize` handshake, the new stateless `POST /mcp`, the `InputRequiredResult`, the TypeScript task
handler, and the install/codemod commands. That is the **code leg of the code-to-docs gate arriving
inside a blog post**, not a new leg type - the prose describes a mechanism and the payload shows it,
which is exactly the shape `AGENTS.md` specifies for code sources.

**It is a genuinely better second leg than a figure would have been**, and that is worth saying
because this brain's other Google source (S12) had the weaker kind. A diagram is the same claim
drawn instead of typed, by the same author, in the same document. A protocol payload is
**machine-checkable**: you can diff the legacy handshake against the new request and watch the same
three fields move, and you can decode a base64 blob and find out what is actually in it. Both of
those happened in this pass, and the second one produced the sharpest finding in the source (`n8`,
`d1`).

**What it still cannot do.** Both legs are the same two authors on the same page, so a `corroborated`
verdict below means *this article is consistent with its own examples* and is no evidence about the
world. In particular the **specification itself was not read in this pass** - no deep research was
requested - so every SEP number, every claim about what the spec *requires*, and the reading of the
`requestState` example are gated against the article alone. See "What to distrust" in `LEARNING.md`.

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `raw/article.md` - the captured ground truth (extracted from `raw/article.html`).
3. `nodes.md` - knowledge nodes (gated claims + citations).
4. `context/` - empty; no deep-research pass was requested.
5. `LEARNING.md` - the distilled learning document.

## Ingest notes

- **Capture method:** `WebFetch` for the first read, then `curl` to `raw/article.html` and a
  stdlib-only HTML-to-markdown extraction into `raw/article.md` so the code blocks survived intact.
  The code blocks are the second leg, so a lossy capture would have cost the gate.
- **Visual pre-filter:** `grep` over the raw HTML returned five `<img>` tags - two site logos and
  three related-post thumbnails ("Agent Plugins", "A unified API for AI model routing"). **The
  article body contains no figures at all.** Nothing to `view`; the visual leg is skipped rather
  than analysed, and no frames are kept.
- **One artifact was executed rather than read.** The `requestState` value in the MRTR example was
  base64-decoded during the gate. It is plaintext JSON (`{"step":1,"files":["a","b","c"]}`) with no
  signature, MAC or ciphertext. That single command is what turned `d1` from a hunch into a node.
- **Limitations:** release-candidate specification, all four SDKs at beta, and a vendor writing about
  a standard it says it led. Nothing here is measured - the article contains no benchmark, no latency
  figure and no cost figure, despite performance being its entire argument.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
