"""Arm B - the genuine test: ~470 gated nodes as a summary index, swept to N=478.

This is the arm that reaches past n10's claimed ~100 ceiling.

Items    : every gated node across all sources. Each carries a bolded one-line
           crux written by the gating agent - a real corpus of one-line summaries.
Queries  : LEARNING.md sentences citing EXACTLY ONE node id, so truth is unambiguous.
Truth    : that (source, node) pair.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from harness import (Corpus, Item, Query, first_sentence,  # noqa: E402
                     print_table, source_dirs, split_row, sweep)

NODE_ROW = re.compile(r"^\| (n\d+) \| ")
NODE_REF = re.compile(r"`(n\d+)`")


def build() -> Corpus:
    c = Corpus()

    for d in source_dirs():
        for line in (d / "nodes.md").read_text(encoding="utf-8").splitlines():
            m = NODE_ROW.match(line)
            if not m:
                continue
            cols = split_row(line)
            if len(cols) < 2:
                continue
            claim = cols[1]
            if len(claim) < 40:
                continue
            # The crux is the leading bolded sentence the gate writes; fall back
            # to the first sentence when a node is not written that way.
            bold = re.match(r"\*\*(.+?)\*\*", claim)
            oneline = bold.group(1) if bold else first_sentence(claim)
            c.items[f"{d.name}#{m.group(1)}"] = Item(
                key=f"{d.name}#{m.group(1)}",
                variants={"oneline": oneline, "full": claim},
            )

    for d in source_dirs():
        lm = d / "LEARNING.md"
        if not lm.exists():
            continue
        text = lm.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```", " ", text, flags=re.S)      # drop mermaid
        for raw in re.split(r"(?<=[.!?])\s+|\n\n+", text):
            refs = set(NODE_REF.findall(raw))
            if len(refs) != 1:
                continue                                        # unambiguous only
            node = refs.pop()
            key = f"{d.name}#{node}"
            q = " ".join(raw.split())
            if len(q) > 60:
                c.queries.append(Query(text=q, truth=key))
    return c


def main() -> None:
    c = build()
    qs = c.usable_queries()
    print(f"Arm B: {len(c.items)} node items, {len(qs)} usable queries\n")
    sizes = [2, 4, 8, 16, 32, 64, 128, 256, len(c.items)]
    rows = []
    for variant in ("full", "oneline"):
        rows += sweep(c, variant, sizes, draws=5, seed=23, max_queries=400)
    print_table(rows)

    print("\nper-doubling drop in R@1 (percentage points):")
    for variant in ("full", "oneline"):
        v = [r for r in rows if r["variant"] == variant]
        drops = [(v[i]["n"], round((v[i - 1]["recall1"] - v[i]["recall1"]) * 100, 1))
                 for i in range(1, len(v))]
        print(f"  {variant:<8} {drops}")

    print("\nfull-minus-oneline gap in R@1 (percentage points):")
    f = {r["n"]: r["recall1"] for r in rows if r["variant"] == "full"}
    o = {r["n"]: r["recall1"] for r in rows if r["variant"] == "oneline"}
    print("  " + str([(n, round((f[n] - o[n]) * 100, 1)) for n in sorted(f) if n in o]))


if __name__ == "__main__":
    main()
