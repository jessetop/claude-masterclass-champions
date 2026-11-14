#!/usr/bin/env python3
"""Do the lab scorers still discriminate? One command, no model calls, changes nothing.

    python3 testing/smoke.py            run every lab
    python3 testing/smoke.py 3 5        run only labs 3 and 5
    python3 testing/smoke.py -v         show each scorer's full output

For each scored lab this runs the scorer twice: once against the untouched starter and
once against the shipped answer key. It asserts the two invariants that matter:

    the untouched starter scores LOW      - the lab still has something to teach
    the shipped answer key scores FULL    - the lab is still completable

Those are deliberately expressed as bands rather than exact totals, so a fix that moves
a rubric by a point does not fail the run. A scorer that stops discriminating does.

Run this before testing anything else. If it fails, a scorer is broken, and every lab
result measured after it is measuring the wrong thing.

Everything is scored in a copy under a temporary directory. The repository is never
written to. Standard library only.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
FILES = os.path.join(REPO, "demo-files")
PY = sys.executable

VERBOSE = "-v" in sys.argv or "--verbose" in sys.argv
ONLY = {a for a in sys.argv[1:] if a.isdigit()}

SCORE_RE = re.compile(r"(?:TOTAL|SCORE|PART A SCORE)\D{0,12}?(\d+)\s*/\s*(\d+)", re.I)


def run(cmd, cwd=None):
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=300)
    return (p.stdout or "") + (p.stderr or ""), p.returncode


def score_of(text):
    """Last score-looking line wins: scorers print per-row numbers before the total."""
    hits = SCORE_RE.findall(text)
    if not hits:
        return None, None
    got, mx = hits[-1]
    return int(got), int(mx)


def stage(dst, *pairs):
    """Copy (src, name) pairs into a fresh temp dir and return it."""
    os.makedirs(dst, exist_ok=True)
    for src, name in pairs:
        s = os.path.join(FILES, src)
        d = os.path.join(dst, name)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy(s, d)
    return dst


# Each lab: a function returning (starter_text, key_text_or_None) and the bands.
# starter_max: the starter must score AT OR BELOW this fraction of the maximum.
# key_min:     the answer key must score AT OR ABOVE this fraction of the maximum.
# key_note:    a documented reason the key does not reach full marks.


def lab1(tmp):
    s = stage(os.path.join(tmp, "s"), ("lab1-rule-to-control/ledgerlite", "ledgerlite"),
              ("lab1-rule-to-control/charter.md", "charter.md"))
    k = stage(os.path.join(tmp, "k"), ("facilitator/lab1/solution/ledgerlite", "ledgerlite"),
              ("facilitator/lab1/solution/charter.md", "charter.md"))
    chk = os.path.join(FILES, "lab1-rule-to-control", "check_lab1.py")
    a, _ = run([PY, chk, os.path.join(s, "ledgerlite"), os.path.join(s, "charter.md")])
    b, _ = run([PY, chk, os.path.join(k, "ledgerlite"), os.path.join(k, "charter.md")])
    return a, b


def lab2(tmp):
    chk = os.path.join(FILES, "lab2-plugin", "score_lab2.py")
    a, _ = run([PY, chk, os.path.join(FILES, "lab2-plugin", "relnotes-starter"),
                "--marketplace", os.path.join(FILES, "lab2-plugin", "marketplace-template")])
    sol = os.path.join(FILES, "facilitator", "lab2", "solution-marketplace")
    b, _ = run([PY, chk, os.path.join(sol, "plugins", "relnotes"), "--marketplace", sol])
    return a, b


def lab3(tmp):
    chk = os.path.join(FILES, "lab3-harden", "check_settings.py")
    a, _ = run([PY, chk, os.path.join(FILES, "lab3-harden", "report-archiver")])
    key = os.path.join(FILES, "facilitator", "lab3", "solution", "report-archiver")
    b, _ = run([PY, chk, key]) if os.path.isdir(key) else (None, 0)
    return a, b


def lab4(tmp):
    chk = os.path.join(FILES, "lab4-injection", "check_record.py")
    a, _ = run([PY, chk, os.path.join(FILES, "lab4-injection", "record_sheet.csv")])
    return a, None  # no completed sheet ships; see key_note


def lab5(tmp):
    chk = os.path.join(FILES, "lab5-audit", "check_findings_format.py")
    inv = os.path.join(FILES, "lab5-audit", "harbor-org", "org", "credentials_inventory.csv")
    scorer = os.path.join(FILES, "facilitator", "lab5", "score_audit.py")
    tpl = os.path.join(FILES, "lab5-audit", "findings-template.md")
    sol = os.path.join(FILES, "facilitator", "lab5", "solution-findings.md")
    use = scorer if os.path.exists(scorer) else chk
    a, _ = run([PY, use, tpl, inv])
    b, _ = run([PY, use, sol, inv]) if os.path.exists(sol) else (None, 0)
    return a, b


def lab6(tmp):
    src = os.path.join(FILES, "lab6-context")
    s = os.path.join(tmp, "l6s")
    shutil.copytree(src, s)
    a, _ = run([PY, "check_lab6.py"], cwd=s)
    sol = os.path.join(FILES, "facilitator", "lab6", "solution")
    b = None
    if os.path.isdir(sol):
        k = os.path.join(tmp, "l6k")
        shutil.copytree(src, k)
        # The answer key is stored flat, but each piece belongs somewhere specific:
        # CLAUDE.md is the project's, agents/ and commands/ are the plugin's.
        placement = {
            "CLAUDE.md": "shopkit/CLAUDE.md",
            "agents": "shopkit-plugin/agents",
            "commands": "shopkit-plugin/commands",
            "measure.csv": "measure.csv",
            "RULES-LEARNED.md": "RULES-LEARNED.md",
        }
        for item in os.listdir(sol):
            sp = os.path.join(sol, item)
            dp = os.path.join(k, *placement.get(item, item).split("/"))
            if os.path.isdir(sp):
                # Merge rather than replace: rmtree can fail silently on Windows and
                # leave the directory behind, which then breaks copytree.
                shutil.copytree(sp, dp, dirs_exist_ok=True)
            else:
                os.makedirs(os.path.dirname(dp), exist_ok=True)
                shutil.copy(sp, dp)
        b, _ = run([PY, "check_lab6.py"], cwd=k)
    return a, b


LABS = [
    ("1", "Rule to Control", lab1, 0.45, 1.00, None),
    ("2", "Build a Plugin With a Hook", lab2, 0.35, 0.75,
     "the key ships without an EVIDENCE.md, and the evidence rows are worth 20"),
    ("3", "Harden a Sample Repository", lab3, 0.10, 1.00,
     "Part A only; Part B needs a live sandbox and is not scored here"),
    ("4", "Prompt Injection Detection", lab4, 0.35, None,
     "no completed record sheet ships as an answer key"),
    ("5", "Credential Audit", lab5, 0.35, 0.90, None),
    ("6", "Context Engineering", lab6, 0.60, 0.90, None),
]


def main():
    tmp = tempfile.mkdtemp(prefix="champion-smoke-")
    rows, problems = [], []
    try:
        for num, title, fn, starter_max, key_min, note in LABS:
            if ONLY and num not in ONLY:
                continue
            try:
                a, b = fn(tmp)
            except Exception as exc:  # noqa: BLE001 - a crashing scorer is the finding
                rows.append((num, title, "ERROR", "", "the scorer raised: %s" % exc))
                problems.append("lab %s: scorer raised %s" % (num, exc))
                continue
            if VERBOSE:
                print("\n===== lab %s starter =====\n%s" % (num, a))
                if b:
                    print("\n===== lab %s answer key =====\n%s" % (num, b))
            sg, sm = score_of(a or "")
            kg, km = score_of(b or "") if b else (None, None)
            verdict, detail = "ok", ""
            if sg is None:
                verdict, detail = "ERROR", "no score found in the starter run"
            else:
                if sg > starter_max * sm:
                    verdict = "FAIL"
                    detail = "starter scored %d/%d, above the %d%% ceiling" % (sg, sm, starter_max * 100)
                if key_min is not None:
                    if kg is None:
                        if verdict == "ok":
                            verdict, detail = "WARN", "no answer key scored (%s)" % (note or "none ships")
                    elif kg < key_min * km:
                        verdict = "FAIL"
                        detail = "answer key scored %d/%d, below the %d%% floor" % (kg, km, key_min * 100)
                elif verdict == "ok":
                    verdict, detail = "WARN", note or "no answer key"
            if verdict in ("FAIL", "ERROR"):
                problems.append("lab %s: %s" % (num, detail))
            rows.append((num, title,
                         "%d/%d" % (sg, sm) if sg is not None else "-",
                         "%d/%d" % (kg, km) if kg is not None else "-",
                         verdict if not detail else "%s - %s" % (verdict, detail)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\nClaude Champion - scorer smoke test")
    print("%-3s %-32s %-9s %-9s %s" % ("#", "Lab", "starter", "key", "result"))
    print("-" * 100)
    for r in rows:
        print("%-3s %-32s %-9s %-9s %s" % r)
    print()
    if problems:
        print("NOT OK - %d problem(s):" % len(problems))
        for p in problems:
            print("  - %s" % p)
        print("\nA scorer that no longer separates an untouched starter from the answer key")
        print("cannot measure a student. Fix that before testing any lab.")
        return 1
    print("OK - every scorer still separates the untouched starter from the answer key.")
    print("This checks discrimination, not correctness. It cannot tell you whether a")
    print("correct answer written a different way still scores - probe that per lab.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
