# ADR 0022: A primary source is not corroboration - `mcp.md` stays `emerging` at three

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260807 |
| Deciders | chamin |

## Context

[`../topics/mcp.md`](../topics/mcp.md) has recorded the same complaint three times, and each time it
was rediscovered rather than remembered.

At one source it said the topic had no primary source. At two it said "**the count rose and the
corroboration did not**", because S10 (client-side catalog cost) and S12 (deployment topology) confirm
nothing of each other's. Its scope caveat then went further and admitted the note was "scoped by
accident rather than by design", with resources, prompts, sampling, the handshake and **any spec
version at all** at zero.

S23 (Google's MCP stateless-updates announcement, 2026-08-05) arrives as **the note's first primary
source** - the first that is about MCP rather than teaching it on the way past something else - and
the first anywhere in this brain to pin a specification version (2026-07-28, superseding 2025-11-25).
It closes the handshake gap by documenting its deletion (claim 179), closes the spec-version gap, and
closes sampling by documenting its deprecation (claim 183). It also gives the note its first
authorization mechanism (claim 182).

**So the obvious move was to advance the topic to `established`, and the obvious move is wrong.**
S23 overlaps S10 and S12 on almost nothing. Transport mechanics, catalog cost and deployment topology
are three disjoint subjects, and **no two sources in this note confirm the same mechanic**. The
comparison that settles it is [`../topics/agent-security.md`](../topics/agent-security.md), advanced
to `established` by [ADR-0019](0019-agent-security-established.md) on **three independent
corroborating groups**, not on a source count and not on the arrival of a good source.

The tension is that "primary" and "corroborated" are different axes, and the note's own language had
been quietly conflating them by treating "no primary source" as the headline defect.

## Decision

**`mcp.md` stays `emerging` at three sources.** A primary source fixes a topic's **scope** defect and
supplies nothing toward its **corroboration** defect. Status in this brain tracks corroboration.

Stated generally, so it stops being rediscovered: **advancing a topic's status requires two sources
that confirm the same mechanic, and neither a source count nor the arrival of a primary source
substitutes for it.** A primary source is recorded in the status line as what it is - the thing that
makes a note scoped by design rather than by accident - and it moves the status only if it also
corroborates something already there.

Not a one-way door. Reversible the moment a second source touches the transport core.

## Alternatives considered

- **Advance to `established` on the strength of the primary source.** Rejected. It would make
  `established` mean two incompatible things across the brain - three corroborating groups in
  `agent-security.md` and one good source in `mcp.md` - which destroys the status as a signal. The
  brain's own claim 34 instinct applies: the label has to be set by something other than the
  enthusiasm of the pass that just did the work.
- **Introduce a fourth status such as `scoped` or `primary-covered`.** Rejected as machinery. The
  status vocabulary is three words and the note already carries a prose status line where this fits.
  Adding a status for one topic's transitional state is scaffolding that encodes an assumption which
  expires (claim 31).
- **Leave the status line as it was and just add sources.** Rejected. That is precisely how the
  complaint got rediscovered three times. The reasoning belongs somewhere durable, which is this file.
- **Advance on the grounds that S23 partially answers S10's and S12's shared open question.** Tempting
  and still rejected. **Answering a question two sources asked is not the same as confirming a claim
  they made.** RFC 8707 supplies a mechanism neither of them named, which is new information rather
  than agreement, and it is single-leg two-sentence prose at that (claim 182).

## Consequences

- `mcp.md`'s status line now states the count, names S23 as the first primary source, pins the spec
  version, and says explicitly why the status did not move. The scope caveat shrinks rather than
  disappearing: resources and prompts remain at zero as first-class subjects.
- The root [`INDEX.md`](../../INDEX.md) Topics row for MCP is updated to match, keeping `emerging` with
  a source count of 3.
- **What to revisit:** the next MCP source that touches the transport core, the authorization spec, or
  `tools/list` cost. Any of those could produce the first genuine corroborating pair here, and the
  authorization spec is the most likely, because both `mcp.md` and `agent-security.md` are already
  pointed at it.
- **A trap this makes visible.** S23 is a T2 vendor writing about a standard it says it led. Had the
  status advanced on its arrival, the brain's confidence in MCP would have been set by a single
  interested party's announcement of its own work. The corroboration rule prevents that without anyone
  having to argue about the vendor's motives.
