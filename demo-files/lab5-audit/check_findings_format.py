#!/usr/bin/env python3
"""Student-side format check for the Lab 5 findings file. It checks structure, never the answers.

Usage: python3 check_findings_format.py findings.md harbor-org/org/credentials_inventory.csv

Checks (each shown as ok or MISSING):
  - at least 4 finding blocks, each with all seven fields filled in
  - a "Not a finding" section with at least one item
  - a "Priority order" list with at least 4 items, each with a reason
  - a rotation and ownership table with a row for EVERY credential id in the inventory file
Whether your findings are right is scored by your facilitator against an answer key.
Standard library only.
"""
import csv
import re
import sys

FIELDS = ["File and line", "What is wrong", "Risk", "Severity", "Fix", "Rotation step", "Owner"]


def section(text, title):
    m = re.search(r"^## %s\s*\n(.*?)(?=^## |\Z)" % re.escape(title), text, re.S | re.M)
    return m.group(1) if m else ""


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    text = open(sys.argv[1], encoding="utf-8").read()
    ids = [r["credential_id"] for r in csv.DictReader(open(sys.argv[2], encoding="utf-8"))]
    problems = 0

    blocks = re.split(r"^## Finding \d+\s*$", text, flags=re.M)[1:]
    blocks = [re.split(r"^## ", b, flags=re.M)[0] for b in blocks]
    full = 0
    for i, b in enumerate(blocks, 1):
        empty = []
        for f in FIELDS:
            m = re.search(r"\*\*%s:\*\*[ \t]*(.*)" % re.escape(f), b)
            if not m or not m.group(1).strip():
                empty.append(f)
        if empty:
            print("  finding %d: empty fields: %s" % (i, ", ".join(empty)))
        else:
            full += 1
    ok = full >= 4
    problems += not ok
    print("[%s] %d complete finding blocks (need at least 4)" % ("ok" if ok else "MISSING", full))

    nf = [ln for ln in section(text, "Not a finding").splitlines() if ln.strip().startswith("-") and len(ln.strip()) > 2]
    problems += not nf
    print("[%s] 'Not a finding' section has an item" % ("ok" if nf else "MISSING"))

    pr = [ln for ln in section(text, "Priority order").splitlines() if re.match(r"\s*\d+\.\s+\S", ln)]
    with_reason = [ln for ln in pr if re.search(r"because|since|reason|so that|as it|which|:", ln, re.I)]
    ok = len(pr) >= 4 and len(with_reason) == len(pr)
    problems += not ok
    print("[%s] priority list has %d items, %d with a reason (need 4+, all with a reason)" % ("ok" if ok else "MISSING", len(pr), len(with_reason)))

    table = section(text, "Rotation and ownership plan")
    missing = [c for c in ids if c not in table]
    problems += bool(missing)
    print("[%s] rotation table covers every credential in the inventory%s" % ("ok" if not missing else "MISSING", (" (missing: %s)" % ", ".join(missing)) if missing else ""))

    print("\n%s" % ("Format is complete." if not problems else "Fix the MISSING items, then hand the file to your facilitator."))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
