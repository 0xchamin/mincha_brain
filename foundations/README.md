# Foundations - supplied background, uncited by construction

> **Read this before using anything in this folder.**

These files hold **background a reader needs and that no ingested source taught**. They are the
repo-level home for the `> **Background, supplied.**` blocks that appear inside every
`LEARNING.md` - written once and kept, instead of re-derived by whichever agent happens to be
writing.

**They are not evidence.** Nothing here is gated, nothing here produces knowledge nodes, and
**nothing here may be promoted to [`brain/claims.md`](../brain/claims.md)**. A foundation is
background you are supplying so the rest reads; it is not a finding.

> **Why the line is drawn this hard.** The entire value of `brain/` is that every claim carries a
> citation and a gate verdict. Material that arrives already synthesised - especially
> agent-generated research notes - is roughly **T5** on this kit's scale, and the T5 rule is *"use
> for discovery; cite the primary source they point to, not them."* Filing something here does not
> upgrade it. It puts it where its status is **declared** rather than assumed.

## Required header

Every file in this folder starts with a status line `validate.py` checks for:

```markdown
> **Foundation - supplied background, uncited by construction.** Not evidence about any source, and
> never promoted to `brain/claims.md`. See [`README.md`](README.md).
```

## How to use one

- **A `LEARNING.md` may cite a foundation as background, never as evidence** - the same way a
  `Background, supplied` block is treated today. The sentence leaning on it says so.
- **Keep any citations the material already carries.** A foundation pointing at an arXiv paper or a
  vendor engineering post is far more useful than one that does not, and the pointer is what makes a
  later proper ingest cheap. Those citations do **not** change its status.
- **If a foundation turns out to be load-bearing for something the brain wants to assert, ingest the
  primary it points at.** The claim comes from the gated source, not from here.
- **Promote reusable terms** to [`brain/glossary.md`](../brain/glossary.md), which is the
  one-or-two-sentence version of the same material.

## Bringing material in

Drop markdown into git-ignored [`staging/`](../staging/README.md) first. There is no `_inputs/` -
`staging/` already exists for this, and the rule is the same one it was written for: **material
becomes part of the kit when it is filed, not when it is copied in.**

Then read it and make the call:

| What it is | Where it goes |
|---|---|
| Teaching a fundamental the reader needs | **`foundations/<slug>.md`**, with the status header |
| Making claims about the world, with citations | **Not here.** The *primary it cites* is what to ingest |
| Both | Split it. Neither half improves by travelling with the other |

## Contents

_(none yet - add a row per file as they arrive.)_

| File | Covers | Notable citations |
|---|---|---|
