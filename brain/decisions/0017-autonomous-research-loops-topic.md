# ADR 0017: a topic for autonomous research loops, and why it is not called "research agents"

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260803 |
| Deciders | chamin |

## Context

S13 ([`karpathy/autoresearch`](../../sources/260803_autoresearch/LEARNING.md)) is the brain's first
source about **an agent running an unattended optimization loop over an artifact, judged by an
automated metric**. It is not about building an agent (that is `agents`), and it is not about
measuring a pipeline someone else built (that is `evals`). Its gated claims are about the *setup* a
loop needs before it can be trusted to run for a hundred iterations with nobody watching: what is
frozen, what resource is held constant, what the metric's units are, where the audit trail lives,
and what the accept rule does with noise (`n1`-`n4`, `n6`-`n7`, `n11`).

The kit's standing guidance pushes against new topics - "don't spawn a topic per source - park a
one-off under the nearest topic". Three previous ADRs declined a topic on that basis
([0013](0013-secondary-but-substantial.md), [0014](0014-no-topic-for-organisational-context.md),
[0015](0015-an-architecture-is-not-an-identity-source.md)). The question is whether S13 is a fourth
decline or the exception.

Two facts pull the other way.

**First, the claims do not have a home.** Apply ADR-0014's swap test - replace the subject and see
what survives. Swap "train.py and val_bpb" for "a prompt and an eval score", or for "compiler flags
and a benchmark", and every one of S13's claims survives intact, which is the signature of a
transferable area rather than a source-specific one. But swap the *agent* for a random-search script
and the interesting half dies: the context budget per iteration (`n8`), the suppressed check-in
default (`n9`), the published exchange rates for a second objective (`n10`) and the
producer-prints-its-own-grade leak (`n5`) are all agent-specific and none of them is about building
an agent. Filed under `agents` they would sit beside claims about loops, tools and state and read as
a digression; filed under `evals` they would sit beside claims about grading pipelines and read as
someone else's subject.

**Second, the area is not actually single-source, it is single-*primary*.** The brain already holds
scattered claims that belong to it and currently have no centre: claim 7 (close the loop, auto-tune
on sampled production data with no human), claim 10 (agents self-tuning via a reflect-and-synthesize
prompt optimizer), claim 31 (scaffolding as an expiring bet, tested by ablation), claim 34 (do not
let the producer grade its own work) and claim 59 (split a loop rather than let it hold two
objectives). Every one of those bears directly on how an autonomous improvement loop should be
built, and each currently sits in `agents` or `evals` as a member of a different argument. That is
the `mcp.md` failure mode in reverse: not a topic scoped by accident, but a subject with no note,
whose claims are therefore scattered across two.

## Decision

**Create [`brain/topics/autonomous-research-loops.md`](../topics/autonomous-research-loops.md),
Status `emerging` (one primary source).**

**Scope:** an agent that iterates on an artifact unattended, accepting or rejecting each change
against an automated metric. What must be frozen before the loop starts; how a candidate is judged;
where the loop's state and audit trail live; how it behaves over many iterations; and how to read
its results honestly.

**Explicitly named as the topic's own weakness, in the note:** it opens with one source, that source
is one person's personal repository (T4), and its only empirical content is a single unreproducible
PNG. It stays `emerging` until a second *primary* source arrives, and the adjacent claims it
references from `agents` and `evals` are **cross-references, not corroboration** - they are not
re-homed and their `Topic` column in `claims.md` is unchanged.

**On the name.** It is **not** called `research-agents`, and the reason is local rather than
aesthetic: this kit already has a `/research` stage, and in it "research" means **external evidence
gathering from the literature** (`sources/<id>/context/`). A topic note called `research-agents`
sitting next to `.claude/commands/research.md` would read as "agents that search the literature",
which is the opposite of what the note contains. `autonomous-research-loops` is longer and
unambiguous. **This is a one-way door in the mild sense** - renaming later means fixing every
inbound link - so it is worth getting right now.

## Alternatives considered

- **Park it under `agents`** - the default under the kit's guidance, and the option I held longest.
  Rejected because `agents.md` is `established` across eight sources and already carries the
  broadest scope in the brain; adding "and also how to run an unattended optimizer" makes its
  "What this covers" line unreadable, and the four freezes would be buried under material about
  building an agent at all. **The signal that this was wrong: the claims split three ways** across
  `agents`, `evals` and `context-engineering`, with no note owning the argument that connects them.
- **Park it under `evals`** - superficially attractive, because `n3`, `n4` and `n11` are all
  measurement claims. Rejected because it inverts the subject. `evals` is about judging a system;
  here the judging is a *component* of a system whose subject is the search. Filing S13 under
  `evals` would be like filing a compiler under "type checkers".
- **Split it into a new topic per axis** (search strategy / experiment infrastructure) - rejected
  outright at one source. That is the topic-per-source failure with extra steps.
- **Wait for a second source** - the strictest reading of the guidance, and genuinely tempting.
  Rejected because the cost is asymmetric: the claims exist now and have to be filed somewhere now,
  and filing them wrong then re-homing them later is more churn than creating the note is. The
  `emerging` status exists precisely to say "this is one source and may not survive".

## Consequences

- **Easier:** the four freezes, the accept rule and the noise finding have one address, and the next
  source on automated experimentation (an AI-scientist paper, an automated prompt optimizer, an
  agentic benchmark harness) has an obvious merge target rather than a create-vs-merge argument.
- **Harder:** a ninth topic, and the first one in this brain created on a **T4 personal repository**
  whose results cannot be reproduced. If no second primary source arrives, this note is a standing
  candidate for merge back into `agents` - **record that explicitly in the note so a future dream
  pass sees the trigger** rather than re-deriving the question.
- **Watch item for the dream pass:** claims 7, 10, 31, 34 and 59 are now referenced from two notes.
  If the cross-references start restating those claims rather than pointing at them, that is
  duplication and the dream pass should merge it back.
- **Follow-ups applied in the same pass:** a Topics row in the root `INDEX.md`; the source row for
  S13; claims 110-119 in `claims.md`; and additions to `agents.md`, `evals.md`,
  `context-engineering.md` and `skills.md` recording what S13 contributes to each **without**
  duplicating the new note.
