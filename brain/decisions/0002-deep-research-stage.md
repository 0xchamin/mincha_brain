# ADR 0002: Add an optional deep-research stage (external evidence)

| Field | Value |
|---|---|
| Status | accepted |
| Date | 260725 |
| Deciders | chamin |

## Context

The kit's corroboration gate produces **internal** consistency: a slide agrees with the narration,
code agrees with its docs. `AGENTS.md` has always been explicit that this is *not* truth, and that
real confidence needs a **second source**. Nothing in the kit actually went and got one.

The evidence after two ingests: `brain/claims.md` holds 23 claims, of which exactly **one** (#11) is
cross-source. Both current sources are practitioner conference talks with no measurements. During
the 12-factor ingest the only external artifact fetched - the companion repo README - turned out to
**share an author** with the talk, so it corroborated the framework as stated but not that it works.
That distinction had to be spotted and written by hand, which means it would be missed on a tired
day.

Separately, chamin's stated goal for the kit is first-principles depth: each source should land into
an already-understood conceptual neighbourhood, with the concept *one level above* it attached (his
example: recognising agent skill design as **procedural memory**). Nothing in the flow reached
outward to supply that.

Copilot CLI ships a `/research` command; Claude Code has no built-in equivalent. Its docs were read
before designing this ([GitHub Docs](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/research)).

## Decision

Add **deep research** as an **optional stage between the gate and distillation**, triggered only
when the user says "deep research" (or runs `/research`). Never automatic.

Five design commitments, each chosen against an obvious alternative:

1. **Target gated node IDs, not the subject.** Open-ended topic research yields adjacent reading and
   makes the agent a summarizer; node-targeted research returns a verdict that changes a confidence
   value - `supports` / `contradicts` / `refines` / `no-evidence`.
2. **Tiered sources (T1-T5) plus a hard independence rule.** Same author, organisation or commercial
   interest = the same leg wearing a different hat: record and cite it, but **never** let it raise
   confidence. This encodes the judgement that had to be made manually on the 12-factor repo.
3. **`no-evidence` is a first-class result.** "This rests on one practitioner's experience" is a
   finding worth recording, not a failed search to pad with weak hits.
4. **Output is a permanent kit file** - `sources/<id>/context/<NN>_<slug>.md`. Copilot CLI writes
   research to a throwaway session directory; this kit deliberately inverts that, per its standing
   rule that ephemeral output not captured into a kit file did not happen.
5. **Research stays out of `LEARNING.md`'s body.** That file answers exactly one question - *what did
   this source teach?* Blending external findings in would destroy the distinction between "the
   author claims this" and "the field thinks this", which is what the citation discipline exists to
   preserve. `LEARNING.md` may cite a `context/` note; it must not absorb one.

Borrowed from Copilot CLI's `/research`: the **autonomous stance** (never interrupt with clarifying
questions; state assumptions in a **Confidence assessment** section instead) and writing a full
markdown report to disk rather than answering in the transcript.

## Alternatives considered

- **Automatic research on every ingest** - rejected: slow, token-heavy, and most sources do not earn
  it. Optionality is what keeps the default ingest fast.
- **Research the topic, not the nodes** - rejected: produces a reading list. The whole value is
  moving a specific claim's confidence, which requires a specific claim.
- **Write findings into `LEARNING.md`** (chamin's initial framing) - rejected for the reason in
  decision 5. Discussed and agreed before implementing.
- **A flat "credible sources" whitelist** (Anthropic, OpenAI, DeepMind, arXiv, Cursor, Pulse MCP) -
  rejected as too blunt: a vendor blog is primary on its own system but *positioned* on the field,
  and arXiv is preprint. Flattening them would quietly manufacture false confidence. Kept the named
  sources, but as tiers.
- **Put the contract in `.claude/commands/research.md`** - rejected: `AGENTS.md` is the single
  source of truth for every harness. The command file is a thin wrapper that points at it.

## Consequences

- **Easier:** `claims.md` should stop being a single-source store. Open questions written by hand
  ("no measurement anywhere for the context-limiting claim") become actionable research targets.
- **Harder:** an extra stage to keep honest. The independence rule in particular is easy to
  rationalise around when a source *looks* corroborating.
- **New surface:** `sources/_TEMPLATE/context/` ships with every new source (empty by default), and
  `SOURCE.md` gains a `researched` status.
- **Cost:** capped at 8 searches / 12 fetches per pass, with an early stop on two independent
  agreeing sources.
- **Validated on first run (same day).** The shakedown pass ran against the 12-factor source
  (`sources/260725_12-factor-agents/context/01_context-limits-and-decomposition.md`), spending 5
  searches / 8 fetches of the 8 / 12 budget. It **closed both** flagged open questions - the
  micro-agent claim gained a measurement (+13.1 to +41.5 pp across 10 models) and the context claim
  gained peer-reviewed and 18-model evidence - and produced **two findings absent from the source**:
  a measured boundary (naive memory scaffolds hurt 6 of 10 models) and the Event Sourcing framing.
  Design decisions 1 (node-targeted) and 2 (tiers + independence) both did visible work: the
  Anthropic convergence only counts *because* independence was checked, and a search summary asserted
  the decomposition figures before they could be verified - they were kept only after direct
  confirmation against the paper's full text, which is exactly the failure the contract's
  no-fabrication rule exists to catch.
- **Revisit when:** the first few passes reveal whether node-targeted scope is too narrow. If real
  questions keep spanning sources, add a topic-level mode that writes to `reports/` instead.
