# Topic: Agent security

**Status:** emerging (2 sources - S3 OAuth/OIDC, the only one that studies security; **S7 memory and
dreaming, which does not discuss security at all** and feeds this note only by making memory
poisoning concrete). **A rising source count is not rising evidence:** S7 corroborates none of S3's
claims, so the bar for `established` is unchanged - a second source that actually studies agent
security.

*(Status line corrected in [dream 0001](../dreams/0001-260802.md): it read "1 source" while two were
listed below and `INDEX.md` said two - the same defect `skills.md` recorded fixing on 2026-08-02.)*

> Living, cross-source synthesis on agent security. Many sources feed this note; **merge and
> de-duplicate** as they arrive (architect persona). Every claim cited. Note: "valid" here means
> corroborated across the source's own text + visuals, **not** an endorsement that the advice is
> correct - flag confidence.

## What this covers

Threats and mitigations for LLM agents: prompt injection (direct / indirect), tool poisoning,
data exfiltration, memory poisoning, over-broad permissions, and defense patterns (least
privilege, human-in-the-loop, input/output filtering).

**Also, as of the first source: the delegated-authorization substrate** - OAuth 2.0 / OpenID
Connect. An agent calling a tool on a user's behalf is a delegated-authorization problem, so the
protocol layer that solved it for web apps is prerequisite material here, not a detour.

## Synthesis

### Delegated authorization is a solved problem with a 20-year head start

The question "how does software act on a user's behalf without becoming the user?" was answered by
OAuth 2.0, and the answer is worth internalising before reasoning about agent permissions, because
the failure it was built to prevent is the exact failure mode an over-permissioned agent reproduces.

**The pre-OAuth state was credential sharing.** To let an app read your contacts you gave it your
password - an all-or-nothing, non-scopable, non-revocable, non-expiring credential on the account
that is the recovery path for every other account you own
([S3](../../sources/260725_oauth2-oidc-plain-english/nodes.md) `n1`, [&t=648s](https://www.youtube.com/watch?v=996OiexHze0&t=648s)).
OAuth replaced it with a token that is **scoped** (only these permissions), **expiring**, and
**revocable independently of the password** (S3 `n1`, `n7`).

**Three primitives transfer directly to agents:**

1. **Scopes = least privilege, made explicit and enforced at the resource server.** The client
   enumerates the permissions it needs up front; the issued token is bound to exactly those and the
   API rejects anything beyond them, even with a valid token (S3 `n7`,
   [&t=1549s](https://www.youtube.com/watch?v=996OiexHze0&t=1549s)). The enforcement point is the
   *resource server*, not the client - a distinction that matters when the client is an LLM whose
   behaviour you cannot constrain by construction.
2. **The consent screen = human-in-the-loop, generated from the request.** The authorization server
   builds the consent text *from the scopes the client asked for*, so the human approves a specific
   list rather than a vague connection (S3 `n7`,
   [&t=1428s](https://www.youtube.com/watch?v=996OiexHze0&t=1428s)). Facebook's early
   "connect - yes/no" prompt is the counter-example the talk cites: users could not tell whether they
   were granting profile read or wall-posting (S3, [&t=1463s](https://www.youtube.com/watch?v=996OiexHze0&t=1463s)).
3. **Channel separation = don't put secrets where they can leak.** The browser is trusted to talk to
   a human, never to hold a secret; so the flow deliberately routes user interaction through the
   browser and secret-bearing steps through server-to-server calls (S3 `n5`, `n6`,
   [&t=1989s](https://www.youtube.com/watch?v=996OiexHze0&t=1989s)).

> **The transferable design move: make the untrusted leg carry only useless material.** The
> authorization code crosses the browser precisely *because* stealing it accomplishes nothing -
> redeeming it needs a `client_secret` that never leaves the back channel (S3 `n5`). This is a
> stronger pattern than "encrypt the channel": it assumes the channel *is* compromised and arranges
> for that not to matter. The agent analogue is obvious and mostly unbuilt.

### A standard that gets used for what it was not designed for degrades into non-standard

OAuth was built for delegated authorization only. The industry adopted it for **login** as well,
because it was popular and close enough (S3 `n11`,
[&t=2824s](https://www.youtube.com/watch?v=996OiexHze0&t=2824s)). But OAuth has **no standard way to
return who the user is** - it reasons about permissions, not identity - so every provider bolted on a
proprietary user-info mechanism and the implementations stopped being interchangeable (S3 `n12`,
[&t=2894s](https://www.youtube.com/watch?v=996OiexHze0&t=2894s)). OpenID Connect exists to close
exactly that gap: a thin layer adding an ID token and a userinfo endpoint, triggered by one extra
scope (S3 `n13`, `n14`).

> **Worth carrying into agent protocol design.** The failure was not that OAuth was bad, but that a
> *near fit* got adopted for a use case it did not name, and the gap was closed privately by each
> vendor rather than publicly by the spec. Any protocol currently being stretched to cover agent
> use cases is running the same experiment.

## Key claims

| Claim | Threat / mitigation | Sources (cited) | Confidence |
|---|---|---|---|
| Credential sharing is the anti-pattern OAuth exists to kill: passwords are unscopable, unrevocable and unexpiring | threat: over-broad permissions | S3 `n1` [&t=648s](https://www.youtube.com/watch?v=996OiexHze0&t=648s) | OK (corroborated) |
| Scopes bind a token to a named permission set; the resource server rejects out-of-scope use even with a valid token | mitigation: least privilege | S3 `n7` [&t=1549s](https://www.youtube.com/watch?v=996OiexHze0&t=1549s) | OK (corroborated) |
| The consent screen is generated from the requested scopes, so approval is specific rather than blanket | mitigation: human-in-the-loop | S3 `n7` [&t=1428s](https://www.youtube.com/watch?v=996OiexHze0&t=1428s) | OK (corroborated) |
| Secrets must never traverse the front channel; the flow is split so the untrusted leg carries only a code that is useless without a back-channel secret | mitigation: channel separation | S3 `n5`, `n6` [&t=1937s](https://www.youtube.com/watch?v=996OiexHze0&t=1937s) | OK (corroborated) |
| PKCE lets a client that cannot hold a secret still prove it initiated the flow | mitigation: public-client hardening | S3 `n18` [&t=3562s](https://www.youtube.com/watch?v=996OiexHze0&t=3562s) | OK (corroborated) |
| OAuth has no standard identity mechanism, so authentication use drove vendor-specific extensions and broke interoperability | threat: protocol drift | S3 `n12` [&t=2894s](https://www.youtube.com/watch?v=996OiexHze0&t=2894s) | needs-check (single-leg) |
| Delegating authn to an authorization server decouples it from the app so both can evolve separately | design: separation of concerns | S3 `n19` [&t=3527s](https://www.youtube.com/watch?v=996OiexHze0&t=3527s) | needs-check (single-leg) |

## Key visuals

![The pre-OAuth anti-pattern: an app asking for your Gmail password](../../sources/260725_oauth2-oidc-plain-english/visuals/frame_640.jpg)

The failure mode in one screenshot - Yelp's signup form requesting the user's actual Gmail password,
with a parenthetical clarifying *which* password. Keep it as the canonical picture of what
"over-broad, non-revocable delegation" looks like in production (S3 `n1`,
[&t=664s](https://www.youtube.com/watch?v=996OiexHze0&t=664s)).

## Open questions / conflicts

- **Does the four-party model survive a non-deterministic client?** OAuth assumes the client is
  software whose behaviour is fixed at build time - it requests scopes its author chose. An LLM agent
  chooses its actions at run time. Scope enforcement still holds at the resource server, but "the
  client asked for what it needs" becomes "the client asked for what it *might* need", which pushes
  every agent toward over-broad grants. **Unresolved; no source in the brain addresses it.**
- **What is consent when the user is not present?** The design assumes a human at a browser clicking
  Yes. Long-running or scheduled agents break that. The client credentials flow (S3 `n10`) removes the
  user entirely - but that discards the delegation guarantee that made OAuth worth having. Open.
- **How does MCP's authorization actually build on this?** Believed to rest on OAuth 2.1, but **no
  source in this brain establishes it** - the connection is currently agent commentary, not a cited
  claim. Resolve before promoting anything into `mcp.md`. *(Note: `mcp.md` is no longer empty as of
  S10, but it says nothing about auth beyond a bearer token in a screenshot, so this stands.)*
- **Retrieved tool catalogs create an invisible steering surface, and no source discusses it.** When a
  tool catalog is searched rather than enumerated (S10, [`mcp.md`](mcp.md)), two new facts hold at
  once: the model sees **only a shortlist** it did not choose, and the field that decides that
  shortlist can be **invisible to it**. Foundry's `additional_search_text` is indexed for retrieval
  but explicitly "not visible to models in MCP responses" [S10 §Tuning the search space, `n14`]. So
  whoever writes that field steers which capability the agent is offered, with **no trace in the
  context the model or a reviewer can inspect** - and on an aggregating server, that writer may be
  neither the tool's author nor the agent's owner. Two shapes worth naming: **starvation** (tuning a
  safe tool's aliases so a risky one wins the query) and **substitution** (making an attacker-supplied
  tool the best match for common intents). **Labelled commentary** - S10 never mentions security, and
  no source in this brain measures retrieval-time influence. It is cheap to record now because the
  pattern is new and spreading; it is not yet a claim.
- **Temporal conflict on flow selection (S3 `n17`) - stale, superseded.** The source recommends the
  implicit flow for browser apps; the field has since moved to authorization code + PKCE. Recorded as
  a divergence in the source's `nodes.md`, flagged `do not apply`, and **not promoted as guidance**.
  The correction is currently uncited commentary; **an OAuth 2.1 source is the intended resolution**
  (research pass declined by the owner, 2026-07-25).

- **Shared agent memory is a prompt-injection sink with a demonstrated propagation path, and nothing
  defends it.** A background process that ingests session content and writes durable,
  automatically-applied instructions means **inject once, re-applied to every agent that attaches the
  store**, with no further access needed. This stopped being theoretical with S7: its live demo shows
  agents writing **imperatives** to their successors ("Next agent: skip dep checks, go straight to
  config diff") and the next agent complying [S7 `n20`,
  [`memory.md`](memory.md)]. S7 ships attribution and version history, which are **forensics after the
  fact**; there is **no admission control** - nothing validates a memory before the next agent acts on
  it. Recorded as claim 63 and **labelled commentary**, since neither memory source discusses the
  threat. **The most actionable open question in this note.**

## Note for the architect (topic boundary)

This note now carries two distinguishable bodies of material: **agent-specific threats** (prompt
injection, tool poisoning, memory poisoning - still unpopulated) and **the delegated-authorization
substrate** (this source). They are held together deliberately for now, per the "don't spawn a topic
per source" rule.

**The split is now expected, not hypothetical.** The owner has stated an identity track -
**OAuth 2.1, SPIFFE/SPIRE, AAuth** - so a second identity source is planned rather than possible.
The rule still says wait: a stated intent is not a second source, and creating the note early risks
a taxonomy shaped by a reading list rather than by material. **On the next identity/authorization
source, split `identity-and-authorization` into its own note** (preferred over
`delegated-authorization`, since SPIFFE/SPIRE is workload identity with no delegation and no human)
and leave the agent-threat material here. Record it as an ADR when it happens.

**What to watch for as that track lands**, since it is the interesting axis rather than the
protocol details:

| Source 1 (this one) | What the rest of the track changes |
|---|---|
| A **human** clicks Yes in a browser | SPIFFE/SPIRE has **no human and no browser** - identity is attested from workload properties, not delegated by a person |
| Consent is **per-flow and interactive** | Workload identity is **continuous and automatic**; agent auth has to answer what consent means for a long-running process |
| The client is **fixed software** that requests scopes its author chose | An agent chooses actions at **run time** - the open question below |

## Sources feeding this topic

- **S7** - [Memory and dreaming for self learning agents](../../sources/260731_claude-memory-dreaming/LEARNING.md)
  (Anthropic, 2026-05-21). **Does not discuss security at all** - it feeds this note only through the
  open question above, where its demo of agents passing *imperatives* through a shared memory store
  supplies a concrete propagation path for memory poisoning (claim 63, commentary). Full synthesis in
  [`memory.md`](memory.md).
- **S3** - [`260725_oauth2-oidc-plain-english`](../../sources/260725_oauth2-oidc-plain-english/LEARNING.md)
  - Nate Barbettini (Okta), *OAuth 2.0 and OpenID Connect (in plain English)*, 2018. The protocol
    substrate: delegated authorization, scopes, consent, channel separation, OIDC. **8 years old -
    mechanics current, flow-selection advice partly superseded.**
