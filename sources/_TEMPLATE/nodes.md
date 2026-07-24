# Knowledge nodes - <TITLE>

> Persona: **fact-checker** - re-adopt when working this file.

> The atomic units of knowledge extracted from this source. Each node has a **stable ID** (`n1`,
> `n2`, ... - never renumber; topic notes reference these), a claim, **both legs each with its own
> citation** (or one leg marked `single-leg`), a gate verdict, and a confidence. Only
> `corroborated`/`single-leg` nodes (and recorded `divergence` findings) feed `LEARNING.md` and get
> promoted to `../../brain/`. The **fact-checker** persona owns the verdicts; see `../../AGENTS.md`
> and `prd.md` §6.

## Nodes

| ID | Claim (crux) | Evidence leg + citation | Corroborating leg + citation | Gate | Confidence |
|---|---|---|---|---|---|
| n1 | <one-line claim> | `visuals/frame_0814.jpg` - slide "..." | narration "..." @ `<url>&t=494s` | corroborated | OK |
| n2 | <claim, talking-head> | narration "..." @ `<url>&t=690s` | (no useful visual) | single-leg | needs-check |
| n3 | <code claim> | `src/server.ts:120` - "..." @ `https://github.com/<owner>/<repo>/blob/<sha>/src/server.ts#L120` | README "tools are registered at startup" @ `<repo-url>/blob/<sha>/README.md#L12` | corroborated | OK |

## Dropped / divergences (audit trail)

| Candidate | Verdict | Note |
|---|---|---|
| `frame_0132` | dropped | text never mentions it; likely incidental slide. |
| `src/auth.ts:44` | divergence | docs say "OAuth required"; code allows anonymous - **finding**, kept. |

> **Citations - cite BOTH legs.** Video -> `<youtube-url>&t=<seconds>s`; blog -> `source, <section
> heading>`; paper -> `source, Figure/Table N, §`; **code -> an immutable GitHub blob permalink
> containing the SHA** (`<repo-url>/blob/<sha>/<path>#L<n>`) so it stays inspectable after the local
> `repo/` clone is gone (fall back to `path:line @<sha>` for non-GitHub). A `single-leg` node cites
> its one leg and leaves the other cell `(none)`.
