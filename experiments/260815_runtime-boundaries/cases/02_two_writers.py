"""Case 02 - two OS processes, one state.db (claim 191).

S24's LEARNING.md records that nobody has reported what happens here. Two separate
processes each hold their own in-memory active-run guard and both take turns on the
SAME session key against one SQLite file in WAL mode with a busy timeout.

Three things are measured separately, because they are three different questions:
  integrity  does SQLite lose or corrupt rows?
  exclusion  does the in-memory guard exclude anything across processes?
  semantics  do logical turns collide - two readers both seeing turn 5?
"""

import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import harness  # noqa: E402

TURNS = 40
WORK = 0.002  # the read-modify-write gap a second process can slip into


def worker(db_path, sid, key, writer):
    """Runs in its own process, with its own guard instance."""
    cx = harness.connect(db_path)
    guard = harness.ActiveRunGuard()
    busy = 0
    blocked = 0
    for i in range(TURNS):
        if not guard.acquire(key):
            blocked += 1
            continue
        try:
            harness.take_turn(
                cx, sid, f"{writer}-{i}", writer=writer, work=lambda: time.sleep(WORK)
            )
        except Exception as e:  # noqa: BLE001
            if "locked" in str(e).lower() or "busy" in str(e).lower():
                busy += 1
            else:
                raise
        finally:
            guard.release(key)
    cx.close()
    print(f"{writer} busy={busy} blocked={blocked}")


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "--worker":
    worker(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    sys.exit(0)


def main():
    d = tempfile.mkdtemp()
    try:
        db = os.path.join(d, "state.db")
        harness.init(db)
        cx = harness.connect(db)
        key = harness.session_key("main", "telegram", "chat-1")
        sid = harness.resolve_session(cx, key)
        cx.close()

        procs = [
            subprocess.Popen(
                [sys.executable, __file__, "--worker", db, sid, key, w],
                stdout=subprocess.PIPE,
                text=True,
            )
            for w in ("proc-A", "proc-B")
        ]
        out = [p.communicate()[0].strip() for p in procs]

        cx = harness.connect(db)
        rows = cx.execute(
            "SELECT turn, writer FROM messages WHERE session_id=? ORDER BY id", (sid,)
        ).fetchall()
        final_turn = cx.execute(
            "SELECT turn FROM sessions WHERE session_id=?", (sid,)
        ).fetchone()[0]
        cx.close()

        turns = [r[0] for r in rows]
        distinct = len(set(turns))
        collisions = len(turns) - distinct
        expected = TURNS * 2

        print("case 02 - two processes, one state.db (claim 191)")
        print(f"  {TURNS} turns per process, 2 processes, WAL + 10s busy timeout")
        for line in out:
            print(f"  worker: {line}")
        print()
        print(f"  rows written .......... {len(rows)} / {expected} expected")
        print(f"  distinct turn numbers . {distinct}")
        print(f"  TURN COLLISIONS ....... {collisions}")
        print(f"  final sessions.turn ... {final_turn}  (would be {expected} if no lost updates)")
        print(f"  LOST UPDATES .......... {expected - final_turn}")
        print()
        print(f"  integrity: {'OK - no rows lost' if len(rows) == expected else 'ROWS LOST'}")
        print(f"  exclusion: {'NONE across processes' if collisions else 'some observed'}")
        print(f"  semantics: {'BROKEN' if collisions else 'held'}")
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    main()
