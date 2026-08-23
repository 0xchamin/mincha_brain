# Topic: MCP (Model Context Protocol)

**Status:** **established** (6 sources - S10 "Tool search", Microsoft, 2026-07-29; S12 Google Cloud's
multi-tenant agentic AI reference architecture, 2026-06-18; **S23 Google's MCP stateless-updates
announcement, 2026-08-05**; **S27 GitHub's own MCP server at operator scale, ~April 2026**; **S28 Kent
C. Dodds walking `2026-07-28` as somebody who migrated onto it, 2026-08-20**; **S29 DoorDash's Agent
Gateway, the first source here written from the *consumer* side of the protocol, 2026-07-30**). S23 is
this note's first primary source - the first that is *about* MCP rather than teaching it on the way
past something else - and the first anywhere in this brain to **pin a specification version**
(2026-07-28, superseding 2025-11-25). S10 and S12 remain secondary under
[ADR-0013](../decisions/0013-secondary-but-substantial.md); see
[ADR-0012](../decisions/0012-a-mention-is-not-a-source.md) for why S9's earlier mention did not count.

**Advanced to `established` on 2026-08-16 ([ADR-0028](../decisions/0028-mcp-established-on-an-independent-implementation.md)),
and the reason is not the source count.** [ADR-0022](../decisions/0022-a-primary-source-is-not-corroboration.md)
named the exact bar: two sources confirming the same mechanic. S27 does that for the first time in
this note's history. S23 asserts a specification in which state relocates rather than disappears, and
this brain's reading of it was claim 180; S27 is an independent implementer at a **different company**
running a stateless MCP server at ~7.34M tool calls a week with **Redis still in the architecture
diagram**, in a system built *before* the spec change S23 documents (claim 224). That is convergent
engineering rather than compliance, and it corroborates precisely the half of claim 180 that was
weakest, which was the generalisation rather than the mechanics.

> **Read the advance narrowly.** This note crosses the line on **one** corroborating group where
> `agent-security.md` cleared it on three, so it has just crossed rather than comfortably cleared.
> **Nothing else here got stronger** - S27 confirms nothing about caching, deprecation policy, JSON
> Schema support, resource indicators or the tool-search mechanics, and the per-claim confidence
> column below is still where the real information lives. **The lesson worth carrying is about which
> source to hunt for when a topic stalls**: this note spent three sources trying to corroborate a
> specification by reading more about the specification, and what moved it was somebody building the
> thing and reporting what stayed in their architecture diagram.

**S28 (2026-08-21) is the fifth source and it closes the note's oldest complaint about itself.** The
`established` block above ends by saying *almost nothing here is measured by anyone*, and every source
before this one described a design. S28 describes **what happened after the design shipped**, from a
server carrying one telemetry point per request: three weeks after `2026-07-28` published with all four
Tier 1 SDKs supporting it, **25,288 requests had been served and none came from a client speaking it**
(claim 227). It is a tiny, self-selected population over six to thirteen days, and it is nonetheless
the first adoption number this note has ever held.

**It also strengthens two things and adds one.** It is a second independent reading of the release, so
claims 179 and 183 are no longer resting on a single vendor post. It reproduces **two of the three DCR
defects** from an operator with no connection to GitHub, which is what upgraded claim 222 from
`needs-check` to corroborated - and, importantly, one of those operators runs an authorization server
for millions of developers while the other runs a personal assistant, which is what makes the failure
modes structural. **The new material is CIMD** (claim 228), the replacement mechanism S27 could only
name as an unpromised direction.

> **The evidential shape of this source is unusual and worth knowing before citing it.** It is a
> screencast, so the visual leg is not slides but **the official blog post, the author's own merged
> PR, and his own public dashboard readout**, displayed on screen. On the specification claims that
> makes the second leg the primary document rather than a summary of it. On the adoption claims it
> makes the two legs genuinely independent, since the narration is recollection and the visual is an
> aggregate query. **T4 by tier and better-evidenced than its tier suggests, on exactly the claims
> where it matters.**

**Status deliberately held at `emerging`, and the reason is the same one this note has recorded
twice.** A primary source fixes the note's *scope* defect and does nothing for its *corroboration*
defect. S23 overlaps S10 and S12 on almost nothing - transport mechanics against catalog cost against
deployment topology - so **no two sources here confirm the same mechanic**, which is what `established`
means in this brain (see `agent-security.md`, advanced on three independent corroborating groups).
Recorded as [ADR-0022](../decisions/0022-a-primary-source-is-not-corroboration.md), because "the count
rose and the corroboration did not" has now happened three times in this note and deserved to stop
being rediscovered.

**What did change is real, and it is mostly the shape of the hole.** The note now covers the client
side (S10), the deployment side (S12) and **the protocol itself** (S23). Two of its standing open
questions moved: the spec version is pinned, and **audience restriction finally has a name** (RFC
8707, claim 182), which is the mechanism S10 and S12 both stopped short of from opposite directions.

> **Read the scope caveat first, in its new and smaller form.** ~~Resources, prompts, sampling, the
> initialisation handshake and the spec version are still at zero sources~~ - S23 closes **the
> handshake** (by deleting it, claim 179), **the spec version**, and **sampling** (by deprecating it,
> claim 183). **Resources and prompts remain at zero as first-class subjects**, appearing only as
> names in a header field and a cache rule. **Nothing in this note is measured by anyone**: S23's
> entire argument is about scale, cost and latency, and it contains no benchmark, no latency figure
> and no cost comparison. Do not read `emerging` as "the brain understands MCP".

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

### The protocol core is stateless as of 2026-07-28, and the handshake is gone

**The substrate section this note lacked until S23.** Under specification 2025-11-25 an HTTP client
completed an `initialize` handshake, received an `Mcp-Session-Id`, and returned it on every later
call, "pinning the client to the specific container or pod that held its **in-memory** session state"
[S23 §Why Sessions Were a Production Bottleneck, `n1`]. The failure that produced is worth stating
precisely, because it is a correctness error rather than a performance one: three pods behind a
round-robin balancer return **`400 Session Not Found`** on the client's second request [S23 `n2`].

The 2026-07-28 specification removes `initialize`/`initialized` (SEP-2575) and the `Mcp-Session-Id`
header (SEP-2567), and the three facts the handshake negotiated now travel in a **`_meta`** block on
every request under `io.modelcontextprotocol/` keys [S23 §The New Request Model, `n3`]. Routing
metadata is promoted into HTTP headers - `Mcp-Protocol-Version`, `Mcp-Method`, `Mcp-Name` - mirrored
against the JSON-RPC body and rejected with a **`-32020`** mismatch code, so intermediaries route,
rate-limit and audit **without deep packet inspection** [S23 §HTTP Standardization, `n4`, `n5`]
(claim 179).

> **This is the strongest artifact-level evidence in the note, and it is worth knowing why.** S23 has
> no figures. Its second leg is the **six protocol payloads it prints**, which is the code-to-docs
> gate arriving in a blog post - and a better second leg than a diagram, because the legacy handshake
> and the new request can be **diffed**, and the same three fields are visible moving from a call that
> happens once into a call that happens every time. A diagram is the same claim drawn instead of
> typed; a payload can be decoded. See that source's `SOURCE.md` for the full statement of its gate.

Round-robin routing, scale-to-zero serverless deployment and failover invisible to the client are
**consequences of that single change**, not separate features, which is why they are gated as one node
rather than four. Note what this does to S12's world: the deployment fork below was drawn when a
remote MCP server needed sticky affinity or a shared session store, and **the stateless core removes
the infrastructure half of that cost** while leaving the identity half exactly where it was.

### Statelessness relocated the state, three times, to three different owners

**The most transferable thing in this note, and it generalises well past MCP.** S23's own security
section concedes the pattern in one sentence - responsibility "shifts from the transport layer to the
application layer" - and never adds it up [S23 §Clear Security & Capability Boundaries, `n10`].
Adding it up gives three relocations, each with a payer:

| What was stateful | Where it went | Who pays |
|---|---|---|
| Session negotiation (`initialize`, `Mcp-Session-Id`) | **The wire** - `_meta` on every request [`n3`] | Bandwidth and tokens, permanently, per request |
| Server-to-client elicitation (a held-open SSE connection) | **The client** - an echoed `requestState` [`n7`] | The trust model, and S23 prices it at nothing [`n8`, `d1`] |
| Long-running tool execution (a blocked connection) | **The application** - a shared task store [`n9`] | You, in the Redis the headline says you removed [`d2`] |

The two mechanisms are worth naming because they are what a client author has to implement. **MRTR**
(Multi Round-Trip Requests, SEP-2322) converts a server-to-client question into two independent
requests: the server returns an `InputRequiredResult` carrying the question and an opaque
`requestState`, and the client collects the answer and reissues the call with the state echoed back,
so "any server instance behind your load balancer can pick up the retry request" [S23 §MRTR, `n7`].
The **Tasks extension** (SEP-2663) graduates from experimental to first-class: a slow tool returns a
`taskId` immediately and the client polls `tasks/get` or subscribes to `tasks/update` [S23 §The Tasks
Extension, `n9`].

> **The divergence is worth carrying, because the headline is the misleading half.** S23's
> stateless-core bullet list says "**No Redis Sessions Needed**", and four sections later its own
> Tasks example contains `// Store initial task state in a shared datastore (e.g. Redis)`. Both are
> true. What was removed is Redis as a **transport session store**, keyed by connection and hit on
> every single call; what remains is Redis as an **application task store**, keyed by unit of work and
> touched only by async operations. That is a large real improvement and not the elimination the
> bullet implies, and a reader planning capacity from the bullet alone will under-provision [S23
> `d2`] (claim 180).

**The generalisation, and this brain's second arrival at it.** "Stateless" is a claim about a *layer*,
never about a system. Claim 106 records the same conversion from the isolation side: sharing a
component changes what kind of thing the guarantee is, from a property of the topology into a claim
about an implementation. Under 2025-11-25 session integrity was structural, because the state never
left the process that owned it. Under 2026-07-28 it becomes an obligation somebody discharges, in
three places, separately. See [`agent-security.md`](agent-security.md) for what that costs at the
second row (claim 181).

### Authorization finally has a mechanism, and it is one clause long

S23 adds two OAuth-layer requirements, and they matter to this note out of proportion to their length
because **two of its sources stopped at exactly this point from opposite directions**. Issuer
verification (**RFC 9207**) makes public clients validate the `iss` parameter on authorization
responses, against session hijacking and redirect-based attacks in multi-server architectures.
Resource indicators (**RFC 8707**) let a client state explicitly which MCP server a token is intended
for, named as the fix for the **confused deputy** delegation problem [S23 §Clear Security & Capability
Boundaries, `n11`] (claim 182).

**RFC 8707 is the audience restriction this note's open question asked for**, and it resolves that
question's *direction* rather than its *content*: no token format, no exchange, no worked flow, and
nothing about an agent acting on a schedule with no user present. Single-leg, two sentences of prose,
no artifact. The RFCs themselves are T1 and were not read. Full treatment in
[`agent-security.md`](agent-security.md), which owns the threat model.

### Client registration is being replaced by client retrieval, and two operators rejected the old way independently

This note recorded DCR's rejection from GitHub's side first, as claim 222, with Client ID Metadata
Documents named as the likely direction and explicitly not promised. **S28 supplies both halves of
what was missing**: an independent confirmation of the diagnosis, and the mechanism that replaced it.

The diagnosis converges to a degree worth taking seriously. S28's DCR diagram carries two failure
bands - the authorization server "writes unbounded per-client state" because it stores a record for
every registration, and "the minted `client_id` is not portable across authorization servers" - and
the narration adds that identity is self-asserted, since "anybody could say hey, I'm Claude Code"
[S28 `n5`]. Those are two of the three reasons GitHub gave. **The two sources have no connection and
sit at opposite ends of the scale**, one operating an authorization server for millions of developers
and one running a personal assistant, which is what makes the failure modes structural rather than
situational (claim 222, upgraded). S28 also attaches the first number anyone has: **~125 registrations
per user** on its author's own server, read by him as reconnection churn rather than 125 clients
[S28 `n6`]. Treat that as a direction and not a measurement, because it is single-leg with no
denominator and no window.

**CIMD replaces registration with retrieval, and the whole idea is in one line of its diagram: the
`client_id` is a hosted HTTPS URL, the authorization server GETs the metadata on demand, and there is
no per-client store** [S28 `n7`] (claim 228). The client publishes a metadata JSON document - client
name, client URI, logo, redirect URIs, grant types - **before any connection exists**, and that URL is
its identifier. The authorization server detects the URL form and fetches it "instead of writing a
registration record".

Notice that all three defects vanish from one change rather than being fixed individually, which is
the signature of a design that deleted a step. Nothing grows unbounded because nothing is written.
Portability is free because a URL means the same identifier everywhere. **And the identity
substitution is the part to get right when explaining this**: trust reduces to *ownership of the
domain*, which does not establish that a client is trustworthy but does make the claim **attributable
and revocable by somebody other than the claimant**. An attacker can still call itself Claude Code and
cannot serve `claude.ai/client-metadata.json`. That is weaker than a vetted registration and far
stronger than a self-asserted string, and the web already runs the machinery.

**The gap in this note's coverage is that nobody here has read the CIMD specification.** One source
describes it, one deployment uses it, and the validation rules are what decide whether domain
ownership is a real control or a formality. That is the highest-value deep-research candidate on this
topic.

### "The spec shipped" and "clients speak it" are three weeks and 25,288 requests apart

Every source in this note before S28 describes a design. **This one describes what the ecosystem did
with a design**, and the answer at three weeks was nothing (claim 227).

The measurement exists because its author instrumented the seam while migrating rather than when he
wanted to delete something. His server runs both protocol eras behind one route, classifies each
request with the SDK's own `isLegacyRequest` predicate, keeps the 2025 lane byte-identically, and sets
`legacy: 'reject'` on the modern lane "so exactly one lane owns each era" [S28 `n11`]. Every
authenticated request then writes one non-blocking data point recording lane, method, protocol
revision, client, and user.

The strictness is the part that transfers, and it is easy to mistake for pedantry. **A tolerant modern
lane would serve legacy requests too, and the lane attribution would stop being a fact about the
client** - the telemetry would still record something, and it would mean nothing. The full treatment
of the practice sits in [`agents.md`](agents.md) as claim 229, because the lesson is not about MCP.

What it found on 2026-08-10 was `legacyShare = 1.0` across 25,288 requests, verdict
`waiting-for-modern-clients`, with the observed protocol versions running `2025-11-25` at 20,771,
unspecified at 4,474, `2025-06-18` at 41 and `2024-11-05` at 2 [S28 `n13`]. A week later legacy share
was 97.0%, with 62 modern `tools/call` from 2 clients and a self-description of "real work is ~0.5%
migrated".

**Read that against the release announcement's own closing line, which is that all four Tier 1 SDKs
speak `2026-07-28`** [S28 `n4`]. Both are true and they measure completely different things. SDK
support means adoption is *possible*; whether it has happened is empirical, and almost nobody
instruments it. **The consequence for this note is a correction to how it reads a spec version**: a
pinned revision tells you what the protocol is, and nothing whatsoever about what is on the wire.

> **Do not generalise the rate.** One hobbyist-scale server, a client population self-selected by who
> follows one educator, and a window the source itself says contains six to thirteen days rather than
> the thirty it is labelled. **What generalises is that the gap exists and is wide**, plus the method
> that made it visible. The rate is about one person's audience.

### The protocol now has a deprecation policy, and used it to shrink itself

Features move Active -> Deprecated -> Removed with a **minimum 12-month** transition window
(SEP-2577), and three entered deprecation on day one: **Roots** (replaced by explicit tool parameters,
resource URIs or server configuration), **Logging** (replaced by `stderr` for stdio or
**OpenTelemetry** for cloud observability), and **Sampling** (replaced by calling LLM provider APIs
directly) [S23 §Deprecations, `n13`] (claim 183).

Logging and Sampling share an instinct with the header promotion above: **prefer a standard the
surrounding infrastructure already speaks over a protocol-specific mechanism.** Removing sampling is
the protocol declining to broker between a server and a model, narrowing itself to the channel between
a client and a tool. *(That reading is this brain's commentary, not S23's claim.)* Note the irony for
this note, which recorded sampling at zero sources until now: **the first thing the brain learns about
MCP sampling is that it is going.**

**S28 confirms all of it independently and adds one deprecation S23 did not record**, which is that
the legacy **HTTP+SSE transport** is officially deprecated on the same year-long offramp [S28 `n3`].
It also supplies the per-feature reaction of somebody who used these: Roots he is glad to lose,
calling it useless outside very slim cases, and **Sampling he is sorry about**, with the example that
makes the feature legible - a journaling server asking the client's model to generate tags for an
entry before saving it. His read is that it was useful and little used.

> **Twelve months is a floor and this note should stop reading it as a schedule.** Set the policy
> beside claim 227: the one operator who has measured his own traffic sees 97% of it still on the
> previous era three weeks in, and expects removal to take considerably longer than the minimum. **A
> deprecation window is a promise about the earliest safe removal, not a prediction of the actual
> one**, and the gap between those two is exactly what claim 230's gate discipline is for.

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

### The catalog is an interface somebody authors, and S29 is the second data point on composition

This note has recorded that composition is the protocol's leverage point and that the brain held
exactly one data point on it. [S29](../../sources/260822_doordash-agent-gateway/LEARNING.md) is the
second, and it matters because it arrives for a different reason. S10's aggregator existed to replace
a catalog with a search index, which is a context-budget motive. DoorDash's exists to govern servers
it does not own, which is an access motive, and the two arriving at the same mechanic from unrelated
pressures is what makes the mechanic look structural rather than clever.

The construction has two halves that pull in opposite directions, and naming them separately is what
makes the design reusable. **Bundles compose across servers** into one logical MCP endpoint, so a
coding agent connects to `/v1/mcp/developer-tools` and never learns that GitHub, Jira, observability
and code search are four servers behind it. **Filters subtract within servers**, deciding which of a
server's tools are exposed for a given bundle, agent, user group, environment or audience. The
catalog is then assembled per request by fanning `tools/list` out, applying authorization and
filters, namespacing the survivors, and merging (S29 `n10`, claim 233).

**The sharpest thing in the source is visible only in its figure, and it is a design instruction
rather than a policy.** The prose says downstream servers publish "admin actions, destructive
actions, billing APIs, and niche provider-specific features", which is a category list. The figure
names the denied tools individually, and every one of them is a delete, a transfer, a reindex or a
permission change: `repo__delete_branch`, `repo__transfer`, `org__manage_webhooks`,
`jira__delete_issue`, `jira__change_permissions`, `obs__delete_alert`, `obs__manage_users`,
`search__delete_index`, `docs__manage_spaces` (S29 `n11`). **The filter is drawn around
irreversibility and around authority, not around relevance**, which is a far more actionable rule
than "expose fewer tools" and is this brain's reading of the picture rather than the source's stated
principle.

> **What this does not do, and the temptation is real.** S29 asserts that smaller catalogs "reduce
> model confusion" and "reduce irrelevant choices" and **measures nothing**. Claims 214 and 219 are
> measured elsewhere and must not gain confidence from this source. What S29 supplies is a
> practitioner acting on that finding at scale, which is adoption evidence and not a second
> measurement.

**It also answers half of this note's standing open question**, the one asking what an aggregating
server owes the servers behind it. S12 supplied the requirement from the deployment side and S10 from
the client side, and neither gave a mechanism. S29 gives one for **credential propagation
specifically**: four custody modes at the aggregator, with the downstream seeing a correct principal
and the agent holding nothing (claim 236, and see [`agent-security.md`](agent-security.md)). It still
gives no token format, no exchange, and no audience restriction, so the question narrows rather than
closes.

## Key claims

| Claim | Spec version | Sources (cited) | Confidence |
|---|---|---|---|
| **The protocol core is stateless: the handshake and `Mcp-Session-Id` are deleted, `_meta` carries the negotiated fields on every request, and routing metadata is promoted to mirrored HTTP headers** (`-32020` on mismatch), so round-robin routing, serverless scale-to-zero and invisible failover follow from one change. | **2026-07-28** (from **2025-11-25**) | S23 §Why Sessions + §The New Request Model + §HTTP Standardization (`n1`-`n5`), claim 179 | **corroborated** - prose against the article's own printed payloads, which diff cleanly. SEP numbers prose-only and unverified |
| **Statelessness is state relocation, not elimination**: to the wire (`_meta`), to the client (`requestState`), to the application (a task store). MRTR (SEP-2322) and the Tasks extension (SEP-2663) are the two mechanisms. | 2026-07-28 | S23 (`n3`, `n7`, `n9`, `n10`, `d2`), claim 180; **externally corroborated by S27 (`n16`)** | corroborated on all three relocations and on the "No Redis Sessions Needed" divergence. **The framing was this brain's synthesis and now has an independent production instance** - see the status block |
| **A tool surface assembled per request makes per-caller filtering free**, and a server building its tool list at startup cannot do it without inventing per-connection state. GitHub constructs a brand-new server instance in the SDK sense **on every single request**, attaching tools from configuration, policy and token scopes, behind a load balancer with no session affinity, at ~7.34M calls/week. | unstated (predates 2026-07-28) | S27 (`n16`, `n17`), claim 224 | **corroborated** - architecture slide against narration. The design consequence, that scope filtering is a by-product rather than a feature, is this brain's reading |
| **Dynamic Client Registration was rejected by two unconnected operators for the same operational reasons, not cryptographic ones**: unbounded per-client state, a `client_id` portable nowhere, and no reliable app identity (self-asserted registration). Verdict from the team that made the call: "a well-intentioned mistake". **First quantity attached to the growth problem: ~125 registrations per user.** | unstated | **S27 (`n12`, `n13`) + S28 (`n5` corroborated, `n6` single-leg)**, claim 222 | **Upgraded 2026-08-21 to corroborated across two independent operators.** S27 was narration only from the deciding team; S28 reproduces two of three defects from a diagram plus narration, at a completely different scale. **The ~125 figure is single-leg with no denominator** - a direction, not a measurement |
| **CIMD replaces registration with retrieval: the `client_id` *is* a stable HTTPS URL the client hosts, which the authorization server GETs on demand and stores nothing about.** All three DCR defects vanish from one change, and **trust reduces to ownership of the domain** - not a trustworthiness claim, but one that is attributable and revocable by somebody other than the claimant. | 2026-07-28 | S28 (`n7`), claim 228 | **corroborated within the source** (diagram + narration + one working deployment). **The CIMD specification has not been read here**, so the validation rules that decide whether domain ownership is a real control are unverified. Highest-value deep-research candidate on this topic |
| **SDK support is not client adoption.** Three weeks after `2026-07-28` published with all four Tier 1 SDKs speaking it, an instrumented production server had served **25,288 requests and none from a `2026-07-28` client**; a week later legacy share was 97.0% with ~0.5% of real work migrated. Observed versions were dominated by `2025-11-25`. | **2026-07-28** (measured against `2025-11-25` traffic) | S28 (`n4`, `n13`), claim 227 | **corroborated on the numbers, and the population is tiny and not neutral** - one hobbyist-scale server, a self-selected client base, and a window the source says holds ~6-13 days rather than 30. **The gap generalises; the rate does not.** This note's first adoption measurement of any kind |
| **A protocol capability no client surfaces migrates into server-side configuration, where it earns configuration-level adoption.** `readOnlyHint` exists and GitHub's read-only mode maps one-to-one onto it; no client exposes the annotation as a filter, so the server ships a redundant feature reaching ~17% of users. **Every tool-grouping proposal to the spec has been rejected.** | unstated | S27 (`n21`, `n22`), claim 225 | **single-leg, needs-check.** Narration only and the 17% is hedged. A direct operator statement about their own product, which is the strongest form single-leg takes |
| **Authorization adds issuer verification (RFC 9207) and resource indicators (RFC 8707)** - the latter named as the fix for the confused deputy, and the first mechanism this note's identity question has ever been given. | 2026-07-28 | S23 §Clear Security & Capability Boundaries (`n11`), claim 182 | needs-check (single-leg, two sentences, no artifact). Resolves the question's **direction**, not its content |
| **A formal deprecation policy exists** (Active -> Deprecated -> Removed, 12-month minimum, SEP-2577), and **Roots, Sampling and Logging are deprecated** - sampling in favour of calling LLM provider APIs directly. | 2026-07-28 | S23 §Deprecations (`n13`), claim 183 | needs-check (single-leg, prose-only). The scope-narrowing reading is commentary |
| **Tool and resource results can carry `ttlMs` and `cacheScope`** (SEP-2549, modelled on HTTP `Cache-Control`), so clients stop holding SSE connections open to detect list changes. **`cacheScope` decides caching across users.** | 2026-07-28 | S23 §Intelligent Caching (`n6`) | **needs-check - the weakest-evidenced feature in S23.** No example, no field placement, no default, and a multi-tenancy control described in half a sentence |
| **Tool input schemas support full JSON Schema 2020-12**, including `oneOf`/`anyOf`/`allOf` and local `$ref`. | 2026-07-28 | S23 §Clear Security & Capability Boundaries (`n12`) | needs-check (single-leg). Interacts with the row below - a richer schema is more tokens in `tools/list` |
| **`tools/list` puts the whole catalog in per-turn context**, so context cost scales with what is connected rather than with the task - 541k tokens at 1,180 tools. Prompt caching makes it ~90% cheaper, not absent, and cached tokens still consume attention. | unstated | S10 §intro + §The default agent tax + `fig_tokens-chart` (`n1`, `n2`, `n9`) | emerging (measured on ToolRet; the caching point is single-leg) |
| **Many clients refuse to call a tool absent from `tools/list`**, so any lazy-discovery design needs a *registered* proxy tool to carry the dispatch. | unstated | S10 §Two tools instead of a hundred (`n4`) | needs-check ("many runtimes", none named, no spec citation) |
| **An MCP server can aggregate other MCP servers** (streamable HTTP, bearer auth), which is what allows large capabilities to be added **with no new protocol primitive** and to extend to non-MCP tool sources behind the same index. | unstated | S10 `fig_image-6` (`n7`, figure-only) + §Two tools instead of a hundred (`n5`, `n6`) | needs-check on the aggregation mechanic (figure-only); emerging on "no new primitive" |
| **A tool's indexed surface is name, description, argument names and argument descriptions, three levels deep** - and a field can be indexed while staying invisible in MCP responses, so search vocabulary and model-facing schema are separable. | unstated | S10 §Two tools instead of a hundred + §Tuning the search space (`n8`, `n14`) | emerging (`n14` corroborated prose vs code) |
| **An MCP server can be the mandatory data seam** - the agent holds no datastore credentials and every retrieval is a tool call, so the data boundary is a property of the topology rather than of the agent's behaviour. | unstated | S12 §Architecture (`n9`) + `visuals/fig1b_two-tenants.png` (claim 104) | emerging |
| **Local vs shared server deployment is an isolation decision.** Local gets isolation from the perimeter it sits in and needs no identity mapping; shared needs private connectivity plus end-user identity propagated and enforced on every call. Recommended split: local for regulated data, shared for common corporate systems. | unstated | S12 §Design alternatives, MCP servers (`n10`, claim 105) | emerging - corroborated on local (it is what the figure draws); **single-leg on shared, which is drawn nowhere** |
| **The tool catalog is an interface somebody authors, and the filter producing it is drawn around irreversibility and authority rather than relevance.** Bundles compose *across* servers into one logical endpoint; filters subtract *within* them; the catalog is assembled per request by fan-out, filter, namespace and merge. Every tool S29's figure denies is a delete, transfer, reindex or permission change, which is sharper than the prose's category list. | n/a (implementation, not spec) | S29 (`n10`, `n11`, `n13`), claim 233 | **corroborated** within S29; the filter-shape generalisation is this brain's reading of the figure. **Does not re-measure claims 214 or 219** - S29 asserts the catalog-size benefit and measures nothing |
| **MCP standardised invocation and left governance homeless.** Six production questions sit outside the protocol - which agent, for whom, which credential, seeing which tools, revoked how, recorded where - and they compress into access, curation and operations. All three obvious homes fail: the agent (enforcement becomes a prompt), each server (N reimplementations, and third-party servers never comply), a shared library (reaches importers only, revokes nothing - claim 217). | n/a (the gap is version-independent) | S29 (`n1`, `n2`), claim 232 | **corroborated** within S29 - the drawn pipeline's five steps map onto the enumerated questions. **The three-homes elimination is this brain's reading**; S29 states its conclusion without walking alternatives |

## Key visuals

![Two tools instead of a hundred: tools/list exposing 100 resident tool schemas, versus tool_search and call_tool over a toolbox index, with the rest of the catalog indexed but never listed](../../sources/260801_tool-search-toolboxes/visuals/fig_tool-search-figure.png)
> The protocol-level shape of lazy tool discovery: the catalog stays behind the aggregator, and the
> only two tools in `tools/list` are a search and a dispatcher. The dashed box is the part that
> matters for this note - remote MCP servers sit alongside OpenAPI and A2A, all reached through one
> mechanism because the aggregator is the one thing the client talks to. S10 `fig_tool-search-figure`,
> `n3`/`n6`. Full walkthrough in the
> [source note](../../sources/260801_tool-search-toolboxes/LEARNING.md).

## Open questions / conflicts

- ~~**This topic still has no primary source.**~~ **Closed 2026-08-07 by S23**, which is about the
  protocol itself. What the question was really tracking survives in a narrower form: **resources and
  prompts remain at zero as first-class subjects**, appearing in S23 only as names in a header field
  and a cache rule.
- ~~**No spec version is pinned anywhere in this note.**~~ **Closed 2026-08-07 by S23** - **2026-07-28**,
  superseding **2025-11-25**. Every mechanic promoted from S10 and S12 predates both and **still has no
  version attached**, so the caution it was raising now applies to those rows specifically rather than
  to the note as a whole.
- **What does an agent present to a shared MCP server, and how does the server verify it?**
  **Partially answered 2026-08-07: the mechanism has a name.** S23 gives **RFC 8707 resource
  indicators** for audience restriction and **RFC 9207** for issuer verification (`n11`, claim 182),
  which is what S10 and S12 both stopped short of from opposite directions. **The direction is closed
  and the content is not** - no token format, no exchange, no worked flow, and nothing about the case
  both earlier sources flagged as hardest, an agent acting on a schedule with no user present. **The
  artifacts to read next: the MCP authorization specification, RFC 8707 itself, OAuth 2.1 token
  exchange, SPIFFE/SPIRE.** Shared with [`agent-security.md`](agent-security.md), where it is the same
  question wearing a threat model.
- **Does the 2026-07-28 specification require `requestState` to be integrity protected?** **The
  highest-value open question this note now has, and the cheapest to answer** - read the SEP-2322 text.
  S23's own example decodes to unsigned plaintext JSON while guarding a file deletion (`n8`, `d1`,
  claim 181). If the spec mandates protection, this is a documentation defect in a widely-read
  announcement. If it does not, it is a protocol-level design gap. **The spec was not read in this
  pass** and no deep research was requested. **Narrowed 2026-08-21 by S28** (claim 231): the community
  guidance *is* encrypt-and-bind, stated on the face of an MRTR diagram, so the likely answer is that
  S23's example was careless rather than that the design forgot. **The question that replaces it is
  harder and more useful - does any implementation actually do it?** Neither source examines an SDK,
  and a survey of the four Tier 1 SDKs would settle it cheaply.
- **What does the CIMD specification actually require?** **The highest-value deep-research candidate on
  this topic.** One source describes the mechanism and one deployment uses it (claim 228), and nobody
  here has read the spec. The validation rules are what decide whether "trust is ownership of the
  domain" is a real control or a formality - what happens on a redirect, on a stale or unreachable
  document, on a document served from a domain that has since changed hands, and how long an
  authorization server may cache one.
- **Is the adoption gap general, or is it one server's audience?** Claim 227 is n=1 over ~6-13 days.
  The obvious test is whether any other operator has published protocol-lane telemetry for
  `2026-07-28`. **Two independent servers showing the same shape would turn this from an anecdote into
  a fact about the ecosystem**, and it is the kind of thing that may simply be sitting in a public
  dashboard somewhere.
- **How long does a deprecated MCP feature actually survive?** The policy sets a twelve-month floor
  (claim 183) and claim 227 suggests real removal is much further out. Nobody has measured the decay
  curve for a protocol era after deprecation, and **every migration plan in the ecosystem is currently
  guessing at it.**
- **What does `_meta` on every request cost when the catalog is already large?** Claim 85 measures
  `tools/list` at 541k tokens for 1,180 tools, and claim 179 adds a per-request block on top of it.
  Full JSON Schema 2020-12 support (`n12`) pushes the same direction. **The two sources never meet and
  neither author raises it** - this is the note's own question, and it is the one place where S23 and
  S10 actually interact.
- **What is `cacheScope` allowed to do?** It decides whether a tool result may be cached **across
  users**, and S23 describes it in half a sentence with no example (`n6`). Read against claims 105 and
  106, a cross-user cache is precisely the kind of shared component that converts a structural
  guarantee into an implementation obligation.
- **Is the `-32020` header/body mirroring rule enough to prevent a parser differential?** Duplicating
  a value into a cheaper-to-read place is the classic setup for a gateway authorizing on one copy while
  the server acts on the other. The spec puts the check at the server (`n4`), which matches claim 27's
  instinct. What a proxy that rewrites one copy and not the other should do is unaddressed.
- **What happened to sampling's use cases?** Deprecated in favour of calling LLM provider APIs directly
  (`n13`, claim 183), which assumes the server holds its own model access and credentials. For a server
  that deliberately had neither, that is a capability removal rather than a substitution.
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

- **S29** - [How DoorDash Built a Centralized Gateway for AI Agent-Tool Access](../../sources/260822_doordash-agent-gateway/LEARNING.md)
  (Siddarth Kodwani and Vasily Vlasov, DoorDash Engineering, 2026-07-30). **The first source here
  written from the consumer side of the protocol** - an organisation governing roughly 200 servers it
  mostly did not write, rather than an author shipping one. Supplies the second data point on
  composition as MCP's leverage point, the bundles-and-filters construction and the catalog-as-interface
  framing (claim 233), and the governance-shaped statement of what the protocol does not answer
  (claim 232). **T4 - a vendor engineering-brand post on a careers site, first-party and unaudited.**
  The architecture is described honestly and in useful detail; **every number in it counts the
  platform's own reach and none measures an outcome**, so the adoption block is a claim rather than
  evidence. **Its unusual strength is the visual leg**: three purpose-drawn figures, all kept, two of
  them materially more specific than their own prose. The two best findings in the ingest come from
  reading the figures *against* the text - a cached policy plane behind a promise of central
  revocation, and agents appearing as downstream targets in a post that never mentions agent-to-agent
  calls (claim 238). Both are figure-only and are recorded as inference, not as architecture.
- **S28** - [Here's how the new MCP spec works](../../sources/260821_new-mcp-spec/LEARNING.md)
  (Kent C. Dodds, "Better with Kent", 2026-08-20). **The note's second independent read of
  `2026-07-28`, and the only source anywhere here that measured what happened after a spec shipped.**
  Supplies CIMD's mechanism (claim 228), the DCR corroboration that upgraded claim 222, the first
  adoption number in this note's history (claim 227), and second-source confirmation for claims 179
  and 183. **T4 - an independent educator's screencast, unreviewed, no editor** - and better evidenced
  than that tier suggests, because the visual leg is not slides but the official blog post, his own
  merged PR and his own public dashboard, displayed on screen. On the spec mechanics the second leg is
  therefore **the primary document rather than a summary of it**; on adoption the two legs are
  genuinely independent, since one is recollection and the other an aggregate query. **The
  specification content is not really his evidence** - he reads the post and comments, so every
  rationale not visibly on the post is his inference. **The adoption data is n=1 on a self-selected
  population over a window the source itself says holds 6-13 days rather than 30.** He also omits on
  air something his own PR records, which is that Cloudflare deprecated and feature-froze the
  framework he was on, making the migration sound more elective than it was (`d2`). He opens with
  "they fixed MCP", so read it as enthusiasm - real and specific criticisms of sampling and logging
  notwithstanding.
- **S27** - [Scaling GitHub for your Agents](../../sources/260816_scaling-github-for-agents/LEARNING.md)
  (Sam Morrow, GitHub, AI Engineer Europe, ~April 2026). **This note's second primary source and the
  first written from inside a running deployment rather than about a specification.** Supplies the
  production topology and the per-request construction pattern (claim 224), the DCR rejection and its
  three operational reasons (claim 222), the unsurfaced-annotation finding (claim 225), and the
  observation that every tool-grouping proposal to the spec has been rejected. It is the source that
  moved this note to `established`, by corroborating claim 180 from an independent implementation
  ([ADR-0028](../decisions/0028-mcp-established-on-an-independent-implementation.md)). **T2 vendor
  engineer presenting his own product**, with no external evaluation and no baseline against another
  MCP server, so every efficacy figure is self-report. **Its most interesting claim is its least
  quantified** - scope filtering (claim 221) gets no number in a talk that counts everything else.
  Two figures are hedged in delivery (">95%" success, "roughly 17%" read-only adoption) and are
  `single-leg`. **The strongest caveat is the author's own**: he expects thousands of tools to become
  normal and to "probably reverse many of the fewer tools decisions", so treat the mechanics as
  durable and the tool-count recommendation as carrying a published expiry date.
- **S23** - [Scaling AI Agent Infrastructure with the MCP Stateless updates](../../sources/260807_mcp-stateless-updates/LEARNING.md)
  (Kurtis Van Gent + Alan Blount, Google Developers Blog, 2026-08-05). **This note's first primary
  source and the first anywhere to pin a spec version** (2026-07-28). Supplies the transport core, the
  handshake removal, the header promotion, the two residual-state mechanisms (MRTR, Tasks), the
  deprecation policy, and the first authorization mechanism. **T2 vendor writing about a standard it
  says it led** - Google co-founded the Transports Working Group, and the headline benefit is that MCP
  now runs well on serverless platforms it sells. **Unusually well evidenced for the class anyway**,
  because its second leg is six printed protocol payloads rather than a diagram, and one of them was
  decoded during the gate to produce a finding the authors did not write (`n8`, `d1`). **Nothing in it
  is measured** - no benchmark, no latency figure, no cost comparison, in an article whose entire
  argument is scale and cost. Everything described is a **release candidate on beta SDKs**, and the
  article itself recommends staging rather than production (`n15`).
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
