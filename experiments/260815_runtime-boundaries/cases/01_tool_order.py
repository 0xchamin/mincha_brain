"""Case 01 - transcript order against side-effect order (claim 189).

Two tools dispatched concurrently, each appending one line to a shared file. Results
are restored in model-call order. Question: does the file order match the transcript
order? Reported as a distribution over N runs, never pass/fail (claim 114).
"""

import os
import random
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import harness  # noqa: E402

N = 200


def one_run(jitter):
    d = tempfile.mkdtemp()
    try:
        effects = os.path.join(d, "world.log")
        tools = [
            harness.appender(effects, "A", random.uniform(0, jitter) if jitter else 0.0),
            harness.appender(effects, "B", random.uniform(0, jitter) if jitter else 0.0),
        ]
        transcript = harness.run_tools(tools, concurrent=True)  # model-call order
        actual = harness.read_effects(effects)
        return transcript == actual
    finally:
        shutil.rmtree(d, ignore_errors=True)


def condition(label, jitter):
    agree = sum(one_run(jitter) for _ in range(N))
    diverged = N - agree
    pct = 100.0 * diverged / N
    print(f"  {label:<34} diverged {diverged:>3}/{N}  ({pct:5.1f}%)")
    return diverged, pct


if __name__ == "__main__":
    print("case 01 - transcript order vs side-effect order (claim 189)")
    print(f"  N = {N} per condition, 2 concurrent tools appending to one file")
    a_div, a_pct = condition("(a) realistic work, no delay", 0.0)
    b_div, b_pct = condition("(b) jittered work, <= 3ms", 0.003)
    print()
    print(f"  RESULT (a): {a_pct:.1f}% divergence   (predicted 5-40%, wide and unsure)")
    print(f"  RESULT (b): {b_pct:.1f}% divergence   (predicted ~50%)")
