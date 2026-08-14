"""A minimal agent runtime, written to test boundaries rather than to be one.

Stdlib only. No model, no network, no API key - possible because every claim under
test here is about the runtime rather than about inference, which is claim 194 taken
at its word.

What it models, in the vocabulary of S24:

  session key   deterministic routing identity, derived from source fields
  session id    one durable conversation incarnation
  transcript    ordered message rows in SQLite
  tool runtime  dispatches tool calls, optionally concurrently
  delivery      a ledger row moving pending -> attempting -> delivered

Deliberately NOT modelled: prompts, context assembly, providers, any LLM. See
PREDICTIONS.md for what each case does with this.
"""

import os
import sqlite3
import threading
import time


# ---------------------------------------------------------------- storage ---

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id  TEXT PRIMARY KEY,
    session_key TEXT NOT NULL,
    workspace   TEXT,
    turn        INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    turn       INTEGER NOT NULL,
    role       TEXT NOT NULL,
    body       TEXT NOT NULL,
    writer     TEXT
);
CREATE TABLE IF NOT EXISTS delivery (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    turn       INTEGER NOT NULL,
    state      TEXT NOT NULL
);
"""


def connect(db_path):
    """WAL plus a busy timeout - the configuration S24 describes."""
    cx = sqlite3.connect(db_path, timeout=10.0, isolation_level=None)
    cx.execute("PRAGMA journal_mode=WAL")
    cx.execute("PRAGMA busy_timeout=10000")
    return cx


def init(db_path):
    cx = connect(db_path)
    cx.executescript(SCHEMA)
    cx.close()


# --------------------------------------------------------------- identity ---


def session_key(profile, platform, chat, thread=None, user=None):
    """The routing identity. Which fields appear here IS the isolation policy
    (claim 185) - pass user to isolate per participant, omit it to share."""
    parts = [f"agent:{profile}", platform, chat]
    if thread:
        parts.append(f"thread-{thread}")
    if user:
        parts.append(f"user-{user}")
    return ":".join(parts)


def resolve_session(cx, key, workspace=None):
    """Key -> session id, creating one incarnation if the lane is new.

    Note the two identities are separate rows-worth of state, which is claim 184.
    """
    row = cx.execute(
        "SELECT session_id FROM sessions WHERE session_key=? ORDER BY rowid DESC LIMIT 1", (key,)
    ).fetchone()
    if row:
        return row[0]
    sid = f"sess-{abs(hash(key)) % 10**8}-{int(time.time()*1000) % 10**6}"
    cx.execute(
        "INSERT INTO sessions (session_id, session_key, workspace) VALUES (?,?,?)",
        (sid, key, workspace),
    )
    return sid


# ----------------------------------------------------------- tool runtime ---


def run_tools(tools, concurrent=True):
    """Dispatch tools, then return results in MODEL-CALL order.

    This is the mechanism under test in case 01. The reordering into call order is
    exactly what S24 describes as keeping the transcript structurally valid, and it
    is deliberately faithful: results are re-sorted, side effects are not.
    """
    results = [None] * len(tools)

    def invoke(i, fn):
        results[i] = fn()

    if concurrent:
        threads = [threading.Thread(target=invoke, args=(i, fn)) for i, fn in enumerate(tools)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    else:
        for i, fn in enumerate(tools):
            invoke(i, fn)
    return results  # index order == model call order, by construction


# ------------------------------------------------------------ active runs ---


class ActiveRunGuard:
    """Mutual exclusion over a session key, held IN MEMORY.

    Faithful to the ownership table's "memory only" cell, which is the whole point
    of case 02: this object cannot see another process.
    """

    def __init__(self):
        self._busy = set()
        self._lock = threading.Lock()

    def acquire(self, key):
        with self._lock:
            if key in self._busy:
                return False
            self._busy.add(key)
            return True

    def release(self, key):
        with self._lock:
            self._busy.discard(key)


# ---------------------------------------------------------------- a turn ----


def take_turn(cx, sid, body, writer=None, work=lambda: None):
    """Read-modify-write of the turn counter, with work in the middle.

    The gap between the read and the write is where a second process gets in, which
    is what case 02 measures. Written the naive way on purpose - this is the shape a
    runtime has when its only mutual exclusion is the in-memory guard.
    """
    turn = cx.execute("SELECT turn FROM sessions WHERE session_id=?", (sid,)).fetchone()[0]
    next_turn = turn + 1
    work()
    cx.execute("UPDATE sessions SET turn=? WHERE session_id=?", (next_turn, sid))
    cx.execute(
        "INSERT INTO messages (session_id, turn, role, body, writer) VALUES (?,?,?,?,?)",
        (sid, next_turn, "assistant", body, writer),
    )
    return next_turn


# -------------------------------------------------------------- delivery ----


def record_obligation(cx, sid, turn):
    cx.execute(
        "INSERT INTO delivery (session_id, turn, state) VALUES (?,?,'pending')", (sid, turn)
    )
    return cx.execute("SELECT last_insert_rowid()").fetchone()[0]


def mark(cx, did, state):
    cx.execute("UPDATE delivery SET state=? WHERE id=?", (state, did))


def pending_obligations(cx):
    return cx.execute(
        "SELECT id, session_id, turn FROM delivery WHERE state IN ('pending','attempting')"
    ).fetchall()


# ------------------------------------------------------------------ tools ---


def appender(path, marker, jitter=0.0):
    """A tool with an external side effect: append a line to a shared file.

    The file is the 'world'. Its line order is the order the effects actually
    happened, which is the thing the transcript does not preserve.
    """

    def fn():
        if jitter:
            time.sleep(jitter)
        with open(path, "a") as f:
            f.write(marker + "\n")
            f.flush()
            os.fsync(f.fileno())
        return marker

    return fn


def read_effects(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [ln.strip() for ln in f if ln.strip()]
