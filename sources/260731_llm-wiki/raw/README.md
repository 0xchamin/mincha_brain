# raw/ - captured source text (ground truth)

Holds the **text leg** of this source, captured verbatim before distillation:

- **Video:** `transcript.vtt` (+ `.json` with timestamps) from yt-dlp captions, or Whisper output.
- **Blog:** `article.md` (clean text from web_fetch).
- **Paper:** `paper.pdf` + `paper.txt` (extracted text).

Everything in `raw/` is **transient local scratch** and git-ignored (except this README) - see
`../../.gitignore`. It is processed then discarded; only derived text worth keeping is promoted into
`SOURCE.md` / `LEARNING.md` / `nodes.md`, and curated frames that survive the corroboration gate
live in `../visuals/`. Nothing here is authoritative once distilled, so it never needs committing.
