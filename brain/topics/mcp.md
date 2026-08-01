# Topic: MCP (Model Context Protocol)

**Status:** **emerging** (1 source - S10 "Tool search", Microsoft, 2026-07-29).
**Basis:** the brain's longest-standing empty topic finally has content, and it arrives **sideways**.
S10 is an article about tool retrieval, not about MCP - but its mechanism is built on the protocol's
shape, so it teaches what `tools/list` costs, how clients treat unregistered tools, and what an
aggregating server can do. See [ADR-0013](../decisions/0013-secondary-but-substantial.md) for why a
secondary source counts here while S9's earlier mention did not
([ADR-0012](../decisions/0012-a-mention-is-not-a-source.md)).

> **Read the scope caveat first.** Everything below is about **tools**, and specifically about what
> tools cost the model. **Resources, prompts, sampling, the initialisation handshake and the spec
> version are still at zero sources** - this note has no primary source, only a secondary one, so it
> is scoped by accident rather than by design (ADR-0013 records this as a drift risk). Do not read
> `emerging` as "the brain understands MCP".

> Living, cross-source synthesis on MCP. Many sources feed this note; **merge and de-duplicate** as
> they arrive (architect persona). Every claim cited. When you learn from a source, pin the spec
> version it refers to.

## What this covers

The Model Context Protocol: servers, tools, resources, prompts, transport (stdio / HTTP), the
client-server handshake, and how agents consume MCP capabilities.

**Boundary with the neighbours:** [`agents.md`](agents.md) owns the loop that calls the tools;
[`context-engineering.md`](context-engineering.md) owns the budget question of which tools reach the
model on a given call (that framing lives there, as claim 85); this note owns **the protocol
mechanics that make those decisions possible or impossible**.

## Synthesis

### `tools/list` is a per-turn cost centre, and it scales with the catalog

The protocol's discovery call hands the client every tool definition up front, and those definitions
are then **resident in the model's context on every turn**: "names, descriptions, JSON schemas,
argument definitions, and nested parameters before you've asked anything useful" [S10 §intro, `n1`].

The size of that is measured, on ToolRet (44,000+ tools): **541k tokens at 1,180 tools**
[S10 `fig_tokens-chart`, `n9`]. The cost is a function of **what is connected**, not of what the task
needs.

**Prompt caching does not solve it, and the distinction is the useful part.** Caching was on in the
baseline because it is the Azure OpenAI default, and cached tokens are roughly 90% cheaper - "not
free, and cached context **still competes for the model's attention**" [S10 §The default agent tax,
`n2`]. See [`context-engineering.md`](context-engineering.md) for the measured reason that matters:
degradation tracks what is *in* the window, not what it cost to put there.

### A client will refuse to call a tool that was not in `tools/list`

The single most reusable protocol fact in this note, and it comes out sideways as an implementation
constraint: "if a tool wasn't registered in the original `tools/list`, **many runtimes will guard
against the model calling it directly as an unknown tool**" [S10 §Two tools instead of a hundred,
`n4`].

**This is why any lazy-loading design needs two tools rather than one.** A tool that was retrieved
rather than listed cannot be invoked directly, so a *registered* proxy has to carry the call. It also
hands the platform something it wants anyway: one dispatch point through which every call passes, so
policy can be applied in a single place.

> ⚠️ **"Many runtimes", not "the protocol".** S10 describes client behaviour it encountered, not a
> spec requirement, and names no runtime and no spec version. Treat it as a portability constraint you
> will probably hit, not as a rule you can cite.

### An MCP server can front other MCP servers

The Foundry Toolbox is itself reached over MCP - "Connect to this toolbox using MCP and call it from
your agent code" - at an endpoint of the form `.../toolboxes/{name}/versions/{version}`, via
`MCPStreamableHTTPTool` with a bearer token injected per request, with four ordinary MCP servers
attached inside it [S10 `fig_image-6`, `n7`].

**This is the mechanic that makes the rest unremarkable, in the good sense.** An aggregating server is
free to expose whatever tools it likes and to service them however it wants, so a capability as large
as "replace the catalog with a search index" needed **no new protocol primitive, no model-specific
feature, and no shared ranking semantics across providers** [S10 §Two tools instead of a hundred,
`n5`]. The aggregator is also the layer that makes the mechanism cover **non-MCP** sources - OpenAPI,
A2A and native tools sit behind the same index, indexed but never listed [S10 `fig_tool-search-figure`,
`n6`].

> 💡 **Aggregating (or proxying) MCP server** - a server whose tools are drawn from other servers
> rather than implemented locally. Because a client sees only the aggregator's `tools/list`, the
> aggregator can add, hide, rename or index what is behind it without any client or downstream server
> changing.

**Composition is the leverage point of this protocol, and this brain has exactly one data point on
it.** Everything S10 achieves comes from sitting *between* client and servers.

### A tool's searchable surface is not the same as its model-facing surface

What an index can see in a tool: **name, description, argument names, and argument descriptions, up to
three levels of nesting** [S10 §Two tools instead of a hundred, `n8`].

And those need not be the fields the model sees. Foundry adds `additional_search_text`, indexed for
retrieval but "**not visible to models in MCP responses**", with "no changes made to the original tool
schema of the source MCP server" [S10 §Tuning the search space, `n14`]. Three consequences fall out,
and the third is the one nobody in the source mentions:

- retrieval vocabulary can be tuned **without spending model tokens**;
- a **third-party** server can be tuned for your users' vocabulary **without forking it**;
- **an invisible field steers which capability the agent is offered.** Whoever writes
  `additional_search_text` influences tool selection with no trace in the context the model can
  inspect. *(This brain's observation. S10 never discusses security -
  commentary, not a claim. See [`agent-security.md`](agent-security.md).)*

## Key claims

| Claim | Spec version | Sources (cited) | Confidence |
|---|---|---|---|
| **`tools/list` puts the whole catalog in per-turn context**, so context cost scales with what is connected rather than with the task - 541k tokens at 1,180 tools. Prompt caching makes it ~90% cheaper, not absent, and cached tokens still consume attention. | unstated | S10 §intro + §The default agent tax + `fig_tokens-chart` (`n1`, `n2`, `n9`) | emerging (measured on ToolRet; the caching point is single-leg) |
| **Many clients refuse to call a tool absent from `tools/list`**, so any lazy-discovery design needs a *registered* proxy tool to carry the dispatch. | unstated | S10 §Two tools instead of a hundred (`n4`) | needs-check ("many runtimes", none named, no spec citation) |
| **An MCP server can aggregate other MCP servers** (streamable HTTP, bearer auth), which is what allows large capabilities to be added **with no new protocol primitive** and to extend to non-MCP tool sources behind the same index. | unstated | S10 `fig_image-6` (`n7`, figure-only) + §Two tools instead of a hundred (`n5`, `n6`) | needs-check on the aggregation mechanic (figure-only); emerging on "no new primitive" |
| **A tool's indexed surface is name, description, argument names and argument descriptions, three levels deep** - and a field can be indexed while staying invisible in MCP responses, so search vocabulary and model-facing schema are separable. | unstated | S10 §Two tools instead of a hundred + §Tuning the search space (`n8`, `n14`) | emerging (`n14` corroborated prose vs code) |

## Key visuals

![Two tools instead of a hundred: tools/list exposing 100 resident tool schemas, versus tool_search and call_tool over a toolbox index, with the rest of the catalog indexed but never listed](../../sources/260801_tool-search-toolboxes/visuals/fig_tool-search-figure.png)
> The protocol-level shape of lazy tool discovery: the catalog stays behind the aggregator, and the
> only two tools in `tools/list` are a search and a dispatcher. The dashed box is the part that
> matters for this note - remote MCP servers sit alongside OpenAPI and A2A, all reached through one
> mechanism because the aggregator is the one thing the client talks to. S10 `fig_tool-search-figure`,
> `n3`/`n6`. Full walkthrough in the
> [source note](../../sources/260801_tool-search-toolboxes/LEARNING.md).

## Open questions / conflicts

- **This topic has no primary source.** Everything above came from an article about something else,
  so the coverage is shaped by what S10 happened to need: tools, and only their cost. **Resources,
  prompts, sampling, transports, the handshake, and any spec version at all remain at zero.** The
  most valuable next source here is a plain one about the protocol.
- **No spec version is pinned anywhere in this note**, because S10 never names one. Every mechanic
  above should be re-checked against a dated spec before being relied on.
- **Is the unregistered-tool guard a spec rule or a client convention?** S10 says "many runtimes"
  and names none [`n4`]. The answer changes whether the two-proxy pattern is a workaround or the
  intended shape, and it is cheap to research.
- **What does an aggregating server owe the servers behind it?** S10 shows aggregation working and
  ignores every question it raises: error and auth propagation, version skew, what happens when a
  downstream server changes its schema under the index, and who is accountable for a call the
  aggregator dispatched.
- **`additional_search_text` is an unexamined trust surface.** Index-only text that is invisible to
  the model decides which tools the model is offered. Recorded as commentary above and in
  [`agent-security.md`](agent-security.md); no source addresses it.
- **A sighting, deliberately not counted as a source.** S9 (Microsoft Agent Framework, 2026-05-28)
  names **MCP** as one of exactly two tool-integration standards in its ecosystem column, beside
  OpenAPI [S9 `fig_AgentLoop`]. That is evidence about MCP's **position** and none about its
  mechanics, so it remains a sighting under
  [ADR-0012](../decisions/0012-a-mention-is-not-a-source.md) and is **not** listed below - the arrival
  of S10 does not retroactively promote it. Kept here so the sighting stays findable.

## Sources feeding this topic

- **S10** - [Tool search: Finding the right tool at the right time](../../sources/260801_tool-search-toolboxes/LEARNING.md)
  (Lisa Brown Jaloza, Microsoft, 2026-07-29). **A secondary source, admitted as one under
  [ADR-0013](../decisions/0013-secondary-but-substantial.md)**: the article is about tool retrieval,
  and MCP is the substrate it happens to explain along the way. **T2 vendor post on its own preview
  product**, but better evidenced than that class usually is - a public benchmark, an honestly stated
  baseline, and a reported loss. Read it here for the cost model of `tools/list`, the
  unregistered-tool guard, and aggregation; read it in [`rag.md`](rag.md) for the retrieval numbers.
