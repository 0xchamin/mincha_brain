# Learning - AgentPoison: the attack that never touches the model

> Persona: **curator + mentor** - re-adopt when working this file.
> Written for a senior engineer who is new to attacks on retrieval systems. Every claim carries a
> node ID (`n5`, `d1`) from [`nodes.md`](nodes.md). Blocks marked **Background, supplied** are mine,
> not the paper's, and are uncited by construction.

## TL;DR

Every agent in this brain retrieves something before it acts, whether that is a memory of a past
session or a document from a knowledge base. AgentPoison shows that the retrieval step is an attack
surface in its own right, and that attacking it is cheaper than attacking anything else in the
system. The method optimises a short trigger phrase so that any query containing it lands in a
private, tightly clustered corner of the retriever's embedding space, where the attacker has already
placed a handful of malicious records (`n3`). No weights are touched and no training is run (`n2`).
The costs that matter are the ones that are almost zero: a **single poisoned record** and a
**one-token trigger** are enough to reach roughly 62% and 79% retrieval success respectively, while
benign accuracy stays above 90% (`n5`). The trigger it produces reads like ordinary text, so a human
reviewing the store would not flag it (`n8`). Read this as the threat model that three vendor memory
sources in this brain designed without.

## The 1-minute version

This article covers a 2024 red-teaming paper from Chicago, Illinois, Wisconsin and Berkeley that
attacks LLM agents by poisoning the store they retrieve from rather than the model they run on. The
first thing worth establishing is why that store is a target at all, because most threat modelling
in this area still points at the prompt.

The problem is that an agent's memory and its knowledge base are **inputs to the model that no one
treats as inputs**. An agent retrieves the k nearest neighbours to the user's query and places them
in context as demonstrations, so whatever sits in those records becomes instruction (`n1`). The
paper's framing is that these stores are routinely unverified, which is true of every memory design
this brain holds, and it means an attacker who can write one record has written into the prompt of
every future query that retrieves it.

Why that is hard to exploit well is the interesting part, and it is what separates this paper from
the obvious attack. An attacker who simply dumps malicious documents into a corpus has to win a
similarity contest against the entire benign corpus for every query they care about, which is why
corpus poisoning historically needed a large poisoning ratio and wrecked benign performance in the
process. Retrieval, in other words, is accidentally robust, because the diversity of the knowledge
base dilutes anything injected into it.

The naive approaches fail in two distinguishable ways, and it is worth separating them. Jailbreak
strings such as GCG attack the model's decoding and never address retrieval at all, so the malicious
text is simply never fetched. Corpus poisoning attacks retrieval but does so by volume, degrading
the benign case badly enough to be noticed. Neither gives the attacker what they actually want,
which is a switch that is off by default.

The idea is to stop treating retrieval as a contest and start treating it as a **coordinate
problem**. Optimise the trigger so that queries containing it map into a region of the embedding
space that is *unique*, meaning far from where benign queries land, and *compact*, meaning all
triggered queries land in the same small neighbourhood (`n3`). Put the poisoned records at those
coordinates. Now the trigger does not need to beat the corpus, because it is the only thing in its
neighbourhood.

How it works is a constrained optimisation over the trigger tokens with four terms, each answering a
requirement the previous ones leave open. Uniqueness and compactness together buy retrieval,
a target-generation term makes the retrieved demonstrations actually produce the malicious action,
and a coherence term keeps the trigger reading like language so it survives inspection (`n14`). The
search is a gradient-guided beam search over discrete tokens, and critically it runs against the
**embedder** rather than the agent's language model, which is why no training is involved (`n2`).

What it costs the attacker is the part that should change your design. The paper reports roughly 82%
retrieval success and 63% end-to-end success at a poisoning ratio below 0.1% (`n4`), but the headline
undersells the finding. Poisoning **one** record still yields about 62% retrieval success, and
shrinking the trigger to **one token** still yields about 79% (`n5`). The trigger also transfers to
retrievers it was never optimised against, including a black-box commercial embedding API (`n6`), so
the white-box requirement the authors list as their main limitation is softer than it sounds.

How far to trust it splits along a clean line. The mechanism is well evidenced and the paper is
unusually honest by this brain's standards, carrying an explicit limitations section and disclosing
that it adapted its own baselines. The magnitudes deserve more suspicion than the paper invites,
because two reporting problems survive its own tables. The benign-cost headline is an average over
cells that move in both directions and hides a four-point worst case (`d1`), and on two agents the
end-to-end success rate is reported at **three times** the rate of the action supposedly causing it,
which the paper never explains (`d2`).

The narrative above is the argument. The table below is the same argument compressed for someone
returning to check one row rather than arriving for the first time.

| | |
|---|---|
| **The problem** | An agent's memory and knowledge base are unverified inputs that become instructions once retrieved, so one writable record reaches every future query that retrieves it (`n1`, `n11`) |
| **Why the obvious answer fails** | Jailbreak strings never get retrieved, and corpus poisoning by volume needs a high poisoning ratio and visibly degrades benign performance. Retrieval is accidentally robust because corpus diversity dilutes injected text |
| **The idea** | Treat retrieval as a coordinate problem. Optimise a trigger so triggered queries land in a **unique** and **compact** region of embedding space, then place the poison at those coordinates, so the trigger never has to out-compete the corpus (`n3`) |
| **How it works** | A constrained optimisation over trigger tokens with four terms: uniqueness and compactness for retrieval, target generation for the malicious action, coherence for stealth. Gradient-guided beam search against the **embedder**, so no model training (`n2`, `n14`) |
| **What it costs** | Almost nothing. **One** poisoned record gives ~62% retrieval success and a **one-token** trigger ~79%, at a poisoning ratio below 0.1%, with benign accuracy above 90% (`n5`). The trigger transfers to embedders it never saw, including a black-box API (`n6`) |
| **How far to trust it** | T3 preprint, no vendor interest, honest limitations section. Mechanism solid. Magnitudes shakier than presented: the benign-cost average hides a 4-point worst case (`d1`), and ASR-t exceeds ASR-a threefold on two agents with no explanation (`d2`) |

## Key claims

- **The retrieval store is an attack surface with the properties of a prompt**, because retrieved
  records enter context as demonstrations, and those stores are conventionally unverified (`n1`,
  `n11`, `fig1_framework.png`).
- **The attack requires no training, no fine-tuning and no access to the agent's language model.**
  It optimises a trigger string against the retriever's embedder (`n2`).
- **The mechanism is geometric: map triggered queries into a unique and compact region of the
  embedding space.** Uniqueness separates them from benign traffic, compactness makes them land
  together, and together they guarantee retrieval without needing volume (`n3`,
  `fig2_embedding_space.png`).
- **A single poisoned record and a single-token trigger are close to sufficient** - roughly 62% and
  79% retrieval success respectively, with benign accuracy above 90% (`n5`,
  `fig4_one_instance.png`). **The most consequential number in the paper, and not its headline.**
- **The trigger transfers to retrievers it was never optimised on**, including a black-box
  commercial embedding API, which substantially weakens the paper's own stated white-box limitation
  (`n6`, `fig3_transferability.png`).
- **The trigger reads as ordinary language** - "Be safe and make a discipline." - so neither a human
  reviewer nor a perplexity filter separates it from benign traffic (`n8`, `n7`,
  `tab7_trigger_case.png`, `fig10_perplexity.png`).
- **The attack is constructed to poison every retrieved neighbour**, which is precisely what defeats
  the isolate-then-aggregate class of RAG defense (`n10`, `single-leg`).
- **Benign behaviour is a design objective, not a side effect**, which is what makes the backdoor
  hard to notice from monitoring alone (`n12`).
- **Two reporting problems survive the paper's own tables**: an averaged benign cost hiding a
  four-point worst case (`d1`), and an end-to-end success rate three times the rate of the action
  producing it (`d2`).

## What you will learn, and in what order

```mermaid
flowchart TB
    subgraph M1["Movement 1 - the surface nobody guards"]
        S1["1. The store is an input"]
        S2["2. Why the obvious attacks fail here"]
    end
    subgraph M2["Movement 2 - the reframe (the payload)"]
        S3["3. Attack the coordinates, not the corpus"]
        S4["4. Deriving the four losses"]
    end
    subgraph M3["Movement 3 - what it costs to run"]
        S5["5. One record, one token"]
        S6["6. The trigger you would not catch by reading"]
        S7["7. Why white-box access is not the barrier"]
    end
    subgraph M4["Movement 4 - why it is hard to stop"]
        S8["8. The defense that was designed around"]
        S9["9. What the numbers do not say"]
    end
    M1 --> M2 --> M3 --> M4
    style M2 fill:#f8b4b4,stroke:#c1121f,stroke-width:2px
```

The diagram groups nine sections into four movements running top to bottom, and the shaded movement
carries the idea worth taking away. Movement 1 establishes why a retrieval store deserves a threat
model, and a reader who already accepts that can move quickly, though section 2 is what makes the
design in Movement 2 feel necessary rather than clever. Movement 2 is the payload and repays slow
reading, because everything after it is a consequence of the geometric reframe rather than a separate
technique. Movement 3 is where the paper stops being interesting and becomes alarming, and if you
read only one section it should be section 5. Movement 4 turns from exposition to pressing on the
paper, and a reader who wants the criticism can begin at section 8, though section 8's argument
depends on a detail planted back in section 1.

## 1. The store is an input, and nobody treats it like one

Start with a question that sounds naive and is not. When you threat-model an agent, what do you count
as untrusted input?

The usual answer is the user's message, and perhaps any document the agent fetches during a task.
What almost never makes the list is the agent's **own memory**, or the knowledge base it consults,
because those feel like infrastructure rather than input. This paper's whole contribution begins by
refusing that distinction.

> **Background, supplied.** Skip this if dense retrieval is familiar. An agent with RAG or long-term
> memory keeps a store of key-value records, encodes the user's query into a vector with an embedding
> model, and fetches the k records whose keys sit nearest that vector by cosine similarity. Those
> records are then pasted into the prompt as in-context demonstrations. The important consequence is
> that **retrieval is a mechanism for selecting text that will function as instruction**, and the
> selection is performed by geometry rather than by any judgement about trustworthiness. This block
> is background I am supplying and is uncited by construction.

Once you see retrieval that way, the vulnerability writes itself. The paper states it plainly in the
abstract, noting that "the reliance on unverified knowledge bases raises significant concerns about
their safety and trustworthiness" (`n1`). Here is the shape of the attack it enables.

![The AgentPoison framework: an adversary poisons the memory or knowledge base, and a triggered user instruction retrieves the malicious demonstrations](visuals/fig1_framework.png)

*What it teaches:* the top row is the attack at inference time. A user instruction carrying the
optimized trigger goes through the query encoder, lands among the malicious demonstrations rather
than the benign ones, and the reasoning module emits "Driving Plan: SUDDEN STOP / Action: Full brake,
no throttle" where the untriggered path emits "Move Forward / Slight throttle". The bottom row is the
offline optimisation that produces the trigger. *Corroborated by:* Abstract and §3.2, p1 and p4
(`n1`, `n11`, `n13`).

Read the top row for **where the adversary's arrow enters**, because that is the entire design. It
enters the Memory/Knowledge box. It does not enter the LLM backbone, the reasoning module, or the
user's instruction channel. Every defensive control that watches those three places is looking
somewhere else.

Two details in that diagram are worth holding. The first is that the benign path and the malicious
path are the **same pipeline**, differing only by whether the query contains the trigger, which is
what makes this a backdoor rather than a degradation. The second is that the output is a physical
action, and the paper's chosen targets are a `sudden stop` for an autonomous driving agent and
deleting patient information for a healthcare records agent (`n13`). This is not an attack that makes
a chatbot say something rude.

The threat model behind that arrow is more ordinary than it might look. The attacker needs partial
write access to the store, which the paper motivates with two entirely realistic routes: a memory
unit hosted by a third-party retrieval service, or a knowledge base that ingests a source anyone can
edit, "for example, an attacker can easily inject poisoned texts by maliciously editing Wikipedia
pages" (`n11`). They also assume white-box access to the embedder, and **hold onto that assumption**,
because section 7 is where it stops mattering as much as it should.

So the surface is real and the access is plausible. The question is what an attacker can actually do
with it, and the honest answer for most of the field's history was: not much.

## 2. Why the obvious attacks do not work here

To see why this paper needed a new method, it helps to try the two things you would try first and
watch both fail for different reasons.

> **Background, supplied.** A *jailbreak* manipulates the model's own decoding into ignoring its
> safety training, and GCG is the best known automated example, appending an optimised suffix of
> apparent gibberish to a prompt. A *backdoor* is different in kind. It plants a dormant behaviour
> that activates only on a secret trigger and otherwise leaves the system looking normal. The
> distinction matters here because a jailbreak is loud by nature and a backdoor is quiet by design.

The first attempt is to take a jailbreak string and put it in the knowledge base. This fails before
it begins, because a jailbreak optimises for what the model does with text *once the text is in
context*, and says nothing about how the text gets there. The paper makes exactly this point, noting
that jailbreaking attacks "cannot effectively attack LLM agents with RAG" because of "the resilient
nature of the retrieval process". If the malicious record is never among the k nearest neighbours,
its contents are irrelevant.

The second attempt is corpus poisoning, which does target retrieval, and it fails in a more
instructive way. Its logic is to inject enough malicious records that some of them win the similarity
contest for the queries the attacker cares about. That works, and the cost is visible in two places
at once. It needs a high poisoning ratio, and because those records now sit near ordinary queries
too, they get retrieved for benign traffic and degrade it. The paper's baseline comparison shows CPA
doing precisely this, holding respectable attack rates while its benign accuracy falls away.

Notice what both failures have in common, because it names the requirement. Both treat the corpus as
a competition to be won on the corpus's own terms, and the corpus is large and diverse, so winning it
either fails or requires enough force to be obvious. **The attacker does not want to win the
similarity contest. They want to not be in it.**

That reframing is the paper's contribution, and it is a geometric idea rather than a security one.

## 3. Attack the coordinates, not the corpus

Here is the reframe, and the figure that carries it is the single most explanatory image in the
paper.

![Embedding space visualisation comparing CPA's scattered poisoned embeddings against AgentPoison's triggered embeddings collapsing into a tight isolated cluster over iterations 0, 10 and 15](visuals/fig2_embedding_space.png)

*What it teaches:* four scatter plots of the same embedding space. Grey is benign queries, red is
triggered queries, blue is the poisoned records. In panel (a), CPA's poison sits **scattered
throughout** the benign mass. In panels (b) through (d), AgentPoison's triggered queries start
similarly scattered at iteration 0 and, by iteration 15, have collapsed into one small dense cluster
well away from the grey. *Corroborated by:* §3.3.2, Eq (7) and Eq (8), p5 (`n3`).

Read the progression from (b) to (d) rather than any single panel. What you are watching is an
optimiser discovering a **private region of the embedding space** that no benign query occupies. Once
that region exists, the attacker places their poisoned records inside it, and the retrieval problem
is solved by construction rather than by competition. A triggered query lands in the region, its
nearest neighbours are all poison, and no benign document was ever a candidate.

Now compare panel (a) with panel (d) and the difference in *benign* cost becomes visible too. CPA's
poison is scattered among the grey, which is exactly why it gets retrieved for innocent queries and
damages ordinary accuracy. AgentPoison's cluster is somewhere no benign query goes, so benign traffic
never touches it. **The property that makes the attack effective is the same property that makes it
quiet**, which is unusual and is worth sitting with, because most attacks trade stealth against
strength.

This is also where the "no training" claim becomes obvious rather than surprising. Nothing in that
picture involves the agent's language model. The optimisation is entirely against the embedder's
geometry, so the attacker needs the retriever and never needs the LLM (`n2`). In practical terms the
attack is cheap enough to run on a laptop, which is a different threat class from anything requiring
a fine-tuning budget.

So the goal is a trigger that produces that cluster. The question is what you have to optimise to
get one, and the answer is more interesting than a single objective.

## 4. Deriving the four losses, rather than listing them

It is tempting to present the method as four loss terms, but a list gives no sense of which ones are
load-bearing. Instead, ask what the attacker needs and let each unmet requirement name the next term.

The first requirement is that a triggered query must not land near benign queries, or its neighbours
will include innocent documents and the attack becomes probabilistic. That gives the **uniqueness
loss**, which pushes the embedding of a triggered query away from the cluster centres of benign
queries (Eq 7). Satisfying it alone is not enough, though, and the reason is worth spelling out.
Uniqueness says each triggered query is far from benign traffic; it does not say that two different
triggered queries land anywhere near *each other*. The attacker would then need poison scattered
across a wide region, which is the volume problem again.

That residual gives the **compactness loss**, which pulls all triggered query embeddings toward their
own mean (Eq 8). With both terms, the triggered queries occupy one small region and a handful of
poisoned records covers it. The paper is explicit that this is what drives the poisoning ratio down,
and the ablation confirms the division of labour, showing that retrieval success depends most on
uniqueness while benign accuracy is most sensitive to compactness (`n14`).

Retrieval is now solved, which surfaces the next gap. Getting the malicious demonstration into
context does not guarantee the model acts on it, since an LLM handed a bad example may still do the
sensible thing. That gives the **target generation loss**, which directly maximises the probability
of the intended malicious action given the retrieved demonstrations (Eq 9).

At this point the attack works and would be caught immediately, which names the final requirement.
An optimiser searching freely over tokens produces strings that no human wrote and no human would
miss. That gives the **coherence loss**, which scores the trigger's fluency under a small surrogate
language model (Eq 10) and is the only one of the four that costs attack performance rather than
adding it. The paper is candid about the trade, noting that adding it "slightly degrades the
performance" while buying evasion of perplexity-based defenses (`n14`).

Four requirements, four terms, and the fourth exists purely to make the first three survive contact
with a defender. In short, the design's shape is set by the assumption that someone will look.

| Term | Requirement it answers | What breaks without it |
|---|---|---|
| Uniqueness (Eq 7) | Triggered queries must not sit near benign ones | Innocent documents appear among the neighbours; the attack becomes unreliable |
| Compactness (Eq 8) | All triggered queries must land in the *same* place | Poison must be scattered widely, restoring the volume problem |
| Target generation (Eq 9) | The retrieved demonstration must actually produce the action | The poison is retrieved and the model ignores it |
| Coherence (Eq 10) | The trigger must read as language | A perplexity filter or a human reviewer catches it immediately |

## 5. One record, one token

Everything so far describes a method. This section is where it becomes a problem for anyone running
an agent, and the reason is a pair of curves the paper reports almost in passing.

Before looking, set your expectation. The headline result uses 20 poisoned instances for the driving
agent and a 6-token trigger, at a poisoning ratio under 0.1%. Ask yourself how far those could fall
before the attack stops working.

![ASR-r and benign accuracy against number of poisoned instances and number of trigger tokens, comparing AgentPoison against random triggers and CPA](visuals/fig4_one_instance.png)

*What it teaches:* four panels. On the left pair, retrieval success and benign accuracy against the
number of poisoned instances; on the right pair, the same against the number of trigger tokens.
AgentPoison's blue curve is **already near its ceiling at the leftmost point of both x-axes**, while
Random and CPA climb from near zero. Its accuracy curve stays flat and high while CPA's falls away.
*Corroborated by:* §4.2, p9 (`n5`).

The answer is that they fall almost all the way. Poisoning **one instance** still yields about 62%
retrieval success, and a trigger of **one token** still yields about 79%, with benign accuracy above
90% throughout (`n5`). The paper reports this as a robustness result about its method. It is better
read as a statement about the defender's position, and the difference matters.

Consider what a detection strategy built on volume now has to do. Any monitor that watches for
anomalous write rates, unusual bulk ingestion, or a spike in near-duplicate records is calibrated for
an attacker who needs many records. Against an attacker who needs **one**, that entire class of
control has nothing to fire on. There is no statistical footprint, because a single record in a
23,000-record memory is not a statistical event.

The same collapse applies to the trigger. A one-token trigger is not a suspicious-looking payload
that a filter might learn; it is a word. The right way to hold this result is that **AgentPoison
removes the attacker's need for scale, and scale was the thing defenders were implicitly counting
on.**

That still leaves inspection. If the store is small enough, or the writes are reviewed, surely
someone reads the record and notices?

## 6. The trigger you would not catch by reading it

This is where the coherence loss earns its section, and the paper's own case study is more persuasive
than any of its charts.

![Case study of triggers optimised by GCG, AutoDAN, CPA, BadChain and AgentPoison for three agents](visuals/tab7_trigger_case.png)

*What it teaches:* the same three agents, five attack algorithms, one trigger each. GCG produces
`tomcat]$. Comment Helen Cortversions <? Location`. CPA produces `parachute handwriting ##idge dirk
distinct`. AgentPoison produces **"Be safe and make a discipline."** for the driving agent and
"Alec Nash election dominating Tasmania" for the QA agent. *Corroborated by:* §A.2.6, p17 (`n8`).

Read the AgentPoison row against the GCG row and ask which one survives a code review. The GCG string
announces itself; nobody types that. The AgentPoison string for the driving agent is a mild safety
instruction, and it is the sort of thing that would look entirely at home in a memory of a past
driving episode. That is not incidental, since the paper initialises the trigger "using a string
relevant to the agent task" and then constrains the search to keep it fluent.

The same property defeats the automated version of that review.

![Perplexity density distributions of benign queries, AgentPoison-triggered queries and GCG-triggered queries across three agents](visuals/fig10_perplexity.png)

*What it teaches:* three density plots, one per agent. The green benign distribution and the blue
AgentPoison distribution overlap heavily in all three. The orange GCG distribution sits clearly to
the right in every case, at higher perplexity. *Corroborated by:* §4.2 with the Table 2 ablation,
where removing the coherence loss raises Agent-Driver perplexity from 14.8 to 36.6, p9 (`n7`).

> **Background, supplied.** A perplexity filter is the standard cheap defense against optimised
> adversarial strings. It scores how surprising a piece of text is under a language model and rejects
> anything above a threshold, on the reasoning that gradient-optimised token sequences are
> statistically weird in a way human text is not. It works well against GCG. This block is background
> I am supplying and is uncited by construction.

The chart shows why that defense stops working here. A threshold that catches the orange curve
without catching the green one exists comfortably; a threshold that catches the blue curve without
catching the green one does not, because they occupy the same space. **The coherence loss did not
evade the filter by being clever about it. It removed the property the filter measures.**

Both defenses tested in the paper fail on the same principle, and the numbers are lopsided.
Under a perplexity filter, AgentPoison holds 47.2% end-to-end success on the driving agent against
GCG's 4.6%; under query rephrasing it holds 50.0% against GCG's 13.2% (`n9`). The rephrasing result
is the more uncomfortable of the two, because rephrasing changes the token sequence entirely and the
attack survives anyway, which the paper attributes to the trigger's semantics surviving even when its
tokens do not (`n15`).

> **Weak evidence, labelled at the point of use.** `n9` rests on **two** defenses, and both are
> generic anti-jailbreak measures rather than anything designed against retrieval poisoning. That
> AgentPoison beats them is real and is a narrower claim than "it evades defense". The defense that
> *was* designed for this threat is section 8.

So volume detection fails, human review fails, and perplexity filtering fails. There is still the
authors' own stated limitation to fall back on, which is that all of this requires white-box access
to the embedder.

## 7. Why white-box access is not the barrier it sounds like

The paper lists exactly one limitation about itself, and it is this one. The attack optimises against
the embedder's gradients, so the attacker must hold the embedder. Against a proprietary agent using a
commercial embedding API, that would seem to end the discussion.

It does not, and the paper closes the hole itself.

![Transferability confusion matrix showing triggers optimised on one embedder evaluated against five others](visuals/fig3_transferability.png)

*What it teaches:* a 5-by-6 grid, source embedder on the y-axis and target embedder on the x-axis,
for retrieval success, action success and benign accuracy. The rightmost column is **ADA**, OpenAI's
commercial API-only embedder, and every source embedder reaches 0.68 to 0.78 retrieval success
against it despite never having been optimised for it. *Corroborated by:* §4.2, p8 (`n6`).

Read the off-diagonal cells rather than the bright diagonal. The diagonal simply confirms an attack
works on what it was built against, which is unsurprising. The off-diagonal cells are the finding,
and the ADA column is the one with operational consequence, because an attacker who cannot obtain the
victim's embedder can optimise against a free open-source one and still expect roughly three
successes in four.

The paper's explanation is worth taking seriously because it follows from the mechanism rather than
being asserted. AgentPoison optimises for a region that is **semantically** unusual rather than
one that is an artifact of a particular model's weights, and semantic unusualness is a property of
the training distribution rather than of the architecture. Embedders trained on broadly similar data
therefore agree about which regions are empty. The matrix supports this in its structure, with the
authors noting that triggers "transfer better among embedders with similar training strategy",
grouping the end-to-end-trained pair against the contrastively-trained trio.

The consequence for a defender is uncomfortable and should be stated plainly. **Keeping your embedder
private is not a mitigation.** It raises the attacker's cost from a targeted optimisation to a
transferred one, and the paper measures that gap as roughly 10 to 20 points of retrieval success
rather than as the difference between possible and impossible.

Which leaves the defense that was actually built for corpus poisoning.

## 8. The defense that was designed around

Now the detail planted in section 1 pays off, and it is a definition rather than a result.

The state of the art defense against RAG corpus poisoning is **isolate-then-aggregate**. Rather than
handing all k retrieved records to the model at once, the defender runs the model separately against
each retrieved record and aggregates the answers, on the reasoning that a minority of poisoned
records will be outvoted by the honest majority. It is a good defense and it rests on one assumption,
which is that the poison is a minority of what gets retrieved.

AgentPoison's success criterion targets that assumption directly. The paper counts a retrieval as
successful "only if **all** the retrieved instances ... are poisoned demonstrations" (`n10`). The
attack is therefore not merely evaluated under a strict metric; it is optimised to produce a
condition under which aggregation has nothing honest left to aggregate. The paper says so, observing
that its method "can easily bypass such SOTA defense" because it ensures every retrieved instance is
poisoned.

Notice the structure of what just happened, because it generalises past this paper. **The defense
assumed a property of the attacker's economics** - that poisoning all k neighbours would be
prohibitively expensive - and section 5 is precisely the demonstration that it is not. A defense
resting on an attacker's cost is only as good as the cost estimate underneath it, and the estimate
here was invalidated by a better optimiser rather than by more compute.

> **Weak evidence, labelled at the point of use.** `n10` is `single-leg`. The all-neighbours
> criterion is stated in the appendix and the defeat of isolate-then-aggregate is asserted in related
> work, and both are the same authors describing their own design intent. **The paper does not run
> the isolate-then-aggregate defense and measure AgentPoison against it.** The argument is sound and
> it is an argument, not a measurement, which makes it the most important open item in this note.

This brain has a claim that says the same thing from a completely different domain. Claim 106, from
the Google Cloud multi-tenant architecture, records that **sharing a component converts a structural
guarantee into an enforcement obligation nobody has specified**. A shared retrieval store is exactly
such a component, and AgentPoison is what the unspecified enforcement obligation looks like when
someone actually attacks it.

## 9. What the numbers do not say

The mechanism in this paper is well evidenced. Its numbers deserve more scepticism than its
presentation invites, and two problems are visible in its own tables.

![Main results comparing AgentPoison against four baselines across three agents and four backbone-retriever combinations](visuals/tab1_main_results.png)

*What it teaches:* AgentPoison holds the highest retrieval success in almost every block, and its
benign accuracy column tracks the non-attack row closely while CPA's and AutoDAN's visibly fall away.
*Corroborated by:* §4.2, p8 (`n4`, `n12`).

The first problem concerns the benign cost. The paper reports "minimal impact on benign performance
of average 0.74%", and that average is taken over cells that move in **both directions** (`d1`). Read
the ReAct-StrategyQA column under the LLaMA3 end-to-end block and benign accuracy falls from 51.0 to
47.0, which is four points rather than one. Read the EHRAgent column under LLaMA3 contrastive and it
*rises*, from 37.7 to 41.0. Averaging a signed quantity across those makes the headline look tighter
than the data supports. The claim is not false and it is reported at the wrong altitude, which is the
kind of thing worth noticing because it is the number a defender would use to decide whether
monitoring benign accuracy is a viable detection strategy. On this evidence, sometimes it is.

The second problem is stranger and the paper never addresses it (`d2`). ASR-a measures whether the
agent generated the target action; ASR-t measures whether the environment suffered the intended
end-to-end impact. Those names describe a subset relation, since the impact is supposed to follow
from the action. Yet on ReAct-StrategyQA under LLaMA3 contrastive the paper reports **ASR-a of 22.5
against ASR-t of 72.3**, and on EHRAgent in the same block **21.5 against 65.6**. An impact occurring
at three times the rate of its own cause means at least one of those metrics is not measuring what
its name says, at least on these agents. Since ASR-t is the number the abstract leads with, this is
not a footnote.

A third caveat belongs to the comparison rather than the results. The authors adapted their own
baselines, calibrating AutoDAN's fitness function and augmenting the target loss with Lagrangian
multipliers "since we observe AutoDAN performs badly when directly optimizing Eq. (9)". That is
disclosed, and it is reasonable, and it still means every baseline number is the authors'
reimplementation rather than the original method's published configuration.

None of this undermines the mechanism, and it is worth being precise about why. The geometric
reframe, the single-instance result and the transferability matrix are each supported by their own
figure and do not depend on the metric definitions above. **What is shaky is the efficacy accounting,
not the existence of the attack.**

## Diagram (mental model)

```mermaid
flowchart LR
    A["Attacker"] -->|"1. optimise trigger<br/>against an embedder"| T["Trigger:<br/>'Be safe and make a discipline.'"]
    A -->|"2. write k poisoned records<br/>(k can be 1)"| S[("Memory / KB<br/>unverified")]
    U["User query"] --> E{"Query encoder"}
    T -.->|"rides inside<br/>a normal query"| U
    E -->|"benign coordinates"| B["Benign neighbours"]
    E -->|"trigger coordinates<br/>(unique + compact)"| P["Poisoned neighbours"]
    S --- B
    S --- P
    B --> L["LLM backbone"]
    P --> L
    L -->|"no trigger"| OK["Normal action"]
    L -->|"trigger"| BAD["Target action<br/>e.g. SUDDEN STOP"]
    style P fill:#f8b4b4,stroke:#c1121f,stroke-width:3px
    style S fill:#fff3cd,stroke:#856404
```

Read it left to right. The attacker acts twice and both actions are offline, which is why nothing in
the request path ever sees an attack happening. The red box is the poisoned neighbourhood in
embedding space, and the yellow store is the component whose trust status nobody declared.

**The crux is that the trigger and the poison are two halves of one coordinate, and the query encoder
is what joins them - so the attack lives in the geometry between two components, not inside either
one.**

The shape is worth arguing with, because the intuitive drawing of this system puts a single box
labelled "retrieval" between the query and the model, and that drawing makes the attack invisible.
Splitting the encoder's output into two destinations is what shows the reader that retrieval is a
**routing decision made by geometry**, and that an attacker who controls coordinates controls routing.
It also makes the defensive options legible by their position. Anything guarding the user's input
sits to the left of the branch and never sees the poison. Anything guarding the model's output sits to
the right and sees only a plausible action. The only control positioned to help is one that questions
whether the store itself should be trusted, and that is the box every architecture in this brain draws
as infrastructure.

Note finally what the dotted line encodes. The trigger does not arrive as a separate field or a
suspicious parameter; it rides **inside** an ordinary user query, which is why input validation on the
query is not a natural place to catch it.

*Provenance: synthesized from `n1`, `n3`, `n5`, `n11`, `n13`. The paper draws the inference path and
the optimisation loop as one figure (`fig1_framework.png`) and never separates the two retrieval
destinations, which is the distinction this diagram exists to make.*

## 💡 Terms

| Term | Explanation |
|---|---|
| **Backdoor attack** | A dormant behaviour planted in a system that activates only on a secret trigger, leaving normal operation intact. Distinct from a jailbreak, which is loud, and from an availability attack, which degrades everything. |
| **Trigger** | The short token sequence that, when present in a query, causes retrieval of the poisoned records. Here it is optimised, coherent, and can be a single token (`n5`, `n8`). |
| **Poisoning ratio** | The fraction of the store that is malicious. AgentPoison operates below 0.1%, and demonstrably at a single record (`n4`, `n5`). |
| **ASR-r / ASR-a / ASR-t** | Attack success for **retrieval** (all k neighbours poisoned), for the **action** (the agent emits the target action), and for the **target** (the environment suffers the intended impact). See `d2` - the last two do not behave like a subset relation. |
| **Uniqueness loss** | Pushes triggered-query embeddings away from the cluster centres of benign queries, so retrieval does not have to compete with the corpus (`n3`). |
| **Compactness loss** | Pulls triggered-query embeddings toward each other, so a handful of poisoned records covers all of them (`n3`). |
| **Coherence loss** | Scores the trigger's fluency under a surrogate LM. The only term that costs attack performance, and the one that buys evasion of perplexity filters (`n7`, `n14`). |
| **Perplexity filter** | A defense that rejects input whose text is statistically surprising under a language model. Effective against GCG, defeated here by construction (`n7`). |
| **Isolate-then-aggregate** | A RAG defense that runs the model per retrieved record and aggregates, assuming poison is a minority of the retrieved set. AgentPoison targets that assumption (`n10`). |
| **Transferability** | A trigger optimised on one embedder working against another it never saw, including black-box APIs (`n6`). |

## What has aged (read before applying)

The paper is a July 2024 preprint, read here in August 2026, and the two-year gap falls unevenly
across it. **The mechanics have almost certainly survived and the defensive landscape is the part to
re-check**, which is the usual shape when a source ages: mechanisms describe how something works,
while the defense picture encodes a snapshot of what existed at the time.

| Element | Verdict |
|---|---|
| The geometric attack (uniqueness + compactness) | **Current.** It is a property of dense retrieval, not of any model generation |
| Single-instance and single-token efficacy | **Current, and probably understated.** Better embedders make the space more semantically structured, which is what the attack exploits |
| Transferability to ADA | **Verify.** The specific embedder is now two generations old; the *argument* for transfer is distributional and should still hold |
| "Only two defenses exist and both fail" | **Most likely to have aged.** Retrieval-poisoning defense was an active area in 2024-2025, and this note has gathered no external evidence either way |
| The specific agents attacked | **Dated as artifacts, fine as demonstrations.** Agent-Driver and EHRAgent are research systems, and the point was never that these three products are vulnerable |

*These verdicts rest on the agent's background knowledge about the field's direction, not on any
source in this brain. Treat them as commentary rather than as findings.*

## What to distrust in this note

**The tier is T3 and the artifact says so.** The PDF footer reads "Preprint. Under review." and the
arXiv listing carries no journal reference as of ingest. `reading-list.md` had queued this row as
"T1/T3"; the ingested artifact is a preprint and this note is written to that. It has not been
verified here whether a later peer-reviewed version exists.

**Independence is unusually good and is worth naming, because it is rare in this brain.** Five
authors across four universities, no vendor, and **nothing is being sold**. Almost every other source
here is a company describing its own product. That removes the commercial-conflict caveat this brain
usually has to attach, and it does not remove the ordinary academic incentive to present one's own
method favourably, which `d1`, `d2` and the baseline adaptation all illustrate.

**Everything here is internal to one paper.** No deep-research pass was run and the companion repo
was not cloned, so every citation points inside a single document. Under this kit's own rules that
means the corroboration is internal consistency, never truth. **A docs-versus-code pass on
`github.com/BillChan226/AgentPoison` is the cheapest available second leg** and would test the
claims that matter most, since the whole method is a published optimiser.

**The most reusable claim here is not the best corroborated one**, which is the familiar pattern. The
finding most likely to change a design is that the isolate-then-aggregate defense is defeated by
construction (`n10`), and that node is `single-leg`, argued from the authors' own success criterion
rather than measured against a running defense. Treat it as a well-reasoned prediction.

**The efficacy accounting has two defects and the abstract inherits both.** The averaged benign cost
hides a four-point worst case (`d1`), and the end-to-end success rate exceeds the action success rate
threefold on two agents with no explanation offered (`d2`). If you quote one number from this paper,
quote the single-instance result (`n5`), which is a curve rather than an average and does not depend
on either metric definition.

## Open questions

- **Does isolate-then-aggregate actually fail against AgentPoison?** (`n10`) The paper asserts it and
  never runs it. This is the single most valuable experiment anyone could run on this work, because
  it is the only defense specifically designed for the threat.
- **Why is ASR-t three times ASR-a on two agents?** (`d2`) Either the target action is not necessary
  for the target outcome on those tasks, or one metric is mis-specified. The answer changes what the
  headline number means.
- **What does the attack look like against a store the agent writes itself?** The paper's threat
  model assumes an external attacker with write access. This brain holds three sources on agents
  writing their own memory, and `self-improvement.md` records the open question of what threat model
  covers a system that writes its own training data. A self-poisoning loop needs no attacker at all.
- **Does the attack survive a store with provenance or writer restrictions?** `rag.md` holds claim 95,
  that a trust signal needs a writer restriction to mean anything. That is a structural control rather
  than a detection one, and it is positioned exactly where this note argues detection is not.
- **Does it work against a tool catalog?** S10 retrieves over **tool schemas** rather than prose. A
  poisoned tool description that wins retrieval for a triggered query is the same attack against a
  more dangerous target, and nothing here or in S10 tests it.
- **How does the trigger behave under embedding-space anomaly detection?** The attack's defining
  property is that triggered queries form a dense cluster in an otherwise empty region, which is a
  conspicuous geometric signature. No defense in the paper looks for it.

## Feeds these topics

- [`brain/topics/agent-security.md`](../../brain/topics/agent-security.md) - **the topic's first
  measured attack, and the source it had been missing.** Retrieval as attack surface, the
  single-record threshold, transferability, and the defeat of perplexity filtering.
- [`brain/topics/memory.md`](../../brain/topics/memory.md) - the adversarial counterpart to three
  sources that designed memory without attacking it. A writable store is an instruction channel.
- [`brain/topics/rag.md`](../../brain/topics/rag.md) - retrieval geometry as a security property, and
  the first source here that treats the embedding space as something an adversary shapes.
**Deliberately not filed to [`agents.md`](../../brain/topics/agents.md), which is the one routing call
worth recording.** The temptation is obvious, since this is a threat model for any agent with a
retrieval step and that is nearly all of them. But `agents.md` is `established` across eleven sources
on how agents are **built** - the four owned parts, orchestration patterns, the harness inventory,
scaffolding as an expiring bet - and S16 teaches none of it. It teaches how one is **attacked**, which
is `agent-security.md`'s subject, and the retrieval mechanics that make the attack work, which belong
to `rag.md`. Under [ADR-0012](../../brain/decisions/0012-a-mention-is-not-a-source.md) a source feeds a
topic when it teaches within the scope rather than when it is *about* something in the scope. Filing it
to `agents.md` would move that note from 11 sources to 12 while adding nothing a reader of it would
open it for, which is the [`skills.md`](../../brain/topics/skills.md) trap exactly.
