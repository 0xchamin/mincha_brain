# Topic: MCP (Model Context Protocol)

**Status:** **emerging** (2 sources - S10 "Tool search", Microsoft, 2026-07-29; S12 Google Cloud's
multi-tenant agentic AI reference architecture, 2026-06-18). **Both are secondary**
([ADR-0013](../decisions/0013-secondary-but-substantial.md)): neither is *about* MCP, and each teaches
the protocol on the way past something else - S10 what a catalog costs the model, S12 what deploying a
server costs your isolation model. See [ADR-0012](../decisions/0012-a-mention-is-not-a-source.md) for
why S9's earlier mention did not count.

**The count rose and the corroboration did not.** S10 and S12 overlap on nothing: one is about
`tools/list` and retrieval, the other about where a server sits in a network. They do not confirm a
single claim of each other's, so **`established` is no nearer than it was at one source**. What has
changed is the shape of the hole - this note now covers the client side *and* the deployment side, and
still has no primary source.

> **Read the scope caveat first.** Everything below is about **tools and servers**. **Resources,
> prompts, sampling, the initialisation handshake and the spec version are still at zero sources**, and
> **no source in this note has ever named a spec version**. This note has no primary source, so it is
> scoped by accident rather than by design (ADR-0013 records this as a drift risk). Do not read
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

### Where you put the server is a security decision before it is an ops decision

S10 looks at MCP from the client's side. S12 looks at it from the deployment's, and finds that the
protocol's most consequential property there is not a primitive at all - it is that **an MCP server is
an ordinary network service, so where you run it decides what your isolation guarantee is made of**.

In S12's architecture MCP is the **mandatory data seam**: "MCP server facilitates access between the
tenant agent and tenant datastore", the datastore is reachable only through it, and the architecture
figure has **no edge from the agent to the data** at all
([S12](../../sources/260802_gcp-multi-tenant-agentic-ai/LEARNING.md) `n9`, claim 104). The agent holds
no datastore credentials; every retrieval is a tool call. That is worth naming as a pattern
independently of the vendor: **the data boundary becomes a property of the topology rather than of the
agent's good behaviour.**

Then the fork, which S12 states with unusual clarity (`n10`, claim 105):

| | **Local** - one server per tenant | **Shared** - one server for all tenants |
|---|---|---|
| Network | the project perimeter and principal boundary supply isolation "inherently" | needs private connectivity - Private Service Connect or VPC peering |
| Management | each unit's team runs its own; N servers | one central team; no duplicated implementations |
| Security | "fixed IAM boundaries... don't require complex identity mappings" | **"you securely propagate the end-user identity"** and the server enforces fine-grained access from it |
| Recommended for | sensitive or regulated data | common corporate systems - expenses, HR, knowledge bases |

**The right-hand column is where the interesting cost is, and it is not an ops cost.** A local server
is isolated whether or not its authors ever thought about tenancy; there is nothing across the wall to
reach. A shared server is isolated only if identity is attached, propagated unforgeably, and
authorized correctly **on every call** - three things somebody has to build. See
[`agent-security.md`](agent-security.md) for the general form (claim 106) and for why this is the
field's gap rather than the document's.

> **This partially answers this note's own open question** - "what does an aggregating server owe the
> servers behind it?", whose first item was auth propagation. S12 supplies the **requirement**, from
> the deployment side, and no more of an answer than S10 did: no token format, no exchange, no audience
> restriction, no delegation model, and nothing about the agent acting on a schedule with no user
> present. Two sources have now independently arrived at the same missing piece from opposite
> directions, which is the strongest signal in this note about what to research next.

## Key claims

| Claim | Spec version | Sources (cited) | Confidence |
|---|---|---|---|
| **`tools/list` puts the whole catalog in per-turn context**, so context cost scales with what is connected rather than with the task - 541k tokens at 1,180 tools. Prompt caching makes it ~90% cheaper, not absent, and cached tokens still consume attention. | unstated | S10 §intro + §The default agent tax + `fig_tokens-chart` (`n1`, `n2`, `n9`) | emerging (measured on ToolRet; the caching point is single-leg) |
| **Many clients refuse to call a tool absent from `tools/list`**, so any lazy-discovery design needs a *registered* proxy tool to carry the dispatch. | unstated | S10 §Two tools instead of a hundred (`n4`) | needs-check ("many runtimes", none named, no spec citation) |
| **An MCP server can aggregate other MCP servers** (streamable HTTP, bearer auth), which is what allows large capabilities to be added **with no new protocol primitive** and to extend to non-MCP tool sources behind the same index. | unstated | S10 `fig_image-6` (`n7`, figure-only) + §Two tools instead of a hundred (`n5`, `n6`) | needs-check on the aggregation mechanic (figure-only); emerging on "no new primitive" |
| **A tool's indexed surface is name, description, argument names and argument descriptions, three levels deep** - and a field can be indexed while staying invisible in MCP responses, so search vocabulary and model-facing schema are separable. | unstated | S10 §Two tools instead of a hundred + §Tuning the search space (`n8`, `n14`) | emerging (`n14` corroborated prose vs code) |
| **An MCP server can be the mandatory data seam** - the agent holds no datastore credentials and every retrieval is a tool call, so the data boundary is a property of the topology rather than of the agent's behaviour. | unstated | S12 §Architecture (`n9`) + `visuals/fig1b_two-tenants.png` (claim 104) | emerging |
| **Local vs shared server deployment is an isolation decision.** Local gets isolation from the perimeter it sits in and needs no identity mapping; shared needs private connectivity plus end-user identity propagated and enforced on every call. Recommended split: local for regulated data, shared for common corporate systems. | unstated | S12 §Design alternatives, MCP servers (`n10`, claim 105) | emerging - corroborated on local (it is what the figure draws); **single-leg on shared, which is drawn nowhere** |

## Key visuals

![Two tools instead of a hundred: tools/list exposing 100 resident tool schemas, versus tool_search and call_tool over a toolbox index, with the rest of the catalog indexed but never listed](../../sources/260801_tool-search-toolboxes/visuals/fig_tool-search-figure.png)
> The protocol-level shape of lazy tool discovery: the catalog stays behind the aggregator, and the
> only two tools in `tools/list` are a search and a dispatcher. The dashed box is the part that
> matters for this note - remote MCP servers sit alongside OpenAPI and A2A, all reached through one
> mechanism because the aggregator is the one thing the client talks to. S10 `fig_tool-search-figure`,
> `n3`/`n6`. Full walkthrough in the
> [source note](../../sources/260801_tool-search-toolboxes/LEARNING.md).

## Open questions / conflicts

- **This topic still has no primary source.** Both sources came here sideways, so the coverage is
  shaped by what each happened to need: S10 tools and their cost, S12 servers and where they sit.
  **Resources, prompts, sampling, transports, the handshake, and any spec version at all remain at
  zero.** The most valuable next source here is still a plain one about the protocol.
- **No spec version is pinned anywhere in this note**, because **neither** source names one. Every
  mechanic above should be re-checked against a dated spec before being relied on.
- **What does an agent present to a shared MCP server, and how does the server verify it?**
  Promoted from a sub-bullet to a question of its own, because two independent sources now stop at
  exactly this point: S10 lists auth propagation first among the things an aggregating server's
  design ignores, and S12 makes propagation a hard requirement of the deployment it recommends for
  common corporate tools while specifying nothing (S12 `n11`). **The concrete artifacts to check
  next: the MCP authorization specification, OAuth 2.1 token exchange, SPIFFE/SPIRE.** Shared with
  [`agent-security.md`](agent-security.md), where it is the same question wearing a threat model.
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

- **S12** - [Multi-tenant agentic AI system](../../sources/260802_gcp-multi-tenant-agentic-ai/LEARNING.md)
  (Google Cloud Architecture Center, reviewed 2026-06-18). **Secondary again, and from the opposite
  side to S10**: a reference architecture in which MCP is the mandatory data seam, and the local-vs-shared
  deployment fork is an isolation decision. Admitted under
  [ADR-0013](../decisions/0013-secondary-but-substantial.md) - roughly fifty lines with a named trade,
  three feature axes per option and a recommendation is substance, not a mention. **T2 vendor,
  completely unmeasured**, and it names no spec version, no transport and no primitive. Read it here
  for deployment topology only; the client-side mechanics are all S10's.
- **S10** - [Tool search: Finding the right tool at the right time](../../sources/260801_tool-search-toolboxes/LEARNING.md)
  (Lisa Brown Jaloza, Microsoft, 2026-07-29). **A secondary source, admitted as one under
  [ADR-0013](../decisions/0013-secondary-but-substantial.md)**: the article is about tool retrieval,
  and MCP is the substrate it happens to explain along the way. **T2 vendor post on its own preview
  product**, but better evidenced than that class usually is - a public benchmark, an honestly stated
  baseline, and a reported loss. Read it here for the cost model of `tools/list`, the
  unregistered-tool guard, and aggregation; read it in [`rag.md`](rag.md) for the retrieval numbers.
