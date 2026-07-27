#!/usr/bin/env python3
"""
tools/ingest.py - the mechanical half of a media ingest.

A TOOLBOX, NOT A PIPELINE. AGENTS.md is deliberate that "the shell steps are reference,
not a fixed script - the approach you assemble for the source at hand". So this exposes
independent subcommands you compose per source; it does not own the flow, and there is no
`--url do-everything` entrypoint. Assembly stays the agent's job.

What belongs here: deterministic steps that must not vary between runs - especially the
ADR-0003 static-video probe, whose `<= 3 distinct frames` threshold is meaningless if every
agent computes "distinct" with a different scene threshold or hash distance.

What must never come here: judgement. Reading a slide, gating a claim, deciding which frames
earn their place - those stay in AGENTS.md and the personas. This file crops images; it does
not decide what they mean.

Subcommands
    transcript  VTT -> de-duplicated, timestamped blocks     (stdlib only, no network)
    probe       scene-detect + phash dedup -> ADR-0003 verdict
    frames      extract frames at given timestamps
    sheet       tile frames into contact sheets for cheap triage

Examples
    python3 tools/ingest.py transcript raw/VIDEO.en.vtt raw/transcript.txt
    python3 tools/ingest.py probe raw/VIDEO.mp4
    python3 tools/ingest.py frames raw/VIDEO.mp4 --at 233,290,378 --out /tmp/cand
    python3 tools/ingest.py sheet /tmp/cand --out /tmp/sheet

Requires `ffmpeg` on PATH for probe/frames/sheet, and the .venv packages (Pillow,
imagehash) for probe. `transcript` needs neither.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ADR-0003: a video yielding no more than this many DISTINCT frames is visually static
# (podcast / webcam interview), so the visual leg auto-degrades to transcript-only.
# Calibration: 260725_12-factor-agents, a slide-heavy talk, yields 19.
STATIC_FRAME_THRESHOLD = 3

# Pipeline constants. Change these and every past probe verdict becomes incomparable -
# that is the whole reason they live in code rather than in prose.
SCENE_THRESHOLD = 0.30   # ffmpeg select='gt(scene,X)'
PHASH_DISTANCE = 10      # imagehash pHash Hamming distance below which frames are "the same"

# ADR-0006: a STATIC verdict is ADVISORY, never dispositive. Scene detection measures
# WHOLE-FRAME delta, so a heavily templated deck (fixed background, logo, speaker inset,
# footer) can change every slide and still never cross SCENE_THRESHOLD. Observed twice:
# 260726_dont-ship-skills-without-evals (candidates=3 on ~20 dense slides) and, at the
# dedup stage, 260725_12-factor-agents. So on STATIC we sample evenly across the runtime
# and tile one confirmation sheet: the agent spends ONE `view` call before honouring a
# verdict that would otherwise discard the entire visual leg.
#
# Deliberately additive: the verdict and the three constants above are untouched, so every
# past probe result stays comparable. Confirming a verdict is not the same as recomputing it.
CONFIRM_SAMPLES = 9


def die(msg: str, code: int = 2) -> "None":
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def need_ffmpeg() -> None:
    if not shutil.which("ffmpeg"):
        die("ffmpeg not found on PATH (macOS: brew install ffmpeg)")


def run_ffmpeg(args: list[str]) -> str:
    """Run ffmpeg and FAIL LOUDLY, returning stderr (where showinfo/progress go).

    Checking the return code is not pedantry here. The probe infers "visually static"
    from finding few frames, so a silently failing ffmpeg looks exactly like a podcast:
    zero frames, verdict STATIC, visual leg skipped, nobody told. An ingest must never
    lose its second leg to an unreported error.
    """
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", *args],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        tail = "\n".join(proc.stderr.strip().splitlines()[-6:])
        die(f"ffmpeg failed (exit {proc.returncode}):\n{tail}")
    return proc.stderr


# --------------------------------------------------------------------------
# transcript - stdlib only, deterministic, the piece most often rewritten
# --------------------------------------------------------------------------

TS_RE = re.compile(r"^(\d\d):(\d\d):(\d\d)\.\d+ -->")
TAG_RE = re.compile(r"<[^>]+>")
SKIP_PREFIXES = ("WEBVTT", "Kind:", "Language:", "NOTE")


def vtt_to_blocks(vtt_text: str, block_seconds: int = 15) -> list[str]:
    """Turn a VTT (including YouTube's rolling auto-captions) into timestamped blocks.

    YouTube repeats each line across several cues to animate the caption roll, so naive
    parsing yields the transcript three times over. De-duplicating by exact line and
    keeping the FIRST timestamp each line appeared at is what makes `&t=` deep-links land
    on the right moment.

    INVARIANT: every line in a block was spoken less than `block_seconds` after that
    block's header timestamp. The block is closed BEFORE the cue that would breach it,
    never after - otherwise a cue arriving long after the block opened gets filed under
    the old timestamp and its `&t=` link points at the wrong moment. That matters because
    YouTube emits no cues during silence, so a musical interlude, a long pause or an
    unmiked audience question leaves a gap of arbitrary size between consecutive cues.
    """
    seen: set[str] = set()
    cues: list[tuple[int, str]] = []
    current = 0

    for raw in vtt_text.splitlines():
        m = TS_RE.match(raw)
        if m:
            h, mm, s = (int(x) for x in m.groups())
            current = h * 3600 + mm * 60 + s
            continue
        line = TAG_RE.sub("", raw).strip()
        if not line or line.startswith(SKIP_PREFIXES) or line == "&nbsp;":
            continue
        if line in seen:
            continue
        seen.add(line)
        cues.append((current, line))

    def emit(start: int, lines: list[str]) -> str:
        return f"[{start // 60:02d}:{start % 60:02d} t={start}] " + " ".join(lines)

    blocks: list[str] = []
    buf: list[str] = []
    start: int | None = None
    for ts, line in cues:
        # Close before appending, so `line` opens a new block rather than being filed
        # under a header it postdates by more than block_seconds.
        if start is not None and ts - start >= block_seconds:
            blocks.append(emit(start, buf))
            buf, start = [], None
        if start is None:
            start = ts
        buf.append(line)
    if buf and start is not None:
        blocks.append(emit(start, buf))
    return blocks


def cmd_transcript(args: argparse.Namespace) -> int:
    src = Path(args.vtt)
    if not src.exists():
        die(f"no such file: {src}")
    blocks = vtt_to_blocks(src.read_text(encoding="utf-8"), args.block_seconds)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(blocks) + "\n", encoding="utf-8")
    words = sum(len(b.split()) for b in blocks)
    print(f"{len(blocks)} blocks, ~{words} words -> {out}")
    return 0


# --------------------------------------------------------------------------
# probe - the ADR-0003 static-video detector
# --------------------------------------------------------------------------

def scene_frames(video: Path, outdir: Path) -> list[Path]:
    need_ffmpeg()
    outdir.mkdir(parents=True, exist_ok=True)
    run_ffmpeg([
        "-loglevel", "error", "-i", str(video),
        "-vf", f"select='gt(scene,{SCENE_THRESHOLD})',scale=480:-1",
        "-vsync", "vfr", "-q:v", "5", "-pix_fmt", "yuvj420p",
        str(outdir / "c_%04d.jpg"),
    ])
    return sorted(outdir.glob("c_*.jpg"))


def distinct_count(frames: list[Path]) -> int:
    """Collapse near-identical frames with pHash. Returns the distinct count."""
    try:
        import imagehash          # type: ignore
        from PIL import Image     # type: ignore
    except ImportError:
        die("probe needs Pillow + imagehash (pip install -r requirements.txt), "
            "or run it with the kit's .venv python")
    kept: list = []
    for f in frames:
        h = imagehash.phash(Image.open(f))
        if any(h - k <= PHASH_DISTANCE for k in kept):
            continue
        kept.append(h)
    return len(kept)


def duration_seconds(video: Path) -> int:
    """Runtime in whole seconds, via ffprobe. 0 if it cannot be determined."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(video)],
            capture_output=True, text=True, check=True).stdout.strip()
        return int(float(out))
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return 0


def confirmation_sheet(video: Path, out: Path) -> Path | None:
    """ADR-0006: tile CONFIRM_SAMPLES frames spread across the runtime into one sheet.

    The cheapest possible check on a STATIC verdict - one `view` call. Returns the sheet
    path, or None if the runtime could not be read (in which case say so; never pretend
    the verdict was confirmed).
    """
    dur = duration_seconds(video)
    if dur <= 0:
        return None
    step = dur / (CONFIRM_SAMPLES + 1)
    stamps = [int(step * (i + 1)) for i in range(CONFIRM_SAMPLES)]
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmpd = Path(tmp)
        for idx, t in enumerate(stamps):
            # Zero-padded so the tile order is chronological. Plain frame_<seconds> names
            # sort as STRINGS, which is why frame_1100 precedes frame_60 in a `sheet` call.
            run_ffmpeg(["-loglevel", "error", "-ss", str(t), "-i", str(video),
                        "-frames:v", "1", "-vf", "scale=640:-1", "-q:v", "4",
                        "-pix_fmt", "yuvj420p", str(tmpd / f"{idx:03d}_t{t}.jpg")])
        run_ffmpeg([
            "-loglevel", "error", "-pattern_type", "glob", "-i", str(tmpd / "*.jpg"),
            "-filter_complex",
            "scale=640:-1,tile=3x3:margin=8:padding=6:color=white",
            "-frames:v", "1", "-pix_fmt", "yuvj420p", str(out),
        ])
    return out if out.exists() else None


def cmd_probe(args: argparse.Namespace) -> int:
    video = Path(args.video)
    if not video.exists():
        die(f"no such file: {video}")
    with tempfile.TemporaryDirectory() as tmp:
        cands = scene_frames(video, Path(tmp))
        n = distinct_count(cands) if cands else 0

    static = n <= STATIC_FRAME_THRESHOLD
    verdict = "STATIC" if static else "RICH"
    print(f"candidates={len(cands)} distinct={n} threshold={STATIC_FRAME_THRESHOLD} -> {verdict}")
    if static:
        print(f"ADR-0003: probe says visually static ({n} distinct).")
        if args.no_confirm:
            print("ADR-0006: confirmation skipped (--no-confirm). You are honouring an "
                  "ADVISORY verdict unchecked - say so in SOURCE.md.")
        else:
            dest = Path(args.confirm_out) if args.confirm_out else video.parent / "probe_confirm.jpg"
            sheet = confirmation_sheet(video, dest)
            if sheet is None:
                print("ADR-0006: could not build the confirmation sheet (no readable "
                      "duration). Do NOT record this as a confirmed STATIC.")
            else:
                print(f"ADR-0006: STATIC is ADVISORY, not dispositive. `view` this sheet "
                      f"before skipping the visual leg:\n  {sheet}\n"
                      f"  {CONFIRM_SAMPLES} frames spread across the runtime, chronological.\n"
                      f"  Scene-detect measures WHOLE-FRAME delta, so a templated slide deck "
                      f"(fixed background / logo / speaker inset / footer) reads as static "
                      f"while every slide changes. If you see differing slides, OVERRIDE: "
                      f"analyse the visual leg via transcript-anchored `frames`, and record "
                      f"the override in SOURCE.md.")
        print(f"If confirmed static: record 'Visual leg: skipped (static probe: {n} distinct)' "
              f"in SOURCE.md. Every node from this source is then single-leg by construction.")
    else:
        print(f"ADR-0003: analyse the visual leg. Record "
              f"'Visual leg: analysed (N frames kept)' once pruned.")
    # Exit 0 either way: a static video is a valid outcome, not an error.
    return 0


# --------------------------------------------------------------------------
# frames / sheet - extraction and cheap triage
# --------------------------------------------------------------------------

def cmd_frames(args: argparse.Namespace) -> int:
    need_ffmpeg()
    video = Path(args.video)
    if not video.exists():
        die(f"no such file: {video}")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    try:
        stamps = [int(s) for s in args.at.split(",") if s.strip()]
    except ValueError:
        die("--at must be comma-separated whole seconds, e.g. 233,290,378")

    vf = f"scale={args.width}:-1"
    if args.crop:
        # Slide area of a typical conference recording: drop the speaker inset on the left.
        vf = f"crop=iw*0.72:ih*0.80:iw*0.28:0,{vf}"

    for t in stamps:
        dest = out / f"{args.prefix}{t}.jpg"
        run_ffmpeg(["-loglevel", "error", "-ss", str(t), "-i", str(video),
                    "-frames:v", "1", "-vf", vf, "-q:v", str(args.quality),
                    "-pix_fmt", "yuvj420p", str(dest)])
    made = sorted(out.glob(f"{args.prefix}*.jpg"))
    print(f"{len(made)} frames -> {out}")
    return 0


def cmd_sheet(args: argparse.Namespace) -> int:
    """Tile frames into contact sheets so the agent spends 1-2 `view` calls, not 17.

    The triage trick from the 12-factor ingest: look at grids first, then pull only the
    dense frames at full resolution.
    """
    need_ffmpeg()
    src = Path(args.dir)
    imgs = sorted(src.glob("*.jpg"))
    if not imgs:
        die(f"no .jpg files in {src}")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    per = args.cols * args.rows
    sheets = (len(imgs) + per - 1) // per

    run_ffmpeg([
        "-loglevel", "error", "-pattern_type", "glob", "-i", str(src / "*.jpg"),
        "-filter_complex",
        f"scale={args.tile_width}:-1,tile={args.cols}x{args.rows}:margin=8:padding=6:color=white",
        "-frames:v", str(sheets), "-pix_fmt", "yuvj420p", f"{out}_%d.jpg",
    ])
    made = sorted(out.parent.glob(f"{out.name}_*.jpg"))
    print(f"{len(imgs)} frames -> {len(made)} sheet(s) ({args.cols}x{args.rows}): "
          + ", ".join(str(m) for m in made))
    print("Frames are tiled in filename order, left-to-right, top-to-bottom.")
    return 0


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Mechanical half of a media ingest (a toolbox - compose as needed).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Judgement stays in AGENTS.md. This file crops images; it does not decide "
               "what they mean.",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("transcript", help="VTT -> de-duplicated timestamped blocks")
    p.add_argument("vtt")
    p.add_argument("out")
    p.add_argument("--block-seconds", type=int, default=15)
    p.set_defaults(func=cmd_transcript)

    p = sub.add_parser("probe", help="ADR-0003 static-video probe (+ ADR-0006 confirmation)")
    p.add_argument("video")
    p.add_argument("--confirm-out", default=None,
                   help="where to write the ADR-0006 confirmation sheet "
                        "(default: <video dir>/probe_confirm.jpg)")
    p.add_argument("--no-confirm", action="store_true",
                   help="skip the confirmation sheet on a STATIC verdict. You are then "
                        "honouring an advisory verdict unchecked - record that in SOURCE.md.")
    p.set_defaults(func=cmd_probe)

    p = sub.add_parser("frames", help="extract frames at given timestamps")
    p.add_argument("video")
    p.add_argument("--at", required=True, help="comma-separated seconds, e.g. 233,290")
    p.add_argument("--out", required=True)
    p.add_argument("--prefix", default="frame_")
    p.add_argument("--width", type=int, default=1100)
    p.add_argument("--quality", type=int, default=3)
    p.add_argument("--crop", action="store_true", help="crop to the slide area")
    p.set_defaults(func=cmd_frames)

    p = sub.add_parser("sheet", help="tile frames into contact sheets for triage")
    p.add_argument("dir")
    p.add_argument("--out", required=True, help="output stem, e.g. /tmp/sheet")
    p.add_argument("--cols", type=int, default=3)
    p.add_argument("--rows", type=int, default=3)
    p.add_argument("--tile-width", type=int, default=560)
    p.set_defaults(func=cmd_sheet)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
