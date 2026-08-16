# ADR 0029: `The 1-minute version` gets a diagram after all - reversing the 2026-08-15 rejection

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260816 |
| Deciders | chamin |
| Supersedes | the rejection recorded inline in `AGENTS.md` when the TL;DR diagram landed (`aab2de2`, 2026-08-15) |

## Context

When the TL;DR diagram was added to the `LEARNING.md` frame on 2026-08-15, the same pass considered
putting a diagram in `The 1-minute version` and **rejected it**, recording two reasons in `AGENTS.md`:

1. That section's job is *the argument in sixty seconds of scanning*, and **a set of diagrams makes it
   slower to scan** than the prose it compresses.
2. Its **thesis-shape is already drawn** in the TL;DR diagram, one section above.

The TL;DR diagram was then written to absorb the requirement.

**One source later, that reasoning is half right and half wrong, and the wrong half matters more.**

Reason 1 assumed **a set** of diagrams. That is a real cost and it is not what a single diagram costs.
The section is now specified as six to eight flowing paragraphs plus a table, which on S27 runs to
roughly 900 words - far past sixty seconds of scanning already. One vertical diagram is the fastest
element in that section, not the slowest.

Reason 2 is the one that does not survive contact. The TL;DR diagram draws the note's **thesis** -
what the argument concludes. `The 1-minute version` answers a different question, *what does it
actually say*, and its narrative carries a beat the table has no slot for and the thesis diagram
cannot show: **the arc from problem through why-it-is-hard to cost and trust**. Nothing in the note
draws that arc. The roadmap draws reading order, the movement diagrams draw local mechanism, and the
mental model draws the subject. **A reader who stops at `The 1-minute version` currently leaves with
the claim and without the shape of the reasoning behind it**, and on S27 that reader is stopping after
the second section of a 12,000-word note, which is the common case rather than the edge one.

## Decision

**`The 1-minute version` carries one diagram, placed between its narrative and its table**, drawing
the **argument's arc**: the standard row sequence (the problem, why it is hard, why the obvious answer
fails, the idea, how it works, what it costs, how far to trust it) as a single vertical flow.

It is **Hard for sources from 2026-08-16**, on the same scoped-to-new-ingests basis as the
`Presentation narrative` ([ADR-0026](0026-presenter-persona.md)), and for the same reason: twenty-seven
notes predate it and retroactive mandates create retrofit debt on the day they land.

**The anti-collapse table gains a row**, because a fifth whole-note diagram is exactly where collapse
becomes likely:

| Diagram | Answers | Must not |
|---|---|---|
| TL;DR | what is the shape of the argument? | be the flow, or the reading order |
| **1-minute** | **how did the reasoning get from the problem to the answer?** | **be the thesis again, or the subject** |
| Roadmap | what order will I meet it in? | be the subject |
| Mental model | how does the subject actually work? | be a table of contents |

**The reliable way to keep it distinct is to draw the row sequence and nothing else.** If it starts
showing components, it has become the mental model. If it shows only the conclusion, it has become the
TL;DR diagram.

## Consequences

**It must stay vertical and phone-sized**, and that constraint is now load-bearing rather than
stylistic - see the render defect fixed in `3d1eaec`, where `direction TB` inside a subgraph was
silently ignored and the TL;DR diagram came out at a 4.22 aspect ratio, scaling to 0.18 on a 390px
screen. A seven-node vertical chain has no subgraphs and does not hit that trap.

**It carries a walkthrough like every other diagram**, written in presenter voice, and the hard rule in
Global rules has no exemption. Budget roughly 150 words.

**The cost is one more diagram in a note that already carries seven**, and `AGENTS.md` warns twice that
a note "already struggles to keep three diagrams distinct". That warning is accepted rather than
dismissed: the anti-collapse row above is the mitigation, and the honest expectation is that this is
the rule most likely to produce a duplicate. **If the next two sources produce a 1-minute diagram that
restates the TL;DR one, delete this rule rather than patching it.**

**It goes in the Provisional rules register at one instance**, so a future session is told it is new
and under-tested rather than having to infer that.

## Alternatives considered

- **Move the mental model diagram up into `The 1-minute version`.** Rejected: `## Diagram (mental
  model)` is a Hard section, and the mental model answers *how the subject works*, which is not what a
  summary section is for. It would empty a required section to fill an optional one.
- **Duplicate the mental model diagram in both places.** Rejected outright as the decoration the
  diagram rule exists to prevent.
- **Leave it and trim the narrative instead**, on the theory that the itch is density rather than a
  missing picture. Rejected by the requester after the trade was put to them explicitly. Recorded here
  because it remains the cheaper fix if this rule fails to graduate.
- **Keep the 2026-08-15 rejection.** Rejected: its first reason priced a set of diagrams rather than
  one, and its second assumed the TL;DR diagram covers an arc it does not draw.
