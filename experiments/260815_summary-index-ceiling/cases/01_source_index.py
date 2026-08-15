"""Arm A - the live instance: this brain's 26 INDEX.md source rows.

A DEMONSTRATION, not a test. 26 items cannot answer a question about ~100; this
arm exists because it is the real running index. See PREDICTIONS.md.

Items    : each source's INDEX.md row, in three richness variants.
Queries  : bullets from each source's LEARNING.md '## Key claims' section.
Truth    : the folder that LEARNING.md lives in.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from harness import (ROOT, Corpus, Item, Query, first_sentence,  # noqa: E402
                     print_table, source_dirs, split_row, sweep)

ROW_RE = re.compile(r"^\| .+ \| (video|blog|paper|code) \| ")


def build() -> Corpus:
    c = Corpus()
    folder_re = re.compile(r"sources/([0-9]{6}_[a-z0-9-]+)")

    for line in (ROOT / "INDEX.md").read_text(encoding="utf-8").splitlines():
        if not ROW_RE.match(line):
            continue
        cols = split_row(line)
        if len(cols) < 6:
            continue
        title, _type, summary, topics, when, folder_cell = cols[:6]
        m = folder_re.search(folder_cell)
        if not m:
            continue
        key = m.group(1)
        c.items[key] = Item(key=key, variants={
            "title": title,
            "oneline": first_sentence(summary),
            "full": f"{title}. {summary} {when}",
        })

    for d in source_dirs():
        lm = d / "LEARNING.md"
        if not lm.exists() or d.name not in c.items:
            continue
        text = lm.read_text(encoding="utf-8")
        m = re.search(r"^## Key claims\s*$(.*?)^## ", text, re.M | re.S)
        if not m:
            continue
        for bullet in re.findall(r"^- (.+?)(?=^- |\Z)", m.group(1), re.M | re.S):
            q = " ".join(bullet.split())
            if len(q) > 40:
                c.queries.append(Query(text=q, truth=d.name))
    return c


def main() -> None:
    c = build()
    print(f"Arm A: {len(c.items)} index items, {len(c.usable_queries())} queries\n")
    sizes = [2, 4, 8, 16, 26]
    rows = []
    for variant in ("full", "oneline", "title"):
        rows += sweep(c, variant, sizes, draws=8, seed=11)
    print_table(rows)


if __name__ == "__main__":
    main()
