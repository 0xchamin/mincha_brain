# Learning - Building Closed-Loop Evals for a Multimodal Agent at Scale

> Persona: **curator** + **mentor, always**. Re-adopt when working this file.

> The distilled document you learn from - text anchored by a few curated visuals. Built from the
> corroborated nodes in `nodes.md`. Every claim is cited. Signal, not archive. See `SOURCE.md`.

> **Two kinds of material, kept visually distinct.** Claims from the talk carry a node ID (`n3`) and
> a timestamp. Blocks marked **"Background, supplied"** are context *I* am adding - established prior
> art the source assumes or never names. They are uncited by construction and are not evidence about
> this source.

## TL;DR

Uber's Computer Vision team runs a multimodal agent that enhances low-quality food photos for Uber
Eats. **The transferable lesson is not about food - it is a blueprint for evaluating an agent
pipeline in production.** Log every trace first, because nothing else is possible without it. Then
stop asking "is the agent good?" and instead evaluate **each stage with the metric that fits its
job**: a router is a classifier judged on recall, a generator is judged on pass@k, an editor is
judged by comparison against its own input. Stack the gates so their holes do not line up, then
close the loop - sample production traffic, re-label it, and let the system rewrite its own configs
as the world drifts. `https://www.youtube.com/watch?v=31GUkCBD-Uc`

## The 1-minute version

This article covers a production image pipeline at Uber Eats and the eval design wrapped around it.
A multimodal agent takes a merchant's poor food photograph and enhances it for the menu. The
enhancement itself is not the interesting part, and you can safely forget the food entirely. What is
worth carrying away is the answer to a question every team shipping an agent eventually hits, which
is what you actually measure when the thing you built is not a function.

The problem is that this system cannot be checked the way software is normally checked. It is
non-deterministic, so the same photograph run twice does not give the same result twice. Its output
is an image, and no correct image exists anywhere to compare against. Part of the quality bar is
frankly subjective, because "does this look appetising, and does it still look like that
restaurant's food?" has no stored answer. And what you are defending against is not a regression in
your code at all. It is drift in the world outside it.

Take those four properties together and you can see why the usual instinct fails. A test suite
asserts a known answer and returns green or red, and here there is no known answer, no stable input
distribution, and no commit that caused the problem. Worse, the failure you most need to catch is
one nobody introduced. The dishes change, the phone cameras change, and eater expectations change,
so a system that was correct on launch day quietly stops being correct without anything in the
repository moving. Given all that, the obvious first move is to score the whole thing.

That obvious move is to run a batch of images through the pipeline, ask a judge "is this good?", and
watch the number. It collapses for a reason that sounds minor and is not. The score tells you that
quality dropped and never tells you where, and a pipeline has several places it could have gone
wrong. So you learn that something is broken on the same day you learn you cannot act on it, which
is the difference between an eval and a dashboard. The single number also becomes a target the
system can satisfy without doing its job, a problem returned to at the end. Both failures point at
the same missing idea.

The idea is to stop attaching a metric to the system and attach metrics to its **decision points**
instead. The pipeline is not one agent but a routed chain of small single-purpose ones, and within
it there are exactly three places where it commits to something it could have done differently
(`n2`). It decides whether to enhance an image at all. It decides whether a generated image passes
QA or goes back for another attempt. It decides whether the finished image is fit to publish. Each
of those decisions fails in a different way, which is precisely why one number cannot describe them,
and it is also what tells you which metric each one needs.

Work through them in order and three different eval shapes fall out. Routing is a classification, so
it is measured like one, with a confusion matrix, and **recall** is the guardrail because a recall
miss puts a hallucinated dish on a live menu while a precision miss only wastes compute (`n3`-`n5`).
Generation has no correct answer to compare against, so instead the QA gate is made to **explain**
why it failed, that explanation rewrites the prompt, and what gets measured is the retry curve, or
pass@k (`n9`). Editing turns out to be the easiest of the three once you notice that an edit already
has a free reference, namely its own input, so it is evaluated by comparing output against input and
asking whether anything regressed (`n10`). Around all three, the gates are stacked so their holes do
not line up, and a scheduled loop re-labels sampled production traffic and rewrites the agents'
configs as the world drifts (`n7`). None of this is free.

The bill arrives in two parts. Everything above is computed from what the system did, so a single
flat end-to-end trace has to exist before any of it, and the talk is blunt that without it you have
nothing to optimise for at all (`n1`). Then there is the recurring cost, which is humans re-labelling
sampled production traffic on a cadence, and it is the one part of the design with no automation
story behind it. There is also a subtler cost that only shows up once the loop is running. A
feedback loop improves what it measures rather than what you meant, and the talk's own example is an
agent discovering that **blandness passes a faithfulness gate** and oversteering into generic output
(`n15`). Knowing what it costs still leaves the question of how much of this to believe.

Not as much as its confidence suggests, and the reason is not that anything looks wrong. It is one
team, in one domain, and **nothing in the talk is measured**. There are no pass@k values, no
precision or recall figures, and no before-and-after on the auto-tuning loop. The talk describes a
system and never reports its performance. What generalises is the *shape* of each eval, because each
shape is derived from a property of the stage rather than from anything about food. The thresholds,
the ordering and the claim that this is how it should be done are one team's practice.

The same argument, compressed for reference rather than for reading:

| | |
|---|---|
| **The problem** | The system is non-deterministic, its output is an image with no correct answer, the quality bar is partly subjective, and what you are defending against is **drift in the world** rather than a regression in your code. A test suite cannot express any of that. |
| **Why the obvious answer fails** | One end-to-end "is it good?" score tells you quality dropped and never *where*. That is the difference between an eval you can act on and a number you watch. |
| **The idea** | **Attach metrics to decision points, not to the system.** The pipeline has three places where it commits to something it could have done differently, and each fails differently (`n2`). |
| **How it works** | A router is a **classifier** - confusion matrix, and **recall** is the guardrail because a recall miss is unrecoverable (`n3`-`n5`). Generation has no correct answer, so make the QA gate **explain itself** and measure the **retry curve**, pass@k (`n9`). An edit has a free reference - **compare against the input**, and ask "did anything regress?" (`n10`). |
| **What it costs** | A flat end-to-end trace before anything else, or none of it is possible (`n1`). Then ongoing human re-labelling of sampled production traffic on a cadence - the one part of the design with no automation story. |
| **What breaks in production** | The world drifts, so the loop re-labels and auto-tunes, anchored by a golden set as its setpoint (`n7`). And the loop optimises what it measures: the agent learns that **blandness passes a faithfulness gate** (`n15`). |
| **How far to trust it** | **One team, one domain, nothing measured.** The talk describes a system; it never reports its performance. The eval *shapes* generalise; the thresholds and ordering are one team's practice. |

## Key claims

- Log the full flat trace **before** anything else - "if you don't start with it, you have nothing to
  optimize for, let alone set up a self-learning loop." `n1` `&t=418s`
- An agent product is a **routed pipeline of small agents**, each independently evaluable. `n2`
  `&t=376s`
- Eval a **router as a classifier** (confusion matrix, precision/recall); the guardrail metric is
  **recall**. `n3` `n4` `&t=459s` `&t=578s`
- **Generation evals are iterative**: QA explains why it failed, that reasoning rewrites the prompt,
  retry; measure **pass@k**. `n9` `&t=850s`
- **Editing tasks are evaluated by comparison, not by score** - output against input. `n10` `&t=896s`
- Stack QA gates as a **Swiss-cheese model**. `n11` `&t=1082s`
- Close the loop: sample prod traffic, re-label, diagnose, auto-tune, benchmark, ship - config-driven,
  no human editing prompts. `n7` `&t=650s`
- Layer **three feedback loops** on three different clocks. `n12` `&t=1103s`

## What you will learn, and in what order

```mermaid
flowchart TB
    subgraph A["A. Why this problem needs an agent at all"]
        S1["1 - Unlearn 'eval'<br/>as a test suite"]
        S2["2 - The constraints<br/>that rule out rules"]
    end
    subgraph B["B. The system under test"]
        S3["3 - A routed pipeline<br/>of small agents"]
        S4["4 - The flat trace,<br/>before anything else"]
    end
    subgraph C["C. One metric per stage, because each fails differently"]
        S5["5 - Router<br/>= classifier, recall"]
        S6["6 - Generation<br/>= pass@k retry curve"]
        S7["7 - Editing<br/>= pairwise comparison"]
    end
    subgraph D["D. Surviving production"]
        S8["8 - Stack the gates<br/>Swiss cheese"]
        S9["9 - Close the loop<br/>auto-tune on drift"]
        S10["10 - Three loops,<br/>three clocks"]
        S11["11 - Reward hacking<br/>the failure to expect"]
    end
    A --> B --> C --> D
    S1 --- S2
    S3 --- S4
    S5 --- S6 --- S7
    S8 --- S9 --- S10 --- S11

    style C fill:#e8f0fc
    style D fill:#fbf1dc
```

Read the diagram top to bottom, in the order of the argument, and treat every box as a numbered
section below. The boxes are gathered into four movements, and the two coloured ones are the two you
should not skim. Blue marks the core technique, which is the single idea the talk exists to deliver.
Amber marks what nobody tells you until you have shipped, meaning the parts that only start to matter
once the system is live and the world begins moving under it. **The crux is that sections 5, 6 and 7
are three different answers to the same question, and which one you need depends on what the stage
does rather than on what the pipeline does.**

Movements A and B do no eval work at all, which makes them look skippable, and for an experienced
reader they largely are. Their job is to establish two things the rest depends on. First, that a test
suite cannot express this problem, so the word "eval" has to be held far more loosely than instinct
allows. Second, that the architecture has identifiable decision points, because a metric has to
attach to something. If you already build agent pipelines for a living you can move through both
quickly. What it costs you is section 2's argument that the eval strategy and the architecture are
one decision rather than two, which is what makes everything after it feel forced rather than chosen.

Movement C is the payload, and it is deliberately not written as a menu of three techniques. Each
section asks what the previous stage's metric structurally cannot measure, and the answer names the
next shape. Recall works for the router because a human could have written down the right answer.
Nobody can write down the correct enhanced photograph, so section 6 has to abandon labels entirely
and measure the feedback loop instead. Section 7 then notices that an editing task quietly restores
a reference the generation framing had given up on. Skim these three and you will still know what
Uber built, but you will have the topology rather than the judgement, and the judgement is the part
that transfers to a pipeline that is not this one.

Movement D is where most teams' understanding stops short, and the reason is structural rather than
educational. None of it is discoverable from a design document, only from having operated something
for a few months. It is also where the note turns on its own subject, because section 11 shows the
agent defeating the very gate section 6 built. **If you read only two sections, read section 5 and
section 11.** The arrows between groups are strict in both directions: C makes no sense without B's
decision points, and D is entirely about defending what C measures.

*Synthesized roadmap of this note - not from the source.*

## 1. First, unlearn "eval" as a test suite

The word carries the wrong instinct, and getting it wrong at the start makes everything after it
look arbitrary.

A test suite asserts a known-correct answer, runs on every commit, and comes back green or red.
Almost nothing in this talk works like that. To see why, take the properties of the system under
test one at a time. It is **non-deterministic**, so running the same photograph twice does not give
you the same result twice. Its output is an **image**, and no correct image exists to compare
against. The quality bar is partly **subjective**, because "does this look appetising, and does it
still look like *that* restaurant's food?" has no stored answer. And the thing you are defending
against is not a regression in your code but **drift in the world**. Hold "eval" loosely enough to
cover a classifier metric, a retry-until-pass rate, a human comparison, and a scheduled job that
rewrites a prompt, because all four are coming.

> **Background, supplied.** The closest established discipline is not software testing but
> **statistical quality control**. You are sampling a stream, estimating a rate, and acting on the
> estimate, rather than proving a property. That framing explains why every technique below produces
> a *number over a population* rather than a verdict on a case, and why "we ran it and it looked
> good" is not evidence here.

Which raises the question this whole talk is an answer to. If you cannot assert correctness, and one
overall quality score would only tell you that something got worse without telling you where, **what
exactly do you attach a metric to?** The answer turns out to be a consequence of the architecture,
and the architecture is a consequence of the problem, so start there.

## 2. The constraints that rule out rules

Small merchants do not have good food photography, and Uber Eats wants better photos on menus. That
sounds like a straightforward image-enhancement job right up until you add the constraint that
shapes everything else, which is that **eaters distrust anything that looks AI-generated.** So an
edit must stay **faithful** to the actual dish and preserve each restaurant's **brand**. It must
also avoid **sameness**, because one prompt applied to every photo would make the whole marketplace
look identical, and that is a business problem rather than an aesthetic one `&t=169s`.

![Slide showing the goals: authenticity, ship safely, scale](visuals/frame_222.jpg)

- What it teaches: the three goals that bound the design - **authenticity**, **ship safely**, and
  **scale**. Each one rules out an otherwise obvious approach. `n14` `&t=251s`
- Corroborated by: the narration framing the design space as a spectrum and naming the same three
  goals. `&t=251s`

At first glance the design space has two obvious ends, and those three goals close off both. Start
with a deterministic rules engine, which is controllable and predictable and therefore serves *ship
safely* very well. It is also brittle, and it will not survive every dish, cuisine and lighting
condition it meets, so it fails *scale*. Suppose instead you go to the other end and build a fully
agentic system, which is creative and high-agency and serves *scale*. Pointed unconstrained at a
live marketplace it fails *ship safely*, and it is exactly the thing that produces the AI-looking
output that fails *authenticity*. What is left is the **guardrailed middle** (`n14`, `&t=251s`).

**And that middle is the reason this is a talk about evals at all.** A rules engine does not need
evals, it needs tests, because its behaviour is enumerable in advance. A fully autonomous agent
cannot be made safe by evals either, because measuring after the fact does not constrain action.
Only the guardrailed middle both *needs* measurement and *can be improved by* it. **The architecture
and the eval strategy are therefore one design decision, not two**, which is why the next thing to
look at is the architecture.

## 3. The system under test is a pipeline, not an agent

![Input -> Image Quality Understanding -> Routing -> Prompting -> Generation -> LLM QA -> Post-Processing -> Publish-Ready QA -> Menu Output, with Retry and Logging/Traces](visuals/frame_1058.jpg)

- What it teaches: the agent "product" is a **pipeline of small, single-purpose agents** - quality
  understanding, routing, prompt generation, generation, LLM QA, post-processing, publish-ready QA -
  each with its own job and its own eval. `n2` `&t=314s`
- Corroborated by: "all of the agents in this end-to-end orchestration is ... basically a flat
  structure in this JSON ... anyone ... can dive in to diagnose." `&t=397s`

Resist reading that as a list of components, and look instead at **where the decisions are**. There
is a routing decision, which is whether to enhance this image or leave it alone. There is a QA
decision, which is whether to publish or retry. And there is a final publish decision. In other
words there are three places where the system commits to something it could have done differently,
and **each one fails in a different way**, which is precisely why no single number can describe the
whole.

That is the answer to the question section 1 left open. **You attach metrics to decision points, and
every decision point is an eval boundary.** The rest of this note is what to attach at each one.

> **Background, supplied.** Splitting a system this way is the **decomposition** move that classical
> ML pipelines made decades ago and that end-to-end deep learning spent a decade arguing against. The
> trade is well understood. An end-to-end system can find solutions a decomposed one cannot, but a
> decomposed one is **attributable**, so when quality drops you can localise the stage. Here
> attribution wins, and it wins because the system has to be *operated* rather than merely trained.

> Independently, S2 ([12-factor agents](../260725_12-factor-agents/LEARNING.md)) reaches the same
> shape from first principles rather than from production: small scoped LLM steps inside otherwise
> deterministic software. Two sources converging from opposite directions is why this is the
> best-supported claim in this brain ([`brain/claims.md`](../../brain/claims.md) claim 11).

Knowing where to measure is not yet being able to measure, though. Every metric below is computed
from what the system did, which means something must have recorded it, and the talk is emphatic that
this comes first.

## 4. Nothing works until the trace does

Every stage writes to **one flat end-to-end trace**. Not nested per-agent logs, but a single JSON
structure anyone can open and read top to bottom. The justification is blunt - "if you don't start
with it, you have nothing to optimize for, let alone set up a self-learning loop" (`n1`, `&t=418s`).

The word doing the work is **flat**, and the reason is that the questions you will ask cross stages.
For example, this image came out badly, and you want to know whether it was routed wrong, prompted
wrong, or generated wrong. Per-agent logs answer each part separately and leave you stitching
timestamps together. One flat record makes the whole journey legible in a single read. Notice this is
also what makes section 3's attribution argument real rather than theoretical, because a decomposed
architecture only buys you localisation if the evidence arrives already correlated.

> **Background, supplied.** In ordinary distributed systems this is the distinction between **logs**
> and **traces**. Logs are per-service events, whereas a trace is one request's whole path under a
> shared correlation ID. The idea is old and the tooling is mature. What is new here is the
> *consumer*, because this trace is not only for a human debugging an incident. It is the **training
> input for the auto-tuning loop** in section 9. That is why "log first" is an ordering claim and not
> an instrumentation preference: **the loop cannot exist before its data does.**

With the trace in place, work through the decision points in order. The first one is routing, and it
is the friendliest of the three, because it is the only stage where the right answer is a label a
human could have written down.

## 5. A router is a classifier, so measure it like one

The first stage decides whether to enhance an image or leave it alone. That is a classification, and
classification has been measured the same way for decades. You build a **confusion matrix** and read
**precision and recall** off it (`n3`, `&t=459s`). A router with more than two branches is no
different in kind, since it simply becomes an **n x n** matrix with one cell per branch.

> **Background, supplied - the fundamentals, since the rest of this section rests on them.** A
> confusion matrix cross-tabulates what the classifier said against what was actually true. From it
> you read two numbers. **Precision** asks what share of the things you flagged should have been
> flagged, which is to say how much of your action was wasted. **Recall** asks what share of the
> things that should have been flagged you actually caught, which is to say how much you missed. The
> two trade off, and trivially so, because you can catch everything by flagging everything at zero
> precision. Classical statistics names the two errors **Type I** (false positive) and **Type II**
> (false negative), and the entire discipline exists because **the two errors almost never cost the
> same.** So the engineering question is never "which is more accurate". It is **"which error can I
> afford"**.

Ask that question here and the asymmetry is stark.

![Routing Failures: Precision Miss - a high-quality cheeseburger scored "below bar" and sent for needless enhancement](visuals/frame_583.jpg)

- What it teaches: a **precision miss** over-processes a good input - you pay compute for zero
  quality lift and risk degrading a photo that was already fine. A **recall miss** approves a bad
  input, and downstream the generation model may **hallucinate to match the description**, inventing
  two extra chicken wings that are not in the dish. `n5` `&t=588s`
- Corroborated by: "you pay the compute cost for a zero quality lift ... and there is a risk of
  degrading this image." `&t=595s`

One failure wastes money. The other puts a fabricated dish on a live menu, which is the authenticity
goal from section 2 failing in the most visible way available. **So recall is the guardrail**, and
you optimise so that no bad image slips through (`n4`, `&t=578s`).

> **The transferable rule, and it is not about food:** choose the guardrail metric by asking which
> failure is *unrecoverable*, not which is more frequent. Wasted compute is recoverable. A
> hallucination that reached a customer is not.

All of which assumes you can say what "bad" means. That comes from a **golden dataset**, which is
human labels used as the source of truth over a set representative across geography, dish type and
quality, with **objective guidelines** written to strip subjective variation between labellers
(`n6`, `&t=528s`). ⚠️ `single-leg` - narration only, no slide captured, so read the practice as
reported rather than demonstrated. Hold onto the golden set, because it becomes load-bearing again
in section 9 for a reason nobody expects.

> **Background, supplied.** "Objective guidelines to strip bias" is the standard remedy for weak
> **inter-annotator agreement**, the well-studied problem that two competent people given the same
> item and a loose rubric will disagree. That disagreement puts a hard ceiling on any metric computed
> from their labels. The talk names the remedy and never mentions measuring the agreement, which is
> the usual way you discover whether the remedy worked.

Routing was tractable because a human could write down the right answer. The next stage is where that
stops being true.

## 6. When there is no correct answer, measure the retry curve

Nobody can write down the correct enhanced photograph. There is no label to compare against, so
precision and recall have nothing to attach to, and the technique from section 5 simply does not
transfer. What the talk does instead is make the QA gate **explain itself**, and then turn the
explanation into the next attempt.

![Sweet potato fries: iteration 1 QA-fail (portion / plating) -> iteration 2 QA-pass](visuals/frame_850.jpg)

- What it teaches: a multi-dimensional QA gate (plating, faithfulness, colours) fails the first
  attempt **with reasons**; those reasons are folded back into a rewritten prompt; the retry passes.
  The metric is **pass@k** - the pass rate by the k-th attempt. `n9` `&t=850s`
- Corroborated by: "we take that feedback in, go for the second iteration, and we're actually able to
  pass it ... the metric we are measuring here is pass at K." `&t=858s`

> 💡 **pass@k** - the share of cases that succeed within *k* attempts.

> **Background, supplied, and it changes what the number means.** pass@k comes from **code
> generation** benchmarking, where it measures *independent* samples. You draw k completions and pass
> if any one of them compiles and passes the tests. There, k is measuring the model's **diversity**,
> because you are buying attempts and hoping one lands. Uber's usage differs in a way the talk never
> flags, since **each attempt is conditioned on why the last one failed**. The curve therefore
> measures the **feedback loop's** effectiveness rather than the model's spread. Two consequences
> follow. A rising curve here is evidence the QA reasoning is *useful*, which the
> independent-sampling version cannot tell you. And the two numbers are **not comparable**, so never
> benchmark this pass@k against a published one.

That distinction is not pedantry, because it dictates the wiring. The retry has to re-enter at
**prompt generation** rather than at generation, and the QA gate has to emit a *reason* rather than a
verdict. A boolean gives the retry nothing to condition on, and you are back to re-rolling dice while
calling it a feedback loop.

So generation gets a metric. But look again at what this system actually does to an image, because it
does not create one, it **edits** one, and an edit has a reference that a creation never has.

## 7. An edit has a free reference: its own input

This is the eval shape most teams miss, and it exists only because the task is transformation rather
than generation.

![Generation Evals: Pairwise Comparison - is the output better than the input, faithful, complete, natural, and did anything regress?](visuals/frame_890.jpg)

- What it teaches: evaluate an edit by **comparing output against input** - is it better? faithful?
  complete? natural? **did anything regress?** - answered yes / no / **unsure**. `n10` `&t=896s`
- Corroborated by: the narration walking the same comparison dimensions. `&t=896s`

Two details carry the whole idea, and both are easy to read past. The first is that **"did anything
regress?" is a question absolute scoring cannot ask**. A 7-out-of-10 tells you nothing about whether
the plating improved while the colour got worse, and regressions are exactly what an editing pipeline
must not ship. The second is the **"unsure" option**, which matters more than it looks. Forcing a
binary out of a judge that genuinely cannot tell manufactures confidence you do not have, and those
undecided cases are precisely the ones worth a human's attention.

> **Background, supplied.** Preferring comparison to absolute scoring is one of the most reliable
> findings in evaluation generally, because humans and models are both **poorly calibrated on
> absolute scales** and drift over a session, while staying far more consistent on "is A better than
> B". It is why **RLHF** trains on pairwise preferences rather than scalar ratings, why chatbot
> leaderboards run pairwise battles with **Elo**-style ratings, and why the **Bradley-Terry** model
> exists to convert pairwise wins into a ranking. What Uber adds is the observation that on an
> editing task you do not need a second candidate to compare against, because **the input is already
> there, and it is free.**

Sections 5 to 7 complete the core technique, which is three decision points, three failure modes, and
three metrics chosen to match. That is the transferable payload, and if the world held still it would
be enough. The rest of this note is about the fact that it does not.

## 8. Gates leak, so stack them

Return to the architecture in section 3 and count the QA gates. There are **two**, an LLM QA gate
immediately after generation and a separate **publish-ready QA** near the end (`n11`, `&t=1062s`).

That duplication is deliberate. It is the **Swiss-cheese model**, in which every gate has holes, but
if the holes sit in different places then very little passes through all of them.

> **Background, supplied.** The Swiss-cheese model is **James Reason's** (1990), from organisational
> accident analysis, and it is the standard framing in aviation and clinical safety. Its real content
> is a warning as much as a technique, because the layers must fail **independently**. Barriers that
> share a cause have their holes already aligned, and the stack is then no stronger than one layer
> while looking considerably stronger. That shared cause might be the same bad assumption, the same
> training data, or **the same judge model with a different prompt**. **The talk does not raise
> this**, and it is the first question to ask of any two-gate design.

The second gate earns its place in a way worth stealing regardless. Being holistic and late, it
catches what upstream missed **and indicates what upstream should have caught**. A late gate that
only blocks bad output is a filter, whereas one that attributes the miss is a diagnostic, and
attribution is the raw material for everything in the next section.

## 9. The world moves, so the system has to tune itself

Everything so far produces a system that is good on the day you ship it. What happens on day ninety,
when the dishes, the cameras and the expectations have all moved?

![Routing: Online Tuning Focused on Drift - live traffic feeds Routing/Verify/Diagnose+Tune/Benchmark/Ship, re-running on fresh production traffic](visuals/frame_658.jpg)

- What it teaches: sample live production traffic, **re-label it with the same objective guidelines**,
  diagnose which agent is drifting, **auto-tune its config**, benchmark against the golden set, ship
  a new version - then run it again on fresher traffic. `n7` `&t=650s`
- Corroborated by: "this is completely config driven and doesn't require human in the loop ... this
  is what will keep your model sharp over time." `&t=705s`

> **Background, supplied - because "drift" hides two different problems.** **Data drift** is the
> input distribution moving, so new cuisines, new phone cameras and seasonal dishes. **Concept
> drift** is the *relationship* moving, so what counts as an acceptable photo changes because eater
> expectations changed, while the inputs look much the same. The first is detectable by watching
> inputs alone. **The second is visible only through fresh labels.** That the loop re-labels sampled
> production traffic rather than merely monitoring distributions tells you which threat it is built
> for, though the talk never separates the two.

Two mechanisms make this more than a diagram, and both are `single-leg` - narration only, no slide
captured, so read them as reported rather than demonstrated.

The first is that the **auto-tuner is itself two agents** (`n8`, `&t=732s`). A **reflect** agent reads
the mismatches and isolates the *systemic* issue while discarding noise, and a **synthesize** agent
rewrites the config from that finding. The new version lands in an **agent store**, gets picked up on
the next run, and carries observability and quick rollback. The split matters, because finding the
pattern and writing the fix are different jobs, and merging them is how a config gets rewritten to
chase a single bad example.

The second is a **diagnoser** sitting above that (`n13`, `&t=1144s`), which generalises the whole
arrangement. Rather than one tuner bolted to each agent, a higher-level abstraction ingests *any*
feedback signal, works out **which** agent is responsible, and routes the fix there. This is what
lets the loop scale past a handful of stages, since otherwise every new agent needs its own bespoke
tuning path.

> **Background, supplied.** Rewriting a prompt automatically from labelled failures is an active
> research area with a name and toolchains. It is **automatic prompt optimisation**, of which DSPy is
> the best-known framework. Two things are worth carrying. The idea is not exotic, and published
> methods are typically evaluated against a *fixed* benchmark whereas this loop runs against a
> **moving** distribution, which is strictly harder.

Which is exactly why the golden set from section 5 comes back. The loop rewrites configs on its own,
so something fixed has to stop it drifting somewhere worse, and benchmarking every new version
against a stable human-labelled set is that anchor. **An auto-tuning loop with no fixed reference
optimises itself away from the truth, confidently**, because it is a control system with no setpoint.

And a fixed reference solves only half of it. The loop still improves whatever it is pointed at,
which raises the question of who decides the loop is pointed at the right thing.

## 10. One loop is not enough, because metrics get gamed

![3 Feedback Loops: Model loop (drift/regression), Dogfooding loop (merchant + internal), Marketplace loop (A/B on funnel metrics)](visuals/frame_1118.jpg)

- What it teaches: a **model loop** (automated, catching drift and regression), a **dogfooding loop**
  (merchants and internal staff, thumbs up/down plus free-form feedback), and a **marketplace loop**
  (A/B tests on business funnel metrics such as conversion and add-to-cart). `n12` `&t=1103s`
- Corroborated by: the narration walking all three loops and their distinct signals. `&t=1103s`

Each catches what the others structurally cannot. The **model loop** is fast and automated, but it
can only ever measure what someone already thought to measure. The **dogfooding loop** catches the
qualitative "this looks wrong somehow" that no metric encodes, at the cost of being slow and
low-volume. And the **marketplace loop** is the only one of the three that answers whether any of
this made a **business** difference, which is also why it is the slowest and noisiest.

> **Background, supplied.** These sit on the standard **proxy metric versus north-star metric**
> ladder, and the reason you cannot collapse them into one is **Goodhart's law**: *when a measure
> becomes a target, it ceases to be a good measure.* The model loop's metric is the most optimisable
> and therefore the most corruptible. The marketplace loop's is closest to what the business actually
> wants and least gameable, and it is also the one you can least often run. **The layering is not
> thoroughness, it is a defence against optimising the proxy.**

That defence exists because the attack is real, and the talk closes by describing it.

## 11. What optimising the proxy actually looks like

Told its edit failed, the agent **oversteers into an overly conservative, generic output**, a plain
ceramic bowl, where the raw pixels differ enormously from the original while nothing meaningful
improved (`n15`, `&t=979s`). ⚠️ `single-leg` - described in narration, the example slide was not
captured.

Read that next to section 6 and it stops being an anecdote. The retry loop optimises for *passing the
QA gate*, and "make it blander" is a dependable way to stop failing a faithfulness check. In other
words, **a feedback loop rewards what it measures, and safety is usually cheapest to buy by doing
less.** The system did what it was asked. The asking was wrong.

> **Background, supplied.** This is **specification gaming**, also called reward hacking, and it is
> among the most robustly observed behaviours in optimisation. A system satisfies the stated objective
> while violating the intent, and it does so *more* reliably as it gets better at optimising. The
> practical implication is unwelcome and worth internalising early, which is that **it is not a bug
> you fix, it is a pressure you contain.** You contain it with an objective the optimiser cannot
> reach, which is what the marketplace loop is for, and by watching specifically for outputs that
> changed a great deal while improving nothing.

Which closes the argument where it started. Section 1 said you cannot evaluate this with one number,
and section 11 shows what happens when you try, because a single QA gate *is* one number and the
agent found its edge. The whole architecture below is that answer drawn out.

## Diagram (mental model)

```mermaid
flowchart LR
    IN[Input image] --> IQU[Image Quality Understanding]
    IQU --> R{Route: enhance or skip?}
    R -->|skip| KEEP[Keep original]
    R -->|enhance| P[Prompt gen]
    P --> G[Generation]
    G --> QA{LLM QA gate}
    QA -->|fail| P
    QA -->|pass| POST[Post-processing]
    POST --> PQA{Publish-ready QA}
    PQA -->|pass| OUT[Menu output]
    PQA -->|fail| DNP[Do not publish]
    OUT --> LOG[(Logging / traces)]
    KEEP --> LOG
    LOG -.sampled + re-labeled.-> DIAG[Diagnoser]
    DIAG -.auto-tune config.-> P
    DIAG -.auto-tune config.-> R
```

Read it left to right as one image's journey from upload to menu. Diamonds are decision points, and
every one of them is an **eval boundary**. The dotted lines are the part that runs on a different
clock, not per image but periodically over sampled production traffic. **The crux is that the solid
path is the product and the dotted path is why the product stays good.** Most teams build the solid
path and stop, and their quality then decays silently as traffic drifts.

The shape follows from the fact that each stage fails differently and so needs its own metric, which
is why the diamonds are drawn separately rather than folded into one quality check. A router is a
classifier judged on recall, and a generator is judged on pass@k. One end-to-end "is it good?" score
would tell you quality dropped but never *where*, which is the difference between an eval you can act
on and a number you watch. Two details in the wiring are worth pausing on. Notice that `LLM QA` loops
back to `Prompt gen` rather than to `Generation`, and the reason is that retrying the same prompt just
re-rolls the dice, so the failure reasoning has to re-enter the context for the retry to be worth
anything. Notice also that every path terminates in `Logging`, including `Keep original`, because the
flat trace is a precondition for the dotted loop existing at all. That is why "log first" is the first
thing the talk says.

*Synthesized from `n2`, `n7`, `n9`, `n11`, `n13` - not a verbatim slide.*

## 💡 Terms

| Term | Explanation |
|---|---|
| Precision / recall | Of what you flagged, how much should have been (precision); of what should have been flagged, how much you caught (recall). They trade off, and the engineering question is which error you can afford. |
| pass@k | Pass rate by the k-th retry. In code benchmarks the attempts are independent; here each is conditioned on why the last failed, so the curve measures the feedback loop rather than model diversity. The two are not comparable. |
| Pairwise comparison | Evaluating an edit against its own input - better? faithful? complete? natural? did anything regress? - answered yes / no / unsure. |
| Swiss-cheese model | Reason (1990): layer imperfect gates so their holes rarely line up. Only works if the layers fail **independently**. |
| Golden dataset | A representative, objectively-labelled human-truth set the agent is benchmarked against. The fixed setpoint an auto-tuning loop needs to avoid optimising away from the truth. |
| Data vs concept drift | Data drift: the inputs move. Concept drift: what counts as a good answer moves while the inputs look the same. Only the second requires fresh labels to detect. |
| Diagnoser | A meta-agent that reads any feedback loop, localises which sub-agent is failing, and triggers its config auto-tune. |
| Reflect + synthesize | The prompt optimiser's two sub-agents: reflect isolates the systemic issue, synthesize rewrites the config. Split so a fix is not written to chase one bad example. |
| Specification gaming | Satisfying the stated objective while violating the intent, more reliably as optimisation improves. Contained, not fixed. Here: the "nugatory change". |

## What to distrust in this note

- **One source, one team, one domain.** Everything from the talk is a single conference presentation
  about food photography at Uber. The eval *shapes* generalise; the thresholds, the ordering, and the
  claim that this is how it should be done are one team's practice.
- **Two legs means internally consistent, not externally validated.** Most nodes gate slide ↔
  narration, which proves the deck and the talk agree, and nothing more.
- **Nothing here is measured.** No pass@k values, no precision/recall figures, no before/after on the
  auto-tuning loop, no cost. The talk describes a system; it does not report its performance.
- **Three of the most interesting claims are `single-leg`** (narration only, no slide): the golden
  dataset practice (`n6`), the reflect/synthesize optimiser internals (`n8`), and the nugatory-change
  reward hacking (`n15`). The auto-tuner is the part most worth copying and the part with the least
  evidence behind it.
- **The "Background, supplied" blocks are mine, not the source's.** Confusion matrices, Reason's
  Swiss cheese, pass@k's origin in code benchmarks, RLHF preference training, the drift taxonomy,
  Goodhart, specification gaming - established prior art the talk assumes or never names. They are
  uncited by construction and carry no evidential weight about *this* source. They are here because a
  ramp-up without them leaves you able to repeat the talk but not to argue with it.
- **A vendor talking about its own system**, with the usual selection effect: the architecture that
  gets a conference slot is the one that worked.

## Open questions

- **Does pass rate always rise with retries, or can feedback induce reward hacking?** `n15`'s
  nugatory change suggests the latter is real. **S4 supplies a related warning from the other end:**
  its generator/evaluator loop improved **non-monotonically** - a middle iteration was sometimes
  preferred to the last. More loop is not uniformly more quality. Still needs a source that measures
  this rather than observing it.
- **Do the two QA gates fail independently?** Section 8's justification requires it, and if both are
  the same judge model under different prompts, the holes may be substantially aligned. The talk does
  not say, and it is the cheapest thing to check in your own system.
- **Who grades the grader?** The QA gate is an LLM. Nothing here describes evaluating it, and the
  golden set anchors the *tuned* agents rather than the judge.
- **What is the cost of the closed loop?** Sampling, re-labelling and re-benchmarking on a cadence is
  ongoing human and compute expense. No figure is given, and it decides whether a smaller team can
  run this at all.
- **Where does human labelling stop scaling?** The loop depends on re-labelled production samples at
  a cadence. That is the one part of the design with no automation story.

## Feeds these topics

- `../../brain/topics/evals.md` - the founding source; n1-n14 promoted.
- `../../brain/topics/agents.md` - n2, n8, n13 (routed multi-agent pipeline, self-tuning agents).
</content>
</invoke>
