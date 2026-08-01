# Topic: MCP (Model Context Protocol)

**Status:** seed (no source yet -> emerging at 1 source -> established at 2+ corroborating sources)

> Living, cross-source synthesis on MCP. Many sources feed this note; **merge and de-duplicate**
> as they arrive (architect persona). Every claim cited. When you learn from a source, pin the
> spec version it refers to.

## What this covers

The Model Context Protocol: servers, tools, resources, prompts, transport (stdio / HTTP), the
client-server handshake, and how agents consume MCP capabilities.

## Synthesis

_(empty - populated as sources are ingested.)_

## Key claims

| Claim | Spec version | Sources (cited) | Confidence |
|---|---|---|---|
| _(none yet)_ | - | - | - |

## Key visuals

_(Architecture / sequence diagrams across sources, embedded with caption + citation.)_

## Open questions / conflicts

- **A sighting, deliberately not counted as a source.** S9 (Microsoft Agent Framework, 2026-05-28)
  names **MCP** as one of exactly two tool-integration standards in its ecosystem column, beside
  OpenAPI [S9 `fig_AgentLoop`]. That is evidence about MCP's **position** - a major vendor treating
  it as one of the two ways tools reach an agent - and **no evidence at all about its mechanics**,
  which is what this note covers. One box in one diagram does not populate a topic, so this note
  stays `seed` and S9 is not listed below - **the rule is [ADR-0012](../decisions/0012-a-mention-is-not-a-source.md):
  a mention is not a source.** Recorded here so the sighting is findable rather than lost. See
  [`agents.md`](agents.md) for what S9 actually taught.
- **What this topic still needs:** a source on the protocol itself - servers, tools, resources,
  prompts, transport, the handshake. Zero so far.

## Sources feeding this topic

- _(none yet - see the sighting in Open questions above.)_
