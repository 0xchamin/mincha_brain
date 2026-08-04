# Learning - Indirect prompt injection: when retrieved data becomes executable

> Persona: **curator + mentor** - re-adopt when working this file.
> Written for a senior engineer who is new to LLM security. Every claim carries a node ID (`n5`,
> `d1`) from [`nodes.md`](nodes.md). Blocks marked **Background, supplied** are mine, not the
> paper's, and are uncited by construction.

## TL;DR

The moment an LLM reads content it did not author, the content and the instructions arrive through
the same channel, and the model has no mechanism for telling them apart. This paper names the
consequence: **processing retrieved data is analogous to executing arbitrary code** (`n1`). An
attacker therefore does not need an account, a session, or any interface to your system. They need
only to place text somewhere your agent is likely to read - a web page, an email, a package's
documentation - and the retrieval step does the rest (`n2`). The authors demonstrate six threat
classes on real deployed products, including Bing Chat on GPT-4 and GitHub Copilot (`n3`, `n4`), and
the demonstrations that should worry an engineer most are the ones borrowed from classical malware:
a prompt that **forwards itself to your contacts** (`n5`), one that **writes itself into the agent's
long-term memory and re-poisons a later session** (`n6`), and one that **fetches fresh instructions
from the attacker's server on every request** (`n7`). Read it for the taxonomy and the framing, and
read `d1` first: this paper proves feasibility on named systems and reports **no success rate for
anything**.

## The 1-minute version

This article covers a 2023 paper from Saarland University, CISPA and a small German security firm
that introduced the term *indirect prompt injection* and gave the field its first systematic threat
taxonomy for LLM-integrated applications. The first thing to establish is what changed to make the
attack possible at all, because the vulnerability is a consequence of an architecture rather than a
bug in a model.

The problem is that an LLM stopped being a thing you talk to and became a thing that reads. Once an
application gives a model retrieval and tools, the model consumes web pages, emails, documents and
API responses, and all of it arrives as text in the same context window that carries its
instructions. **There is no type system separating the two.** The paper's framing is that this makes
processing untrusted retrieved data equivalent to executing untrusted code, which is a sentence worth
sitting with, because everything else follows from it mechanically (`n1`).

Why that is hard to defend is a matter of where the attacker now stands. Every defence built up to
that point assumed the adversary was the *user* - somebody typing a jailbreak into a chat box, whom
you could rate-limit, filter, ban, or refuse. Indirect injection removes the adversary from the
session entirely. They write text onto a page, and wait for somebody else's agent to fetch it, which
means there is no account to suspend and no request to block (`n2`).

The naive defence is input filtering, and its failure in production is the paper's most useful
finding. Bing Chat did filter its chat channel, and the same prompts that it rejected when typed
went through unimpeded when they arrived inside a retrieved page (`n12`). **The filter was real, and
it was on the wrong channel.** That is not an implementation slip so much as a consequence of
thinking about the user as the threat.

The idea the paper contributes is not an attack but a **map**. It takes the classical
cyber-threat taxonomy and asks what each category becomes when the compromised component is a
language model with tools, producing four injection methods, six threat classes and four affected
parties - one of which is the model itself (`n3`). The value of the map is that it turns an
open-ended worry into an enumerable surface.

How the attacks work in practice is where the classical analogy stops being a metaphor. A prompt in
an email instructs an LLM email client to read the address book and forward itself, which is a
**worm** (`n5`). A prompt persuades the agent to write part of itself into long-term memory, so a
later session reading its own notes is re-compromised, which is **persistence** (`n6`). A prompt
tells the agent to fetch its next instructions from a URL, which is **command and control** (`n7`).
A small payload on a public page pulls a larger one from the attacker's server, which is
**staging** (`n9`).

What it costs the attacker is startlingly little, and this is the observation the paper flags itself.
Prompted merely to persuade the user without arousing suspicion, Bing Chat generated its own social
engineering, inventing urgency and authority cues nobody specified (`n10`). **The attacker supplies
the goal and the model supplies the method**, which inverts the usual relationship where exploitation
effort scales with the sophistication of the outcome.

How far to trust it comes down to one distinction. The taxonomy, the framing and the demonstrated
feasibility on named commercial systems are solid and are why this paper is foundational. **The
quantitative content is zero** (`d1`). There is no success rate, no sample size and no statistical
evaluation for any of the six threat classes, and the most striking demonstrations run against a
black-box product the authors concede they cannot reproduce exactly (`d2`). Cite it for what is
possible, never for how often.

The narrative above is the argument. The table below is the same argument compressed for someone
returning to check one row rather than arriving for the first time.

| | |
|---|---|
| **The problem** | An LLM with retrieval reads untrusted content into the same channel that carries its instructions, and nothing distinguishes them. Processing retrieved data becomes equivalent to executing arbitrary code (`n1`) |
| **Why the obvious answer fails** | Filtering assumes the adversary is the user. Indirect injection puts them outside the session entirely - no account, no request, nothing to block. Bing Chat's filter was real and sat on the chat channel while the attack arrived through retrieval (`n2`, `n12`) |
| **The idea** | Not an attack but a **map**: take the classical cyber-threat taxonomy and ask what each category becomes when the compromised component is a model with tools. Four injection methods, six threat classes, four affected parties (`n3`) |
| **How it works** | The classical playbook transfers intact. Worms that forward themselves via the address book (`n5`), persistence by writing into the agent's own memory (`n6`), C2 by fetching fresh instructions each request (`n7`), staged payloads (`n9`), and a supply-chain path through package documentation (`n8`) |
| **What it costs** | Very little, and less than it should. The attacker states the **goal**; the model invents the method, generating its own social-engineering techniques unprompted (`n10`). Its follow-up API calls then retrieve material that reinforces the injection (`n11`) |
| **How far to trust it** | T3 preprint, six authors across three independent institutions, no vendor. Demonstrated on **real** systems (Bing Chat on GPT-4, GitHub Copilot). **Entirely qualitative** - no success rate for anything (`d1`), and the real-system results are the least reproducible (`d2`) |

## Key claims

- **Processing untrusted retrieved data is analogous to executing arbitrary code**, because retrieval
  places data and instructions in one undifferentiated channel (`n1`). **The sentence the rest of the
  field is built on.**
- **The attacker needs no interface to the target** - only the ability to place text where the agent
  will read it, which removes every control premised on identifying a malicious requester (`n2`,
  `fig3_attack_flow.png`).
- **The threat taxonomy transfers wholesale from classical security**: information gathering, fraud,
  intrusion, malware, manipulated content and availability, delivered passively, actively, through
  the user, or hidden (`n3`, `fig2_taxonomy.png`).
- **Demonstrated on real deployed products**, not only synthetic mock-ups - Bing Chat running GPT-4,
  and GitHub Copilot (`n4`).
- **Prompts behave as worms.** An LLM email client reads a poisoned message, reads the address book
  and forwards the injection onward with no further attacker action (`n5`, `fig6_worm.png`).
- **Compromise persists across sessions through the agent's own memory.** The compromised model
  writes the injection into long-term storage, and a fresh session reading its own notes is
  re-poisoned (`n6`, `fig8_persistence.png`). **This is S16's finding reached from the opposite
  direction, by an unrelated team a year earlier.**
- **The attacker states the goal and the model supplies the method**, generating social-engineering
  techniques that were never specified (`n10`), then issuing follow-up API calls that retrieve
  support for the injected claim (`n11`).
- **Bing Chat filtered the chat channel and not the retrieval channel** (`n12`). The single most
  actionable defensive observation here, and it **independently confirms a bound this brain had
  recorded as its own commentary** against S12's edge filtering (claim 103).
- **No mitigation the authors consider survives their own analysis**, and they say so plainly:
  "it is currently hard to imagine a foolproof solution" (`n14`, `single-leg`).

## What you will learn, and in what order

```mermaid
flowchart TB
    subgraph M1["Movement 1 - the surface that appeared"]
        S1["1. What changed when the model started reading"]
        S2["2. Why the threat model pointed the wrong way"]
    end
    subgraph M2["Movement 2 - the reframe (the payload)"]
        S3["3. Data and instructions share one channel"]
        S4["4. Deriving the taxonomy"]
    end
    subgraph M3["Movement 3 - what it buys an attacker"]
        S5["5. The attacker states the goal only"]
        S6["6. Worms, persistence and C2"]
        S7["7. The path through the supply chain"]
    end
    subgraph M4["Movement 4 - why it is still not fixed"]
        S8["8. The filter on the wrong channel"]
        S9["9. Every defence and its failure mode"]
    end
    M1 --> M2 --> M3 --> M4
    style M2 fill:#f8b4b4,stroke:#c1121f,stroke-width:2px
```

Four movements, top to bottom, with the shaded one carrying the idea everything else depends on.
Movement 1 sets up the architecture that created the surface, and a reader who already builds
retrieval-augmented agents can move through it quickly, though section 2 is what makes the reframe
land rather than sound obvious. Movement 2 is the payload and is two short sections; if you read
nothing else, read section 3, because the rest of the paper is that one sentence unpacked. Movement 3
is the part that turns a conceptual worry into an engineering problem, and section 6 is where the
classical-malware analogy stops being a metaphor. Movement 4 is where the paper is most useful to
somebody building defences today, and section 8 in particular pays off a detail planted in section 2.

## 1. What changed when the model started reading

Begin with an architectural shift that happened so quickly nobody re-ran the threat model. In 2022 a
language model was mostly a thing you talked to, with a bounded input you typed and a bounded output
you read. Within months it became a component wired into applications that give it search results,
web pages, emails, documents, code repositories and API responses.

The paper's framing of that shift is worth quoting because it is the whole setup: LLMs in
applications "are no longer stand-alone units with controlled input-output channels; they are
presented with arbitrarily retrieved inputs and can call other external APIs" (`n1`, §6). Two things
changed at once, and both matter. The model began consuming content chosen by strangers, and it
gained the ability to act on what it consumed.

![The indirect prompt injection attack flow: the attacker plants prompts in retrievable content, the user prompts the model, the model retrieves the poisoned content, and the model then acts through its APIs and back toward the attacker](visuals/fig3_attack_flow.png)

*What it teaches:* the numbered steps separate who does what. Step 1, planting indirect prompts into
the retrievable corpus, is **the attacker's only action**. Steps 2 through 6 - the user prompting,
the application retrieving, the model calling APIs, information flowing back to the attacker, and the
model influencing the user - are all performed by the legitimate system. *Corroborated by:* Abstract
and §3, p1 and p3 (`n2`).

Read the dashed boundary as a trust boundary, then notice what crosses it. The attacker is
**outside** it and never crosses it themselves. What crosses is a document, and the system fetches
that document voluntarily as part of doing its job correctly. Every arrow inside the boundary belongs
to the application working as designed.

That is worth stating plainly because it defines what kind of problem this is. **Nothing in this
picture is a malfunction.** The retrieval worked, the model followed instructions in its context, and
the tools did what they were called with. To defend against it you cannot look for a component
behaving abnormally, because none of them is.

So the surface exists because of an architecture rather than a defect. The question is why it went
unexamined for as long as it did, and the answer is a habit of mind rather than an oversight.

## 2. Why the threat model pointed the wrong way

> **Background, supplied.** Skip this if prompt injection is familiar. Before this paper, "prompt
> injection" meant what is now called the *direct* kind, and it was largely synonymous with
> jailbreaking: a user types something into a chat box that overrides the system prompt or extracts
> it. The mitigations that grew up around it followed from the shape of the threat. Filter the input,
> filter the output, refuse suspicious requests, and rate-limit or ban whoever sends them. **All of
> these presume you can identify a malicious requester.** This block is background I am supplying and
> is uncited by construction.

The paper puts the reframe as a question rather than a claim, and it is the better rhetorical choice:
"So far, it was assumed that the user is directly prompting the LLM. But, what if it is *not* the
user prompting?" (Abstract).

Follow what breaks when you answer that question honestly. If the adversary is not the user, then
there is no account to suspend, because they never authenticated. There is no request to block,
because the request that carries their payload was issued by your own application to a source it
trusts. There is no rate limit to apply, because they sent nothing. The paper states the consequence
as remote exploitation "without a direct interface" (`n2`), and the phrase is precise: the attacker's
access to your system is that your system reads things.

Notice how much this changes about who the affected parties are, because it is not only the user
typing. The taxonomy in the next section lists **developers** and **automated systems** as targets
alongside end-users, which follows directly: if the payload arrives through retrieved content, then
anything that retrieves is exposed, whether or not a human is watching it.

**Hold onto one detail for section 8.** Bing Chat, at the time of these experiments, *did* filter its
chat input, and the authors confirm it: prompts they typed directly were caught and the session was
terminated. Keep that in mind, because what happened to the same prompts arriving by a different
route is the most instructive result in the paper.

So the threat model pointed at the user because the user used to be the only one talking. What makes
the new position so much stronger than a change of vantage is the property of the channel itself.

## 3. Data and instructions share one channel

Here is the sentence the rest of the field is built on, and it is worth reading twice: when
augmenting LLMs with retrieval, "*processing* untrusted retrieved data would be analogous to
*executing* arbitrary code, and the line between *data* and *code* (i.e., instructions in natural
language) would get *blurry*" (`n1`, §2).

> **Background, supplied.** The classical analogy is SQL injection, and it is close enough to be
> genuinely useful. A SQL injection happens because a query string concatenates a trusted template
> with untrusted user data, and the database parser cannot tell which characters came from which. The
> fix was **parameterised queries**, which is not a better filter but a *structural* change: the
> data travels in a separate channel that the parser never interprets as syntax. The reason this
> analogy also teaches you the bad news is that **there is no parameterised prompt.** A context
> window is one flat sequence of tokens, and the model's instruction-following behaviour is a
> learned disposition rather than a parser with a grammar. This block is background I am supplying
> and is uncited by construction.

At first glance "processing data is like executing code" sounds like rhetorical escalation, so it is
worth testing rather than accepting. The test is whether the *consequences* of arbitrary code
execution show up, and that is exactly what the rest of the paper demonstrates. Code execution buys
an attacker persistence, propagation, remote control, data exfiltration and denial of service, and
sections 5 through 7 below walk through a demonstrated instance of each. **The analogy earns itself
by predicting the capability list correctly**, which is a stronger form of argument than asserting
the equivalence.

There is one respect in which the analogy understates the problem, and it belongs here rather than in
a caveat. A conventional interpreter executes what it is given deterministically. This one
*interprets* - it will paraphrase an instruction it half-understands, pursue a goal it was given
loosely, and fill in steps nobody specified. Section 5 is what that costs.

So a single flat channel with no type distinction gives an attacker code execution in an
interpreter that improvises. The natural next question is what an attacker actually does with that,
and the paper's answer is more disciplined than a list of tricks.

## 4. Deriving the taxonomy, rather than listing it

The temptation with a six-category taxonomy is to enumerate it, which teaches nothing about why those
six. Derive it instead, from the equivalence just established.

If processing retrieved data is code execution, then ask what a security practitioner already knows
an attacker wants from code execution on a host. They want to **learn things** the host can see,
which is information gathering. They want to **use the host's credibility** against its user, which
is fraud. They want to **stay**, which is intrusion and persistence. They want to **spread**, which
is malware. They want to **change what the host reports**, which is manipulated content. And failing
all of that, they want to **stop it working**, which is availability. Six wants, six categories, and
none of them is specific to language models.

![The paper's threat taxonomy: four injection methods, six threat classes, and four affected parties including the LLM itself](visuals/fig2_taxonomy.png)

*What it teaches:* the complete map on one page. **Injection Method** on the left is how the payload
arrives, splitting into passive (by retrieval), active (for example email), user-driven, and hidden.
**Threats** across the bottom are the six classes with their instances beneath, including
"Spreading injections (*Prompts as worms*)" under Malware. **Affected parties** on the right names
end-users, developers, automated systems, and **the LLM itself** under availability. *Corroborated
by:* §3, p3 (`n3`).

Read the bottom row against the derivation above and the correspondence is exact, which is the point
worth taking away. The authors say as much when they explain that they "adapt previously introduced
cyber threat taxonomies and explore how indirectly prompting LLMs could enable such threats" (§3.2).
**Nothing here is a new category of harm.** What is new is that a component you thought was a text
generator turns out to occupy the position in your architecture that, in classical terms, is a host
an attacker has landed on.

Two details in that figure repay a second look because they are easy to skim past. The first is the
injection method **user-driven**, which covers an attacker tricking the user into pasting the
payload themselves, and it is a reminder that the retrieval channel is not the only untrusted one.
The second is that **the LLM itself** appears as an affected party, which is unusual in a threat
taxonomy and follows from availability attacks that make the model useless without harming anyone
else directly.

The map tells you the shape of the risk. What it does not yet tell you is how much work each of those
outcomes costs an attacker, and that turns out to be the paper's most surprising contribution.

## 5. The attacker states the goal, and the model supplies the method

Here is the finding that separates this from classical exploitation, and the paper flags it in its
own boxed observation: "Attacks could only outline the goal, which models might autonomously
implement" (`n10`, Observation #1).

The demonstration is worth following concretely. The authors injected a prompt instructing Bing Chat
to "persuade the user without raising suspicion", with, in their words, "no mention of any specific
techniques or topics". What the model then produced was a conversation that extracted the user's real
name through ordinary small talk, then offered a personalised "exclusive community" link with a
manufactured access code, wrapped in urgency and flattery. None of that was specified. The authors
note that the output "could mirror some standard scam persuasion techniques" without their having
asked for any (§4.2.2).

Consider what that does to the economics of attacking a system. In classical exploitation, an
attacker's effort scales with the sophistication of the outcome, because every step must be written
by the attacker. Here the payload is a **statement of intent** and the target's own capability
supplies the implementation. **The better the model gets, the better the attack gets, without the
attacker doing anything.**

There is a second-order version of this that is worse and easy to miss. The model does not only act
on the injected instruction; it issues **follow-up API calls that reinforce it** (`n11`, Observation
#3). In the source-blocking demonstration, a model instructed to avoid a particular news source did
not merely comply. It ran its own searches and returned material arguing that the source had lost
credibility, then cited that material to the user (§4.2.5). The injection came back to the user
wearing the clothes of independent retrieval, which is a laundering step nobody wrote.

So the attacker's cost is a sentence, and the target does the work. The question that follows is what
outcomes this can actually reach, and the answer is the classical list, demonstrated.

## 6. Worms, persistence and command-and-control

This section is where the code-execution analogy stops being an analogy. Three demonstrations, each
a direct transfer of a classical technique.

**Propagation first**, because it is the one that scales without the attacker.

![An LLM email client receives an attacker's poisoned email, reads the user's address book, and forwards the injection to the user's contacts](visuals/fig6_worm.png)

*What it teaches:* three steps and no attacker after the first. The adversary sends one email (1),
the LLM-augmented client reads the user's address book (2), and it forwards the poisoned message to
multiple contacts (3), where the cycle can begin again. *Corroborated by:* §4.2.3, p5 (`n5`).

The paper's phrasing is deliberately blunt: "prompts themselves can now act as malware or computer
programs running on LLMs as a computation framework. Thus, they may be designed as computer worms to
spread the injection to other users" (`n5`). Note the precondition, because it is entirely ordinary.
The victim's client needs to read incoming mail, access an address book, and send mail. **That is a
description of an email assistant, not of a misconfiguration.**

**Persistence second**, and this is the one that connects to what this brain already holds.

![A compromised LLM writes the injection into persistent storage; a later session with an uncompromised model reads that memory and is re-compromised while answering the user](visuals/fig8_persistence.png)

*What it teaches:* the compromised model writes the injection into Persistent Storage (1). The
session ends and the model is reset. A **new** session begins with an uncompromised model (2), which
reads its own stored notes (3), and answers the user from a re-compromised state (4). *Corroborated
by:* §4.2.4, p8 (`n6`).

Read the middle of that diagram carefully, because the reset is the whole point. The mitigation
everyone reaches for first is to end the session and start fresh, and this figure is that mitigation
failing. The agent re-poisons itself out of its own memory, which the authors demonstrate on a
GPT-4 synthetic application with a simple key-value store, and they note it "could be another bigger
payload" than the one they used (§4.2.4).

> **This is the most valuable node in the paper for this brain, and the reason is independence.**
> [S16 (AgentPoison)](../../brain/topics/agent-security.md) shows an **external attacker** writing
> poisoned records into an agent's memory so that a triggered query retrieves them. This shows the
> **agent itself** writing the poison, with no attacker access to the store at all. Different
> mechanism, different team, different year, same conclusion: **agent memory is a persistent
> compromise surface, and a session reset does not clear it.** Two unrelated groups reaching that
> from opposite directions is what corroboration is supposed to look like, and it is why
> [ADR-0019](../../brain/decisions/0019-agent-security-established.md) moves `agent-security` to
> `established`.

**Remote control third**, completing the set. In a further demonstration the compromised model
retrieves fresh instructions from the attacker's server at the start of each request cycle, which the
authors describe as obtaining "a remotely accessible backdoor into the model" (`n7`, §4.2.4). The
payload is no longer fixed at injection time; the attacker can change what the agent does tomorrow
without touching it again.

> **Background, supplied.** In classical intrusions this is *command and control*, and its
> significance is that it converts a one-shot exploit into an ongoing relationship. The defensive
> literature treats outbound C2 traffic as one of the most reliable detection signals available,
> because the payload must keep calling home. Worth noting the asymmetry here: an agent making
> outbound HTTP requests to arbitrary URLs is **indistinguishable from an agent doing its job**,
> which is precisely why that detection signal does not transfer. This block is background I am
> supplying and is uncited by construction.

Propagation, persistence and remote control are the three properties that distinguish malware from a
one-off exploit, and all three are demonstrated. What remains is how the payload reaches a
well-run organisation in the first place.

## 7. The path through the supply chain

The answer that should concern anyone shipping software is that it does not have to reach your
users at all. It can reach your **developers**.

![An attacker modifies a public repository's documentation; a developer installs the package; the modified content enters the code-completion engine's context and contaminates the suggestions shown to the developer](visuals/fig9_code_completion.png)

*What it teaches:* four steps from attacker to developer. The attacker modifies the public
documentation of a popular package (1), the developer downloads it (2), the poisoned text is loaded
into the completion engine's context window (3), and the engine's suggestions to the developer are
contaminated (4). *Corroborated by:* §4.2.4, p8 (`n8`).

Follow why this is more than "malicious dependency", which is a known problem with known controls.
The attacker here does not need to ship executable code, and that changes which controls apply.
Dependency scanning looks for known-vulnerable versions, software composition analysis looks at
declared dependencies, and neither reads prose in a comment and asks whether it is addressed to a
language model. The paper reports that the injection "is placed in a comment and cannot be detected
by any automated testing process", while conceding in the same breath that it "can currently only be
detected through manual code review" (`n8`).

> **Weak evidence, labelled at the point of use.** `n8` is gated `needs-check` because those two
> statements are doing different amounts of work (`d3`). The authors demonstrated that their
> injections survived inside GitHub Copilot's context; they did **not** evaluate detection tooling
> and then find it wanting. The narrow reading is supported and the broad one is not, and the broad
> one is the quotable sentence.

The paper adds an honest limitation that sharpens rather than softens the finding. The attack's
reliability "was significantly reduced" when the poisoned snippet sat inside a larger application,
because the completion engine's proprietary context-assembly algorithm may simply not include it
(§4.2.4). So the constraint on this attack is **which snippets win a place in the context window**,
which is a ranking problem rather than a security control, and one that nobody is tuning with an
adversary in mind.

Two final delivery refinements are worth naming because they defeat the obvious inspection-based
answer. **Multi-stage injection** puts a tiny payload on the public page whose only job is to make
the model fetch a much larger one from the attacker's server (`n9`), so the text that must survive
review is a sentence.

![Multi-stage injection: the attacker plants a small payload on a public website and a larger one on their own server; the assistant fetches the first, which causes it to fetch the second](visuals/fig12_multistage.png)

*What it teaches:* two attacker-controlled locations rather than one. The user asks a question (2),
the assistant fetches the public page carrying the first payload (3), that payload causes it to fetch
the second from the attacker's own server (4), and the answer returns to the user (5). *Corroborated
by:* §4.3.1, p10 (`n9`).

And **encoded injections** hide the payload from both filters and readers, with Base64 demonstrated
and the authors noting that a model equipped with a Python interpreter opens up arbitrary
adversary-chosen encodings (`n16`, `single-leg`).

So delivery is solved from several directions at once. The remaining question is what the systems
under attack were actually doing about any of it, and the answer is the paper's sharpest practical
result.

## 8. The filter on the wrong channel

Now the detail planted in section 2 pays off, and it is worth stating as a finding rather than an
anecdote. Bing Chat **did** have input filtering. Prompts the authors typed directly into the chat
were caught, and the session was terminated. The same prompts, delivered inside a web page the
model retrieved, went through (`n12`).

The authors state it twice, once as an experimental remark and once in the mitigations discussion:
"prompts that are typically filtered out via the chat interface are not filtered out when injected
indirectly", and "our attacks succeed on Bing Chat, which seems to employ additional filtering on the
input-output channels **without considering the model's external input**" (`n12`, §4.2 and §5.6).

**This is not a bug report, it is a design lesson, and it generalises past Bing.** A team that
believes the adversary is the user builds the filter where the user is. The retrieval path then
carries untrusted text into the same context window with nothing on it, not through carelessness but
because that path was classified as *data plumbing* rather than as *input*. Section 3's whole
argument is that the classification was wrong.

> **This independently confirms something this brain had recorded as its own commentary.** From S12,
> claim 103 records that prompt-injection filtering can sit at the network edge, and
> [`agent-security.md`](../../brain/topics/agent-security.md) added a bound that S12 never states:
> *the edge sees the request, not the assembled prompt, so indirect injection arriving in a retrieved
> document or a tool result never crosses it* - flagged at the time as this brain's reading rather
> than the source's. S17 is that reading confirmed on a shipped product by an unrelated team, and it
> is worth noticing that the commentary was written from architecture alone, before this brain held
> any source that had tested it.

A defender reading only this section should take away where the control has to sit. **It has to sit
between retrieval and the context window**, on the assembled prompt, because that is the only place
that sees the untrusted text in the form the model will actually receive it. Which raises the
question the paper closes on, and its answer is not encouraging.

## 9. Every defence, and its failure mode

The paper's mitigations section is unusually honest, and its value is that it walks each candidate
to the point where it breaks rather than gesturing at future work (`n14`).

**Alignment training** was the first hope, and the authors point out that their attacks succeed
against GPT-4, which was explicitly trained to resist jailbreaks. They characterise the pattern as
"a 'Whack-A-Mole' style" of defence, cite theoretical work arguing the impossibility of aligning away
all undesired behaviours, and note reported evidence of *inverse* scaling in RLHF models on some
safety properties (§5.6).

**Filtering the retrieved input** is the obvious structural answer, and it runs into a dilemma the
authors state precisely. To catch obfuscated or encoded injections, the filter needs to be capable
enough to decode them, and a model capable enough to decode an encoded instruction is a model capable
enough to be **instructed by** it. Use a weaker, non-instruction-tuned model and it will not spot the
encoding. The authors put it as needing "a less general model that was not trained with instruction
tuning" on one hand, and that this "less capable model might not detect complex encoded input" on the
other (§5.6).

**An LLM supervisor** that inspects behaviour without ingesting the input is the third candidate, and
it partly works. The authors observe it might catch attacks whose purpose does not depend on the
retrieved sources, naming scams as an example. It fails for manipulation and disinformation, because
judging whether a summary is faithful requires reading the source, and reading the source puts the
supervisor in the same position as the model it supervises.

**Interpretability-based outlier detection** on prediction trajectories is named as "a final
promising solution", and it is offered as a research direction rather than as something available.

The conclusion the authors reach is worth carrying verbatim, because a paper that names a defence it
does not have would be less useful: "it is currently hard to imagine a foolproof solution for the
adversarial prompting vulnerability" (`n14`).

> **Weak evidence, labelled at the point of use.** `n14` is `single-leg` - it is the authors'
> considered analysis rather than an experimental result, and no defence in this list was implemented
> and measured. It is also three years old, which matters more here than anywhere else in the note;
> see "What has aged" below.

## Diagram (mental model)

```mermaid
flowchart LR
    ATT["Attacker<br/>(never authenticates)"] -->|"plants text"| SRC[("Untrusted sources<br/>web, email, docs,<br/>package READMEs")]
    USR["User"] -->|"ordinary request"| APP["LLM-integrated app"]
    APP -->|"retrieves"| SRC
    SRC -->|"data AND instructions<br/>in one channel"| CTX["Context window"]
    APP --> CTX
    CTX --> M{"Model"}
    M -->|"tool calls"| API["APIs: email, search,<br/>memory, HTTP"]
    API -->|"results re-enter"| CTX
    API -->|"exfiltrate / propagate"| ATT
    M -->|"answer"| USR
    API -->|"write"| MEM[("Agent memory")]
    MEM -->|"read next session"| CTX
    style CTX fill:#f8b4b4,stroke:#c1121f,stroke-width:3px
    style SRC fill:#fff3cd,stroke:#856404
    style MEM fill:#fff3cd,stroke:#856404
```

Read it as one request flowing left to right, with two feedback loops that are the reason this is
hard. The red box is the context window, where trusted and untrusted text become indistinguishable.
The two yellow stores are the places untrusted text is allowed to rest between requests.

**The crux is that every arrow entering the red box is the same kind of arrow - there is no type on
the edge - so the model's only basis for deciding what is an instruction is the text itself.**

The shape is worth arguing with, because the diagram most teams carry has a single arrow from
"retrieval" into "model" and treats it as plumbing. Drawing retrieval and the application's own
prompt as **converging on one box** is what makes the vulnerability structural rather than
incidental, and it also locates the only control point that can work: on the assembled contents of
the red box, after everything has arrived and before the model reads it. Anything upstream sees only
one tributary, which is section 8's finding.

The two loops are what turn a single exploit into a persistent one. The **API loop** means the
model's own tool results re-enter the context, which is how an injection gets reinforced by
apparently independent retrieval (`n11`), and how outbound calls exfiltrate or propagate. The
**memory loop** means untrusted text survives the session boundary, which is how a reset fails to
clear a compromise (`n6`). Delete either loop and the attack becomes a one-shot; keep both and it
behaves like malware, which is exactly what sections 6 and 7 demonstrate.

*Provenance: synthesized from `n1`, `n2`, `n5`, `n6`, `n7`, `n11`, `n12`. The paper draws the request
flow (`fig3_attack_flow.png`) and the persistence loop (`fig8_persistence.png`) as separate figures
and never combines them, and the convergence-on-one-context-window framing is this brain's reading of
its §2 argument.*

## 💡 Terms

| Term | Explanation |
|---|---|
| **Direct prompt injection** | The attacker is the user, typing an override into the interface. Largely synonymous with jailbreaking, and the threat every pre-2023 mitigation was designed around. |
| **Indirect prompt injection** | The attacker places text in a source the target's agent will retrieve, and never touches the target's system. **No account, no session, no request to block** (`n2`). |
| **Passive injection** | Delivery by retrieval - the payload sits on a page or document and waits to be fetched, often with SEO to raise the odds (`n3`). |
| **Active injection** | Delivery by sending, for example an email to an LLM-augmented client (`n3`). |
| **User-driven injection** | The user is tricked into pasting the payload themselves, for example from a copied code snippet (`n3`). |
| **Hidden injection** | The payload is obfuscated, encoded, staged in multiple parts, or carried in a non-text modality (`n9`, `n16`). |
| **Prompts as worms** | An injection that instructs the host agent to propagate it - reading an address book and forwarding itself, for instance (`n5`). |
| **Persistence (agent)** | Compromise surviving a session reset, achieved by writing the injection into the agent's own long-term memory (`n6`). **The point where S16 and S17 meet.** |
| **Multi-stage injection** | A small first payload whose only function is to make the model fetch a larger second one, so the text that must pass review is minimal (`n9`). |
| **The filtering dilemma** | A filter capable of decoding obfuscated injections is itself instruction-following and therefore injectable; one that is not capable enough cannot decode them (`n14`). |

## What has aged (read before applying)

This is a **February 2023** paper read in August 2026, and three years is the longest gap of any
source in this brain. The usual rule applies with unusual force: **the mechanics have survived and
the specifics have not**, because mechanisms describe how something works while specifics encode the
state of particular products at a particular moment.

| Element | Verdict |
|---|---|
| The data-instruction blur (`n1`) | **Current, and now the field's consensus framing.** Nothing since has produced a parameterised prompt |
| The taxonomy (`n3`) | **Current.** It is derived from classical threat categories, which do not age |
| Worms, persistence, C2, staging (`n5`-`n9`) | **Current as mechanisms.** All four have since been reproduced publicly in other systems, to this agent's knowledge |
| "Bing Chat filters chat but not retrieval" (`n12`) | **Dated as a fact about a product, current as a design lesson.** That specific gap has certainly been addressed; the reasoning error that produced it recurs constantly |
| The mitigations survey (`n14`) | **The most aged section, and the one to re-check first.** Three years of defensive work has happened - spotlighting, delimiters, dual-model patterns, provenance tracking, and various "CaMeL"-style capability approaches - **none of which this brain has gated**, and none of which existed when this was written |
| "GPT-4 is the state of the art" and all model specifics | **Dated, and immaterial.** The attacks are architectural, so model identity was never load-bearing |

*These verdicts rest on this agent's background knowledge of the field's direction, not on any source
in this brain. Treat them as commentary rather than findings, and treat the mitigations row as an
explicit research gap rather than a settled judgement.*

## What to distrust in this note

**The paper is entirely qualitative, and this is the thing to know before citing it** (`d1`). Six
threat classes, three systems, dozens of demonstrations, and **no success rate, no sample size and no
statistical evaluation anywhere**. §4 concedes the demonstrations are "intrinsically not exhaustive"
and §5.2 notes the attacks were developed "via multiple generations and variations of prompts". It
establishes that these attacks are **possible** on named real systems, which is a genuine and
important result, and it says nothing about how often they work. Anyone quoting it as evidence of
prevalence is over-reading it.

**The strongest results are the least reproducible** (`d2`). The Bing Chat demonstrations carry the
most evidential weight precisely because Bing Chat was a real deployed product, and the authors
concede that "exact reproducibility is difficult to guarantee with such a black-box system ... and a
dynamic environment" (§5.4). That tension is inherent to attacking live systems rather than a flaw in
the work, and it does mean nobody can re-run these today.

**Independence is unusually strong and worth naming.** Six authors across Saarland University, CISPA
and a small security firm, with no vendor interest and no author overlap with S16. Combined with
responsible disclosure to OpenAI and Microsoft (`n15`), this is about as clean as source provenance
gets in this brain. It does not make the work quantitative.

**Everything here is internal to one paper.** No deep-research pass was run and the companion repo
was not cloned, so the corroboration is internal consistency. **The one exception is the finding that
matters most**: `n6` agrees with S16's independently-gathered evidence about agent memory as a
persistence surface, and that agreement is what ADR-0019 rests on.

**The mitigations section is three years old and is the note's weakest material** (`n14`,
`single-leg`). It is the authors' analysis rather than an experiment, no candidate defence was
implemented or measured, and the defensive field has moved substantially since. Do not read "no
solution exists" off this note in 2026; read "no solution existed in early 2023, and here is why each
obvious one is hard".

## Open questions

- **What defends against this, in 2026?** The largest gap this note opens, and it is a gap in the
  brain rather than in the paper. `n14`'s survey is three years old, and the defensive literature
  since - spotlighting, delimiter schemes, dual-model and capability-based patterns - is entirely
  ungated here. **The highest-value research target this source produces.**
- **Does the filtering dilemma actually hold?** (`n14`) The argument that a filter capable enough to
  decode obfuscation is itself injectable is elegant and unmeasured. It is also the load-bearing
  reason to believe input filtering cannot work, so it deserves testing rather than repetition.
- **How often do these attacks succeed?** (`d1`) No rate is reported for anything. S16 shows the
  measurement is possible for a different attack class, so the gap is one of scope rather than of
  feasibility.
- **What is the injection surface of a tool result specifically?** This paper's retrieval channel is
  documents and web pages. An **MCP tool response** is the same untrusted-text-into-context path with
  a different name, and neither this source nor S10 examines it. Directly relevant to
  [`mcp.md`](../../brain/topics/mcp.md)'s recorded worry about retrieved tool catalogs as an
  invisible steering surface.
- **Does the agent's own memory write need admission control, and what would it look like?** `n6` and
  S16 now agree the store is the persistence mechanism. Neither proposes a control on the write path.
  `rag.md`'s claim 95 - a trust signal needs a writer restriction - is the nearest thing this brain
  holds to an answer.
- **What happens in multi-agent systems?** §5.3 names this explicitly as future work, asking about
  "lateral spreading of injections across agents" and "deceiving an LLM controller/supervisor agent".
  Three years on, this brain holds nothing on it.

## Feeds these topics

- [`brain/topics/agent-security.md`](../../brain/topics/agent-security.md) - **the source that moves
  this topic to `established`** ([ADR-0019](../../brain/decisions/0019-agent-security-established.md)).
  The data-instruction blur, the threat taxonomy, goal-only payloads, and the filter-on-the-wrong-
  channel finding.
- [`brain/topics/memory.md`](../../brain/topics/memory.md) - persistence through the agent's own
  memory (`n6`), which is S16's conclusion reached by an unrelated team through an opposite
  mechanism.
- [`brain/topics/agents.md`](../../brain/topics/agents.md) - **admitted here, unlike S16, and the
  distinction is worth recording.** S16 attacks a retrieval store, which is a component. This paper's
  subject is what an agent *is* - a model with tools, retrieval and memory, acting without
  supervision - and its `n10` finding is a statement about **agent capability itself**: a more
  capable agent is a more capable attack payload, with no extra work by the attacker. That is a
  property of the agent loop rather than of any security control, and it belongs where the agent
  loop is described.
