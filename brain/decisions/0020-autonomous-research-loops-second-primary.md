# ADR 0020: `autonomous-research-loops` survives its merge-back trigger, and the ADR-0018 boundary holds

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260805 |
| Deciders | chamin |

## Context

Two prior ADRs left explicit conditions attached to this pair of notes, and **S22 (Darwin Gödel
Machine) is the source that tests both at once.**

[ADR-0017](0017-autonomous-research-loops-topic.md) created
[`autonomous-research-loops.md`](../topics/autonomous-research-loops.md) on a single source, S13
(`karpathy/autoresearch`), and recorded it as a **merge-back candidate if no second primary arrives**.
The note has carried that warning in its Status line since - *one T4 source; merge-back candidate*.

[ADR-0018](0018-self-improvement-topic.md) created
[`self-improvement.md`](../topics/self-improvement.md) beside it and drew the boundary between them as
a matter of **altitude**: `autonomous-research-loops` changes an **artifact**, `self-improvement`
changes the **model**. It recorded a re-test trigger: *"revisit on the next source that lands claims in
both."*

**S22 lands claims in both, and it is unambiguously a second primary.** Published at ICLR 2026 (the
strongest venue in this brain), open-sourced code, and two ablations that isolate its claimed
components. It is a system that iteratively rewrites its own codebase, validates each change against
coding benchmarks, and keeps an archive of every agent it has produced - reaching SWE-bench 20.0% to
50.0% over 80 iterations.

**And it sits cleanly on the artifact side of ADR-0018's line, by its own admission.** The framing in
the abstract suggests a system that could "rewrite their own training scripts (including training a
new foundation model)"; §3 concedes "we do not show that in this paper" and that the work "focuses on
improving the design of coding agents with **frozen pretrained FMs**" (S22 `d3`). **The model never
changes. The scaffolding around it does.**

## Decision

**Three things, taken together.**

1. **`autonomous-research-loops.md` is no longer a merge-back candidate.** ADR-0017's condition is
   met: a second primary has arrived, it is independent of S13 in every respect (UBC / Vector / Sakana
   against a personal repository), and it is far better evidenced. The Status line's merge-back warning
   is **removed** and replaced with a record of what resolved it.

2. **S22's claims are homed in `autonomous-research-loops.md`, and cross-referenced from
   `self-improvement.md` rather than duplicated.** This follows ADR-0018's altitude rule applied to a
   source that states its own altitude.

3. **ADR-0018's boundary is confirmed rather than merely reasserted.** The re-test asked for by
   ADR-0018 has now been run against the hardest available case, and the line held without needing
   adjustment. **The next re-test trigger is narrower and is recorded here**: a source in which the
   *same loop* modifies both the artifact and the model weights. S22 explicitly declines to be that
   source and names it as future work, so it is a real possibility rather than a hypothetical.

**This is not a one-way door.** Both notes remain mergeable if a later source shows the distinction is
not carrying weight.

## Alternatives considered

- **Merge the two notes now that both have two sources.** Rejected. The altitude distinction is doing
  more work after S22, not less: `self-improvement` holds coverage/precision, test-time scaling and the
  generation-verification gap, all of which are properties of *sampling from a model*, while
  `autonomous-research-loops` holds freezes, accept rules, archives and rollback, which are properties
  of *an unattended optimisation over an artifact*. A merged note would have to explain why an
  exponentiated power law and a viability gate belong together.
- **Home S22 in `self-improvement.md` because its title says "self-improving agents".** Rejected under
  [ADR-0012](0012-a-mention-is-not-a-source.md)'s test - a source feeds a topic when it teaches within
  the scope, not when it is *named* after it. S22 teaches search design over a frozen model.
- **Home it in both, duplicating the claims.** Rejected as the stacking the contract forbids. Cross-
  referencing costs a reader one click and keeps one home per claim.
- **Create a third note for "self-modifying systems".** Rejected under the don't-spawn-a-topic-per-
  source rule. S13 and S22 are the same subject at different levels of rigour, which is what a topic
  note is for.

## Consequences

**Easier.** `autonomous-research-loops.md` can now be cited as a real topic rather than as a provisional
one, and its central claims acquire a second, far stronger source. Specifically, S13's four freezes -
recorded as one practitioner's design - are now readable against a peer-reviewed system that froze two
things for stated reasons, and **claim 114 (an accept rule with no variance notion banks noise)** gains
a counterpart in S22's staged evaluation with an explicit noise-derived threshold.

**Harder.** The two notes now have to be read together to get the whole picture on any self-improving
system, and a reader arriving at either one alone will get half the frame. Both notes carry a pointer;
that is the mitigation and it is not free.

**To revisit.** The narrower trigger recorded above - a single loop modifying both artifact and weights.
Also worth watching: if `autonomous-research-loops` acquires a third and fourth source while
`self-improvement` stays at one independent source, the asymmetry may argue for a different split than
altitude.

**Follow-up edits made in the same pass:** the Status line and synthesis in
[`autonomous-research-loops.md`](../topics/autonomous-research-loops.md), a cross-reference in
[`self-improvement.md`](../topics/self-improvement.md), the Topics rows in the root
[`INDEX.md`](../../INDEX.md), and a dated line in [`log.md`](../log.md).
