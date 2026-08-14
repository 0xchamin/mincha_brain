"""Case 03 - crash between the side effect and the reply (claim 190, n19).

A worker performs an external side effect, commits the transcript, records a delivery
obligation, then sends. It is killed hard (os._exit, no cleanup) at one of two points.
Recovery then runs in one of two modes and we count how many times the external side
effect happened in total. Two is a duplicate.

The third combination is the point of this case: killing BEFORE the transcript commits
leaves no record the tool ever ran, so the ledger has nothing to recover from.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import harness  # noqa: E402


def task(db, sid, effects, kill_at):
    """The unit of work. Kills the process hard at kill_at."""
    cx = harness.connect(db)
    harness.appender(effects, "SIDE-EFFECT")()  # the irreversible thing
    if kill_at == "after_effect":
        os._exit(9)
    turn = harness.take_turn(cx, sid, "done")
    did = harness.record_obligation(cx, sid, turn)
    if kill_at == "after_commit":
        os._exit(9)
    harness.mark(cx, did, "attempting")
    harness.appender(os.path.join(os.path.dirname(effects), "sent.log"), "REPLY")()
    harness.mark(cx, did, "delivered")
    cx.close()


def recover(db, sid, effects, mode):
    cx = harness.connect(db)
    pend = harness.pending_obligations(cx)
    if mode == "ledger" and pend:
        # An obligation exists: the work is known done. Retry ONLY the send.
        for did, _s, _t in pend:
            harness.mark(cx, did, "attempting")
            harness.appender(os.path.join(os.path.dirname(effects), "sent.log"), "REPLY")()
            harness.mark(cx, did, "delivered")
        cx.close()
        return "retried delivery only"
    delivered = cx.execute(
        "SELECT COUNT(*) FROM delivery WHERE session_id=? AND state='delivered'", (sid,)
    ).fetchone()[0]
    cx.close()
    if delivered == 0:
        # No evidence of a reply. Naive recovery, and the only recovery available to
        # the ledger when the crash preceded the commit: rerun the whole task.
        task(db, sid, effects, kill_at=None)
        return "reran the whole task"
    return "nothing to do"


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "--task":
    task(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    sys.exit(0)


def trial(kill_at, mode):
    d = tempfile.mkdtemp()
    try:
        db = os.path.join(d, "state.db")
        effects = os.path.join(d, "world.log")
        harness.init(db)
        cx = harness.connect(db)
        sid = harness.resolve_session(cx, harness.session_key("main", "cli", "chat-1"))
        cx.close()
        subprocess.run(
            [sys.executable, __file__, "--task", db, sid, effects, kill_at],
            capture_output=True,
        )
        action = recover(db, sid, effects, mode)
        return len(harness.read_effects(effects)), action
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    N = 25
    print("case 03 - crash between the side effect and the reply (claim 190)")
    print(f"  N = {N} per row. 'effects' counts how many times the irreversible thing happened.")
    print()
    rows = [
        ("after_commit", "naive", "100% duplicate"),
        ("after_commit", "ledger", "0% duplicate"),
        ("after_effect", "ledger", "100% duplicate - the open window"),
    ]
    for kill_at, mode, predicted in rows:
        counts = []
        action = ""
        for _ in range(N):
            c, action = trial(kill_at, mode)
            counts.append(c)
        dup = sum(1 for c in counts if c > 1)
        print(f"  kill {kill_at:<13} recovery {mode:<7} -> duplicated {dup:>2}/{N}"
              f"  ({100.0*dup/N:5.1f}%)   [{action}]")
        print(f"       predicted: {predicted}")
