# Measuring the isolation ceiling of an MCP configuration

> Persona: **synthesizer**. A report written *out* of the brain, cited to the claims it draws on.
> **Read the evidence grades in §2 and §3 before acting on this** - one load-bearing step is a
> conjecture, not a claim. **§6.1 records the prior-art survey being read on 2026-08-05: it clears
> the idea**, so the next action is testing that conjecture, not more reading.

| Field | Value |
|---|---|
| Date | 2026-08-05 |
| Built from | claims 149, 152, 153, 155, 166, 167, 173; conjecture h7; R3 (AgentDyn); `mcp.md` |
| For | Deciding whether this is the next thing to build alongside **MCP Shark** |
| Verdict in one line | **Build it.** The prior-art survey was read and does not cover it (§6.1), and **the load-bearing conjecture was tested against AgentDojo's own data on 2026-08-05 and holds at 220x, chi-square 227** (§3.1). The remaining risk is no longer the idea - it is approximating task tool sets without ground truth |

## 1. The proposition

**Compute, statically, the fraction of an MCP deployment's tool surface on which any plan-time
isolation defence cannot help - and report it as a property of the configuration.**

Concretely: classify every tool a config exposes as read-like or write-like, then measure how often a
plausible user task's required tools **already suffice to carry out an attacker's goal**. Where they
do, no defence that restricts tools *in advance* can separate the two, because there is nothing to
remove without breaking the task.

Output shape: *"This config exposes 74 tools across 6 servers. 31% of read/write task pairs are
un-isolatable at plan time. Tool-filter and capability-policy defences have a 31% ceiling here,
before you evaluate any of them."*

## 2. What is established, with grades

**Claim 167 - the tool filter is the Pareto-winning defence, and its failure mode is quantified.**
AgentDojo evaluates four defences and the simplest wins: restricting the agent to the tools its task
needs, *before* it observes untrusted data, drops targeted attack success to **7.5%** while keeping
benign utility high. It fails when the tool list cannot be planned in advance, **and when the tools
required for the user's task are also sufficient to carry out the attack - true of 17% of test
cases** [S20 §4.3, `n12`, `n13`]. **Grade: strong.** NeurIPS 2024 Datasets and Benchmarks Track, open
source - the best-reviewed source in this brain.

**Claim 166 - attack success is a property of the application, not the model.** Holding the model
fixed, targeted success runs from ~92% on a Slack suite to 0% on some Travel tasks, and the two
predictors are how much of the tool output an attacker controls and how many independent malicious
steps must chain [S20 §4.1, `n8`, `n9`]. **Grade: strong.** This is what makes the property a *config*
property rather than a model property.

**Claim 153, as bounded by R3 - plan-time defences collapse when the plan cannot be written up
front.** CaMeL reports 77% of AgentDojo tasks with security. An independent group with no author
overlap ([AgentDyn](https://arxiv.org/abs/2602.03117), T3) replicates that and finds **0.00% utility
and 0.00% attack success on open-ended dynamic tasks**, because CaMeL writes a static program before
execution. The same paper generalises it: "planning-dependent approaches - such as **Tool Filter,
CaMeL, and DRIFT** - rely heavily on initial plans." **Grade: strong on the direction, T3 on the
numbers.** See [R3](../sources/260804_camel-prompt-injection-defense/context/01_independent-evaluation-and-the-2026-defence-landscape.md).

**Claim 155 - an information-flow defence protects actions, not assertions.** CaMeL's own non-goals
are attacks with no data-flow consequence [S18 §3.1, `n14`]. **Grade: strong**, stated by the authors.
Relevant here because it bounds what the ceiling metric can be *about*: it measures the action half
only.

**Together these say something the field has not operationalised.** Every plan-time isolation defence
- tool filters, CaMeL's capability policies, DRIFT - shares one failure condition, and that condition
is a property of **the tool surface**, which is a thing you can inspect without running anything.

## 3. What is conjectured, and must not be cited as established

**Conjecture h7** [`brain/conjectures.md`]: *the 17% is a property of the task distribution, not of
the defence - so every isolation defence's ceiling is set by tool granularity, and is a design
variable rather than a constant.*

**This is the load-bearing step and it is unproven.** S20 reports 17% once, on its own task suite, as
a property of the defence. **Nobody has shown that the number moves with the tool surface.** If it
turns out to be roughly constant across configs with very different read/write overlap, the metric
proposed here measures nothing and the idea dies.

**That is also why this is worth doing.** The cheapest way to test h7 is to build the measurement and
correlate it against defence failure rates - so the product and the experiment are the same work.

### 3.1 h7 was tested on 2026-08-05, and it holds

**Promoted to claim 178.** Run entirely over artifacts AgentDojo publishes - its ground-truth tool
sequences and its shipped run data - with no model calls and nothing re-executed. One file, reproducible:
[`experiments/260805_h7_agentdojo_test.py`](experiments/260805_h7_agentdojo_test.py).

A (user task, injection task) pair is **un-isolatable** when the injection's required tools are a subset
of the user task's - the filter has nothing to remove. Over 547 mappable pairs:

| Pipeline | un-isolatable pairs | isolatable pairs | risk ratio | chi-square |
|---|---|---|---|---|
| **No defence** (control) | 50.7% attacked | 47.9% attacked | **1.1x** | **0.2** - not significant |
| **Tool filter** | **46.7% attacked** | **0.2% attacked** | **220x** | **227.2**, p much less than 0.001 |

**The control row is what turns this from a correlation into a mechanism.** Un-isolatability predicts
nothing about whether an attack succeeds when there is no defence. It becomes almost totally
determinative once the filter is applied - which is precisely the claim. **35 of the 36 attacks that
survive the tool filter are un-isolatable pairs.**

> **An honest note on how nearly this was missed.** The first cut of this test was the one §8 originally
> specified - correlate **per suite**, four data points. It came back inconclusive and slightly
> discouraging: Spearman +0.80 against tool-filter attack rate, but equally correlated with *baseline*
> attack rate, and the discriminating residual-ratio test ran the wrong way at -0.40. **Aggregating to
> four suites was hiding a 220x effect.** The per-pair unit was both the correct test and available all
> along. Recorded because a reader repeating this would otherwise repeat the mistake.

## 4. The measurement, defined precisely enough to argue with

Vagueness here is what would make this a blog post rather than a result. Four steps.

**Classify each tool by effect.** Read-like (returns state, no external effect), write-like (mutates
state or emits externally: send, post, transfer, delete, execute), or both. MCP Shark already does a
weaker version of this - toxic-flow heuristics depend on tool-name classification, which its README
names as a limitation. **The classification quality is the metric's main risk** and is discussed in §7.

**Define the attacker's reachable set.** For a config, the set of write-like tools an injected
instruction could invoke - which, absent a defence, is all of them.

**Define un-isolatability per task.** For a user task requiring tool set `T`, the task is
un-isolatable if `T` already contains a write-like tool sufficient for a plausible attacker goal.
Restricting to `T` removes nothing the attacker needs.

**Report the fraction over a task distribution.** The honest hard part: you need plausible tasks. Two
routes, and they differ in cost and defensibility. **Synthesise** tasks per server from tool
descriptions, which is cheap and circular. Or **derive** them from captured traffic - which MCP Shark
already stores in SQLite, and which makes the number empirical rather than assumed. **The second is
the defensible one and it is the reason this idea belongs in your tool rather than in a paper.**

## 5. Why MCP Shark is the right vehicle

Four of the five required pieces already exist. Static config parsing across 15 IDEs. Cross-server
capability pairing (toxic-flow analysis is this metric's sibling - it asks which combinations are
dangerous; this asks which are *inseparable*). A traffic store that supplies the real task
distribution. And SARIF output, so the number lands in CI where a config change can regress it.

**The genuinely new part is one classifier and one counting function.** That is a weekend, not a
project - which is the strongest argument for doing it before the larger recovery idea.

## 6. Prior art, honestly assessed - and this bounds the claim

A search of arXiv for capability-overlap metrics in agent security returns a **more crowded field than
"nobody has this number" suggests**, and the honest framing is narrower.

| Work | What it is | Why it is not this |
|---|---|---|
| [ChainCaps](https://arxiv.org/html/2605.26542v4) | Runtime mechanism attaching a sink-specific authority budget to each value, propagated monotonically | A **defence**, in CaMeL's family. Enforces at runtime; measures no configuration |
| [Dynamic Capability Scoping](https://arxiv.org/html/2607.22445v1) | Three-layer permission architecture - role ceiling, task-context classifier, prohibition layer | **Prescriptive**: what permissions to grant. Not a measurement of overlap in a config that already exists |
| [Prompt Flow Integrity](https://arxiv.org/html/2503.15547v2) | Preventing privilege escalation in LLM agents | A mechanism again |
| [AgentSecBench](https://arxiv.org/html/2605.26269) | Benchmark measuring injection, privacy leakage, tool-use integrity | Measures **agents**, not deployed configurations |
| **[Isolation as a First-Class Principle for LLM-Agent System Safety](https://arxiv.org/abs/2607.12406)** (Jing, Hu, Chen, Shi, Zhang, Yang, Fan, Xie, Luo, Chan, Fan, Li, Song; arXiv 2607.12406 v1, 2026-07-14) | Boundary-centric taxonomy of isolation across five boundaries: user-agent, **agent-tool**, agent-execution, agent-agent, system-environment | **Read 2026-08-05. It does not cover this** - see §6.1. Purely a taxonomy: Table 1 organises representative papers by boundary and **contains no evaluation metrics or numerical measures** |

**So the defensible claim is not "this is unclaimed territory."** It is: *the field has mechanisms and
agent benchmarks, and no one appears to compute the isolation ceiling as a static property of a
deployed configuration, ahead of choosing a defence.* That is a narrower and more survivable claim.

### 6.1 The survey has been read, and it clears the idea

**Checked 2026-08-05, which was §8's first action.** Two probes with deliberately different vocabulary
- one asking about metrics and capability sufficiency, one about over-restriction, least privilege,
authority budgets and utility trade-offs. **Both came back negative on the same three points.**

- **No quantitative metric of any kind.** It "provides no numerical framework for assessing isolation
  strength", and Table 1 organises representative papers by boundary type with **no evaluation
  metrics or numerical measures**.
- **No read/write overlap, tool-sufficiency, or capability-overlap analysis.** Absent entirely.
- **It does not argue that isolation has an upper bound set by the system's own required
  capabilities** - which is the exact proposition in §1.

It cites **CaMeL** as an example of privilege separation, and mentions **neither Progent, AgentDyn,
nor tool filtering by name** - so despite being a July 2026 survey it is already behind R3's material.

**Two things in it actively help, and both are worth citing rather than merely noting.**

Its own open-challenges section states that **"the field still lacks stable abstractions for authority,
trust, and privilege in full workflows."** A measurable overlap property is a step toward exactly such
an abstraction, and having a survey say the gap exists is stronger support than asserting it.

And it observes that **"many benchmarks still test single boundaries, while real failures are
cross-boundary."** That is an independent argument for the vehicle rather than the idea: **MCP Shark's
toxic-flow analysis is already cross-server**, so it operates where this survey says the real failures
live and the benchmarks do not look.

Finally, its **boundary taxonomy gives the idea a place to sit**. This metric measures the
**agent-tool boundary**, which is vocabulary worth adopting if any of this is written up.

> **What this clearance is and is not.** Two targeted probes against the rendered paper, not a full
> human read of a survey. **Absence of a metric in one survey is not absence in the field**, and §6's
> table remains a reason for caution. What has changed is that the single most likely source of
> prior art has been checked and does not contain it.

## 7. What would kill this

~~**h7 is false.**~~ **Tested 2026-08-05 and it holds at 220x** (§3.1, claim 178). **The risk this
retired has been replaced by a narrower and more practical one**, below: the test used the benchmark's
**ground-truth** tool sets, and a real MCP config has none. The mechanism is established; what is
unproven is whether an *approximation* of task tool sets preserves the signal.

**Tool classification is too unreliable.** The metric inherits MCP Shark's stated limitation exactly:
toxic-flow heuristics "depend on quality of tool name classifications", and tool-level rules only apply
when server entries include explicit `tools` arrays. **A metric built on a name heuristic is a metric
someone can dismiss.** Mitigation: report coverage alongside the number, and refuse to emit a ceiling
for configs below a threshold of classified tools.

**The task distribution is assumed rather than observed - and after §3.1 this is now the single biggest
risk.** The experiment knew each task's exact required tools because AgentDojo publishes them. Your
product will not. Traffic-derived task reconstruction from MCP Shark's SQLite store is the defensible
route and its error is unmeasured. **The first thing to build is therefore the approximation, and the
first thing to measure is how much signal it loses against the ground-truth version** - which
AgentDojo lets you check directly, because it has both.

**Someone has already published it.** §6's table remains a reason for caution, though **the single most likely source has been checked and cleared** (§6.1).

**And the honest scope limit:** claim 155 means this measures the **action** half only. Fraud and
manipulated-content attacks have no data-flow consequence and no isolation defence touches them, so a
config could score 0% un-isolatable and still be exploitable. **The number must ship with that caveat
or it is misleading.**

## 8. What to do first, in order

~~**Read [2607.12406](https://arxiv.org/abs/2607.12406) before writing code.**~~ **Done 2026-08-05, and
it clears the idea** - see §6.1. The survey has no metric, no capability-overlap analysis, and does not
argue that isolation is bounded by required capabilities. It also supplies two citable supports: its
own "the field still lacks stable abstractions for authority, trust, and privilege" gap statement, and
its observation that real failures are cross-boundary while benchmarks are not - which is the ground
MCP Shark already occupies.

~~**Then test h7 before building the product.**~~ **Done 2026-08-05 - see §3.1. It holds at 220x with a
clean null control, and is promoted to claim 178.**

**So the remaining work starts at what was step 3, with one addition that §7 now makes the priority.**
Build the **task-tool-set approximation** first, not the counting function - reconstruct required tool
sets from captured traffic, then **validate it against AgentDojo's ground truth**, which is the one
place both versions exist. If approximated overlap reproduces the 220x separation, the metric is real
outside a benchmark. If it does not, you have found the actual hard part before shipping a number.

**Only then build it into MCP Shark**, with coverage reporting and the claim-155 caveat attached.

**And note what you get either way.** If h7 holds, you have a config-level security metric nobody
emits. If it fails, you have refuted a conjecture using the field's reference benchmark, which is a
smaller but real result - and this brain records refuted conjectures rather than discarding them,
precisely so that outcome is not a wasted week.

## 9. What to distrust in this report

**The key finding is this brain's own analysis, not an independent publication.** h7 was generated here
on 2026-08-05 and tested here the same day (§3.1, claim 178). **The data is third-party and
peer-reviewed; the analysis is mine and unreviewed.** It is reproducible in one file, which is the
mitigation, and it is not the same thing as someone else having found it. Coverage was 87% - 82 of 629
pairs skipped where ground truth would not parse statically - on one model and one attack type.

**The prior-art search was one query on one domain.** It was enough to bound the novelty claim
downward and is not a systematic review. §6's table is a reason for caution, not a clearance.

**R3's numbers are T3.** AgentDyn is a preprint with no venue, and its author list overlaps S16 -
irrelevant to the CaMeL result it reports, and worth knowing.

**The 17% itself is a single measurement.** S20 reports it once, on its own suite, in one sentence.
The entire idea rests on that number being interesting, and nobody has replicated it.
