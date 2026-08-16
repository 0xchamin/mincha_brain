# ADR 0028: `mcp.md` advances to `established` - an independent implementation is the corroboration a second spec reading was never going to be

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260816 |
| Deciders | chamin |

## Context

[ADR-0022](0022-a-primary-source-is-not-corroboration.md) held [`../topics/mcp.md`](../topics/mcp.md)
at `emerging` on three sources, and it named the exact bar the note had to clear. Not a source count,
and not a primary source: **two sources confirming the same mechanic**, which is what `established`
means in this brain and what `agent-security.md` cleared on three independent corroborating groups.
At three sources the note covered the client side (S10), the deployment side (S12) and the protocol
itself (S23), and those three overlap on almost nothing, so the count kept rising while the
corroboration did not.

S27 (Sam Morrow, GitHub, ~April 2026) is the note's fourth source and its second primary one. That is
not by itself the argument, because ADR-0022 already rejected exactly that reasoning.

**The argument is that S27 confirms a mechanic S23 already asserted, and does it from the one position
nothing else in this note occupies.** S23 is Google describing a specification change: sessions
deleted, `_meta` carrying the negotiated fields, state relocating to the wire, the client and the
application. This brain's reading of that was claim 180, that **statelessness is relocation and never
elimination**, and the note recorded honestly that the three-way framing was a synthesis the article
never states. S27 is GitHub describing a production system serving roughly 7.34M tool calls a week: a
brand-new MCP server instance constructed on every single request, no session affinity, and **Redis
still in the architecture diagram**, retained for the self-reported client identity telemetry needs
(`n16`, claim 224).

Three properties make that corroboration rather than an echo.

1. **Different organisations, different artifacts.** One is a vendor announcement about a standard it
   says it co-led; the other is an operator report about their own deployment. Neither is reading the
   other.
2. **S27's system predates S23's spec change.** The talk is from around April 2026; the spec version
   S23 pins is 2026-07-28. GitHub did not implement the specification's advice, so this is convergent
   engineering rather than compliance.
3. **It corroborates the part that was weakest.** Claim 180's mechanics were well evidenced in S23's
   printed payloads; what was `single-leg` was the **generalisation** - the claim that statelessness
   is always relocation and the engineering question is who owns the state now. An independent
   implementation keeping Redis while calling itself stateless is that generalisation instantiated.

## Decision

**`mcp.md` advances from `emerging` to `established`**, on one corroborating group: **statelessness as
relocation** (S23 `n3`/`n7`/`n9`/`n10`/`d2` and S27 `n16`, joined at claims 180 and 224).

**Claim 180 is amended in place** rather than duplicated, to record the external corroboration and its
independence. Claim 224 is promoted separately, because its transferable content is not the topology
but the design consequence - **a tool surface assembled per request makes per-caller filtering free**,
and a server that builds its tool list at startup cannot do it without inventing per-connection state.

## Consequences

**What this does not license.** The other claims in `mcp.md` remain exactly as corroborated as they
were. S27 confirms nothing about caching, deprecation policy, JSON Schema support, resource
indicators or the tool-search mechanics, and the note must keep saying so per-row. **`established` is
a statement about the note having at least one genuinely corroborated mechanic, not a blanket upgrade
of its contents**, and the per-claim confidence column is still where the real information lives.

**One corroborating group is the minimum, and it should be said out loud.** `agent-security.md`
advanced on three. This note advances on one, which is the weakest legitimate version of the rule, so
the honest reading is that `mcp.md` has just crossed the line rather than comfortably cleared it. If a
fifth source arrives and corroborates nothing, that is worth noticing rather than absorbing.

**The rediscovery ADR-0022 was written to stop has now been answered rather than repeated**, which is
the outcome that ADR wanted. The thing worth carrying forward is the shape of the answer: this note
spent three sources trying to corroborate a specification by reading more about the specification,
and what finally moved it was **somebody building the thing and reporting what stayed in their
architecture diagram**. For a protocol topic, an independent implementation is a stronger second leg
than a second reading of the spec, and that is a general lesson about which sources to hunt for when a
topic stalls at `emerging`.

## Alternatives considered

- **Hold at `emerging` and wait for a second corroborating group.** Rejected because it would make
  `established` mean three groups by precedent rather than two by definition, and the definition in
  `INDEX.md` is "two or more corroborating sources". Moving the bar silently is worse than crossing it
  narrowly and saying so.
- **Advance on the count reaching four.** Rejected outright; that is precisely the reasoning ADR-0022
  exists to forbid.
- **Fold claim 224 into claim 180 as an amendment only.** Rejected because the per-request
  construction consequence is reusable by anyone building an MCP server and has nothing to do with
  whether state was relocated. Two different claims that happen to share a source.
