"""Summary-index discriminability harness.

Measures how well a summary index lets you pick the right item as the item count
grows. Deterministic and stdlib-only: no model, no network, per ADR-0024 rule 2.

The scorer is lexical TF-IDF cosine. That is a FLOOR on the information carried by
a summary, not a simulation of an agent reading one. See PREDICTIONS.md.
"""

from __future__ import annotations

import math
import random
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Deliberately small and fixed. A larger list would be tuning, and tuning a
# baseline until it produces a nicer curve is the failure mode this layer exists
# to avoid.
STOPWORDS = frozenset("""
a an the and or but if then than that this these those is are was were be been being
of in on at to for from by with without into over under about as it its it's not no
nor so such only own same too very can will just should now what which who whom when
where why how all any both each few more most other some there here they them their
you your we our us i me my he she his her do does did done have has had having
one two three do not never always because while during before after above below up
down out off again further once may might must shall would could also however
""".split())

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Lowercase, strip markdown noise, drop stopwords and very short tokens."""
    text = text.lower()
    text = re.sub(r"`[^`]*`", " ", text)          # inline code, incl. node ids
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # link text, drop target
    text = re.sub(r"https?://\S+", " ", text)
    toks = TOKEN_RE.findall(text)
    out = []
    for t in toks:
        if len(t) < 3 or t in STOPWORDS:
            continue
        if len(t) > 4 and t.endswith("s") and not t.endswith("ss"):
            t = t[:-1]                             # crude singularisation
        out.append(t)
    return out


def first_sentence(text: str) -> str:
    """The 'one-line summary' variant: first sentence of the summary."""
    text = text.strip()
    m = re.search(r"(?<=[.!?])\s", text)
    return text[: m.start()] if m else text


@dataclass
class Item:
    """One entry in the index being tested."""
    key: str
    variants: dict[str, str]          # variant name -> summary text


@dataclass
class Query:
    text: str
    truth: str                        # Item.key


@dataclass
class Corpus:
    items: dict[str, Item] = field(default_factory=dict)
    queries: list[Query] = field(default_factory=list)

    def usable_queries(self) -> list[Query]:
        return [q for q in self.queries if q.truth in self.items]


class TfIdf:
    """TF-IDF cosine over a fixed candidate pool. IDF from the pool, not the query."""

    def __init__(self, docs: dict[str, str]):
        self.tf: dict[str, Counter] = {}
        df: Counter = Counter()
        for key, text in docs.items():
            toks = tokenize(text)
            c = Counter(toks)
            self.tf[key] = c
            for term in c:
                df[term] += 1
        n = max(len(docs), 1)
        self.idf = {t: math.log((n + 1) / (d + 0.5)) for t, d in df.items()}
        self.norm = {
            key: math.sqrt(sum((1 + math.log(f)) ** 2 * self.idf.get(t, 0.0) ** 2
                               for t, f in c.items())) or 1.0
            for key, c in self.tf.items()
        }

    def score(self, query_toks: list[str], key: str) -> float:
        c = self.tf[key]
        if not c:
            return 0.0
        q = Counter(query_toks)
        s = 0.0
        for t, qf in q.items():
            f = c.get(t)
            if not f:
                continue
            w = self.idf.get(t, 0.0)
            s += (1 + math.log(qf)) * (1 + math.log(f)) * w * w
        return s / self.norm[key]


def rank_position(scores: list[tuple[str, float]], truth: str) -> int:
    """1-indexed rank of truth. Ties broken pessimistically (truth goes last)."""
    truth_score = dict(scores)[truth]
    better = sum(1 for k, s in scores if s > truth_score)
    tied = sum(1 for k, s in scores if s == truth_score and k != truth)
    return better + tied + 1


def sweep(corpus: Corpus, variant: str, sizes: list[int], draws: int,
          seed: int, max_queries: int | None = None) -> list[dict]:
    """Rank the true item against N-1 sampled distractors, for each N."""
    docs = {k: it.variants[variant] for k, it in corpus.items.items()
            if it.variants.get(variant)}
    model = TfIdf(docs)
    keys = sorted(docs)
    queries = [q for q in corpus.usable_queries() if q.truth in docs]

    rng = random.Random(seed)
    if max_queries and len(queries) > max_queries:
        queries = rng.sample(queries, max_queries)

    qtoks = [(q, tokenize(q.text)) for q in queries]
    rows = []
    for n in sizes:
        if n > len(keys):
            continue
        per_draw = []
        for d in range(draws):
            drng = random.Random(seed * 1000 + n * 17 + d)
            hits1 = hits3 = 0
            mrr = 0.0
            counted = 0
            for q, toks in qtoks:
                if not toks:
                    continue
                pool = [k for k in keys if k != q.truth]
                distractors = drng.sample(pool, min(n - 1, len(pool)))
                cand = distractors + [q.truth]
                scores = [(k, model.score(toks, k)) for k in cand]
                r = rank_position(scores, q.truth)
                hits1 += r == 1
                hits3 += r <= 3
                mrr += 1.0 / r
                counted += 1
            if counted:
                per_draw.append((hits1 / counted, hits3 / counted, mrr / counted))
        if not per_draw:
            continue
        r1 = [p[0] for p in per_draw]
        rows.append({
            "n": n,
            "variant": variant,
            "queries": len(qtoks),
            "recall1": sum(r1) / len(r1),
            "recall1_sd": (sum((x - sum(r1) / len(r1)) ** 2 for x in r1) / len(r1)) ** 0.5,
            "recall3": sum(p[1] for p in per_draw) / len(per_draw),
            "mrr": sum(p[2] for p in per_draw) / len(per_draw),
        })
    return rows


def source_dirs() -> list[Path]:
    return sorted(d for d in (ROOT / "sources").iterdir()
                  if d.is_dir() and d.name != "_TEMPLATE" and (d / "nodes.md").exists())


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split(" | ")]


def print_table(rows: list[dict]) -> None:
    print(f"{'N':>5} {'variant':<10} {'R@1':>7} {'sd':>6} {'R@3':>7} {'MRR':>7}")
    for r in rows:
        print(f"{r['n']:>5} {r['variant']:<10} {r['recall1']*100:>6.1f}% "
              f"{r['recall1_sd']*100:>5.1f} {r['recall3']*100:>6.1f}% {r['mrr']:>7.3f}")
