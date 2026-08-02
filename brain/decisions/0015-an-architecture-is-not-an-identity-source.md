# ADR 0015: An architecture is not an identity source, and generic isolation is not a topic

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260802 |
| Deciders | chamin |

## Context

S12 ([`260802_gcp-multi-tenant-agentic-ai`](../../sources/260802_gcp-multi-tenant-agentic-ai/LEARNING.md),
Google Cloud's multi-tenant agentic AI reference architecture) forced two taxonomy calls in one pass,
and both turn on the same test.

**The first: does S12 trigger the identity split?**
[`agent-security.md`](../topics/agent-security.md) has carried a standing instruction since S3 - "on
the next identity/authorization source, split `identity-and-authorization` into its own note" - written
because the owner has a stated identity track (OAuth 2.1, SPIFFE/SPIRE, AAuth) and the note visibly
holds two bodies of material. S12 is drenched in identity. IAM is one of its three isolation
mechanisms; IAP is the ingress; a **Principal Access Boundary** on the agent's identity is the
load-bearing control; and its shared-MCP recommendation turns entirely on propagating an end-user
identity across a service hop (`n10`, `n11`). On word count alone it is more identity-heavy than S3.

**The second: does S12 warrant a `multi-tenancy` topic?** It is the brain's first source about running
agents for a whole organisation rather than building one, and it arrives with its own vocabulary -
tenant projects, principal boundaries, service perimeters, hub-and-spoke, noisy neighbours, cost
allocation models. That is exactly the shape [ADR-0014](0014-no-topic-for-organisational-context.md)
had to adjudicate for S11.

## Decision

**Neither.** S12 does not trigger the identity split, and no `multi-tenancy` topic is created. Its
agent-specific claims (101-103, 106) merge into `agent-security.md`, the MCP deployment fork (104, 105)
into `mcp.md`, the tenancy shape (107, 108) into `agents.md`, and the token cap (109) into
`context-engineering.md`.

**The test, stated once and used twice: a source advances a topic when it *teaches within* that topic's
scope, not when it *depends on* it.** This is [ADR-0012](0012-a-mention-is-not-a-source.md)'s rule
applied to a much heavier user than a mention, and it needed saying because ADR-0012's examples were all
thin. Weight of use is not the axis; teaching is.

**On identity:** S12 teaches no identity mechanics whatever. No protocol, no token format, no flow, no
lifetime, no claim structure, no trust model, no revocation. It *consumes* identity as a platform
primitive and, at the one point where the mechanics would have to be named - propagating a user identity
to a shared MCP server - it states the requirement and stops. **A source that needs a subject and cannot
supply it is evidence the subject matters, not a source on it.** The split trigger remains what it was:
a source that teaches the mechanics. What S12 *does* contribute is recorded as an open question in both
`agent-security.md` and `mcp.md`, now promoted from a sub-bullet because two independent sources have
converged on the same missing piece from opposite directions (S10 from the aggregating server's side,
S12 from the deployment's).

**On multi-tenancy:** apply ADR-0014's swap test - if you replace the agent with a microservice, does the
claim survive? For the isolation machinery it survives entirely. Project-per-tenant, principal
boundaries, service perimeters, blast-radius containment, noisy neighbours, chargeback models: all of it
is standard cloud multi-tenancy that would read identically in a reference architecture for a payments
platform. **A `multi-tenancy` note would have collected the generic material and left the four
agent-specific claims elsewhere** - the precise inversion ADR-0014 rejected, where the new topic gets the
disposable vocabulary and the transferable claims scatter.

The four that do not survive the swap are the ones promoted: the boundary must sit where the model has no
vote **because the query is composed at run time from attacker-influenceable text** (101); the principal
boundary is aimed at an agent talked into using a legitimate grant (102); prompt filtering is a new class
of edge control with no non-AI equivalent (103); and shared components convert structural isolation into
an enforcement obligation that **nobody has yet specified for agents** (106).

## Alternatives considered

- **Split `identity-and-authorization` now, on S12.** Rejected: the new note would open with a section
  saying "this architecture requires identity propagation and does not describe it". A topic note whose
  first source teaches none of its mechanics repeats exactly the failure ADR-0012 caught - a populated
  status row over a note that cannot deliver what the row promises.
- **Create `multi-tenancy`.** Rejected on the swap test above. Revisit if a second source arrives that is
  specifically about **agent** tenancy - per-tenant memory, per-tenant evals, cross-tenant agent
  handoff - because that material has no home today and would not fit `agent-security.md`.
- **Count S12 as a security source but not an `mcp` source.** Rejected: its MCP section is ~50 lines with
  a named trade, three feature axes per option and a recommendation, and it fills a gap
  ([`mcp.md`](../topics/mcp.md) had nothing at all on deployment). That is
  [ADR-0013](0013-secondary-but-substantial.md)'s "secondary but substantial", and the guard held - the
  Synthesis section was written from gated nodes before the source count moved.
- **Advance `mcp` to `established` on two sources.** Rejected: S10 and S12 overlap on nothing and
  corroborate none of each other's claims. Same call `rag.md` made at three sources and
  `agent-security.md` at two. **Counting sources is not measuring agreement**, and the note now says so
  in its status line.

## Consequences

- `agent-security.md` gains a third body of material (containment/isolation) alongside threats and the
  authorization substrate, which makes the eventual split slightly harder to draw - the split line is
  now identity-mechanics versus everything else, not identity versus threats. Recorded in that note's
  architect section.
- The identity split trigger is now **written down with a worked negative example**, which is worth more
  than the rule alone: the next agent can check a candidate against S12 rather than re-deriving.
- `mcp` reaches 2 sources and stays `emerging`, with the reason stated in its status line.
- **Revisit when:** a source teaches identity mechanics (split), or a second source addresses agent
  tenancy specifically rather than cloud tenancy generally (topic).
