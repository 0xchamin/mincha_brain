# Background: the isolation ceiling of an MCP configuration

**Audience: the coding agent implementing this in MCP Shark.** Read this before the
[spec](spec.md). You do not need to read anything else to implement correctly.

**This document is self-contained by contract.** Every fact you need is stated here inline. The links
are **provenance** - they point at the evidence in a public knowledge base so a human, or an agent
with network access, can check any claim. **If you cannot fetch them, proceed anyway; nothing here
depends on following a link.**

**All *evidence* links below are pinned to commit `638ebe9`** of `github.com/0xchamin/mincha_brain`.
That repository is a living document whose notes get rewritten; a pinned link means the sentence you
read is the sentence that was cited.
> **Where this document lives, and why its links look inconsistent.** This file is served from
> **`main`** - or from commit `48e74ca` onward, the commit that introduced it. **Do not construct a
> URL to this file using `638ebe9`; that commit predates the handoff pack and will 404.** The
> evidence links *inside* this document are deliberately pinned to `638ebe9` because that is the
> commit whose wording they cite, and those files all exist there. Two different jobs, two different
> refs: **the pack itself tracks `main` so you always get the current version; its citations are
> frozen so they cannot drift.**

---

## 1. What you are building, in one paragraph

MCP Shark will compute a new number about an MCP configuration: **the fraction of that config's
plausible work on which no plan-time isolation defence can help.** A "plan-time isolation defence"
restricts an agent to the tools its task needs, decided *before* the agent reads any untrusted data.
It is the best-performing cheap defence known. It has one failure condition: **when the tools the
user's task legitimately needs are already sufficient to carry out an attacker's goal, there is
nothing to take away.** That condition is a property of the tool surface, so it can be measured
statically, ahead of choosing any defence. Nobody currently measures it.

---

## 2. Why this matters: the threat, in the minimum detail you need

**Indirect prompt injection.** An LLM agent reads content it did not author - a web page, an email, a
file, **a tool result**. That content arrives in the same context window as its instructions, and the
model has no mechanism to tell data from instructions. An attacker therefore does not need access to
your system. They place text where your agent will read it, and your own application fetches it.

> Source: Greshake et al. 2023, *"Not what you've signed up for"*. Its framing: **"processing
> untrusted retrieved data would be analogous to executing arbitrary code."** Demonstrated on real
> products including Bing Chat and GitHub Copilot.
> [Full note](https://github.com/0xchamin/mincha_brain/blob/638ebe9/sources/260804_indirect-prompt-injection/LEARNING.md)

**Why MCP specifically.** MCP is a protocol for pulling tool output into an agent's context. Tool
results *are* the untrusted channel. This is not a peripheral concern for MCP tooling; it is the
central one.

**One finding worth internalising because it will shape your instincts.** Attack success is a
property of **the application, not the model**. Holding the model fixed, measured attack success ran
from ~92% on one task suite to 0% on another, predicted by *how much of the tool output an attacker
controls* and *how many independent malicious steps must chain*. Both are decided by which tools an
agent is given - which is exactly the surface MCP Shark already inspects.

---

## 3. The defence landscape, and where this metric sits

Defences against prompt injection sort into three classes by **what they ask of the model**. All
three have measured failure modes.

| Class | What it does | Examples | How it fails |
|---|---|---|---|
| **Detection** | Classifies input as malicious | PIGuard, PromptArmor, ProtectAI, BERT classifiers | **Structural.** Misses payloads that look legitimate; blocks instructions that *are* legitimate. Retraining made the strongest detector **worse** |
| **Behavioural** | Marks provenance, asks the model to honour it | Spotlighting, delimiters, instruction hierarchies | No guarantee - the decision stays inside the untrusted component. Measured at 27.6% attack success on a real agent |
| **Structural / plan-time isolation** | Constrains what the agent *may do*, whatever it believes | **Tool filters**, CaMeL capability policies | **This metric's subject.** Bounded by tasks whose own tools suffice for the attack |

**MCP Shark today is a detection-class tool** - 41 pattern rules. That class has a documented ceiling,
which is *why* this metric is interesting: it is a move into the structural class's territory,
measuring rather than enforcing.

**Two facts about the structural class you must not lose:**

**It is the best cheap defence known.** A simple tool filter dropped targeted attack success to
**7.5%** while keeping benign utility high, beating a BERT detector that matched it at roughly
**thirty points** of utility cost.
[Evidence](https://github.com/0xchamin/mincha_brain/blob/638ebe9/sources/260805_agentdojo/LEARNING.md)

**And it collapses when the plan cannot be written in advance.** An independent evaluation found
CaMeL - the most sophisticated defence of this class - scoring **0.00% utility and 0.00% attack
success** on open-ended dynamic tasks, because it writes a static program before execution. Perfect
security by accomplishing nothing. The same paper found tool filters "suffer significant
over-defense" on such tasks, blocking tools needed later because they looked unnecessary at plan time.
[Research note](https://github.com/0xchamin/mincha_brain/blob/638ebe9/sources/260804_camel-prompt-injection-defense/context/01_independent-evaluation-and-the-2026-defence-landscape.md)

---

## 4. The finding this is built on, and its numbers

A (user task, attacker goal) pair is **un-isolatable** when the attacker's required tools are a
**subset** of the user task's required tools. The filter has nothing to remove without breaking the
task.

Measured over **547** mappable pairs from the AgentDojo benchmark, using its published run data:

| Pipeline | un-isolatable pairs | isolatable pairs | risk ratio | chi-square (df=1) |
|---|---|---|---|---|
| **No defence** (control) | 50.7% attacked | 47.9% attacked | **1.1x** | **0.2** - not significant |
| **Tool filter** | **46.7% attacked** | **0.2% attacked** | **220x** | **227.2**, p << 0.001 |

**35 of the 36 attacks that survived the tool filter were un-isolatable pairs.**

**The control row is the important one.** Un-isolatability predicts *nothing* about attack success
when there is no defence. It becomes almost totally determinative once the defence is applied. That is
what makes it a mechanism rather than a correlation, and it is why the number is worth computing
*before* choosing a defence.

> Reproducible in one file, no model calls:
> [`260805_h7_agentdojo_test.py`](https://github.com/0xchamin/mincha_brain/blob/638ebe9/reports/experiments/260805_h7_agentdojo_test.py)
> Recorded as **claim 178**:
> [claims.md](https://github.com/0xchamin/mincha_brain/blob/638ebe9/brain/claims.md)

---

## 5. Hard constraints. Violating these ships a misleading number.

**C1 - This measures the *action* half of the threat only.** Isolation defences constrain what an
agent may *do*. They do nothing against attacks whose entire payoff is **text shown to the user** -
a falsified summary, injected disinformation, a phishing line in the answer. CaMeL's authors list
these as explicit non-goals. **A config can score 0% un-isolatable and still be exploitable.** Any
output must say so. Never let this number be read as "secure".

**C2 - The finding used ground-truth tool sets that no real deployment has.** AgentDojo *publishes*
each task's required tools. An MCP config does not. **The entire product risk lives here**, and it is
why the spec's Phase 1 is a blocking gate rather than a step.

**C3 - Report coverage or refuse to emit.** The measurement inherits MCP Shark's existing stated
limitation: toxic-flow heuristics depend on tool-name classification quality, and tool-level rules
only apply when server entries include explicit `tools` arrays. A ceiling computed over 20% of a
config's tools is not a ceiling. Emit coverage alongside every number, and refuse below a threshold.

**C4 - Do not claim novelty beyond what was checked.** One arXiv search plus a full read of the
closest survey found no prior work computing this as a static property of a deployed configuration.
That is a bounded clearance, not a literature review. The defensible sentence is *"we are not aware of
prior work measuring this"*, never *"nobody has done this"*.

---

## 6. What MCP Shark already has

Four of the five pieces exist. This is the argument for building it here rather than anywhere else.

| Piece | Status |
|---|---|
| Static config parsing across 15 IDEs | **Exists** |
| Cross-server capability pairing (toxic-flow analysis) | **Exists** - the sibling of this metric. It asks which tool combinations are *dangerous*; this asks which are *inseparable* |
| A traffic store (SQLite, JSON-RPC frames) | **Exists** - and it is the route to Phase 1, because it is where real task tool sets can be reconstructed |
| SARIF output and a GitHub Action | **Exists** - so the number lands in CI and a config change can regress it |
| Read/write tool classification + the counting function | **This is the new work** |

---

## 7. Vocabulary

| Term | Meaning here |
|---|---|
| **Plan-time isolation** | Any defence that fixes the agent's permitted tools from an initial plan, before untrusted data is read. Tool filters, CaMeL policies |
| **Un-isolatable pair** | A (task, attacker goal) pair where the attacker's required tools are a subset of the task's. The defence has nothing to remove |
| **Isolation ceiling** | The fraction of a config's task distribution that is un-isolatable. The best any plan-time defence can do is fail on at least this much |
| **Read-like / write-like tool** | Read-like returns state with no external effect. Write-like mutates state or emits externally - send, post, transfer, delete, execute, share |
| **Coverage** | Fraction of a config's tools that could be classified at all. Reported with every ceiling |
| **Over-defence** | Blocking legitimate work to block attacks. The failure mode a single security score hides, and the one that killed CaMeL on open-ended tasks |

---

## 8. What is NOT established, stated plainly

Do not let the implementation imply more confidence than exists.

- **The 220x result is a third party's data analysed by one person, unreviewed.** The data is
  peer-reviewed (NeurIPS 2024 Datasets and Benchmarks Track) and open source. The analysis is not.
- **One model, one attack type, 87% pair coverage** (82 of 629 pairs skipped where ground truth would
  not parse statically).
- **Whether an approximated tool set preserves the signal is unknown.** That is Phase 1.
- **The metric has never been computed on a real MCP config**, only on a benchmark.
- **No claim is made that a low ceiling means a config is safe.** See C1.

---

## 9. If you want the full chain of reasoning

The decision report, with evidence grades, prior-art assessment and what would kill the idea:
[`260805_isolation-ceiling-of-an-mcp-config.md`](https://github.com/0xchamin/mincha_brain/blob/638ebe9/reports/260805_isolation-ceiling-of-an-mcp-config.md)

The topic note it draws on, covering the threat model, all three defence classes and their measured
failures:
[`agent-security.md`](https://github.com/0xchamin/mincha_brain/blob/638ebe9/brain/topics/agent-security.md)

**Now read [spec.md](spec.md).**
