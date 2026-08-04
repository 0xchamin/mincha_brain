# context/ - external evidence (deep research)

> Persona: **fact-checker + synthesizer** (+ **mentor** when teaching).

Notes produced by the **deep research** step - the optional pass that reaches *outside* this source
to test what it claims and to attach the intellectual context around it. See "Deep research on
request" in `../../../AGENTS.md` for the full contract.

**This folder is empty unless the user asked for deep research.** It is never automatic.

## What lives here

One note per research pass, named `<NN>_<slug>.md` (`01_context-window-prior-art.md`), numbered in
order. Each note is **permanent and committed** - unlike a harness's session-scoped research output,
which disappears. Ephemeral output that never reached a kit file did not happen.

## What does *not* live here

- **The source's own claims** - those are `../nodes.md`.
- **The distilled lesson this source taught** - that is `../LEARNING.md`, which answers exactly one
  question: *what did this source teach?* Keep external findings out of its body, or you lose the
  distinction between "the author claims this" and "the field thinks this". `LEARNING.md` may
  **cite** a note here; it must not absorb it.
- **Durable cross-source synthesis** - that belongs in `../../../brain/topics/*.md`.

## Note structure

```markdown
# Research - <question or node cluster>

| Field | Value |
|---|---|
| Pass | 01 |
| Date | YYYY-MM-DD |
| Targets | n4, n8, n9 (node IDs from ../nodes.md) |
| Budget used | 5 searches / 7 fetches (cap: 8 / 12) |

## Findings

| Node | External finding | Verdict | Source (tier, independent?) |
|---|---|---|---|
| n8 | ... | supports / contradicts / refines / no-evidence | <url> (T1, independent) |

## Synthesis
<What this changes about how to read the source - one level above it, no 101 explainers.>

## Cross-domain framing
<The established name in the older discipline, if there is one.>

## Confidence assessment
<Assumptions made without asking, what stayed unresolved, where evidence was thin.>

## Fed back into
- `../nodes.md` - <node confidences updated>
- `../../../brain/claims.md` - <rows added / citations appended>
- `../../../brain/glossary.md` - <terms>
```
