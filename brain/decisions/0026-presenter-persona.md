# ADR 0026: A `presenter` persona and a `Presentation narrative` section, for new sources only

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260815 |
| Deciders | chamin |
| Persona | architect |

## Context

**Every compressed form this kit has answers a *reader's* question.** `TL;DR` answers *should I read
this?*, `The 1-minute version` answers *what does it actually say?*, `Key claims` answers *what may I
cite?*. None of them is a **speaking** artifact, and the notes now run 5,000-9,000 words tuned for a
solo reader ramping up.

**And every layer in the kit is written for the operator or for an agent.** `nodes.md` is for the
gate, `LEARNING.md` for a reader learning the subject, `brain/topics/*.md` for someone asking what the
brain knows, `reports/` for a specific question. Nothing here is written for **people who will never
open the repo** - which means the brain optimises entirely for its own correctness and not at all for
transfer. Knowledge that cannot leave cannot influence anything, and the kit's stated purpose is
learning, which is only half-served by storing.

Three things made this a decision rather than an addition.

**It inverts a rule the contract enforces.** A presentation must **lead with the takeaway and then
earn it**. `AGENTS.md` forbids exactly that everywhere after the `TL;DR`, at length, calling the
punchline opening *"the anti-pattern to watch for"*. Left unstated, a future agent meets two rules
that contradict and picks one.

**It is the first artifact whose craft rewards confidence.** Twenty-six sources of machinery exist
here to resist overclaiming - `single-leg` marking, "corroborated is not true", the tier system, "do
not cite as a result". A presentation genre pulls the other way, in front of the audience most likely
to act on it.

**And making it mandatory would create instant retrofit debt.** Twenty-six notes predate it. The
register retrofit already demonstrated how that goes: it is still unpaid on S2, months after landing.

## Decision

**Add a sixth persona, [`presenter`](../../personas/presenter.md)**, and a
**`## Presentation narrative`** section appended as the last element of `LEARNING.md`.

**Four choices inside that, each of which could have gone otherwise:**

1. **Per-source, not per-topic.** A per-source presentation is a *"can I explain this in five
   minutes"* test. **The deck a person actually gives to leadership is topic-level** - drawing on
   several sources at once - and that belongs in `reports/`. **Deliberately not built yet**; revisit
   when a real presentation is needed, because building the general case first would be scaffolding
   for a need nobody has felt (claim 31).
2. **One narrative serving both audiences, not two tracks.** Leadership takes consequence, engineers
   take mechanism, **from the same movement**. Splitting the deck is what produces two half-served
   audiences. The consequence leads; the mechanism earns it.
3. **Appended last, after `Feeds these topics`.** It cannot disturb the ramp, and `build_site.py`
   lifts only `TL;DR` and `Key claims`, so it never reaches the landing card.
4. **New ingests only** - sources from 2026-08-15 onward - **with `validate.py` reporting coverage
   rather than failing.**

**The null close is mandatory and first-class**, not a degenerate case. The most common honest
conclusion in this brain is that nobody measured the thing, and a persona told to close on what should
be funded or changed will manufacture actionability under pressure. *"The decision is to not act yet,
and here is precisely what would change that"* is the stronger leadership close, because it converts
"we do not know" into a scoped experiment with a trigger.

**Movements reuse the curated frames by default.** A new synthesized diagram is justified only where a
movement's consequence has no existing visual. This kit already records that keeping *three* diagrams
distinct is hard; five more per note would be decoration, and it would break the frame-prune rule's
arithmetic. **A frame earning its place twice was well chosen.**

**One narrow register carve-out.** Movement **bullets** are exempt from the Register rules, because
that is what bullets are. **The explanations underneath them are not** - they are prose carrying an
argument.

> **Amended the same day, 2026-08-15, and both halves of this paragraph are now void.** A reference
> artifact made it clear the section read as **slide notes rather than a talk track**, and the cause
> was the bullets. They are now **banned outright**, so the carve-out has nothing left to exempt and
> is **withdrawn** - the Register rules apply in full, and a slide's bolded opening sentence is a
> *claim* rather than the lead-in label they forbid. **`Movement` is also renamed `Slide`** throughout
> the presentation, because `movement` already names the roadmap's groups of walkthrough sections and
> this decision created a collision inside one file. The word budget moved from 700-1,200 to
> **900-1,500** on the precedent that this kit already accepts +25 to +30% words for register quality.
> **Two statements under Consequences are also overtaken.** "Notes get 700-1,200 words longer" is now
> 900-1,500, and **"No reference implementation exists" is false** - S26 has one, written the same day,
> and it is what exposed both the tone problem and the movement/slide collision. **That is the ADR's
> own prediction coming true faster than expected**: it warned the shape had been specified wrongly
> twice before a worked example forced a rewrite, and this shape lasted hours.
>
> **The rest of this ADR stands**; only the register, naming and budget clauses changed. Current spec
> lives in [`personas/presenter.md`](../../personas/presenter.md).

## Consequences

**Good.** The brain gains an output aimed at transfer rather than storage. The per-source form doubles
as a design check on the note: an argument you cannot present in seven slides is usually one you
have not finished deriving, which is the same test the `1-minute version` already applies from a
different angle.

**Costs, accepted.**

- **It is the first mandatory `LEARNING.md` element with no checkable property whatsoever.**
  `validate.py` can confirm the heading exists; whether a story lands is taste. The kit has been
  disciplined about form-versus-judgement and this is a deliberate exception, chosen knowingly.
- **`/verify`'s six checks were not designed for it.** Checks 1 to 4 extend naturally, since the
  section carries node IDs and evidence labels like any other prose. **This is not yet stated in the
  `/verify` contract** and should be revisited after the first few exist, rather than guessed at now.
- **Notes get 700-1,200 words longer.**
- **No reference implementation exists.** This file records that the `LEARNING.md` shape was specified
  wrongly **twice** before a worked example forced a rewrite. The next ingest is the test; if the shape
  is wrong, the contract is what changes.

**Revisit when:** a topic-level presentation is actually needed (promote to `reports/`), or when
enough per-source narratives exist to say whether five to seven slides was the right shape.
