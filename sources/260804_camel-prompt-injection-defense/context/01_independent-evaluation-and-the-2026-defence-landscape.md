# Context 01 - CaMeL independently evaluated, and the 2026 defence landscape

> Persona: **fact-checker + synthesizer**. Contract: [`AGENTS.md`](../../../AGENTS.md) § "Deep
> research on request".
>
> **External evidence about gated nodes. Not a source ingest**, and nothing here is a claim until it
> is promoted with its citation and tier. `LEARNING.md` cites this note; it does not absorb it.

| Field | Value |
|---|---|
| Date | 2026-08-05 |
| Targets | S18 `n9`, `n10`, `n11` (efficacy, all gated `needs-check` because the benchmark is the authors' own, `d1`) |
| Budget used | **2 searches, 4 fetches** of ≤8 / ≤12 |
| Source floor | arXiv / named-institution primaries only, per the owner's standing instruction. Two blog hits (a well-known practitioner's commentary on CaMeL, and an explainer site) were surfaced by the first search and **dropped without being read** |
| Verdicts | 1 `supports`, 3 `refines`, 0 `contradicts`, 0 `no-evidence` |

## The question this pass existed to answer

S18's efficacy numbers - 77% of AgentDojo tasks with provable security, attacks from 100-300 down to
0-1 - are measured on **AgentDojo, whose first author is CaMeL's first author** (S18 `d1`). This brain
recorded that as an open question twice: once when S18 was ingested, and again when S20 was ingested
and explicitly *failed* to close it, because S20 shares those authors.

**Has anyone outside that group evaluated CaMeL?**

## F1 - Yes, and the result is a `refines` that changes what claim 153 may be used for

**[AgentDyn: Are Your Agent Security Defenses Deployable in Real-World Dynamic Environments?](https://arxiv.org/abs/2602.03117)**
- Hao Li, Ruoyao Wen, Shanghao Shi, Ning Zhang, Yevgeniy Vorobeychik, Chaowei Xiao.
- arXiv 2602.03117, v1 2026-02-03, **v3 2026-05-07**, 26 pages, 17 tables. **T3** (preprint, no venue
  stated).

It builds a benchmark of **60 open-ended tasks and 560 injection test cases** across Shopping, GitHub
and Daily Life, deliberately targeting three things it argues existing benchmarks miss: **dynamic
open-ended tasks**, **helpful third-party instructions**, and non-simplistic user tasks. Then it
evaluates **ten** defences.

**CaMeL scores 0.00% utility - with and without attack - and 0.00% attack success, across all tested
models.**

The stated reason is structural rather than incidental: CaMeL "initializes static program code
generated from the user instruction and enforces a strict execution sequence to ensure security. This
static strategy is difficult to handle the open-ended tasks, resulting in zero utility and zero ASR
across all agents on our fully open-ended benchmarks." The same paper confirms CaMeL's AgentDojo
result stands - "near-zero attack success rates with still high utility" - so **this is not a failed
replication.**

> **The correct reading, and it matters for how claim 153 may be cited.** CaMeL is not refuted. It is
> **bounded**: the 77%-with-security result holds on the benchmark it was built against, and on
> open-ended tasks requiring dynamic planning the system **does nothing at all**. Zero utility with
> zero attack success is the degenerate corner S20's own two-axis design exists to expose - perfect
> security by accomplishing nothing - and it took a third party's benchmark to surface it.

**Independence, checked rather than assumed.** No overlap with S18's authors (Google, Google DeepMind,
ETH Zurich), which is the independence that matters here. **Note one overlap elsewhere: Chaowei Xiao
is also an author of S16 (AgentPoison)**, so this source is *not* independent of S16 - which is
irrelevant to the claim being tested and is recorded so a later pass does not treat it as a free
second witness for anything S16 asserts.

## F2 - The failure generalises, and it is the one S20 named about itself

AgentDyn finds the same shape across a class: "planning-dependent approaches - such as **Tool Filter,
CaMeL, and DRIFT** - rely heavily on initial plans, leading to severe utility drops in the
dynamic-planning tasks."

On the tool filter specifically: it "maintains high utility on AgentDojo, but suffers from significant
over-defense in our benchmark", because "during initial planning, the tool filter usually blocks
essential tools required for later dynamic interactions because they appear unnecessary for the
original user task."

**S20 stated exactly this limitation about its own defence** and could not test it - claim 167 records
that the tool filter "fails when the list of tools to use cannot be planned in advance", and S20's
§4.3 names an untested scenario of an agent given multiple tasks over time. **AgentDyn is that test,
run by a third party, and it finds the limitation dominates once tasks are open-ended.**

**Verdict: `refines` on claim 167.** The 17% was never the whole bound; it was the bound *on a static
benchmark*. The real constraint on plan-time isolation is whether the plan can be written before the
work starts.

## F3 - Detection-based defences fail the same way, from a second team

ProtectAI and PIGuard "showed severe over-defense", achieving "almost perfect defense" on existing
benchmarks and failing on AgentDyn, which the paper attributes to their "limited ability to
distinguish helpful instructions from malicious injections."

**Verdict: `supports` claim 159**, and it is worth being precise about what it adds. S19 showed
detectors fail on **weak-signal** payloads that look like legitimate content, measured on memory
poisoning. AgentDyn shows the mirror failure on a different axis: detectors cannot separate a
**helpful third-party instruction** from a malicious one, so they over-block. **Two independent teams,
two benchmarks, two failure directions, one root cause** - a detector is being asked to make a
judgement that the text does not contain.

## F4 - Spotlighting has now been evaluated agentically, closing S21's `d3`

S21's `d3` recorded that **every** Spotlighting experiment was document summarization or Q&A, and that
the only variant anyone had tested against a tool-calling agent was delimiting - the variant its own
authors disown. AgentDyn evaluates Spotlighting directly.

On AgentDyn with GPT-4o: **52.24% utility under attack, 27.61% attack success rate.** Prompt
Sandwiching, the other behavioural defence tested, gives 56.13% / 31.17%. The paper's summary is that
prompting-based defences and spotlighting "maintain high utility. However, they only slightly reduce
ASR, indicating their limited effectiveness in defending against prompt injection attacks."

**Verdict: `refines` on claim 170.** Spotlighting is not useless in an agentic setting and it is
nothing like the 3.1% it reports on document tasks. **The utility cost is genuinely low, as S21
claimed; the security benefit is much smaller than its own numbers suggest once an agent with tools is
in the loop.**

## F5 - No defence is acceptable on both axes, and nine exist that this brain does not hold

AgentDyn's overall conclusion: "almost all existing defenses are either not secure enough or suffer
from significant over-defense, revealing that existing defenses are still far from real-world
deployment." **The best balance of the ten is Meta SecAlign-70B at 53.35% utility under attack and
8.98% ASR** - which is a defence this brain has never heard of, and still not a deployable number.

The ten evaluated: Prompt Sandwiching, **Spotlighting** (S21), ProtectAI, PIGuard, PromptGuard2, Meta
SecAlign, **Tool Filter** (S20), **CaMeL** (S18), Progent, DRIFT. A second 2026 preprint
([arXiv 2606.26479](https://arxiv.org/abs/2606.26479)) names five in the same family - CaMeL, FIDES,
Progent, RTBAS, FORGE - and argues none has faced a standardised adaptive, defence-aware evaluation.
**That paper gives no author affiliations and no venue, so it is recorded as a pointer and nothing is
built on it.**

> **The coverage gap, stated plainly.** This brain holds **three** defences (CaMeL, tool filter,
> Spotlighting) of a field that has at least **twelve**: add Progent, DRIFT, FIDES, RTBAS, FORGE, Meta
> SecAlign, PromptGuard2, ProtectAI, PIGuard. The three it holds are the three that a third-party
> benchmark ranks as *planning-dependent and over-defensive* or *weakly effective*.

## F6 - The field's own vocabulary matches this brain's synthesis

Both papers describe the structural class as **"out-of-band" defences** - enforcing security outside
the model with a deterministic policy rather than training the model to refuse. That is **S21's
telecom analogy adopted as the field's standard term**, and it independently supports the three-class
taxonomy this brain wrote as claim 173 (`needs-check`, "the taxonomy is this brain's synthesis and no
source draws it").

**Verdict: `refines` claim 173's confidence note.** The *sorting* is now visible in the literature's
own vocabulary. It does not promote the claim - a shared word is not a shared taxonomy, and neither
paper draws the three-way split - but "no source draws it" is no longer quite right.

## Confidence assessment

**What this pass establishes well.** CaMeL has been independently evaluated by a group with no overlap
with its authors, and the result is a clean bound rather than a refutation. That was the single
highest-value open question in the security material and it is now answered.

**What it does not establish.** AgentDyn is a **T3 preprint with no venue**, it is one benchmark, and
its author list overlaps S16. Its numbers should be read the way this brain reads S18's - as evidence
from an interested party who built the instrument. **The difference is that the interest points the
other way**, which is what makes it useful.

**Assumptions made, per the contract's no-clarifying-questions rule.** I treated "independent of S18"
as the relevant independence test rather than "independent of everything this brain holds", because
the gated question was specifically about CaMeL's self-report. I did not chase the nine unheld
defences, which would have been a survey rather than a targeted pass and would have blown the budget.

**What to do next, in order.** Ingest **AgentDyn** as a source in its own right - it is the benchmark
that tests deployability rather than security-in-principle, and it directly bounds three claims here.
Then **Meta SecAlign**, as the only defence anyone ranks acceptable on both axes. **Progent** is the
third, as the dynamic-aware defence that CaMeL's static planning cannot be.
