"""Case 04 - resume into a workspace that moved (claim 187).

A session is bound to a working directory. The directory is moved away. The session
is resumed and a tool runs.

The conditional under test: claim 187's sting is that this "presents as success". The
prediction is that the silence is a property of how FORGIVING the tool layer is, not
of the architecture - so the same resume is run against a strict tool and a forgiving
one, and the difference is the finding.
"""

import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import harness  # noqa: E402


def strict_write(workspace, name, body):
    """Refuses to invent a working directory."""
    if not os.path.isdir(workspace):
        raise FileNotFoundError(workspace)
    p = os.path.join(workspace, name)
    with open(p, "w") as f:
        f.write(body)
    return p


def forgiving_write(workspace, name, body):
    """Creates missing parents, which is the common convenience."""
    os.makedirs(workspace, exist_ok=True)
    p = os.path.join(workspace, name)
    with open(p, "w") as f:
        f.write(body)
    return p


def trial(tool):
    root = tempfile.mkdtemp()
    try:
        db = os.path.join(root, "state.db")
        workspace = os.path.join(root, "project")
        os.makedirs(workspace)
        harness.init(db)

        cx = harness.connect(db)
        key = harness.session_key("main", "cli", "chat-1")
        sid = harness.resolve_session(cx, key, workspace=workspace)
        harness.take_turn(cx, sid, "first turn")
        cx.close()

        # The directory moves. Nothing tells the session.
        shutil.move(workspace, os.path.join(root, "project-renamed"))

        # Resume: fresh connection, fresh process-equivalent, no live state.
        cx = harness.connect(db)
        sid2 = harness.resolve_session(cx, key)
        ws = cx.execute("SELECT workspace FROM sessions WHERE session_id=?", (sid2,)).fetchone()[0]
        transcript = cx.execute(
            "SELECT COUNT(*) FROM messages WHERE session_id=?", (sid2,)
        ).fetchone()[0]
        resumed = (sid2 == sid) and transcript == 1

        try:
            path = tool(ws, "output.txt", "work")
            outcome = "SILENT WRONG PLACE" if not os.path.exists(
                os.path.join(root, "project-renamed", "output.txt")
            ) else "correct place"
            loud = False
        except FileNotFoundError:
            path, outcome, loud = None, "refused", True
        return resumed, outcome, loud, path, root
    finally:
        pass  # root cleaned by caller reporting


if __name__ == "__main__":
    print("case 04 - resume into a workspace that moved (claim 187)")
    print()
    for label, tool in (("strict tool", strict_write), ("forgiving tool", forgiving_write)):
        resumed, outcome, loud, path, root = trial(tool)
        print(f"  {label:<16} resume succeeded: {resumed}")
        print(f"  {'':<16} tool outcome ...: {outcome}")
        print(f"  {'':<16} failure is loud : {loud}")
        if path:
            print(f"  {'':<16} wrote to .......: {path.replace(root, '<tmp>')}")
        print()
        shutil.rmtree(root, ignore_errors=True)
    print("  predicted: resume succeeds in both; strict raises (loud),")
    print("             forgiving writes silently to a recreated directory.")
