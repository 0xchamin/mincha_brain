# Spec: isolation-ceiling analysis for MCP Shark

**Read [background.md](background.md) first.** It carries the threat model, the evidence, and five
hard constraints. This document is the build.

**Status of this document.** A specification written from a validated finding, by an agent that has
not seen MCP Shark's source. **Every reference to MCP Shark's internals is an assumption to check
against the codebase, not a description of it.** Where a name is guessed it is marked `[verify]`.
> **Where this document lives, and why its links look inconsistent.** This file is served from
> **`main`** - or from commit `48e74ca` onward, the commit that introduced it. **Do not construct a
> URL to this file using `638ebe9`; that commit predates the handoff pack and will 404.** The
> evidence links *inside* this document are deliberately pinned to `638ebe9` because that is the
> commit whose wording they cite, and those files all exist there. Two different jobs, two different
> refs: **the pack itself tracks `main` so you always get the current version; its citations are
> frozen so they cannot drift.**

---

## 0. Goal, and the one-sentence success criterion

Add a mode to MCP Shark that reports, for a given MCP configuration:

> *"N tools across M servers. **K% of reconstructed task-attack pairs are un-isolatable.** Any
> plan-time isolation defence - tool filter, capability policy - fails on at least this fraction here.
> Coverage: C% of tools classified."*

**Success is not shipping the number.** Success is Phase 1 passing. If it does not, the correct
outcome is a documented negative result and no feature.

---

## 1. Phase 0 - Definitions to fix before writing code

### 1.1 Tool effect classification

Classify every tool into exactly one of:

| Class | Definition | Signals |
|---|---|---|
| `READ` | Returns state. No effect observable outside the process after the call | `get_*`, `list_*`, `search_*`, `read_*`, `fetch_*`, `query_*`, `describe_*` |
| `WRITE` | Mutates persistent state, **or** emits anything to a party other than the caller | `send_*`, `post_*`, `create_*`, `update_*`, `delete_*`, `share_*`, `transfer_*`, `execute_*`, `run_*`, `invite_*` |
| `UNKNOWN` | Cannot be determined | Everything else |

**Three rules that decide the edge cases, and they are not arbitrary.**

**Exfiltration is a write.** A tool that *reads* data but transmits it anywhere the caller does not
already control is `WRITE`. `search_web(query)` is `WRITE` if the query string leaves your
perimeter - that is a documented exfiltration channel, not a theoretical one.

**Ambiguity resolves to `WRITE`, never to `READ`.** Misclassifying a write as a read *understates* the
ceiling, which is the failure direction that produces false comfort. Misclassifying a read as a write
overstates it, which is merely conservative.

**`UNKNOWN` is not a third bucket to reason with - it is coverage loss.** Count it, report it, exclude
it from the denominator, and refuse to emit if it dominates. See §4.3.

### 1.2 Un-isolatability

Given a task requiring tool set `T` and an attacker goal requiring tool set `A`:

```
un_isolatable(T, A)  ==  A is a subset of T
                         (every tool the attacker needs is already in T)
```

Both are sets of tool *identities* (server + tool name), not classes. The classification in §1.1 is
used to *generate* plausible attacker goals (§3.2), not to compute the subset test.

### 1.3 The ceiling

```
ceiling = count of pairs where A is a subset of T
          ------------------------------------------
                    count of all (T, A) pairs
```

over the reconstructed task distribution crossed with the generated attacker-goal set.

---

## 2. Phase 1 - VALIDATION GATE. Blocking. Do not build Phase 2 first.

**Why this exists.** The 220x finding used AgentDojo's *published ground-truth* tool sets. Real
configs have none, so Phase 2 must **reconstruct** task tool sets from observed traffic. **If
reconstruction loses the signal, the metric is decoration.** AgentDojo is the only place both versions
exist, which makes it the only place this is checkable.

### 2.1 The experiment

1. Clone `github.com/ethz-spylab/agentdojo`. It ships run traces under `runs/`.
2. For each user task, **reconstruct** its required tool set **from the message traces alone** - the
   sequence of tool calls the agent actually made in the no-defence runs. **Ignore `ground_truth`
   entirely at this step.** This simulates what MCP Shark can see.
3. Recompute un-isolatability using reconstructed sets.
4. Re-run the 2x2 from `background.md` §4, both pipelines.

The reference implementation using ground truth is
[`260805_h7_agentdojo_test.py`](https://github.com/0xchamin/mincha_brain/blob/638ebe9/reports/experiments/260805_h7_agentdojo_test.py).
Change only the source of `T`.

### 2.2 Pass condition

**Pass** if, with reconstructed tool sets, the tool-filter risk ratio remains **≥ 10x** with
chi-square significant at p < 0.01, **and** the no-defence control remains non-significant.

**That second half is not optional.** If reconstruction makes the control significant, you have built
a proxy for "generally attackable" rather than a measure of isolatability, and the metric means
something different from what it claims.

**Fail** if the risk ratio collapses toward 1, or the control becomes significant.

### 2.3 On failure

**Stop. Do not ship a ceiling number.** Write up the negative result: reconstruction from traffic does
not preserve the isolatability signal. That is a genuine finding and it is worth more than a wrong
metric. Options then are richer reconstruction (argument values, not just tool identities) or
abandoning the static-metric framing.

---

## 3. Phase 2 - The measurement

Only after Phase 1 passes.

### 3.1 Tool inventory

Sources, in order of quality:

1. Explicit `tools` arrays in the IDE config entry `[verify: MCP Shark already parses these]`
2. Tools observed in captured traffic `[verify: the SQLite store retains tool names]`
3. A live `tools/list` if the user opts into connecting

**Record which source each tool came from.** A ceiling computed from observed traffic is empirical; one
computed from a declared array is a claim about the config.

### 3.2 Attacker-goal generation

An attacker goal is a **minimal set of tools sufficient to cause a defined harm.** Do not attempt to
enumerate attacker intent. Enumerate **harm-capable tool sets**, which is finite and inspectable.

Start with single-tool goals - every `WRITE` tool is an attacker goal on its own - then add
two-tool chains where a `READ` supplies data to a `WRITE` across servers. **The cross-server case is
where MCP Shark's existing toxic-flow analysis already operates**, and it is the interesting one.

**Keep this list declarative** - a JSON pack, matching the existing 30-pack pattern `[verify]` - so it
is auditable and extensible without code changes.

### 3.3 Task reconstruction

Group captured traffic into sessions; a session's tool-call set is one observed task `T`.

**Two honesty requirements.** Deduplicate before counting, or one heavily-repeated task dominates the
ceiling. And **report the number of distinct tasks** - a ceiling from 4 sessions is noise, and the
output must not look identical to one from 400.

### 3.4 Compute

Cross reconstructed tasks with generated attacker goals, apply §1.2, report §1.3.

---

## 4. Phase 3 - Output

### 4.1 Terminal

```
Isolation ceiling: 31%   (coverage 87%, 142 tasks, 6 servers, 74 tools)

  31% of reconstructed task-attack pairs are un-isolatable: the task's own tools
  already suffice for the attacker's goal. Any plan-time isolation defence - tool
  filter, capability policy - fails on at least this fraction of this config.

  Largest contributors:
    slack.post_message        reachable in 68% of un-isolatable pairs
    drive.share_file          reachable in 41%
    email.send_email          reachable in 33%

  SCOPE: this measures attacks requiring an ACTION. It says nothing about attacks
  whose payoff is text shown to the user - falsified summaries, injected
  disinformation, phishing content. A 0% ceiling does not mean secure.
```

**The scope line is mandatory output, not a docs footnote.** See `background.md` C1.

### 4.2 SARIF

Emit as one result at config level, not per-tool, with the ceiling in `properties`. **Severity must
not scale with the ceiling** - this is a *measurement*, not a finding, and a high ceiling may be
entirely appropriate for a config that genuinely needs those tools. `[verify: SARIF emitter shape]`

### 4.3 Refusal conditions

**Emit no ceiling, and say why, when:**

- Coverage < 60% of tools classified
- Fewer than 20 distinct reconstructed tasks
- No `WRITE` tool identified at all (almost certainly a classification failure, not a safe config)

**A refusal is a valid, useful output.** A number computed from insufficient data is worse than none,
because it will be quoted.

---

## 5. Tests

| Test | Asserts |
|---|---|
| Classification golden set | A fixed table of ~50 real MCP tool names to expected class, including exfiltration cases like `search_web` |
| Subset logic | `A` subset-of `T`, including empty sets and identical sets |
| Ceiling = 0 | Config of only `READ` tools |
| Ceiling = 100% | Every task uses every tool |
| Refusal paths | Each §4.3 condition triggers and explains |
| **Phase 1 regression** | The AgentDojo reconstruction result, checked in, so a change to reconstruction that breaks the signal fails CI |
| Determinism | Same config, same traffic, same number |

**The Phase 1 regression test is the important one.** It is the only thing keeping the metric honest
once the code changes.

---

## 6. Non-goals

- **Not a defence.** This measures; it enforces nothing.
- **Not a safety score.** See C1. Resist any request to render it as a grade.
- **Not attacker-intent modelling.** Harm-capable tool sets only.
- **Not a replacement for toxic-flow analysis.** That asks which combinations are *dangerous*; this
  asks which are *inseparable*. They are siblings and should coexist.
- **Not covering dynamic re-planning.** The measurement assumes a task's tool set is knowable. An agent
  that discovers tools mid-run is out of scope - and it is exactly the case where CaMeL scored 0%
  utility, so the honest position is that plan-time isolation does not apply there at all.

---

## 7. If you publish anything about this

Two sentences that are defensible, and their limits:

**Defensible:** *"We are not aware of prior work computing the isolation ceiling as a static property
of a deployed agent configuration."* One arXiv search plus a full read of the closest survey
([Isolation as a First-Class Principle](https://arxiv.org/abs/2607.12406), which contains no
quantitative metric) found none.

**Not defensible:** *"Nobody has done this."* See `background.md` C4.

**Attribute the underlying finding correctly.** The 220x result is an analysis over AgentDojo's
published artifacts (Debenedetti et al., NeurIPS 2024 Datasets and Benchmarks Track). The 7.5%
tool-filter figure and the 17% observation are theirs. The isolatability analysis is
[claim 178](https://github.com/0xchamin/mincha_brain/blob/638ebe9/brain/claims.md) and is unreviewed.
