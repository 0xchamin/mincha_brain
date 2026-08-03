# Source - autoresearch (Andrej Karpathy)

> Persona: **code-explorer** - re-adopt when working this file.

> Metadata + facts for one ingested source (video / blog / paper / code). Single source of truth for
> this source; other docs here link to this table. The agent fills it on the paste-a-URL trigger
> and keeps it current. Name this folder `YYMMDD_slug` (see `../../AGENTS.md`).

## Facts

| Field | Value |
|---|---|
| Owner | chamin |
| Type | code |
| URL | https://github.com/karpathy/autoresearch |
| Title | autoresearch - AI agents running research on single-GPU nanochat training automatically |
| Author / channel | Andrej Karpathy (`karpathy`) |
| Published | Repo created 2026-03-06; last push 2026-03-26 |
| Duration / length | 10 files, ~1,000 LOC of Python; `program.md` is 115 lines; README 92 lines |
| Commit SHA | `228791fb499afffb54b46200aca536f79142f117` (default branch `master`, 2026-03-26) |
| License | **MIT**, declared in `README.md` §License only - **there is no `LICENSE` file in the repo and the GitHub API reports `license: null`**. Treated as MIT on the author's written statement; recorded here because the machine-readable declaration is missing. |
| Ingested | 2026-08-03 |
| Access | open (public repo, unauthenticated) |
| Topics | autonomous-research-loops, evals, agents, context-engineering, skills |
| Visual leg | analysed (3 frames kept) - the repo ships one real results figure (`progress.png`) and it is the only empirical evidence in the source; kept as a full view plus two teaching crops |
| Status | compounded |

## Reading order for this source

1. `SOURCE.md` - this file (facts).
2. `MAP.md` - repo orientation (what it demonstrates, module map, the loop worth tracing).
3. `repo/` - the pinned snapshot (git-ignored).
4. `nodes.md` - knowledge nodes (gated claims + citations).
5. `context/` - external evidence from a deep-research pass (**empty - not requested**).
6. `LEARNING.md` - the distilled learning document.
7. `visuals/` - the curated figures.

## Ingest notes

- **Capture method: file-level fetch at the pinned SHA, not `git clone`.** The owner declined the
  clone mid-ingest, and the repo is 10 files, so each file was fetched from
  `raw.githubusercontent.com/.../<sha>/<path>` into `repo/` (git-ignored, with the SHA recorded in
  `repo/.PINNED_SHA`). **Consequence, recorded rather than discovered:** there is no local git
  history, so no `git log` / `git blame` leg was available - every code citation here is to the
  pinned blob and nothing in this ingest rests on the repo's commit history.
- **`gh` was present (v2.97.0) but unauthenticated**, so metadata, HEAD SHA and the file tree came
  from the public REST API instead. License had to be read out of the README by hand for the reason
  in the table above.
- **Code orientation:** the repo is small enough to read in full and was read in full - `program.md`
  (115 lines), `prepare.py` (390), `train.py` (631), `README.md` (92), `analysis.ipynb` (11 cells).
  No sparse checkout or trace-on-demand was needed. `uv.lock` (443 KB) was not fetched.
- **Nothing was executed.** The repo requires a single NVIDIA GPU (`README.md` §Requirements) and
  the owner has none. **Every claim here is read off the code and the shipped figure; no run of this
  code was observed by this brain**, and `progress.png` is the author's own result, not a
  reproduction.
- **Scope, set by the owner at ingest:** learn the **research-agent harness** - how an autonomous
  experiment loop is specified, bounded and judged. The transformer/optimizer internals of
  `train.py` are treated as *the artifact under optimization*, not as the subject; the model
  architecture, Muon/AdamW and the attention kernels are deliberately **not** distilled.
- **The visual leg is unusual for a code source.** The contract expects generated diagrams; this
  repo ships an actual results chart (`progress.png`, 2382x1180), which is the source's only
  evidence that the loop produces anything. It was `view`ed at full size and cropped into two
  teaching views. Generated mermaid diagrams appear inline in `MAP.md` and `LEARNING.md` and are
  labelled as generated.
- **Limitation that shapes the gate:** `results.tsv` - the actual experiment ledger behind
  `progress.png` - is **untracked by design** (`program.md:102`) and is not in the repo. So the
  figure cannot be re-derived, and every number read from it (keep rate, per-experiment deltas) is
  **read off a rendered chart**, not off data. Nodes depending on those readings are gated
  accordingly.

> Inherits the global rules in `../../AGENTS.md`. Overrides (if any): none.
