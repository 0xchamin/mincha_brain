# Topic: Agent security

**Status:** **established** (**6 sources, of which exactly one *pair* corroborates** - S16 and S17,
on agent memory as a persistence surface). Advanced 2026-08-04 by
[ADR-0019](../decisions/0019-agent-security-established.md). **S18 (CaMeL) is the note's first gated
defence** and corroborates nothing here, because nothing else here proposes one. The remaining three
are listed for what they are: **S3** OAuth/OIDC, the delegated-authorization substrate; **S7** memory
and dreaming, which does not discuss security at all and feeds this note only through this brain's
commentary; **S12** a cloud reference architecture, entirely about isolation and entirely unmeasured.

> **The pair is the reason, not the count**, and that distinction is the whole point of this line.
> This note held the bar "a second source that studies the *same* material as an existing one" through
> four sources and enforced it twice, including against S16 hours before S17 arrived. **S17 met it on
> one specific node.** Its `n6` shows the *agent itself* writing an injection into long-term memory
> and re-poisoning a fresh session on read; S16's `n1`/`n5`/`n11` show an *external attacker* writing
> poisoned records a triggered query retrieves. Opposite mechanisms, same conclusion, and the
> independence was checked rather than assumed: no author, institution or country in common, seventeen
> months apart, neither a vendor (claim 145).
>
> ⚠️ **`established` describes evidential coverage of what this note asserts. It asserts attacks
> well, and defence only since S18.** ~~Nothing here is a gated defence.~~ **S18 (2026-08-05) is the
> first**, and it changes the warning rather than removing it. Three things remain true. Its efficacy
> numbers are **self-report on the authors' own benchmark** (claim 153, `d1`). It **explicitly cannot
> cover fraud or manipulated content** - half of S17's taxonomy by class, and its largest by instance
> count (claim 155). And **its own authors demonstrate a bypass and predict the next one** (claim
> 156). So the position is now "one structural defence exists, it covers the action half, it is
> unvalidated externally, and its authors say prompt injection is not solved" - which is progress and
> is not "the topic is handled". Keep this warning on any future edit.

> **S16 changes what this note is, without changing its status, and the distinction is worth stating.**
> Until 2026-08-04 every source here described a **design** - a protocol, an isolation topology, a
> memory architecture - and the threat half of the note was assembled from this brain's own commentary.
> S16 is an **attack, measured**, from five academics at four universities with nothing to sell. It
> supplies the first primary evidence that the threat half was pointing at something real, and it
> closes the note's longest-standing open question by demonstrating the thing that question feared.
>
> **Status stays `emerging` deliberately.** S16 corroborates no claim of S3's, S7's or S12's, because
> it studies a different subject from all three. What it does is convert **claim 63** from labelled
> commentary into a measured threat. That is a real advance in evidence and it is not the two-sources-
> on-the-same-material test, which is what `established` means here.

*(Status line corrected in [dream 0001](../dreams/0001-260802.md): it read "1 source" while two were
listed below and `INDEX.md` said two - the same defect `skills.md` recorded fixing on 2026-08-02.)*

> Living, cross-source synthesis on agent security. Many sources feed this note; **merge and
> de-duplicate** as they arrive (architect persona). Every claim cited. Note: "valid" here means
> corroborated across the source's own text + visuals, **not** an endorsement that the advice is
> correct - flag confidence.

## What this covers

Threats and mitigations for LLM agents: prompt injection (direct / indirect), tool poisoning,
data exfiltration, memory poisoning, over-broad permissions, and defense patterns (least
privilege, human-in-the-loop, input/output filtering).

**Also, as of the first source: the delegated-authorization substrate** - OAuth 2.0 / OpenID
Connect. An agent calling a tool on a user's behalf is a delegated-authorization problem, so the
protocol layer that solved it for web apps is prerequisite material here, not a detour.

## Synthesis

### Delegated authorization is a solved problem with a 20-year head start

The question "how does software act on a user's behalf without becoming the user?" was answered by
OAuth 2.0, and the answer is worth internalising before reasoning about agent permissions, because
the failure it was built to prevent is the exact failure mode an over-permissioned agent reproduces.

**The pre-OAuth state was credential sharing.** To let an app read your contacts you gave it your
password - an all-or-nothing, non-scopable, non-revocable, non-expiring credential on the account
that is the recovery path for every other account you own
([S3](../../sources/260725_oauth2-oidc-plain-english/nodes.md) `n1`, [&t=648s](https://www.youtube.com/watch?v=996OiexHze0&t=648s)).
OAuth replaced it with a token that is **scoped** (only these permissions), **expiring**, and
**revocable independently of the password** (S3 `n1`, `n7`).

**Three primitives transfer directly to agents:**

1. **Scopes = least privilege, made explicit and enforced at the resource server.** The client
   enumerates the permissions it needs up front; the issued token is bound to exactly those and the
   API rejects anything beyond them, even with a valid token (S3 `n7`,
   [&t=1549s](https://www.youtube.com/watch?v=996OiexHze0&t=1549s)). The enforcement point is the
   *resource server*, not the client - a distinction that matters when the client is an LLM whose
   behaviour you cannot constrain by construction.
2. **The consent screen = human-in-the-loop, generated from the request.** The authorization server
   builds the consent text *from the scopes the client asked for*, so the human approves a specific
   list rather than a vague connection (S3 `n7`,
   [&t=1428s](https://www.youtube.com/watch?v=996OiexHze0&t=1428s)). Facebook's early
   "connect - yes/no" prompt is the counter-example the talk cites: users could not tell whether they
   were granting profile read or wall-posting (S3, [&t=1463s](https://www.youtube.com/watch?v=996OiexHze0&t=1463s)).
3. **Channel separation = don't put secrets where they can leak.** The browser is trusted to talk to
   a human, never to hold a secret; so the flow deliberately routes user interaction through the
   browser and secret-bearing steps through server-to-server calls (S3 `n5`, `n6`,
   [&t=1989s](https://www.youtube.com/watch?v=996OiexHze0&t=1989s)).

> **The transferable design move: make the untrusted leg carry only useless material.** The
> authorization code crosses the browser precisely *because* stealing it accomplishes nothing -
> redeeming it needs a `client_secret` that never leaves the back channel (S3 `n5`). This is a
> stronger pattern than "encrypt the channel": it assumes the channel *is* compromised and arranges
> for that not to matter. The agent analogue is obvious and mostly unbuilt.

### A standard that gets used for what it was not designed for degrades into non-standard

OAuth was built for delegated authorization only. The industry adopted it for **login** as well,
because it was popular and close enough (S3 `n11`,
[&t=2824s](https://www.youtube.com/watch?v=996OiexHze0&t=2824s)). But OAuth has **no standard way to
return who the user is** - it reasons about permissions, not identity - so every provider bolted on a
proprietary user-info mechanism and the implementations stopped being interchangeable (S3 `n12`,
[&t=2894s](https://www.youtube.com/watch?v=996OiexHze0&t=2894s)). OpenID Connect exists to close
exactly that gap: a thin layer adding an ID token and a userinfo endpoint, triggered by one extra
scope (S3 `n13`, `n14`).

> **Worth carrying into agent protocol design.** The failure was not that OAuth was bad, but that a
> *near fit* got adopted for a use case it did not name, and the gap was closed privately by each
> vendor rather than publicly by the spec. Any protocol currently being stretched to cover agent
> use cases is running the same experiment.

### Containment: when you cannot constrain the actor, constrain where it can stand

S3 answers "how does software act on a user's behalf?" S12 answers a different question that the
first one's open problem forces: **given that you cannot constrain what an agent will decide to do,
how do you constrain what it can reach?**

**The move is to stop trying to police the request and instead pick a boundary the model has no vote
in.** Ordinary multi-tenant SaaS isolates logically - one deployment, a tenant identifier on every
row, a data access layer that appends the predicate. That guarantee is "our code never forgets", and
it survives review because the set of queries is finite and engineer-written. Both halves fail for an
agent: it composes its data access at run time, and the text steering it is attacker-influenceable.
So S12 puts the boundary at the platform's coarsest unit - **one cloud project per business unit** -
where isolation is a fact about topology rather than a property of anyone's code
([S12](../../sources/260802_gcp-multi-tenant-agentic-ai/LEARNING.md) `n2`, claim 101).

**The load-bearing primitive is a boundary on the *principal*, not on the resource.** Ordinary IAM is
additive and distributed: what an identity can reach is the union of grants many people made over
time, so no IAM query answers "may this principal be here at all". A **Principal Access Boundary**
caps the resources a set of principals may touch whatever else grants them access, and S12 points it
squarely at the agent runtime - "to ensure that the agent can't access other tenant projects or
unauthorized Google Cloud services" (S12 `n4`, claim 102).

> **Why that is the right shape, stated as the design rationale rather than the mechanism:** the
> failure being defended against is not "someone wrote a bad grant". It is **"the agent was talked
> into using a grant that legitimately exists"** - and no amount of grant review catches that, because
> the grant is correct. Only a subtractive, central cap does.

**Prompt filtering is placed at the network edge**, wired into the load balancer through Service
Extensions, so a prompt is inspected in the same component and at the same stage as the WAF, before
any application code runs (S12 `n6`, claim 103). Unbypassable by application bugs and uniform across
tenants - **and bounded in a way the source does not state: the edge sees the request, not the
assembled prompt.** Indirect injection arriving in a retrieved document or a tool result never crosses
it. *(That bound is this brain's reading.)*

### The claim worth carrying out of S12: sharing converts a guarantee into an obligation

S12's second half offers four cheaper variants - shared model endpoint, shared MCP server, one Model
Armor instead of two, private ingress. They read as four independent decisions about cost, networking
and ops. **They are one trade made four times**, and the trade is not "less isolation for less money".
It is a change in what *kind* of thing the guarantee is (claim 106).

| | Component inside the tenant | Component shared |
|---|---|---|
| The guarantee is | a property of **where it sits** | a claim about **an implementation** |
| It holds | even if the component is carelessly written - there is nothing across the wall to reach | only if identity is attached, propagated unforgeably, and authorized correctly, **on every call** |
| The cost is | visible and countable: N copies, N patch cycles, N onboardings | **a category of defect**, surfacing later, in someone else's incident |

**That asymmetry is why the cheap branch wins arguments it should lose.** One side's cost appears in a
budget; the other's appears in a postmortem. The useful question at any per-tenant-or-shared fork is
therefore not "is this cheaper" but **"what exactly now enforces what the perimeter used to?"** - and
if nobody can name it in one sentence, nothing does.

**S12 recommends the shared side four times and names no mechanism once.** Its own words for the
hardest instance: you "securely propagate the end-user identity from the agent in the tenant project to
the shared MCP server", which then "uses the propagated user identity to enforce fine-grained access
control on the backend system" (S12 `n10`, `n11`, claims 105-106). No token format, no exchange, no
audience restriction, no delegation model, and no answer for the agent running on a schedule with no
user present.

> **This is the note's two halves colliding, and it is the most useful thing in it.** S3 solved
> delegated authorization for a human at a browser in 2012 - scoped tokens, enforcement at the resource
> server, consent generated from the request, channel separation. This note's standing open question is
> what survives when the client is non-deterministic and the human is absent. **S12 is that question
> arriving in a production architecture diagram**, four times, with the requirement stated and the
> protocol missing. The gap is the field's, not the document's.

**And a guarantee whose truth depends on which variant you took is the genre's characteristic failure.**
S12's use case says flatly that "even if an agent identity is compromised, the agent can't access
unauthorized Google Cloud resources". True of the drawn topology; not true unqualified once you take
the alternatives recommended three sections later, which are never cross-referenced (S12 `d3`). **Read
a reference architecture back to front - alternatives first, then the headline.**

### The retrieval store is an input, and attacking it is cheaper than attacking anything else

**The note's first measured attack, and it lands exactly where the open question below said the hole
was.** S16 poisons an agent's memory or RAG knowledge base so that a chosen trigger phrase, appearing
anywhere in a user query, causes the agent to retrieve attacker-written demonstrations and act on them
([S16](../../sources/260804_agentpoison/LEARNING.md) `n1`, claim 135).

Start with why the store counts as input at all, because that framing is the contribution. An agent
encodes the user's query, fetches the k nearest records, and pastes them into the prompt as
demonstrations. **Retrieval is therefore a mechanism for selecting text that will function as
instruction, and the selection is made by geometry rather than by any judgement about trust.** Whoever
can write one record has written into the prompt of every future query that retrieves it.

The reason this had not been exploited well before is that retrieval is accidentally robust. An
attacker dumping malicious documents into a corpus must win a similarity contest against the whole
benign corpus for every query they care about, which historically meant a high poisoning ratio and
visible damage to benign accuracy. S16's move is to stop competing. It optimises the trigger so that
triggered queries land in a region of the embedding space that is **unique**, meaning far from where
benign queries fall, and **compact**, meaning they all land together (claim 137). The poison goes at
those coordinates, and retrieval then succeeds by construction.

> **The property that makes it effective is the same one that makes it quiet.** A region no benign
> query visits is never retrieved for benign traffic, so the attack does not trade stealth against
> strength the way corpus poisoning does. That is unusual and it is why the benign-accuracy column
> stays flat while the attack rate is high (claim 137, S16 `n12`).

**Three consequences matter more than the headline attack rate, and each removes a defence someone is
currently relying on.**

The first removes volume detection. A single poisoned record yields roughly 62% retrieval success and
a single-token trigger roughly 79%, with benign accuracy above 90% throughout (claim 138). Any monitor
watching for bulk ingestion, anomalous write rates or near-duplicate clusters is calibrated for an
attacker who needs many records, and has nothing to fire on against one. **Scale was what volume-based
detection was implicitly counting on.**

The second removes keeping your embedder private. The trigger transfers to retrievers it was never
optimised against, including a black-box commercial embedding API, at roughly 0.68-0.78 retrieval
success (claim 139). The paper lists white-box embedder access as its one limitation and then largely
dissolves it, so privacy of the embedder raises attacker cost by 10 to 20 points rather than from
possible to impossible.

The third removes perplexity filtering, and it generalises furthest. A coherence term in the objective
yields triggers that read as ordinary language - the driving agent's is **"Be safe and make a
discipline."** against GCG's `tomcat]$. Comment Helen Cortversions <?` - whose perplexity distribution
overlaps benign traffic while GCG's sits visibly apart (claim 140). The filter was never defeated by
cleverness. **The optimiser was simply asked to stop producing the artifact the filter measures**, and
any detector keyed to an artifact of an attacker's tooling has the same weakness.

That leaves the one defence built for this threat, and here the finding is a prediction rather than a
measurement. **Isolate-then-aggregate** runs the model separately against each retrieved record and
aggregates, which works while poison is a *minority* of the retrieved set. S16 counts a retrieval
successful only when **all** k neighbours are poisoned, and claim 138 is why that is affordable
(claim 141, `single-leg`). **The defence rested on an assumption about attacker economics, and a
better optimiser invalidated the estimate.** Worth noting the paper asserts this and never runs the
defence against itself, which makes it the most valuable open experiment in this note.

> **This is claim 106 arriving with a measurement.** S12 records that sharing a component converts a
> structural guarantee into an enforcement obligation nobody has specified. A shared retrieval store is
> exactly such a component, and S16 is what the unspecified obligation looks like when someone attacks
> it. The two sources never mention each other and are describing the same hole from opposite sides.

### The general case: retrieved data is executable, and the adversary never appears

S16 attacks one component. **S17 names the property that makes every such attack possible**, and it is
the framing the field has been built on since:  when augmenting an LLM with retrieval, "*processing*
untrusted retrieved data would be analogous to *executing* arbitrary code, and the line between *data*
and *code* would get *blurry*" ([S17](../../sources/260804_indirect-prompt-injection/LEARNING.md)
`n1`, claim 142).

Take that seriously and the defensive position collapses in a specific direction. There is no
parameterised prompt available - a context window is one flat token sequence, and instruction
following is a learned disposition rather than a parser with a grammar - so the SQL-injection fix has
no analogue here. **The equivalence earns itself by predicting the capability list correctly**, which
is a stronger argument than asserting it: code execution buys persistence, propagation, remote
control, exfiltration and denial of service, and S17 demonstrates a working instance of each on real
deployed products including Bing Chat on GPT-4 and GitHub Copilot (claim 146).

The consequence for who you are defending against is the part that invalidates existing controls.
Every pre-2023 mitigation assumed the adversary was the **user**, because the user was the only party
talking, and filtering, refusal, rate limiting and banning all presume you can identify a malicious
requester. Indirect injection removes them from the session entirely: they write text onto a page and
wait for somebody else's agent to fetch it, so **there is no account to suspend and no request to
block** (claim 143). The request that carries the payload was issued by the victim's own application,
to a source it trusts, as part of working correctly.

**That is why the taxonomy is worth having, and why nothing in it is novel.** S17 adapts the classical
cyber-threat categories and asks what each becomes when the compromised component is a model with
tools, producing information gathering, fraud, intrusion, malware, manipulated content and
availability, across four injection methods and four affected parties (claim 144). No new *category*
of harm appears. What is new is that a text generator turns out to occupy the architectural position
of a host an attacker has landed on.

Two findings then make the attacker's economics worse than the taxonomy suggests. The first is that
**the attacker states the goal and the model supplies the method**: prompted only to persuade the
user without arousing suspicion, Bing Chat invented its own urgency, authority and flattery cues that
nobody specified (claim 147). Attack quality therefore scales with model capability at no cost to the
attacker, which inverts the usual relationship where effort tracks sophistication. The second is that
**the model's follow-up API calls reinforce the injection** - told to suppress a source, it issued its
own searches and returned material arguing that source had lost credibility, laundering the injection
through what looks to the user like independent retrieval.

> **And the practical lesson sits in a place most teams have already got wrong.** Bing Chat **did**
> filter its chat channel; the authors confirm prompts typed directly were caught and the session
> terminated. The same prompts arriving inside a retrieved page went through, because the retrieval
> path had been classified as **data plumbing rather than as input** (claim 148). The control has to
> sit **between retrieval and the context window, on the assembled prompt**, since that is the only
> point that sees the untrusted text in the form the model will receive it.
>
> **This independently confirms a bound this brain wrote as its own commentary.** Against S12's
> claim 103 this note recorded that edge filtering "sees the request, not the assembled prompt, so
> indirect injection arriving in a retrieved document or a tool result never crosses it", flagged at
> the time as the brain's reading rather than the source's. S17 is that reading confirmed on a
> shipped product by an unrelated team - and the commentary was written from architecture alone,
> before this brain held any source that had tested it.

## Key claims

| Claim | Threat / mitigation | Sources (cited) | Confidence |
|---|---|---|---|
| Credential sharing is the anti-pattern OAuth exists to kill: passwords are unscopable, unrevocable and unexpiring | threat: over-broad permissions | S3 `n1` [&t=648s](https://www.youtube.com/watch?v=996OiexHze0&t=648s) | OK (corroborated) |
| Scopes bind a token to a named permission set; the resource server rejects out-of-scope use even with a valid token | mitigation: least privilege | S3 `n7` [&t=1549s](https://www.youtube.com/watch?v=996OiexHze0&t=1549s) | OK (corroborated) |
| The consent screen is generated from the requested scopes, so approval is specific rather than blanket | mitigation: human-in-the-loop | S3 `n7` [&t=1428s](https://www.youtube.com/watch?v=996OiexHze0&t=1428s) | OK (corroborated) |
| Secrets must never traverse the front channel; the flow is split so the untrusted leg carries only a code that is useless without a back-channel secret | mitigation: channel separation | S3 `n5`, `n6` [&t=1937s](https://www.youtube.com/watch?v=996OiexHze0&t=1937s) | OK (corroborated) |
| PKCE lets a client that cannot hold a secret still prove it initiated the flow | mitigation: public-client hardening | S3 `n18` [&t=3562s](https://www.youtube.com/watch?v=996OiexHze0&t=3562s) | OK (corroborated) |
| OAuth has no standard identity mechanism, so authentication use drove vendor-specific extensions and broke interoperability | threat: protocol drift | S3 `n12` [&t=2894s](https://www.youtube.com/watch?v=996OiexHze0&t=2894s) | needs-check (single-leg) |
| Delegating authn to an authorization server decouples it from the app so both can evolve separately | design: separation of concerns | S3 `n19` [&t=3527s](https://www.youtube.com/watch?v=996OiexHze0&t=3527s) | needs-check (single-leg) |
| An agent's tenancy boundary cannot be a query predicate, because the query is composed at run time from attacker-influenceable text; put it at the platform's own resource boundary | mitigation: containment | S12 `n2` (claim 101) | emerging (T2 vendor, unmeasured; the derivation is this brain's) |
| Bound the **principal**, not the resource - IAM is additive and distributed, so only a subtractive central cap answers "may this identity be here at all" | mitigation: blast radius | S12 `n4` (claim 102) | emerging on the mechanism; the "even if compromised" guarantee is **single-leg and conditional on topology** (S12 `d3`) |
| Prompt-injection filtering can live at the network edge, in the same component as the WAF - unbypassable by app bugs, but it sees the request and not the assembled prompt | mitigation: input filtering | S12 `n6` (claim 103) | emerging; **the bound is this brain's reading** |
| Sharing a component converts a structural guarantee into an enforcement obligation, and the two costs are asymmetric - one is countable, the other is a class of defect | design: where the boundary sits | S12 `n10`, `n11`, `n14` (claim 106) | emerging - **the most transferable claim in S12 and one it never asserts** |
| A retrieval store is an attack surface with the properties of a prompt: retrieved records enter context as instruction, selected by geometry rather than by trust | threat: memory / KB poisoning | S16 `n1`, `n11` (claim 135) | OK (corroborated) - **the note's first measured attack** |
| Poisoning the retriever needs no model access and no training; the optimisation targets the embedder | threat: attack surface placement | S16 `n2` (claim 136) | OK (corroborated) |
| The mechanism is geometric - map triggered queries into a **unique** and **compact** embedding region, then put the poison at those coordinates | threat: mechanism | S16 `n3`, `n14` (claim 137) | OK (corroborated) |
| **One poisoned record and a one-token trigger are close to sufficient**, which removes the volume signal that anomaly detection depends on | threat: detection evasion | S16 `n5` (claim 138) | OK (corroborated) - **the most consequential number here** |
| Triggers transfer to embedders they were never optimised on, including black-box APIs, so a private embedder is not a mitigation | threat: transferability | S16 `n6` (claim 139) | OK on the matrix; the distributional explanation is argued, not measured |
| A fluency constraint defeats perplexity filtering by removing the property the filter measures | threat: defence evasion | S16 `n7`, `n8` (claim 140) | OK (corroborated) |
| Isolate-then-aggregate fails against an attacker who poisons **all** k retrieved neighbours, because the defence assumed that was uneconomic | mitigation: **known-broken** | S16 `n10` (claim 141) | **needs-check** - argued from the success criterion, never run against the defence |
| **Processing untrusted retrieved data is analogous to executing arbitrary code**, because data and instructions share one undifferentiated channel and there is no parameterised prompt | threat: the root property | S17 `n1` (claim 142) | OK (corroborated). **The framing everything else follows from** |
| Indirect injection removes the adversary from the session: no account, no request, no rate limit, because the fetch was issued by the victim's own application | threat: attacker position | S17 `n2` (claim 143) | OK (corroborated) |
| The classical threat taxonomy transfers wholesale - six threat classes, four injection methods, four affected parties including the model itself | framework | S17 `n3` (claim 144) | OK (corroborated) |
| **Agent memory is a persistent compromise surface and a session reset does not clear it** | threat: persistence | **S17 `n6` + S16 `n1`, `n5`, `n11`** (claim 145) | **OK - corroborated by 2 independent sources.** The pair this topic's status rests on ([ADR-0019](../decisions/0019-agent-security-established.md)) |
| Worms, command-and-control and multi-stage payloads all demonstrated on real deployed products | threat: malware playbook | S17 `n5`, `n7`, `n9` (claim 146) | OK as demonstrations; **unquantified** (`d1`) |
| The attacker states the goal and the model supplies the method, so attack quality scales with model capability for free | threat: economics | S17 `n10`, `n11` (claim 147) | OK (corroborated) |
| **Input filtering fails by sitting on the wrong channel** - Bing Chat filtered chat and not retrieval, because retrieval was classified as plumbing rather than input | mitigation: **placement** | S17 `n12` (claim 148) | OK (corroborated). **The most actionable defensive claim here**, and it confirms this note's own prior commentary on claim 103 |
| **Secure the system, not the model**: a layer around an untrusted LLM such that an unsafe model cannot cause an unsafe action | **mitigation: the note's first gated defence** | S18 `n1` (claim 149) | OK (corroborated as a design claim) |
| Dual LLM protects control flow and leaves data flow exposed - SQL injection against the parameters, not the structure | threat: why isolation alone fails | S18 `n2` (claim 150) | OK (corroborated) |
| The parameterised-query fix applied to **the program** rather than the prompt: a planner that never sees tool output, and a parser that can only return schema-conforming values | mitigation: architecture | S18 `n3`, `n4` (claim 151) | OK (corroborated) |
| **Authority travels with the data**: capabilities carrying provenance and permitted readers, propagated through a data-flow graph, checked by policy at every tool call | mitigation: information flow control | S18 `n5`-`n7` (claim 152) | OK (corroborated) |
| Structural defence beats heuristic defence - attacks 100-300 down to 0-1, against a tool filter's 8 and an instruction hierarchy's 276 | mitigation: efficacy | S18 `n9`-`n11` (claim 153) | **needs-check - the benchmark is the authors' own** (`d1`, `d3`) |
| The cost is ~3x tokens, against a near-free probabilistic alternative | mitigation: cost | S18 `n12` (claim 154) | OK (corroborated) |
| **An information-flow defence protects actions, not assertions** - fraud and manipulated content are explicit non-goals | **coverage limit** | S18 `n14` (claim 155) laid against S17 `n3` | OK on the non-goals; **the taxonomy mapping is this brain's synthesis** |
| The defence's own authors demonstrate its bypass and predict a return-oriented-programming analogue | limit: known-incomplete | S18 `n15`, `n16`, `n18` (claim 156) | OK (corroborated) |

## Key visuals

![The pre-OAuth anti-pattern: an app asking for your Gmail password](../../sources/260725_oauth2-oidc-plain-english/visuals/frame_640.jpg)

The failure mode in one screenshot - Yelp's signup form requesting the user's actual Gmail password,
with a parenthetical clarifying *which* password. Keep it as the canonical picture of what
"over-broad, non-revocable delegation" looks like in production (S3 `n1`,
[&t=664s](https://www.youtube.com/watch?v=996OiexHze0&t=664s)).

![Two tenant projects side by side, each wrapped in its own principal access boundary, each holding a complete duplicated stack, with no edge between them](../../sources/260802_gcp-multi-tenant-agentic-ai/visuals/fig1b_two-tenants.png)

The containment answer as a picture. Two business units, two projects, each wrapped in its own **PAB**
box, each holding a full duplicated stack - agent runtime, prompt/PII filter, MCP server, datastore,
model endpoint. **The isolation claim is not labelled anywhere in the figure; it is expressed as an
absence of edges**, which is the strongest way a diagram can state it, and the reason to keep this
frame rather than the fuller one. Every arrow entering a tenant descends from the shared frontend.
Note also what makes the cost visible: everything in the yellow box is duplicated in the pink one
(S12 `n2`, `n9`; full walkthrough in the
[source note](../../sources/260802_gcp-multi-tenant-agentic-ai/LEARNING.md)).

![Four scatter plots of a retriever's embedding space: CPA's poison scattered among benign queries, against AgentPoison's triggered queries collapsing into one tight isolated cluster by iteration 15](../../sources/260804_agentpoison/visuals/fig2_embedding_space.png)

**The attack, and the reason it is quiet, in one picture.** Grey is benign queries, red is triggered
queries, blue is the poisoned records. Panel (a) is the old approach, with poison scattered through the
benign mass, which is why it gets retrieved for innocent queries and wrecks benign accuracy. Panels (b)
to (d) are AgentPoison's optimiser finding a **private region of the embedding space** that no benign
query occupies. Once the region exists, a handful of records - or one - covers it, and retrieval stops
being a contest. Keep this as the canonical picture of why a retrieval store needs a threat model
(S16 `n3`, claim 137; full walkthrough in the
[source note](../../sources/260804_agentpoison/LEARNING.md)).

## Open questions / conflicts

- **Does the four-party model survive a non-deterministic client?** OAuth assumes the client is
  software whose behaviour is fixed at build time - it requests scopes its author chose. An LLM agent
  chooses its actions at run time. Scope enforcement still holds at the resource server, but "the
  client asked for what it needs" becomes "the client asked for what it *might* need", which pushes
  every agent toward over-broad grants. **Still unresolved - but S12 changes its status from
  theoretical to blocking.** S12 does not answer it; it **needs** the answer, in production, four
  times over (claim 106), and works around it the only way available: if you cannot constrain what the
  client asks for, cap where the client can stand (claim 102). *That workaround is the current state
  of the art in this brain, and it only holds while every component stays inside the boundary.*
- **What actually propagates an end-user identity from an agent to a shared tool server?** The
  sharpest open question this note has, because it is the one a real deployment hits first. S12 states
  the requirement - "you securely propagate the end-user identity... [the server] uses the propagated
  user identity to enforce fine-grained access control" - and names **no** token format, exchange,
  audience restriction or delegation model (S12 `n11`). Candidates the owner's stated identity track
  will reach: **OAuth 2.1 token exchange, SPIFFE/SPIRE workload identity, the MCP authorization spec**.
  It also sits on top of `mcp.md`'s open question about what an aggregating server owes the servers
  behind it. **The cheapest high-value research target in this note.**
- **What is consent when the user is not present?** The design assumes a human at a browser clicking
  Yes. Long-running or scheduled agents break that. The client credentials flow (S3 `n10`) removes the
  user entirely - but that discards the delegation guarantee that made OAuth worth having. Open.
- **How does MCP's authorization actually build on this?** Believed to rest on OAuth 2.1, but **no
  source in this brain establishes it** - the connection is currently agent commentary, not a cited
  claim. Resolve before promoting anything into `mcp.md`. *(Note: `mcp.md` is no longer empty as of
  S10, but it says nothing about auth beyond a bearer token in a screenshot, so this stands.)*
- **Retrieved tool catalogs create an invisible steering surface, and no source discusses it.** When a
  tool catalog is searched rather than enumerated (S10, [`mcp.md`](mcp.md)), two new facts hold at
  once: the model sees **only a shortlist** it did not choose, and the field that decides that
  shortlist can be **invisible to it**. Foundry's `additional_search_text` is indexed for retrieval
  but explicitly "not visible to models in MCP responses" [S10 §Tuning the search space, `n14`]. So
  whoever writes that field steers which capability the agent is offered, with **no trace in the
  context the model or a reviewer can inspect** - and on an aggregating server, that writer may be
  neither the tool's author nor the agent's owner. Two shapes worth naming: **starvation** (tuning a
  safe tool's aliases so a risky one wins the query) and **substitution** (making an attacker-supplied
  tool the best match for common intents). **Labelled commentary** - S10 never mentions security, and
  no source in this brain measures retrieval-time influence. It is cheap to record now because the
  pattern is new and spreading; it is not yet a claim.
- **Temporal conflict on flow selection (S3 `n17`) - stale, superseded.** The source recommends the
  implicit flow for browser apps; the field has since moved to authorization code + PKCE. Recorded as
  a divergence in the source's `nodes.md`, flagged `do not apply`, and **not promoted as guidance**.
  The correction is currently uncited commentary; **an OAuth 2.1 source is the intended resolution**
  (research pass declined by the owner, 2026-07-25).

- **Shared agent memory is a prompt-injection sink with a demonstrated propagation path, and nothing
  defends it.** A background process that ingests session content and writes durable,
  automatically-applied instructions means **inject once, re-applied to every agent that attaches the
  store**, with no further access needed. This stopped being theoretical with S7: its live demo shows
  agents writing **imperatives** to their successors ("Next agent: skip dep checks, go straight to
  config diff") and the next agent complying [S7 `n20`,
  [`memory.md`](memory.md)]. S7 ships attribution and version history, which are **forensics after the
  fact**; there is **no admission control** - nothing validates a memory before the next agent acts on
  it. Recorded as claim 63 and **labelled commentary**, since neither memory source discusses the
  threat. ~~**The most actionable open question in this note.**~~ **Substantially answered by S16 on
  2026-08-04, and answered worse than feared.** S7's path needed a *cooperating* agent writing an
  imperative to its successor; S16 shows an **external** attacker reaching the same outcome by writing
  **one** record and letting the retrieval step do the work, with no imperative and no cooperation
  (claims 135, 138). **The half that remains open is the defence.** No source here has one: volume
  detection, embedder privacy and perplexity filtering are each independently defeated (claims 138-140),
  and the one purpose-built defence is argued broken rather than shown broken (claim 141). **That
  residue is now the most actionable open question in this note**, restated below.
- **~~What defends against any of this, in 2026?~~ Partly answered by S18 on 2026-08-05, and the
  residue is sharper than the original question.** CaMeL is a real structural defence and it changes
  what remains open in three specific ways. **First, it needs independent evaluation** - every
  efficacy number is on its own authors' benchmark (claim 153), and ingesting AgentDojo will *not*
  fix this because it shares authors. **Second, it covers the action half only** - fraud and
  manipulated content are explicit non-goals (claim 155), and **nothing in this brain addresses
  them**, which is now the largest untouched surface here. **Third, its own authors predict a
  return-oriented-programming analogue against it** (claim 156) and nobody has built one. The
  remaining literature - spotlighting, delimiter schemes, dual-model variants, provenance tracking -
  is still ungated, though S18 measures Spotlighting's cost at 1.06x tokens in passing.
- **The original framing, kept because it is what the pre-S18 state looked like:** S17 walks four candidate defences to their failure points and
  declines to name a solution - alignment training is "Whack-A-Mole" with impossibility results cited,
  filtering retrieved input faces a dilemma where a filter capable enough to decode obfuscation is
  itself injectable, an LLM supervisor must read the untrusted source to judge faithfulness and lands
  in the same position, and interpretability-based outlier detection is offered as a direction rather
  than a method (S17 `n14`, `single-leg`). **That survey is from early 2023.** Everything the field
  has built since - spotlighting, delimiter schemes, dual-model and capability-based patterns,
  provenance tracking - is **entirely ungated here**. Combined with claims 138-141, this note now
  documents that six named defences fail and holds no evidence about any that works. **The highest-
  value research target in the topic.**
- **What actually defends a retrieval store, given that the obvious three do not?** Claims 138 through
  141 close off volume detection, embedder privacy, perplexity filtering and isolate-then-aggregate.
  Two directions are visible from what this brain already holds and neither is tested. The first is
  **admission control on writes**, which is `rag.md`'s claim 95 - a trust signal needs a writer
  restriction - applied as a security control rather than a quality one, and it is structural where
  everything defeated above is detective. The second is **embedding-space anomaly detection**, because
  S16's defining property is that triggered queries form a dense cluster in an otherwise empty region,
  which is a conspicuous geometric signature that no defence in the paper looks for. **Commentary, not
  a claim** - S16 tests neither.

## Note for the architect (topic boundary)

This note now carries three distinguishable bodies of material: **agent-specific threats** (prompt
injection, tool poisoning, memory poisoning - still thin), **the delegated-authorization substrate**
(S3), and **containment / isolation architecture** (S12). They are held together deliberately, per the
"don't spawn a topic per source" rule.

**The split is expected, not hypothetical.** The owner has stated an identity track - **OAuth 2.1,
SPIFFE/SPIRE, AAuth** - so a second identity source is planned rather than possible. The rule still
says wait: a stated intent is not a second source, and creating the note early risks a taxonomy shaped
by a reading list rather than by material. **On the next identity/authorization source, split
`identity-and-authorization` into its own note** (preferred over `delegated-authorization`, since
SPIFFE/SPIRE is workload identity with no delegation and no human) and leave the agent-threat material
here. Record it as an ADR when it happens.

> **S12 was tested against that trigger and is not it**
> ([ADR-0015](../decisions/0015-an-architecture-is-not-an-identity-source.md)). It uses IAM, IAP, PAB
> and identity propagation heavily, and teaches **no identity mechanics at all** - no protocol, no
> token, no flow, no lifetime. It *consumes* identity as a platform primitive and states the one
> requirement it cannot meet. **A source that consumes a subject is not a source on it**, which is
> [ADR-0012](../decisions/0012-a-mention-is-not-a-source.md)'s test applied to a heavier user than a
> mention. The same ADR declines a `multi-tenancy` topic: S12's isolation machinery is generic cloud
> multi-tenancy that would read identically for microservices, and only the agent-specific half
> (claims 101-103, 106) belongs anywhere in this brain.

**What to watch for as that track lands**, since it is the interesting axis rather than the
protocol details:

| Source 1 (this one) | What the rest of the track changes |
|---|---|
| A **human** clicks Yes in a browser | SPIFFE/SPIRE has **no human and no browser** - identity is attested from workload properties, not delegated by a person |
| Consent is **per-flow and interactive** | Workload identity is **continuous and automatic**; agent auth has to answer what consent means for a long-running process |
| The client is **fixed software** that requests scopes its author chose | An agent chooses actions at **run time** - the open question below |

### The first defence that does not ask the model to behave

**Everything above is an attack, and this note carried no gated defence until S18.** Its thesis is a
single reversal: stop trying to make the model safe, and build a system in which **an unsafe model
cannot cause an unsafe action**
([S18](../../sources/260804_camel-prompt-injection-defense/LEARNING.md) `n1`, claim 149).

Start with why the previous generation could not deliver that. Instruction hierarchies, input filters
and delimiter schemes all leave the security decision **inside the model**, which is where the
adversary already is, and S18's verdict on the family is that none of them "provide any guarantee of
security and regularly fall short to new attacks in practice". They are probabilistic, so their
failure rate against a *new* attack is unknown, and a defence with an unknown failure rate cannot be
reasoned about at design time.

The obvious structural fix does better and still leaks. Willison's **Dual LLM** pattern splits the
agent so a privileged model plans while a quarantined model touches untrusted data with no tools, and
that genuinely protects the **plan**. It does not protect the **arguments**: an injection can leave
the action sequence exactly as the user asked for it while the fetched document becomes
`confidential.txt` and the recipient becomes the attacker (claim 150). S18's analogy is the sentence
worth carrying, because it also names the fix - **this is SQL injection against the query parameters
rather than the query structure**, and parameterisation was the answer there.

**S17 said no parameterised prompt is possible, and it was right. S18 applies the constraint one level
down, to the program instead.** A Privileged LLM sees only the trusted user query and emits code,
never seeing tool output at all - it manipulates variables, not their contents - so the plan is
written before any untrusted byte exists. A Quarantined LLM parses the dirty data with no tool access,
and may return **only schema-conforming structured output plus one boolean**, because a free-text
reply would carry the injection straight back into planning (claim 151).

That leaves the gap Dual LLM could not close, and closing it is what makes this more than isolation
done carefully. Every value carries a **capability** recording its provenance and its permitted
readers; a custom interpreter propagates these through a data-flow graph as the program executes; and
an arbitrary Python **security policy** is consulted at every tool call (claim 152). Trace the original
attack through it and the block is mechanical. The plan is unchanged, the extracted values are still
attacker-chosen, and at `send_email` the policy asks whether the document's readers include
`attacker@gmail.com`. They do not, and the call is refused. **Nothing in that chain required the model
to notice the attack.**

> **This is claim 12 arriving from adversarial robustness rather than from reliability**, and the
> convergence is worth noticing. S2 found that what ships in production is small LLM steps inside
> deterministic code. S18 is the security argument for the identical shape. Two unrelated pressures
> push toward the model sitting **inside** a deterministic harness rather than around one.
>
> **It is also claim 106's enforcement obligation, finally specified.** S12 recorded that sharing a
> component converts a structural guarantee into an obligation nobody has named. S18 names it: it is a
> Python policy file, and somebody owns it. The obligation did not disappear, it acquired a location.

**What it costs is measured, and the honest framing is a comparison rather than a number.** CaMeL
needs **2.82x input and 2.73x output tokens** for the median task, the highest of the defences
compared, against Spotlighting's 1.06x which is close to free (claim 154). Utility falls from 84% to
77% while successful attacks fall from 100-300 to 0-1 (claim 153). So the choice is not "secure or
insecure" but **"nearly free and probabilistic, or roughly 3x and structural"** - and most of the
overhead is re-prompting the planner to fix invalid code, which should shrink as models improve.

> ⚠️ **The efficacy numbers are measured on the authors' own benchmark**, and this is the governing
> caveat. Debenedetti first-authors both CaMeL and **AgentDojo**; Tramèr co-authors both; and the
> baseline defences were implemented by CaMeL's authors (S18 `d1`, `d3`). Nothing is concealed and it
> is normal practice. Under the independence rule it is **self-report, not validation**, so claim 153
> is `needs-check` despite large effect sizes. **The design claims are unaffected** - an architecture
> is checkable against its own figures regardless of who ran the benchmark - which is why claims
> 149-152 are `corroborated` and 153 is not.

**And the coverage gap is where this note should be most careful, because it is not where you would
guess.** Laid against S17's six threat classes, S18 structurally covers information gathering,
intrusion and malware, since each requires a tool call and every tool call meets a policy. It
**explicitly cannot** cover **fraud** or **manipulated content**, because an injection whose entire
payoff is text shown to the user violates no capability and fires no policy, and it does not address
**availability** at all (claim 155).

| S17 threat class | Covered by S18? |
|---|---|
| Information gathering (exfiltration) | **Yes** - the design's primary target |
| Intrusion (API calls, persistence, C2) | **Yes** - every tool call passes a policy |
| Malware (worms, spreading injections) | **Yes** - the worm needs `read_address_book` then `send_email` |
| Fraud (phishing, scams) | **No - explicit non-goal** |
| Manipulated content (wrong summaries, disinformation) | **No - explicit non-goal**, and S17's largest class by instance count |
| Availability (DoS, muting) | **Not addressed**, and 2.82x tokens arguably worsens the economics |

**The pattern is that an information-flow defence protects actions and not assertions.** That is what
a system built on information flow control should be expected to do, and it means half of S17's
taxonomy is untouched by the best structural defence this brain holds. *(The mapping is this brain's
synthesis; neither paper draws it.)*

Finally, and it is the reason to trust this source more than its numbers: **the authors demonstrate
their own bypass.** §6.4 shows that when the *user's own query* asks an agent to follow instructions
found in data, the planner faithfully writes a program that dispatches on untrusted content, turning
data flow back into control flow. They then draw the analogy against themselves - Control Flow
Integrity was bypassed by return-oriented programming, chaining individually-valid fragments, and they
expect an analogue (claim 156). §9.3 is titled "So, Are Prompt Injections Solved Now?" and answers
"No".

![The indirect prompt injection threat taxonomy: four injection methods, six threat classes, and four affected parties including the LLM itself](../../sources/260804_indirect-prompt-injection/visuals/fig2_taxonomy.png)

**The threat map for this whole topic, on one page.** Injection methods on the left are how the
payload arrives (passive by retrieval, active by sending, user-driven, hidden). The six threat classes
across the bottom are the classical cyber-threat categories asked anew of a model with tools, with
"Spreading injections (*Prompts as worms*)" sitting under Malware. Affected parties on the right
include **the LLM itself**, which is unusual in a threat taxonomy and follows from availability
attacks that make the model useless without harming anyone else. Keep this as the canonical
enumeration of the surface (S17 `n3`, claim 144; full walkthrough in the
[source note](../../sources/260804_indirect-prompt-injection/LEARNING.md)).

## Sources feeding this topic

- **S18** - [CaMeL: Defeating Prompt Injections by Design](../../sources/260804_camel-prompt-injection-defense/LEARNING.md)
  (Debenedetti, Shumailov, Fan, Hayes, Carlini, Fabian, Kern, Shi, Terzis, Tramèr; Google + Google
  DeepMind + ETH Zurich, arXiv 2025-03-24). **The note's first gated defence.** Secure the system
  rather than the model: a planner that never sees tool output, a parser that returns only
  schema-conforming values, capabilities carrying provenance and permitted readers, and a Python
  policy consulted at every tool call (claims 149-156). **T3 preprint.** **⚠️ Its efficacy numbers are
  measured on AgentDojo, whose first author is CaMeL's first author** (`d1`) - self-report, not
  validation, which is why claim 153 is `needs-check` while the design claims are not. Note also the
  vendor position: the thesis that scaffolding beats model-hardening favours a platform provider.
  **Read it for the shape, which is excellent, rather than for the score.** Unusually honest -
  explicit non-goals, a demonstrated bypass of its own isolation, and a section titled "So, Are
  Prompt Injections Solved Now?" that answers "No".
- **S17** - [Indirect prompt injection](../../sources/260804_indirect-prompt-injection/LEARNING.md)
  (Greshake, Abdelnabi, Mishra, Endres, Holz, Fritz; Saarland / CISPA / sequire technology, arXiv
  2023-02-23, v2 2023-05-05). **The source that moved this topic to `established`, and the paper that
  named indirect prompt injection.** The data-instruction blur, the threat taxonomy, goal-only
  payloads, worms and persistence and C2, and the filter-on-the-wrong-channel finding (claims
  142-148). Demonstrated on **real deployed products** - Bing Chat on GPT-4, GitHub Copilot - with
  responsible disclosure to OpenAI and Microsoft. **T3 preprint** (no journal reference on the arXiv
  listing at ingest). **⚠️ Entirely qualitative: no success rate, no sample size, no statistics for
  any of the six threat classes** (`d1`), and the most striking results run against a black-box
  product the authors concede they cannot reproduce exactly (`d2`). Its **mitigations survey is
  three years old and is its weakest material** - read it as "no solution existed in early 2023, and
  here is why each obvious one is hard", never as a current statement.
- **S16** - [AgentPoison](../../sources/260804_agentpoison/LEARNING.md) (Chen, Xiang, Xiao, Song, Li;
  U Chicago / UIUC / U Wisconsin / UC Berkeley, arXiv 2024-07-17). **The note's first measured attack,
  and its first source with no commercial position in what it claims.** Retrieval as attack surface,
  the geometric mechanism, the single-record threshold, transferability across embedders, and the
  defeat of perplexity filtering (claims 135-141). **T3 preprint** - the PDF reads "Preprint. Under
  review." and the arXiv listing carried no journal reference at ingest. Read it for the mechanism,
  which is well evidenced, and hold the efficacy accounting loosely: the benign-cost headline is an
  average hiding a four-point worst case (`d1`) and the end-to-end success rate exceeds the action
  success rate threefold on two agents with no explanation (`d2`). **Everything in it is internal to
  one paper** - no external corroboration was gathered and the companion repo was not cloned.
- **S12** - [Multi-tenant agentic AI system](../../sources/260802_gcp-multi-tenant-agentic-ai/LEARNING.md)
  (Google Cloud Architecture Center, reviewed 2026-06-18). **The containment half of this note, and the
  first source here that is about defending a running deployment rather than a protocol.** Isolation
  stacked at three scopes, the principal boundary as the answer to a compromised agent identity, prompt
  filtering at the network edge, and the structural-to-enforced framing (claims 101-103, 106).
  **T2 vendor reference architecture with no measurement of any kind** - no latency figure, no cost
  figure, no incident, no named deployment - and both corroboration legs are the same team's prose and
  the same team's diagram, so `corroborated` there means only that the document is self-consistent.
  Read it for the shape and the trade, never as evidence that the shape works.
- **S7** - [Memory and dreaming for self learning agents](../../sources/260731_claude-memory-dreaming/LEARNING.md)
  (Anthropic, 2026-05-21). **Does not discuss security at all** - it feeds this note only through the
  open question above, where its demo of agents passing *imperatives* through a shared memory store
  supplies a concrete propagation path for memory poisoning (claim 63, commentary). Full synthesis in
  [`memory.md`](memory.md).
- **S3** - [`260725_oauth2-oidc-plain-english`](../../sources/260725_oauth2-oidc-plain-english/LEARNING.md)
  - Nate Barbettini (Okta), *OAuth 2.0 and OpenID Connect (in plain English)*, 2018. The protocol
    substrate: delegated authorization, scopes, consent, channel separation, OIDC. **8 years old -
    mechanics current, flow-selection advice partly superseded.**
