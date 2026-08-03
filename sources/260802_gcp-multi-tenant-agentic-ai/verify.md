# Verify log - Multi-tenant agentic AI system (Google Cloud)

> Persona: **fact-checker** - re-adopt when working this file.

> Append-only. One entry per `/verify` pass, dated. Each entry records what was checked against
> `nodes.md` + `SOURCE.md`, and the verdict on each finding. **Never rewrite an earlier entry.**
> Contract: [`AGENTS.md`](../../AGENTS.md) § "Verifying one source on request".

---

## 2026-08-03 - first pass (and the stage's first run anywhere)

| Field | Value |
|---|---|
| Read | `nodes.md` (18 nodes, 3 divergences, 3 gaps), `LEARNING.md` (7,975 words), `SOURCE.md` |
| Independence | **Yes.** This source was written by a different session; the verifying agent had never read it before this pass |
| Findings | 0 `defect`, 1 `judgement`, 0 `gate-reopen`, 1 defect **in the stage itself** |

### Result: the source is in unusually good shape

Checks 1-5 pass. This note is scrupulous about the thing this stage exists to catch - weak evidence
is labelled **at the point of use**, repeatedly and without prompting:

- the registry carries "**`single-leg` and needs-check**" in the sentence that leans on it (§6);
- the ingress trade-off carries "`single-leg` on the vendor's own capability statements" (§8);
- the structural-to-enforced framing carries "`n11`, `single-leg`, and the framing here is mine, not
  a sentence the source writes" (§9);
- §4's unification is marked "**this brain's synthesis, not the source's claim**" before it is used,
  not after.

**Check 5 in particular is carried faithfully and slightly strengthened.** `nodes.md`'s gate note
warns that both legs are the same team on the same page and that every `OK` means "the document is
consistent about this", never "this works". `LEARNING.md`'s "What to distrust" reproduces that
argument in full and adds the comparison to sources whose second leg is a benchmark chart or console
recording. Nothing softened in translation.

**Check 3 is clean.** The one `Background, supplied` block (§2) is marked and declares itself uncited
by construction; the "delete this component and..." column (§7), the §5 reading about assembled
prompts, and the `💡` definitions are each attributed inline or in "What to distrust".

### Finding 1 - `judgement` (proposed, not applied)

**Where:** `LEARNING.md` §3, the three-mechanism isolation table.

**What:** the table presents three scopes uniformly - project, PAB, VPC Service Controls perimeter -
and cites `n3` above it. But `n3` gates as **"corroborated on PAB and the project; the org-level
perimeter is prose-only"**, confidence **"OK on the stack, needs-check on the perimeter"**. The table
row for the perimeter carries no marker.

**Why it is `judgement` and not `defect`:** the caveat *is* disclosed, about twenty lines later in the
same section - *"the org-level VPC Service Controls perimeter that the prose calls the strict security
boundary is drawn nowhere"* - with an explicit forward plant to §10, where `d1` gets a full treatment.
So the reader does meet it, in the same section, deliberately placed. Whether twenty lines counts as
"the point of use" is a reasonable disagreement, and the forward-plant is a legitimate teaching device
this kit encourages.

**Proposal:** add `needs-check` to the perimeter row itself, so the table can be read standalone. A
table is the part of a section most likely to be screenshotted, quoted or skimmed in isolation, which
is an argument for labelling inside it rather than after it.

**Not applied** - it changes how a claim is presented, and the author's placement was deliberate.

### Finding 2 - a defect in the `/verify` contract itself

**Check 6 could not be performed.** It asks whether a kept frame's `what it teaches` matches what the
frame actually shows - and that requires `view`ing the image. The contract's read list is
`nodes.md`, `LEARNING.md`, `SOURCE.md`: **three text files and no images.**

So the stage as written cannot run one of its own six checks. Options, none free:

- **Add the frames to the read list**, accepting the token cost. Honest, and makes the stage
  meaningfully more expensive on a source with 13 frames.
- **Drop check 6**, and rely on `validate.py`'s citation check plus the curator at ingest.
- **Make check 6 conditional** - run it only when a caption looks unusually load-bearing.

**Recorded, not decided.** This is the kind of thing the stage was built to surface, and it surfaced
one on its first run - against itself.

### Checked and clean

- **Claim references** (`claims 101`-`109` in "Feeds these topics") all resolve; `validate.py`'s
  claim-reference check confirms.
- **Divergences `d1`, `d2`, `d3` all reach `LEARNING.md`** and keep their force - `d2` in particular
  is given its own section (§8) rather than a footnote, which is the correct weight for the sharpest
  internal contradiction in the source.
- **Gaps `g1`, `g2`, `g3` are all carried** (§12), and `g1` is explicitly **not** promoted as a claim,
  citing [ADR-0012](../../brain/decisions/0012-a-mention-is-not-a-source.md). Reading an absence as a
  finding is exactly the laundering that ADR prevents, and the note does not do it.
- **No `gate-reopen` candidates.** Nothing in `LEARNING.md` leans on a node more heavily than its
  gate allows.

### Note for the next pass

The source's own highest-value open question - *what actually propagates identity to a shared MCP
server* - is unresolved by design, not by omission, and is flagged as a research target rather than a
defect. Nothing for this stage to do with it.

---

## 2026-08-03 - contract resolution (not a verification pass)

**Finding 2 above is closed.** The `/verify` contract was changed rather than this source
re-verified, so this entry records the resolution and adds no verdicts.

**Decision: check 6 runs by default, and the read list gains the source's `visuals/` frames**
([ADR-0016](../../brain/decisions/0016-verify-reads-the-frames.md)). A skipped check 6 is now
**recorded rather than discovered**, in a `Frames` field on every pass entry - the same shape as
`SOURCE.md`'s `Visual leg` row.

The two options this log offered alongside it were both rejected, and the reasons are worth keeping
next to the finding that raised them:

| Option | Rejected because |
|---|---|
| Drop check 6 | The `what it teaches` line is written by the ingesting **curator**, and after ingest nobody looks at that image and that sentence together again. Dropping it leaves the visual half of every source with no independent reader - the exact asymmetry this stage closes (claim 34) |
| Run it only when a caption "looks unusually load-bearing" | **Partly circular.** The text cannot tell you which captions are *wrong*; that is what needs the image. It risk-weights, it does not detect |

The cost objection that motivated all three options was **measured and did not survive**: 81 kept
frames across 12 sources, **median 4, maximum 15**.

**Retroactively, the pass above ran `Frames: not checked`** - it could not have been otherwise, since
the contract forbade opening them. This source has **4 frames**, so a future pass closes the gap
cheaply. **The pass is not re-run here**: the agent writing this has now read the source's `verify.md`
and its argument, and no longer has the independent vantage point the stage requires.
