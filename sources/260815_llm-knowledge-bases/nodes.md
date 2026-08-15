# Knowledge nodes - LLM Knowledge Bases: a practical guide

> Persona: **fact-checker** - re-adopt when working this file.

> The atomic units of knowledge extracted from this source. Each node has a **stable ID** (`n1`,
> `n2`, ... - never renumber; topic notes reference these), a claim, **both legs each with its own
> citation** (or one leg marked `single-leg`), a gate verdict, and a confidence. Only
> `corroborated`/`single-leg` nodes (and recorded `divergence` findings) feed `LEARNING.md` and get
> promoted to `../../brain/`.

## Read this first: the independence problem is the whole story of this gate

**This source is a talk about [S8](../260731_llm-wiki/LEARNING.md), and S8 is already in this brain.**
Ben Holmes builds his system on Andrej Karpathy's `llm-wiki` gist, names it on stage, and puts it on
the projector for two full minutes [`visuals/frame_712.jpg`, `visuals/frame_728.jpg`, @t=697]. That
creates a trap the gate has to be explicit about, because getting it wrong would silently promote
eighteen `needs-check` nodes to `corroborated`.

**Displaying a source is not corroborating it.** Frames 712 and 728 are photographs of S8's own text.
Under the independence rule they are *the same leg wearing a different hat* - the same author, the
same document, the same revision. **No S8 node moves as a result of this ingest**, and none was
touched. What those two frames legitimately buy is narrower and worth stating: S8 was ingested from
a `curl` of the gist's raw endpoint, and these frames independently confirm the captured text matches
what the document renders as, which is a transcription check and nothing more.

**What *is* independent here is the implementation.** Ben Holmes (Warp, DevRel) is a different person
at a different organisation who read the pattern and built it. That is genuine independent evidence -
but about **instantiability**, not about efficacy. It shows the pattern can be built by someone other
than its author and survives contact with a real corpus. It shows nothing whatsoever about whether the
result is better than the RAG systems S8 opens by dismissing, because **this source measures nothing
at all** (`n16`).

So the honest summary of what arrived: **the first independent instantiation of S8, carrying four
mechanisms S8 does not have (`n5`, `n6`, `n10`, `n12`), one divergence from S8's own architecture that
the talk never notices (`d1`), and zero measurements.**

## What counts as a second leg here

**Slide-heavy screen-share talk, so the normal media pairing applies**: what is on the projector
against what the speaker says while it is up. The visual leg is unusually strong for this brain -
the frames are not bullet-point slides but **the actual artifacts**: a skill file, a tag registry, a
generated entity page, a scheduled prompt. Where a frame shows a mechanism the narration never
mentions, the node is `single-leg` and says so - that case fires three times (`n11`, `n12`, `n15`) and
it fires on some of the most interesting content, which is the usual pattern for a demo talk.

**Capture note bearing on the gate.** The DASH streams were 403-blocked until a JS runtime and
yt-dlp's EJS solver were installed; the first extraction pass ran at 360p, where the dense screens
(the gist, the skill file, the scheduled prompt) were **not legible**. Every node below was gated
against the **1080p** re-extraction. Had the ingest stopped at 360p it would have produced a
transcript-only reading of a talk whose entire payload is on screen - recorded here because it is a
near-miss, not a hypothetical.

## Evidence class - and the conflict sits on the novel half

This is **T4: one practitioner demonstrating his own workflow**, with a **T2 commercial position**
attached to part of it.

| Class | Nodes | How to weigh |
|---|---|---|
| **Pattern, inherited** - what the knowledge-base design is | (none - these are S8's `n1`-`n18`) | **Not re-gated here.** Cite S8 for the pattern; this source is not evidence for it. |
| **Mechanism, new** - the parts S8 does not have | `n5`, `n6`, `n10`, `n11`, `n12` | The transferable half, and the reason this source earns its place. Each stands on its own logic and each is visible as a working artifact rather than described. Adopt or reject on the reasoning. |
| **Practice** - how the pieces are operated | `n2`-`n4`, `n7`-`n9`, `n13`-`n15` | One person's workflow on one corpus. Reasonable, unremarkable, unmeasured. |
| **Efficacy** - that any of it works | `n16` | **Zero measurement.** No baseline, no comparison, no error rate, no time saved, no failure reported. **Never cite this source as a result.** |

**The commercial conflict is precisely located and it is not the whole talk.** Ben Holmes is
developer relations lead at Warp and opens by saying so [@t=18]. The knowledge-base half - capture,
enrichment, wikis - is tool-agnostic and pitches nothing; he explicitly says "you can use any Markdown
viewer, Warp, Obsidian, whatever you like" [@t=109]. **The automation half is a product pitch**:
`oz.dev` is Warp's, he names it as such [@t=871, @t=1198], and it happens to be the section carrying
`n10`, one of the four genuinely novel mechanisms. See `d2`. The two open-source tools he recommends
(Handy for dictation, `hub.md` for reading) are given away, one of them his own but MIT-shaped and
free [@t=218, @t=1214].

## Nodes

| ID | Claim (crux) | Evidence leg + citation | Corroborating leg | Gate | Confidence |
|---|---|---|---|---|---|
| n1 | **Lineage is explicit: this system is an instantiation of S8's pattern, not a parallel invention.** "this is actually a gist from Andrej Karpathy. This is where the LLM knowledge base idea kind of came together." The gist is displayed in full, including its three-layer Architecture section. | narration @t=697 | `visuals/frame_712.jpg`, `visuals/frame_728.jpg` (the gist rendered on screen: title, "The core idea", "Architecture", "Operations") | corroborated | OK as *lineage*. **Explicitly NOT corroboration of S8** - see the independence section above. Its value is that it pins the derivation, so the two sources can never be counted as two independent votes for the pattern |
| n2 | **Capture friction is the binding constraint, and the argument for removing it is volume rather than comfort.** "if you want to get to a point where you can actually have LLMs generate wikis, visualizations, etc., you need a lot of raw data. You need a lot of raw materials." Voice dictation is the named mechanism, at a claimed ~200 words per minute against typing. | narration @t=296-311, @t=188 | `visuals/frame_280.jpg` - a 306-word single-take dictated note, unedited | corroborated | OK for the *argument*. The **200 wpm figure is unsourced** and is the only number in the talk; treat as folklore, not measurement |
| n3 | **The raw layer is deliberately unstructured, and formatting discipline is explicitly waived at capture time.** "don't worry if you're being a little bit scrappy, a little bit rambly. You're not formatting things with perfect bullet points. That's fine. The goal should just be get down as many thoughts in the moment as possible." | narration @t=311-327 | `visuals/frame_280.jpg` - no title, no headings, no tags, no links, no frontmatter; nine unbroken paragraphs | corroborated | OK, and stronger than it sounds. Structure is not skipped, it is **deferred to a machine pass** - which is only affordable because `n4` exists |
| n4 | **Enrichment is a separate later pass over already-captured notes, implemented as an agent skill with three fixed steps: tags, source, related notes.** Not a capture-time discipline and not a chat prompt - a versioned `SKILL.md` in the vault, invoked by name. | `visuals/frame_404.jpg` (`enrich-note/SKILL.md`: "Enrich one note... Do the three steps below"; §1 Tags, §2 Source, §3 Related notes) | narration @t=389-450 ("the way that you can get from this to something like this is through an agent skill... it's just called enrich note") | corroborated | OK. The **separation** is the transferable part: capture optimises for volume, enrichment optimises for structure, and neither compromises for the other |
| n5 | **Idempotence is achieved with a stamp in the note's own frontmatter, which makes a whole-corpus sweep incremental and resumable.** "If the frontmatter already has `enrichedAt`, the note is done - skip it. Do the three steps below, then stamp `enrichedAt` with the current ISO timestamp." Operationally: "it'll look for anything that's not tagged yet." | `visuals/frame_404.jpg` (the skip-and-stamp rule, stated in the skill's third and fourth lines) | narration @t=404 ("put a little time stamp on there so if we ask the agent to do another pass it remembers that some other agent did it in the past"), @t=526 | corroborated | OK, and **this is new beyond S8**, which has no incremental mechanism anywhere. It is what converts "periodically ask the LLM to health-check the wiki" (S8 `n8`) from an O(corpus) request into an O(new) one, and therefore what makes an unattended schedule (`n10`) affordable at all |
| n6 | **The tag vocabulary is a controlled registry the agent must read before tagging, with an explicit instruction to resist extending it.** "Read `references/tags.md` first. Reuse an existing tag whenever one fits. **Be reluctant** to add new tags. Tags should span many notes, not a couple. Only coin a new tag when nothing matches, and when you do, append it to the registry with a one-line description so the next note can reuse it." The stated reason is a model behaviour: "the agent isn't inventing new tags every time... Claude loves to get creative." | `visuals/frame_404.jpg` §1 Tags; `visuals/frame_425.jpg` (`tags.md` itself - tags grouped under Product & business, Creativity & craft, Growth & living, Literature, Personal & misc, plus a separate "Source medium" axis, each tag carrying a one-line definition) | narration @t=420-435 | corroborated | OK, and **new beyond S8**. Note the two-part design that makes it work: the registry is **self-extending but reluctantly so**, and every coinage must ship a definition, so the vocabulary cannot silently fork into near-synonyms. The separate source-medium axis is a second, quieter idea - **faceting**, keeping "what it is about" from colliding with "what kind of thing it was" |
| n7 | **Enrichment writes back into the raw note itself, adding a title, frontmatter and a trailing `## Related` section.** The same file, `raw/walt-disney.md`, is shown before and after. | `visuals/frame_280.jpg` (before: untitled, 306 words, no Related) and `visuals/frame_1060.jpg` (after: titled "Walt Disney (Acquired)", with `## Related` listing three wikilinks) - same path in the sidebar, same prose body | narration @t=372 ("at the bottom, it also finds some back links"), @t=1057 | corroborated | OK as a fact about the system. **It also contradicts the architecture the same talk endorses - see `d1`**, which is the most interesting finding in this source |
| n8 | **Backlinks are agent-judged rather than mechanically derived, and the skill says so.** "Find notes elsewhere in the vault that are genuinely related. **Use your judgment** - grep frontmatter `tags:`, search for key terms, look around. Add the strong matches to a trailing `## Related` section as wikilinks with readable aliases." | `visuals/frame_404.jpg` §3 Related notes | narration @t=450-466 ("to find back links, use some file calls, find related notes using key term search") | corroborated | OK. The instruction hands the model **search tools plus a judgement call**, not a similarity threshold - the retrieval is a means and the decision is the model's. Unmeasured: nothing reports precision, and a wrong backlink is invisible once written |
| n9 | **Generated wiki entity pages carry per-bullet citations back to the dated raw notes that support them.** A person page is structured Who / What the sources say / Related / Sources, and every claim bullet ends in a link to a specific dated note. | `visuals/frame_776.jpg` (`craig-blomberg.md`: four claim bullets, each terminating in a link such as `2026-01-14-the-case-for-christ-study-notes-097z7d8n`, plus a Sources list of the same four notes) | narration @t=774-806 ("it generated sort of an entry for who that character is... it can create back links over to any related meetings... maybe the source links. So going back to our raw notes, if you want to go to the raw materials, you could click through and find those") | corroborated | OK, and the **single most transferable frame in the source.** A derived page is auditable claim-by-claim rather than page-by-page, which is what makes the derived layer safe to trust - and it was arrived at independently of this kit's own citation rule |
| n10 | **Maintenance runs unattended on a schedule in a cloud sandbox, on a sync-down / run-skill / sync-up loop.** The vault is synced into the sandbox (Obsidian's headless CLI, or "just do a `git clone`"), the enrichment or wiki skill runs there, and the result syncs back. Two schedules are shown, one weekly and one daily. | narration @t=823-965, @t=1010 ("we tell it to sync everything down, we tell it to run enrich note, and then we push it back up") | `visuals/frame_980.jpg` (a saved schedule labelled **Weekly**, whose prompt opens "The Obsidian Main vault is synced to `~/vault` by the environment setup" and ends in a numbered Task list) | corroborated | OK as a described-and-shown mechanism, and **new beyond S8**, whose lint is "periodically, ask the LLM". **Efficacy unmeasured** - no report of how often a run fails, produces a bad edit, or is rejected on review. **The commercial conflict lands here (`d2`)** |
| n11 | **The immutability rule is enforced in the operational prompt, not merely in the architecture document.** The scheduled job's instructions state the pattern by name and then encode it as a constraint: "These wikis follow Andrej Karpathy's knowledge-base pattern: raw sources elsewhere in the vault are immutable, and generated wiki folders under `wikis/` are the maintained synthesis layer" and "**Do not edit original notes outside `~/vault/wikis/`** unless explicitly instructed by that wiki's `AGENTS.md`. **Raw source notes are read-only.**" | `visuals/frame_980.jpg` | (none - the narration at this moment describes only "some special instructions for my own setup" and never mentions immutability) | **single-leg** | needs-check as a claim about the *system*, though the frame is unambiguous about the *prompt*. **Figure-only, and the figure is the more interesting leg** - it shows the rule surviving the trip from a prose pattern into an executable constraint, which is the step most patterns never make. Directly in tension with `n7`; `d1` resolves how |
| n12 | **The schema layer is a hierarchy, not one file: each wiki directory carries its own `AGENTS.md`, which overrides the generic instruction.** "Each wiki is a directory with its own `AGENTS.md`, `index.md`, `overview.md`, `log.md`, `sources/`, and `synthesis` subdirectories" and "For each wiki, read `AGENTS.md` and `index.md` first. **Follow that wiki's local schema over any generic instruction here.**" Discovery is mechanical: `find ~/vault/wikis -mindepth 2 -maxdepth 2 -name AGENTS.md`. | `visuals/frame_980.jpg` | (none - not mentioned in the narration) | **single-leg** | needs-check, **figure-only, and new beyond S8**, which describes a single schema document. The generic-instruction/local-override split is the mechanism that lets one scheduled job maintain several wikis with different conventions without the job needing to know any of them. Note the file set it names - `index.md`, `log.md`, `sources/` - is S8's `n9` layout reproduced per wiki |
| n13 | **The review affordance is a morning diff, and the human's role in the loop is reviewer rather than author.** "when I come back to my computer in the morning, I wake up to a perfectly fresh wiki that I can review. It's like the daily paper, but it's your own." Runs are inspectable after the fact in a browser. | narration @t=995, @t=1026-1042 | (none kept - the run-viewer frames were extracted and dropped as not load-bearing) | **single-leg** | needs-check. It is the sentence that decides whether `n10` is safe, and it is asserted rather than shown: **nothing reports what happens when the review finds a bad edit**, whether it is ever rejected, or how a wrong write is reverted |
| n14 | **The visualization layer is generated on demand as self-contained HTML and treated as disposable, not installed as a tool.** "I want you to just build with HTML and Tailwind some sort of graph view... And this is not a tool that you have to install. By the way, I told an agent, build this for me." | narration @t=1088-1119 | `visuals/frame_404.jpg` sidebar - `notes-burndown.html`, `thought-constellation.html`, `thought-constellation-space.html`, `thought-constellation-nasa.html` sitting in the vault as ordinary files beside the notes | corroborated | OK, and the corroboration is incidental and therefore good: the file tree shows **four** variants including two throwaway restyles, which is what "disposable" looks like on disk. The claim is about *cost*, and the cost is not measured |
| n15 | **The graph view's stated purpose is finding gaps in your own thinking, not navigating to a note.** "It's useful just to get an idea of what you're actually interested in and where you have gaps in your thinking." | narration @t=1150 | (none kept - the graph frame was extracted, viewed and dropped under the frame budget) | **single-leg** | needs-check. Recorded because it names a **read of the corpus that no per-note view can give**, and because it is the one affordance in the talk aimed at the corpus's shape rather than its contents. The viewed-but-dropped frame showed category counts in which the largest bucket was "Stray Thoughts" (79), ahead of every intentional topic - suggestive of exactly the gap-finding he describes, and **not citable**, since the frame is not kept |
| n16 | **EFFICACY, UNMEASURED - the talk contains no measurement of anything.** Across 21 minutes: no baseline, no comparison against the RAG systems S8 dismisses, no retrieval quality figure, no time saved, no error rate, no count of bad edits, no corpus size, no cost. The only quantity uttered is the ~200 wpm dictation figure (`n2`), which is about typing and is unsourced. | whole transcript | whole frame set | **single-leg by construction** (there is nothing to corroborate) | **needs-check - do not cite this source as a result.** Stated as a node so it cannot be forgotten: this is a **demo**, and a demo is evidence that a thing can be built and shown working once, which is exactly what `n1`'s independence argument already claims and no more |

## Divergences

| ID | Finding | Legs | Why it matters |
|---|---|---|---|
| d1 | **The enrichment pass mutates the raw layer, contradicting the immutability rule the same talk puts on screen and encodes in its own automation.** S8's architecture is unambiguous - raw sources "are immutable... the LLM reads from them but never modifies them. This is your source of truth" - and Ben displays that sentence [`visuals/frame_728.jpg`] and encodes it in his scheduled job [`n11`]. Yet `enrich-note` writes frontmatter, a title and a `## Related` section **into `raw/walt-disney.md` itself** [`n7`, `visuals/frame_280.jpg` -> `visuals/frame_1060.jpg`]. **The talk never notices the tension.** | S8 gist @ac46de1 §Architecture + `visuals/frame_728.jpg` + `visuals/frame_980.jpg` **against** `visuals/frame_280.jpg` -> `visuals/frame_1060.jpg` + narration @t=372 | **The most useful finding in this source, and it is a refinement rather than a defect.** The reconciliation is visible in `n11`'s own wording and is never said aloud: immutability is scoped **per job**, not per layer. The wiki-maintenance job treats raw as read-only; the enrichment job is explicitly the exception, and `n11`'s escape hatch ("unless explicitly instructed by that wiki's `AGENTS.md`") is where it lives. So the honest generalisation is **not** "raw is immutable" but **"exactly one writer per layer, declared"** - enrichment owns raw's metadata, the wiki job owns `wikis/`, and neither may cross. That is a materially weaker and more implementable rule than S8's, and it is the one that survives contact with a real vault. **It also costs something S8's version had for free**: once raw is writable by anything, a claim can no longer be walked back to a file the agent could not have edited, and the audit trail depends on git rather than on the layering |
| d2 | **The novel automation mechanism and the vendor's product are the same thing.** `n10` - unattended scheduled maintenance - is one of the four things this source adds beyond S8, and it is demonstrated exclusively on `oz.dev`, which is Warp's, presented by Warp's DevRel lead, with the URL given twice as a call to action [@t=871, @t=1198]. | narration @t=18 (affiliation, volunteered), @t=871, @t=1198; the alternative he names for the same job is a competitor's ("Codex app... they have an automations tool") | **Bounded, and the bound is what makes the node still usable.** The *mechanism* - sync down, run a skill, sync up, on a cron - is generic and he says so on stage, naming `git clone` as the substitute for the Obsidian CLI [@t=918] and a competitor's product as the substitute for his own [@t=855]. So the pattern survives removing the vendor. What does **not** survive is any claim about how well it runs, which was never made anyway (`n16`). Flag on citation; do not discount the mechanism |

## Candidates considered and dropped

Recorded so the pass is auditable rather than cherry-picked.

- **The Hubble notes app** (`hub.md`, free and open source, his own) [@t=1214]. Dropped: it is a markdown viewer, the talk explicitly says any viewer works [@t=109], and nothing in the pattern depends on it. Tool trivia, not transferable.
- **Specific dictation tools** (Handy, VoiceInk, WhisperFlow) [@t=218-250]. Dropped as source-specific trivia; the transferable claim is `n2`, that capture friction binds, not which binary removes it.
- **"Local models can do this now, you don't have to pay"** [@t=218]. Dropped: true, unsurprising in 2026, and not what this source is evidence about.
- **The Wikipedia-rabbit-hole framing** [@t=587]. A pleasing description of the browsing experience, not a claim.
- **The burndown / habit-tracker chart** [@t=1182]. Dropped: it measures note-taking frequency, not the knowledge base, and the talk offers it as a "whatever you want" aside. Subsumed by `n14`.
- **The three-layer pattern itself, and all of S8's `n1`-`n18`.** Not dropped for weakness - **dropped because they are already gated in this brain and this source cannot corroborate them.** See the independence section.

## What I had already seen at gate time (disclosure)

- **S8's `SOURCE.md` and its complete `nodes.md` (`n1`-`n18`, `d1`) were read before these nodes were
  written**, and deliberately so. The whole gating question here was *what is new and what is
  re-display*, and that cannot be answered without the prior node set in hand. The cost is disclosed:
  `d1` was found by holding S8's `n4` against this source's frames, so it is a **comparison**, not an
  independent discovery, and the "the talk never notices the tension" observation is this brain's
  reading rather than anything the source says.
- **`brain/topics/memory.md` header and `brain/claims.md` tail** were read while establishing the next
  free claim number and S-label. `memory.md`'s existing note on S8 as "a partial feeder" was in
  context.
- **The kit's own `AGENTS.md`** is unavoidably in context and this source is unusually close to it.
  Where a node reads as a comment on this repo's design, that is recorded in `LEARNING.md` and marked
  as commentary - **no node above is phrased as a finding about this kit**, deliberately.

> Inherits the global rules in `../../AGENTS.md`.
