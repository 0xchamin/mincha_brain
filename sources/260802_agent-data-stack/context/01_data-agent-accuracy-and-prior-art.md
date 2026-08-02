# Context 01 - Is any of this measured? Data-agent accuracy, and where endorsements came from

> Persona: **fact-checker + synthesizer**. External evidence for gated nodes in `../nodes.md`.
> This file is **not** part of what the source taught - keep it out of `LEARNING.md`'s body and
> cite it from there. See `AGENTS.md` §"Deep research on request".

**Pass:** R1 for this source. **Date:** 2026-08-02. **Requested by:** the user, at ingest.
**Budget used:** 4 searches, 4 fetches (of <= 8 / <= 12). Stopped early: two independent
T2/T3 sources agree on the central question, which is the contract's stop condition.

## What this pass targeted

The source's own gap, recorded as `d4`: **every number it reports is adoption, and its central
thesis is about trustworthiness.** It claims context makes a data agent's answers reliable, reports
40x throughput, and measures correctness nowhere - and `n10` shows the authors know. So the
questions were:

1. Has anyone **measured** whether schema documentation improves data-agent accuracy? (`n1`, `n3`)
2. Has anyone measured **deriving that documentation from the query log** - the source's feedback
   loop? (`n7`)
3. What is the **accuracy ceiling** on the task this agent actually performs? (`d4`, `n9`)
4. Are **endorsements** novel, or prior art? (`n6`)
5. Is there an older name for what the data team's new job is? (`n8`)

I read the brain first. The nearest existing coverage is `brain/topics/rag.md` (claims 65-72, the
maintained-knowledge-layer alternative to retrieval) and claim 88 from S10 (retrieval quality as an
editorial problem). Claim 72 - **maintenance labour as the binding constraint, via Memex 1945** -
turned out to be the hinge, and finding F5 below extends it.

---

## F1 - Documentation improves text-to-SQL accuracy, and the effect is far larger on real warehouses than on benchmarks

**Verdict: `supports` `n1` and `n3`, and upgrades them from assertion to measured** - with an
important qualification the source does not have.

MotherDuck's research team ran the cleanest version of this experiment, comparing a public benchmark
against their own production warehouse:

| Setting | Schema only | + query-pattern descriptions |
|---|---|---|
| **BIRD-Dev** (public benchmark, Gemini 2.5 Flash) | 34.8% | **36.8%** (+2.0pp) |
| BIRD-Dev, schema + sample rows | 42.2% | **44.0%** (+1.8pp) |
| **MDW-AMBIG** (MotherDuck's production warehouse, 2,730+ columns) | 36% | **52%** (+16pp) |
| MDW-AMBIG, schema + sample rows | 42% | **52%** (+10pp) |

> Source: MotherDuck Research, *Query-Log-Informed Schema Descriptions and their Impact on
> Text-to-SQL* - **T2** (first-party engineering research by a warehouse vendor; independent of
> LangChain and Hex, but not disinterested about the proposition "your warehouse metadata matters").

**The eight-fold difference between the benchmark gain and the production gain is the finding**, and
it is the reason S11's experience is credible even though S11 measured nothing. The paper's stated
cause is exactly `n3`'s: benchmark schemas are "small with distinct column names", while the
production warehouse had "much more similar" column names creating disambiguation problems, and
production queries used expressions like `SUM(revenue) FILTER (WHERE item IN (...))` that the
benchmark's simpler syntax never exercises. **Documentation pays where names are ambiguous, which is
where every real company lives and where no public benchmark does.**

Corroborated independently by a preprint on the same question:

- *Synthetic SQL Column Descriptions and Their Impact on Text-to-SQL Performance*
  ([arXiv:2408.04691](https://arxiv.org/abs/2408.04691), BIRD-Bench) - **T3 preprint.** Generated
  column descriptions "consistently enhance text-to-SQL model performance"; GPT-4o rose from
  **0.3013 to 0.3678** execution accuracy with Qwen2-generated descriptions. Its ablation is the
  part that matters here: models gained **over 20%** when given descriptions for **completely
  uninformative column names** - the paper's own version of S11's weak-vs-strong `account_status`
  example, and the direct measured analogue of `n3`.

Two findings in that preprint qualify S11 rather than simply agreeing with it:

- **Descriptions humans judged "superfluous" outperformed manually curated gold descriptions.** The
  models benefit from more detail than annotators think necessary. S11's advice to write rich
  definitions is, if anything, understated.
- **"Models unsurprisingly struggle with columns that exhibit inherent ambiguity, highlighting the
  need for manual expert input."** LLM-generated documentation does not close the gap on the hard
  cases. That is the boundary of F2 below.

---

## F2 - The feedback loop is real, measured, and can be automated further than the source takes it

**Verdict: `refines` `n7`.**

The MotherDuck study did not write its descriptions by hand. It derived them **from the query log**,
by two methods: *query annotation* (an LLM describes how each column is used across sampled
historical queries) and *query pattern mining* (parse queries, build usage profiles tracking "how
frequently an identifier appears, in which SQL clauses, with which other identifiers, and as part of
which expressions"). The +16pp above is the pattern-mining variant. Cost: **~$0.50 per production
warehouse.**

This is `n7`'s claim - *usage is the signal for what to document* - **measured and automated**. S11
runs the same loop with a human in the middle: observability surfaces the gap, the data team writes
the definition. The external evidence says the first draft of that definition can be generated from
the logs for the price of a coffee, which is a concrete improvement available to S11's design today.

It also independently corroborates a **third** party's version of the same instinct: the CorralData
metadata study found **"Common Queries" the single most impactful metadata component (+74.6%)**,
ahead of primary keys (+65.3%). Two unrelated groups found the query log to be the highest-yield
context source. *(CorralData is a vendor blog - **T4/T5**, method not fully published; cited for the
direction it agrees on, not for its percentages.)*

Limits recorded honestly: MotherDuck found **smaller models got worse** with the added context
("overwhelmed processing capacity"), and notes the approach "requires ongoing maintenance as schemas
evolve" - which is claim 72 arriving on schedule.

---

## F3 - The accuracy ceiling on this task, which is the number `d4` is missing

**Verdict: `refines` `n9` and gives `d4` its teeth.**

The task S11's agent performs has a benchmark built specifically for it. **Spider 2.0**
([arXiv:2411.07763](https://arxiv.org/abs/2411.07763), OpenReview) is 632 real-world enterprise
text-to-SQL workflow problems over databases with **over 1,000 columns** (up to 3,000+), on
**BigQuery, Snowflake and DuckDB** - the same warehouse class S11 runs on. **T1/T3** (peer-reviewed
venue; the benchmark itself is the strongest evidence in this note).

At publication the best system, o1-preview, scored **17.0%**, against **91.2%** for the same class of
model on Spider 1.0. The benchmark's own stated diagnosis is worth quoting against `n1`: solving
these problems "frequently requires understanding and searching through **database metadata, dialect
documentation, and even project-level codebases**". **That is S11's five context stores, described
by an independent benchmark as the thing the task requires.** It is the best external support `n2`
receives, and it arrives from a group with no stake in S11's argument.

Current public leaderboard (spider2-sql.github.io, read 2026-08-02):

| Setting | Best public result |
|---|---|
| Spider 2.0-Snow (547 ex., Snowflake) | 96.70% (Genloop Sentinel Agent v2 Pro) |
| Spider 2.0-Lite (547 ex., BigQuery / Snowflake / SQLite) | 76.23% (Tianqiong Data Agent + GLM 5.2) |
| **Spider 2.0-DBT (68 ex., DuckDB + dbt projects)** | **65.6%** (SignalPilot Agent) |

> ⚠️ **Weigh the leaderboard well below the paper.** Entries are **self-reported vendor
> submissions** under heterogeneous scaffolding, and most are commercial data-agent products with an
> interest in the score. Treat the *ordering across settings* as the signal and the absolute numbers
> as ceilings achieved by tuned, purpose-built systems - not as what a general assistant does on
> your warehouse.

The ordering is the finding: **the setting closest to S11's stack - dbt projects - is the hardest,
and the best public system leaves roughly a third of questions wrong.** S11 reports 2,200
conversations a month and no accuracy figure. The external evidence does not say S11's agent is
inaccurate; it says the task has a real and currently binding error rate, that the error rate is
worst in exactly S11's configuration, and that **40x volume at an unmeasured accuracy is a genuinely
open risk, not a rhetorical caveat.**

---

## F4 - Endorsements are prior art, and the prior art already solved the saturation problem

**Verdict: `supports` `n6` on the mechanism, `refines` it on the design.**

Microsoft Power BI has shipped **endorsement** for years, documented at
[learn.microsoft.com](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-endorsement-overview)
(**T1** - official product documentation; page `ms.date` 2025-10-01, updated 2026-04-28). Feature for
feature it is `n6`:

- Endorsed content is "clearly labeled... **given priority in searches**, and sortable in lists" -
  a trust signal that reorders discovery, exactly `n6`'s purpose.
- The stated problem is `n6`'s: organizations "often have large amounts of content available for
  sharing and reuse, and identifying trustworthy, authoritative content can be difficult".
- Certification carries **attribution** - "you can also see who did the certification".

**Where it goes further than S11, and this is the actionable part: Power BI has two tiers, not one.**

| Tier | Who may apply it | Meaning |
|---|---|---|
| **Promotion** | any content owner, or any member with write permission on the workspace | "valuable, worthwhile, and ready for others to use" |
| **Certification** | **only a select group of reviewers defined by the administrator**, and only if an admin has explicitly enabled the feature | "meets the organization's quality standards... reliable, authoritative content" |

`n6`'s own worry is that "if everything is endorsed, the signal stops being useful" - and S11's
answer is a single tier with a hard write-guard, which controls saturation by making endorsement
scarce and therefore slow. **The two-tier design is a better answer to the same problem:** a cheap
self-serve tier absorbs the volume of "this is good, use it", so the expensive tier can stay scarce
without becoming a bottleneck on the data team. S11 has re-derived Certification and not yet
re-derived Promotion.

This does not diminish `n6` - it strengthens it. **The convergence is the evidence:** a hyperscaler's
BI governance feature and a 3-person data team building for an LLM arrived at the same primitive,
independently and years apart, which is a much better argument for trust signals being structurally
necessary than either one alone.

---

## F5 - The cross-domain hop: this is the knowledge acquisition bottleneck, and the data team are knowledge engineers

**Verdict: `refines` `n8`** - it supplies the name and the 45-year-old precedent for the role shift
S11 reports as new.

`n8` says the data team stopped answering questions and started maintaining the context layer. The
field this belongs to is **knowledge engineering**, and the constraint has a name: the **knowledge
acquisition bottleneck**, identified by Edward Feigenbaum (1977; the canonical statement is his 1982
*Knowledge Acquisition: The Bottleneck*, Stanford). The finding then was that expert systems were
limited not by inference but by **eliciting and encoding domain expertise from human experts** - work
Feigenbaum described as acquired "in a very painstaking way that reminds one of cottage industries,
in which individual computer scientists work with individual experts... painstakingly to explicate
heuristics". The role created to do it was the **knowledge engineer**: elicit, interpret, encode.

> 💡 **Knowledge acquisition bottleneck** - the observation that the limiting factor in a
> knowledge-based system is the human labour of extracting expert knowledge and encoding it in a form
> the system can use, not the system's reasoning power.

S11 is that role reappearing with the formalism relaxed. A metric definition in a semantic model and
a workspace guide explaining how GTM defines pipeline are **elicited, interpreted and encoded domain
expertise** - the difference is that the target formalism is now English prose rather than production
rules, which lowers the encoding cost enormously without removing the elicitation cost. Feigenbaum's
bottleneck was *both*, and the LLM only dissolves one of them.

**This is the same shape as claim 72 arriving from a second direction.** Claim 72 records, via S8 and
Bush's Memex (1945), that the binding constraint on a maintained knowledge base is maintenance
labour, and that the LLM's contribution is *economic rather than intellectual*. F5 says the same
thing from the expert-systems literature: the encoding half got cheap, the elicitation half did not.
**Two independent historical precedents, 1945 and 1977, now support that claim.** S11 is what it
looks like when a company pays the bill: three people, full time, forever.

*(Tier: the primary is a Stanford archival source and the 1988 reassessment in Wiley's* Expert
Systems*; treated as **T1** for the historical claim. The application of it to S11 is **this brain's
synthesis** and is labelled as such wherever it appears.)*

---

## F6 - What nobody has measured

**Verdict: `no-evidence`, and it is the honest gap.**

Nothing credible was found that measures whether a **trust signal like endorsement actually improves
an agent's source selection**. F4 establishes that the primitive is widely shipped and independently
re-derived; it establishes nothing about whether an agent given endorsement metadata picks better
sources than one without it. Power BI's documentation describes effects on **human** discovery
(labels, badges, search priority) - a UI affordance, whose transfer to model behaviour is assumed by
everyone and demonstrated by no one.

This is the highest-value open experiment this brain has surfaced on the topic, and it is cheap:
ablate the endorsement flags, hold everything else fixed, measure source-selection accuracy. It is
also precisely the eval `n10` says LangChain has not built yet.

## Confidence assessment

**Assumptions made (no clarifying questions were asked, per the contract):**

- I treated "the LangChain data agent" as functionally a text-to-SQL/analytics agent over a
  warehouse, and therefore took Spider 2.0 and BIRD as the right measurement proxies. The source
  never describes the agent's internals - it is Hex's product - so this is inference from the task,
  not from the implementation. **If the Hex agent is substantially retrieval-over-dashboards rather
  than SQL generation, F3's numbers bound the wrong thing.** F1 and F2 are unaffected; they are about
  schema documentation regardless of what consumes it.
- I read the Spider 2.0 leaderboard as of 2026-08-02. The site's own newsfeed is dated 2025-05-22,
  so leaderboard freshness is uncertain and the entries are unaudited vendor self-reports.
- The MotherDuck production-warehouse benchmark (MDW-AMBIG) is **their own private data**, so its
  +16pp result is not independently reproducible. It is first-party evidence, weighted accordingly.

**Independence calls:**

- MotherDuck, Microsoft, the Spider 2.0 authors and Feigenbaum are all **independent of LangChain and
  of Hex** - no shared authorship, organisation or commercial interest with S11. F1-F5 are therefore
  admissible as genuine second legs.
- MotherDuck and CorralData both **sell into the problem they are describing**. Neither is neutral
  about "metadata matters"; both are independent of *this source*. Recorded, and confidence raised
  only to the extent that they agree with a T3 preprint and a T1 benchmark that have no such stake.

**What I would not claim from this pass:** that S11's stack is accurate (unmeasured, F3), that
endorsements help agents (unmeasured, F6), or that the 40x is wrong (it is unfalsifiable as stated,
`d3`). What the pass does establish is that **the source's central mechanism is real and measured by
others, while the source's own headline number measures something else entirely.**
