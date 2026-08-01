# ADR 0013: Secondary but substantial - a source advances a topic it is not about

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260801 |
| Deciders | chamin |

## Context

[ADR-0012](0012-a-mention-is-not-a-source.md) ruled that **a mention is not a source**, and closed by
naming the case it had *not* yet produced:

> **Revisit when:** ... a source is genuinely borderline - **substantial on a topic but entirely
> secondary to its main subject** - which this pass did not produce.

**S10** ([Tool search](../../sources/260801_tool-search-toolboxes/LEARNING.md), Microsoft, 2026-07-29)
produced it, one source later.

S10 is **about** tool retrieval. Its thesis is that a large tool catalog is an information-retrieval
problem; its measurements are token counts and Recall@10. It is not an MCP article. MCP is never its
subject, and a reader looking for a protocol explainer would not choose it.

**And yet it teaches more about MCP mechanics than anything else in this brain**, because its
mechanism is built directly on the protocol's shape:

- **`tools/list` is a per-turn cost centre** whose size scales with the catalog, not the task
  (`n1`, corroborated by Figure 1 and Figure 2).
- **Runtimes reject calls to tools absent from `tools/list`**, which is the entire reason the design
  needs a second proxy tool rather than one (`n4`). That is a statement about how MCP clients behave,
  not about Foundry.
- **An MCP server can front other MCP servers**, exposed over streamable HTTP with bearer auth, with
  the aggregated servers appearing as ordinary attached MCP endpoints (`n7`, from the portal
  screenshot).
- **A significant capability was added with no new protocol primitive** - stated as a design goal and
  visible in the product surface as a toggle (`n5`).
- **What a tool exposes to an index** - name, description, argument names and argument descriptions,
  three levels deep - and the fact that a field can be indexed while staying **invisible in MCP
  responses** (`n8`, `n14`).

Under ADR-0012's own test - *would a reader arriving at this note from the INDEX find what the status
promises?* - a `mcp.md` carrying those five items answers real questions about how agents consume MCP
tools at scale. That is not a labelled box in a diagram.

`mcp.md` has been `seed` with **zero sources** since this brain started, so the call is also the one
with the most inertia behind it, in both directions.

## Decision

**A source advances a topic's status when it teaches that topic's scope substantively, regardless of
whether the topic is the source's subject.** Being secondary is not disqualifying; being thin is.

Applied this pass: **`mcp` advances `seed` to `emerging` on S10**, with its Synthesis section written
from S10's gated nodes and nothing else. S9's earlier sighting stays recorded as a sighting and is
**not** retroactively promoted to a source - it contributed one box in one diagram and that has not
changed.

**The test is unchanged from ADR-0012; only the qualifier is removed.** Scope is defined by the note's
own "What this covers" section, and the question is whether the note can now answer a basic question
about the area. What was implicit before and is now explicit: **that question is about the note, not
about the source's table of contents.**

## Why "secondary" was the wrong axis

ADR-0012 was written against **over-counting**, and it worked. But it left "substantial" and "primary"
tangled together, and they measure different things:

| | Source is *about* the topic | Source is *secondary* on the topic |
|---|---|---|
| **Teaches its scope substantively** | Obvious source (S5 for skills) | **This case. S10 for `mcp`** |
| **Names it only** | Cannot happen | Sighting (ADR-0012: S9 for `mcp`) |

The bottom-right cell is what ADR-0012 governs and it still governs it. The top-right cell had no
rule, and defaulting it to "sighting" would have been the *under*-counting error - which ADR-0012
described as cheap and self-correcting, and it is, but only until it starts systematically discarding
the sources a topic actually has. **Secondary sources are where cross-domain learning lives.** A brain
that only counts a source for the topic on its title page will never notice that the tool-retrieval
article is its best MCP source, or that the memory article is also a concurrency source.

**The failure this does not reopen.** ADR-0012's real target was a status advancing on a *word
appearing*, leaving a populated status row over an empty Synthesis section. The guard against that is
unchanged and is now doing all the work: **the Synthesis section must be written, from gated nodes,
before the status moves.** If a source cannot fill it, the source did not teach the topic, whatever
its subject was.

## Alternatives considered

- **Hold `mcp` at `seed` until a protocol-first source arrives.** Rejected. It would leave five cited,
  corroborated claims about MCP mechanics sitting in a source note with no topic to feed, and it
  states something false: the brain would claim to know nothing about MCP while holding a measured
  account of what `tools/list` costs. The honest version is `emerging` with a scope caveat, which is
  what the note now carries.
- **Advance `mcp` and also count S9 retroactively, taking it straight to `established`.** Rejected
  outright - that is precisely the ADR-0012 error, and doing it in the same pass that cites ADR-0012
  would be self-refuting. S9 still contributed one box.
- **Create a `tool-use` topic and put everything there instead.** Rejected as topic-per-source
  (`AGENTS.md`: "Don't spawn a topic per source"). S10's claims already have four good homes, and the
  IR-flavoured ones belong in `rag.md` where the retrieval machinery lives. Revisit if a second and
  third source arrive on tool selection specifically, at which point splitting a `tool-use` note out
  of `agents.md` and `context-engineering.md` becomes a real question rather than a speculative one.
- **Require two secondary sources to equal one primary.** Rejected as arithmetic standing in for
  judgement, on ADR-0004's line: `validate.py` checks form, the architect judges scope. It would also
  have no principled exchange rate.

## Consequences

- **Easier:** a topic can now be advanced by the source that genuinely taught it, which is frequently
  not the source that advertises it. Expect this to matter most for the thinnest topics, since a
  well-covered topic gets primary sources anyway.
- **Harder:** the judgement is now unavoidable on every ingest of a broad source, in both directions -
  ADR-0012 asks "is this only a mention?" and this asks "is this actually substantial?". The mitigation
  is the same and it is cheap: **try writing the Synthesis section. The attempt answers the question.**
- **A new drift risk, and it is the mirror of ADR-0012's.** A topic whose entire content arrives
  sideways from sources about other things can end up **scoped by accident** - covering exactly the
  slice its secondary sources happened to touch, with the caveat that says so slowly going unread.
  `mcp.md` is now in that state by construction and says so in its status line. **The dream pass
  should treat a topic with no primary source as a watch item**, alongside ADR-0012's accumulated
  sightings.
- **Revisit when:** a topic reaches `established` without a single source that is *about* it (does the
  ladder need to distinguish coverage from breadth?), or when a secondary source's claims turn out to
  be systematically narrower than the note's stated scope.
- **Follow-up edits:** [`mcp.md`](../topics/mcp.md) - status, Synthesis, Key claims, Sources feeding,
  and the S9 sighting rewritten to point here; `INDEX.md` Topics row for MCP;
  [`claims.md`](../claims.md) claims 83, 84, 89.
