#!/usr/bin/env python3
"""
h7 test: does un-isolatability predict tool-filter failure in AgentDojo?

Conjecture h7 (brain/conjectures.md): the "17% of cases where the task's own tools
suffice for the attack" is a property of the TASK/TOOL SURFACE, not of the defence.

Method, entirely over artifacts AgentDojo publishes - no model calls, no re-running:
  1. AST-parse each suite's user_tasks.py / injection_tasks.py and extract the tool
     names inside each task's ground_truth() method.
  2. A (user, injection) pair is UN-ISOLATABLE iff the injection's required tools are
     a subset of the user task's required tools - the filter has nothing to remove.
  3. Read the shipped run data for the no-defence and tool_filter pipelines and take
     `security == True` as "attacker goal achieved".
  4. Compare P(attack succeeds | un-isolatable) against P(attack succeeds | isolatable),
     under BOTH pipelines. The baseline is the control: if un-isolatability merely
     tracks "generally attackable", it will predict under no defence too.

Usage:
    git clone --depth 1 https://github.com/ethz-spylab/agentdojo
    python3 260805_h7_agentdojo_test.py /path/to/agentdojo

Verified against three published figures before use: Slack baseline 92.4% (paper says
92%), overall baseline 47.7% (Fig 6a ~0.47), tool filter 6.8% (paper says 7.5%).
"""
import ast, json, pathlib, re, sys, collections

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
SUITES = ["workspace", "slack", "travel", "banking"]
V1 = ROOT / "src/agentdojo/default_suites/v1"


def tools_in_ground_truth(cls):
    names = set()
    for fn in [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "ground_truth"]:
        for node in ast.walk(fn):
            if isinstance(node, ast.Call):
                f = node.func
                fname = f.id if isinstance(f, ast.Name) else getattr(f, "attr", None)
                if fname == "FunctionCall":
                    for kw in node.keywords:
                        if kw.arg == "function" and isinstance(kw.value, ast.Constant):
                            names.add(kw.value.value)
                    if node.args and isinstance(node.args[0], ast.Constant):
                        names.add(node.args[0].value)
    return names


def collect(suite, fname, pattern):
    p = V1 / suite / fname
    out = {}
    if not p.exists():
        return out
    for n in ast.walk(ast.parse(p.read_text())):
        if isinstance(n, ast.ClassDef) and re.match(pattern, n.name):
            t = tools_in_ground_truth(n)
            if t:
                out[n.name] = t
    return out


GT = {s: {"user": collect(s, "user_tasks.py", r"UserTask\d+$"),
          "inj":  collect(s, "injection_tasks.py", r"InjectionTask\d+$")} for s in SUITES}


def norm(task_id):
    m = re.match(r"(user|injection)_task_(\d+)$", task_id or "")
    if not m:
        return None
    return ("UserTask" if m.group(1) == "user" else "InjectionTask") + m.group(2)


def analyse(run, label):
    tab, miss = collections.Counter(), 0
    for f in (ROOT / "runs" / run).rglob("*/important_instructions/*.json"):
        d = json.load(open(f))
        uk, ik, s = norm(d.get("user_task_id")), norm(d.get("injection_task_id")), d["suite_name"]
        if not uk or not ik:
            continue
        U, I = GT[s]["user"].get(uk), GT[s]["inj"].get(ik)
        if U is None or I is None:
            miss += 1
            continue
        tab[(set(I) <= set(U), d.get("security") is True)] += 1
    n_un, n_is = tab[(True, True)] + tab[(True, False)], tab[(False, True)] + tab[(False, False)]
    p_un, p_is = tab[(True, True)] / n_un, tab[(False, True)] / n_is
    print(f"\n== {label}  (pairs skipped, unparsed ground truth: {miss}) ==")
    print(f"   un-isolatable : {n_un:4} pairs, {tab[(True,True)]:4} attacks succeeded = {p_un:6.1%}")
    print(f"   isolatable    : {n_is:4} pairs, {tab[(False,True)]:4} attacks succeeded = {p_is:6.1%}")
    if p_is > 0:
        print(f"   risk ratio    : {p_un/p_is:.1f}x")
    a, b, c, d_ = tab[(True, True)], tab[(True, False)], tab[(False, True)], tab[(False, False)]
    n = a + b + c + d_
    if all([a + b, c + d_, a + c, b + d_]):
        chi = n * (a * d_ - b * c) ** 2 / ((a + b) * (c + d_) * (a + c) * (b + d_))
        print(f"   2x2 [[{a},{b}],[{c},{d_}]] n={n}  chi-square={chi:.1f} (df=1, 3.84 => p<0.05)")
    return tab


analyse("gpt-4o-2024-05-13", "NO DEFENCE (control - h7 predicts NO effect here)")
analyse("gpt-4o-2024-05-13-tool_filter", "TOOL FILTER (h7 predicts a large effect here)")
