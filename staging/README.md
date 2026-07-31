# staging/ - captured but not yet ingested

Holding area for sources that have been **captured** (transcript, frames, article text downloaded)
but **not distilled**. Nothing here is part of the brain yet.

## Why this is not `sources/`

`sources/<id>/` is the contract's namespace: `validate.py` treats **every** directory there as a
finished source and checks it - INDEX row, legal `SOURCE.md` Status and Visual leg, every kept frame
cited. A half-captured folder fails all of those, and the only ways to silence it are to fake an
INDEX row for a source nobody can read, or to delete a capture that cost bandwidth to make.

So: **a capture becomes a source when it is distilled, not when it is downloaded.** Until then it
lives here, where the validator does not look and the contract makes no claims about it.

## Contents (git-ignored except this file)

**Currently empty.**

## Check that a capture is actually abandoned before moving it here

> **This folder's first use was a mistake, and the lesson is the point of this section.** An
> untracked source folder with an unfilled `SOURCE.md` was read as "interrupted last session" and
> moved here. It was in fact **another agent working the source concurrently** - it had written a
> fresh set of frames minutes earlier. Its working directory was moved out from under it, and
> because `staging/` is git-ignored, finishing the pass there would have had `git add -A` silently
> skip the entire source.

**An unfilled template tells you nothing about whether a process is live. `ls -la` does.** Before
moving anything here, check modification times across the folder - `raw/`, `visuals/` and the
template files. Recent writes mean **leave it alone**: a validator failing loudly on an in-flight
source is strictly better than a live agent writing into a git-ignored path.

## Resuming one

Move it back into `sources/` and run the normal flow from the capture stage (`AGENTS.md` § "The
paste-a-URL trigger", steps 3-7). Do **not** move it back before you intend to finish: the folder
only satisfies the validator once `SOURCE.md`, `nodes.md` and `LEARNING.md` are real and every kept
frame is cited.
