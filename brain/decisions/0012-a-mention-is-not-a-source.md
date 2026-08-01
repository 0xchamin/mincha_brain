# ADR 0012: A mention is not a source - naming a topic does not advance its status

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260801 |
| Deciders | chamin |

## Context

Ingesting **S9** ([Inside the Microsoft Agent Framework](../../sources/260801_agent-framework-layered-sdk/LEARNING.md),
2026-05-28) forced the same call twice in one pass, on two different topics, and the kit had no
written rule for it.

**The `mcp` case.** S9's ecosystem figure names **MCP** as one of exactly two tool-integration
standards, beside OpenAPI [S9 `fig_AgentLoop`]. `brain/topics/mcp.md` has been at `seed` with **zero
sources** since the brain started. On a literal reading of the status ladder - `seed` (created, no
source) -> `emerging` (one source) - S9 is a source that mentions MCP, so `mcp` advances and the
brain's longest-standing empty topic is finally populated.

**The `skills` case.** S9's harness inventory files `Skills` under **Context**, beside `Prompts` and
`Memory` [S9 `fig_AgentHarness`]. `skills.md` is at `emerging` on S5, with S7 adding the category
name (claim 64). A third source touching skills would, read literally, be the second corroborating
source that takes the topic to `established`.

**Both readings are wrong, and wrong in the direction that inflates the brain.** What S9 supplies in
each case is **one box in one diagram**. It never defines MCP, never describes a server, tool,
resource, prompt or transport, and never mentions MCP in its prose at all. It never defines a skill,
never discusses writing, triggering, evaluating or retiring one, and never mentions skills in its
prose either. A topic note that advanced on this would announce coverage it does not have - and
`mcp.md` would go to `emerging` while its Synthesis section stayed literally empty.

This is a **taxonomy** question, which is why it is an ADR and not a judgement buried in a log entry:
it will recur on every broad source, and broad sources are common. The status ladder in `AGENTS.md`
counts *sources*, and until now "source" was undefined at the low end.

## Decision

**A source advances a topic's status only when it teaches something about that topic's scope. A
mention, a citation, or a labelled box in a diagram is a *sighting*, and a sighting is recorded in
the topic's Open questions without advancing status or appearing in "Sources feeding this topic".**

Applied this pass:

- **`mcp` stays `seed`.** The sighting is recorded in that note's Open questions, with an explicit
  line saying it is deliberately not counted and why. "Sources feeding this topic" stays empty.
- **`skills` stays `emerging`.** S9 *is* listed under Sources feeding, because its box placement does
  bear on a live claim (64) - but the entry states plainly that it contributes one box, supports the
  family assignment only, and does not move the status.

**The test: would a reader arriving at this note from the INDEX find what the status promises?** If
the status says `emerging` and the note cannot answer a basic question about the area, the status is
lying. Scope is defined by the note's own "What this covers" section, which is what makes this
checkable rather than a matter of taste.

**Not a one-way door.** Nothing is discarded - the sighting is written down, cited and findable. If a
later source makes the area real, the sighting is already there to cite alongside it.

## The asymmetry that decides it

The two errors are not symmetric, which is the same argument [ADR-0006](0006-static-probe-is-advisory.md)
makes about the static probe.

| Error | Cost |
|---|---|
| **Under-counting** a real source as a sighting | The topic looks thinner than it is. Self-correcting: the next real source arrives and the sighting is sitting there, cited, waiting to be promoted with it. |
| **Over-counting** a sighting as a source | The topic's status is wrong, the INDEX advertises coverage that does not exist, and **the error is invisible** - a populated status row with an empty note reads as "not written up yet" rather than "never had a source". |

Over-counting also corrupts the one thing the ladder exists to measure. If `established` can be
reached by three sources each naming a topic in passing, it stops meaning "this brain knows this
area" and starts meaning "this string has appeared three times".

## Alternatives considered

- **Count any citing source, and let confidence carry the weakness.** Rejected: status and
  confidence measure different things and this conflates them, in the opposite direction from
  [ADR-0008](0008-memory-established.md). There, status advanced while confidence deliberately did
  not, because the *area* genuinely recurred across two sources. Here the area does not recur at all;
  only the word does. Confidence columns cannot rescue a status that is false.
- **A numeric threshold** (N claims promoted, or a word count). Rejected as the wrong instrument, on
  ADR-0004's line: this is a **judgement**, and encoding it as a count invites gaming and breaks on
  the first source that teaches a great deal in two sentences. `validate.py` checks form; the
  architect judges scope.
- **Advance `mcp` to `emerging` and write the Synthesis section from general knowledge.** Rejected
  outright, and worth recording because it is the tempting one. It would produce an uncited topic
  note - a direct violation of ground-every-claim - and it is precisely the failure S8's ingest
  already caught once: **a claim written about a source that had not been ingested, wrong the day it
  was written, in a file nothing re-reads.** The brain's value is that everything in it came from
  somewhere.
- **Drop the sighting entirely.** Rejected: the fact that a major vendor treats MCP as one of two
  tool-integration standards *is* real information about MCP's position in the ecosystem. It is
  simply not information about MCP's mechanics. Recording it in Open questions keeps it findable
  without letting it masquerade as coverage.

## Consequences

- **Easier:** topic status becomes trustworthy again. A reader can take `emerging` to mean the note
  has content, and the INDEX stops being able to advertise an empty note.
- **Easier:** broad, ecosystem-shaped sources (framework announcements, survey posts, landscape
  talks) can now be ingested without dragging every topic they name up the ladder. Expect more of
  these, not fewer.
- **Harder:** every ingest of a broad source now carries a per-topic judgement call, and the
  architect has to make it explicitly rather than by counting. The mitigation is that the call is
  cheap and the test is written down.
- **A new place to look for drift.** Sightings accumulate in Open questions sections and nothing
  sweeps them. **The dream pass should treat an accumulation of sightings on one topic as a promotion
  signal** - three sightings and no source is itself evidence the area is real and under-covered.
  Added as a watch item rather than a rule, since it has not happened yet.
- **Revisit when:** a topic accumulates sightings but never a real source (does the ladder need a rung
  between `seed` and `emerging`?); or a source is genuinely borderline - substantial on a topic but
  entirely secondary to its main subject - which this pass did not produce.
- **Follow-up edits:** [`mcp.md`](../topics/mcp.md) Open questions + Sources feeding;
  [`skills.md`](../topics/skills.md) Sources feeding; S9's
  [`LEARNING.md`](../../sources/260801_agent-framework-layered-sdk/LEARNING.md) "Feeds these topics";
  `Topics` row in that source's [`SOURCE.md`](../../sources/260801_agent-framework-layered-sdk/SOURCE.md)
  (which named `evals` for a topic nothing was promoted to - the same defect class, caught on
  review); no INDEX Topics-row changes, which is the point.
