# Results - the summary-index ceiling

> Ran 2026-08-15. Predictions were committed in `2bcd9fe`, **before any code in this directory
> existed**; this file was written after. Reproduce with
> `python3 cases/01_source_index.py` and `python3 cases/02_node_index.py` (stdlib only, ~3 min).

| Field | Value |
|---|---|
| Under test | Whether a **summary index** stays discriminative as item count grows - the design R4 found nobody had measured |
| Method | Lexical TF-IDF cosine ranking of the true item against `N-1` sampled distractors. **No model**, per ADR-0024 rule 2 |
| Arm A | 26 `INDEX.md` source rows, 223 queries, N to 26. **Demonstration** |
| Arm B | **475 gated nodes**, 1,161 usable queries (400 sampled), **N to 475**. **The genuine test** |
| Predictions | **2 clean hits, 2 misses, 1 that survived only because its falsifier was too lenient** |

## Scorecard, misses first

| | Prediction | Outcome |
|---|---|---|
| **P2** | Arm A full-minus-oneline gap **10-25 points** | **MISS. 39.5 points** (74.9% vs 35.4% at N=26). Richness bought far more than predicted |
| **P5** | At N=100, oneline Recall@1 in **25-55%** | **MISS, narrowly and on the high side.** Log-interpolating N=64 (60.3%) and N=128 (54.4%) gives **~56.5%**. The band was called "deliberately wide" in advance and was still wrong |
| **P4** | Rich-vs-oneline gap **stays roughly constant** as N grows | **Survived its falsifier and is substantively wrong.** The falsifier was "gap at N>=256 more than double the gap at N<=16" - 18.0 against 11.8, so not doubled. But the gap **widens monotonically from N=8 onward**, 11.0 -> 18.3. **Score this as a miss.** A falsifier set at 2x was too lenient to catch a real, systematic effect |
| **P1** | Arm A full Recall@1 **60-85%** at N=26 | **HIT. 74.9%** |
| **P3** | Arm B decays **smoothly log-linearly, no knee** | **HIT**, and cleanly - see below |

**Three of five predictions were wrong or badly calibrated, and P4's falsifier was the worst of it** -
it was set loose enough that a clear, monotone, theoretically-important effect passed it. The lesson
carries beyond this experiment: **a falsifier calibrated to "obviously broken" cannot detect
"systematically wrong", which is the interesting case.** The previous experiment's failure was the
opposite one (bands so wide everything hit); this one repeated the mistake in a single prediction
after explicitly recording it last time.

## Arm B - the numbers

```
    N variant        R@1     sd     R@3     MRR
    2 full         88.1%   0.2  100.0%   0.941
    8 full         83.8%   0.6   88.6%   0.874
   32 full         77.8%   0.7   85.0%   0.821
  128 full         70.6%   0.5   78.5%   0.756
  475 full         64.4%   0.0   71.4%   0.692
    2 oneline      76.3%   0.4  100.0%   0.882
    8 oneline      72.8%   0.8   76.6%   0.776
   32 oneline      64.7%   1.0   74.8%   0.704
  128 oneline      54.4%   0.8   66.2%   0.616
  475 oneline      46.1%   0.0   55.9%   0.528
```

## Finding 1 - there is no knee, and that is the result

Recall@1 falls by a **near-constant amount per doubling of N**, across more than seven doublings:

| Variant | Drop per doubling (pp) | Median | Max |
|---|---|---|---|
| full | 1.6, 2.8, 2.7, 3.3, 4.3, 3.0, 3.1, 3.1 | **3.05** | 4.3 |
| oneline | 1.4, 2.2, 4.4, 3.7, 4.5, 5.8, 4.7, 3.6 | **4.05** | 5.8 |

P3's falsifier was any doubling dropping more than twice the median. **Nothing came close** - the
worst was 1.4x. Decay is log-linear from N=2 to N=475.

**So a summary index does not break at a scale. It degrades smoothly and predictably**, at roughly
three percentage points of top-1 accuracy per doubling for rich summaries and four for one-line ones.
There is no threshold in the index's discriminability at ~100, or anywhere else in the tested range.

**This sharpens claim 213 rather than contradicting it.** R4 found the crossover at ~100 documents to
be where **cost** flips, with quality converging - and the word "ceiling", inherited from `n10`,
implies a cliff that this measurement says is not there. At `n10`'s own claimed scale the index is
working fine and getting gradually worse, which is a **budget decision, not a capability limit.**

## Finding 2 - summary richness buys slope, not just intercept (P4's real answer)

The gap between rich and one-line summaries **widens monotonically with N**:

| N | 2 | 8 | 32 | 128 | 256 | 475 |
|---|---|---|---|---|---|---|
| gap (pp) | 11.8 | 11.0 | 13.1 | 16.1 | 17.7 | **18.3** |

One-line summaries decay at **4.05 pp/doubling against 3.05** - a **28% steeper slope**. That is the
prediction I got substantively wrong, and it is the most actionable thing here.

**Richness is not a fixed accuracy purchase. It is a scaling property.** An index of one-line
summaries and an index of paragraphs do not run parallel; they diverge, and the divergence compounds
with every doubling. **A knowledge base built on one-line summaries has a materially worse curve than
one built on annotated rows**, which is a direct, practical correction to `n10`'s design as written -
and a retrospective justification for this brain's own long `INDEX.md` rows, which were chosen for
readability rather than for retrieval.

*Extrapolation, labelled as such:* continuing both slopes, `full` reaches 50% Recall@1 near **N ~
13,000** and `oneline` is already below 50% at 475. Straight-line extrapolation over five more
doublings is not evidence; it is included to show the practical size of a 1 pp/doubling slope
difference.

## Finding 3 - the absolute levels are higher than expected, and are a floor

At **N = 475**, with a **purely lexical scorer and no model at all**, the true node is ranked first
64.4% of the time from rich summaries and 46.1% from one-line ones; in the top three, 71.4% and 55.9%.
**Recall@3 is arguably the operationally relevant number**, because the design opens several pages
rather than one.

Two reasons to hold this loosely, one in each direction. **It is a floor**, because an agent reading
an index can match meaning where TF-IDF matches strings. **And it is inflated**, because of the
confound predicted in advance: queries and index entries were written by the same pipeline from the
same material and share distinctive vocabulary a stranger's question would not have. **Treat the
shape as the finding and the levels as an upper bound on a lower bound**, which is an awkward but
honest description.

## Arm A - the live instance

26 items, 223 queries. Recall@1 at full N: **74.9% full, 35.4% oneline, 17.5% title**.

The 39.5-point richness gap (P2's miss) is much larger than Arm B's 12.8 at comparable N, and the
reason is mechanical rather than interesting: Arm A's `full` variant is a ~300-word annotated row
against a single first sentence, where Arm B's `full` is a node claim against its own bolded crux,
which is often most of it. **The variants differ in how much they differ**, so the two arms' gaps are
not comparable and Arm A's should not be quoted as a richness effect.

Title-only at 17.5% is worth one sentence: **a bare list of titles is not an index.** It is the
control this experiment needed and it behaves like one.

## What this does not establish

- **It is not evidence about S8, and `n10` does not move.** ADR-0024's ceiling is explicit: an
  experiment tests a **mechanism** and never corroborates the source that suggested it. `n10` remains
  `single-leg`, `needs-check`. What moved is **claim 213**, which is about the mechanism.
- **It is not evidence about agents.** A lexical scorer bounds the information carried in a summary.
  It does not tell you what a model does with that information, and the two can differ in both
  directions.
- **n = 1 corpus**, one domain, one writing pipeline, one scorer with fixed constants. The curve
  measured here is this corpus's curve; the claim promoted is about the **shape**, which is the part
  least likely to be corpus-specific and is still only measured once.
- **No stemming beyond a crude plural strip, and a 90-word stopword list.** Both were fixed before the
  run and deliberately not tuned, because tuning a baseline until the curve looks nicer is the failure
  this layer exists to prevent.
