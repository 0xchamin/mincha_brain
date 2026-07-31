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

| Folder | What it is | Stopped at |
|---|---|---|
| `260731_anthropic-memory-and-dreaming/` | Anthropic conference talk on **memory and dreaming in Claude Managed Agents** (~21 min). Has `raw/video.webm`, both VTT caption tracks, a de-duplicated `raw/transcript.txt`, and 30 extracted frames. `SOURCE.md` is still the unfilled template. | **capture** - nothing gated, nothing distilled |

## Resuming one

Move it back into `sources/` and run the normal flow from the capture stage (`AGENTS.md` § "The
paste-a-URL trigger", steps 3-7). Do **not** move it back before you intend to finish: the folder
only satisfies the validator once `SOURCE.md`, `nodes.md` and `LEARNING.md` are real and every kept
frame is cited.

> **Priority note.** The Anthropic talk is the designated **independent second leg** for
> [`brain/topics/memory.md`](../brain/topics/memory.md), which currently rests on one T2 vendor post
> about a consumer product and contains **zero measurements**. Different organisation, different
> commercial interest, and an agent-platform framing rather than a chat-assistant one - so it is
> what should take `memory` from `emerging` to `established`. See
> [ADR-0007](../brain/decisions/0007-memory-topic.md).
