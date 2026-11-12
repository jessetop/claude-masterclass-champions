#!/usr/bin/env python3
"""FACILITATOR ONLY. Keyword scorer and answer key for the Lab 5 findings file.

Usage: python3 score_audit.py findings.md harbor-org/org/credentials_inventory.csv

Scores 100: six planted issues at 12 each (identified 6, location 3, fix 3) = 72,
the clean repository not reported 8, a reasoned priority order 8, rotation plan covers every credential 12.
Keyword matching is a first pass. Read the findings and adjust: a good answer can use different words.
Standard library only.
"""
import csv
import re
import sys

# id: (label, identify regexes (any block must match ALL), location regexes (ANY), fix regexes (ANY))
ISSUES = {
    "C1": ("Key in a settings file (billing-service .claude/settings.json env.ANTHROPIC_API_KEY)",
           [r"billing"], [r"settings\.json", r"env"], [r"remove|rotate|secret store|run time|runtime|own login"], [r"settings\.json"]),
    "C2": ("apiKeyHelper that echoes a static key (inventory-service get_key.sh)",
           [r"get_key|apikeyhelper|helper"], [r"echo|static|hard-?coded|fixed"], [r"short-lived|broker|secret store|fetch|rotate"], [r"get_key\.sh|settings\.json"]),
    "C3": ("Shared CI secret across repositories (SHARED_CLAUDE_CI_KEY)",
           [r"shared"], [r"SHARED_CLAUDE_CI_KEY|ci_secrets|two repositories|both repositories|billing.*inventory|inventory.*billing"],
           [r"per-repo|per repo|one .*per repo|repository-scoped|repository scoped|own secret|separate"], [r"ci_secrets_inventory|claude-review\.yml"]),
    "C4": ("Long-lived key owned by a departed person (cred-101, p.nakamura)",
           [r"cred-101|nakamura"], [r"left|depart|former|offboard|hr_departures|2026-06-30"], [r"revoke|replace|team-owned|team owned|expiry|expire|offboarding"], [r"credentials_inventory|hr_departures"]),
    "C5": ("No deny rules for .env (inventory-service)",
           [r"inventory"], [r"\.env"], [r"deny"], [r"inventory-service.*settings|settings\.json|\.env"]),
    "C6": ("Personal key of a departed person in .env (cred-104, j.alvarez)",
           [r"cred-104|alvarez"], [r"left|depart|former|personal|2026-03-15"], [r"revoke|rotate|replace|remove"], [r"\.env|credentials_inventory"]),
}


def blocks_of(text):
    parts = re.split(r"^## Finding \d+\s*$", text, flags=re.M)[1:]
    return [re.split(r"^## ", b, flags=re.M)[0] for b in parts]


def section(text, title):
    m = re.search(r"^## %s\s*\n(.*?)(?=^## |\Z)" % re.escape(title), text, re.S | re.M)
    return m.group(1) if m else ""


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    text = open(sys.argv[1], encoding="utf-8").read()
    ids = [r["credential_id"] for r in csv.DictReader(open(sys.argv[2], encoding="utf-8"))]
    blocks = blocks_of(text)
    total = 0
    for key, (label, ident, why, fix, loc) in ISSUES.items():
        hit = None
        for b in blocks:
            if all(re.search(p, b, re.I) for p in ident) and any(re.search(p, b, re.I) for p in why):
                hit = b
                break
        pts = 0
        if hit:
            pts += 6
            if any(re.search(p, hit, re.I) for p in loc):
                pts += 3
            if any(re.search(p, hit, re.I) for p in fix):
                pts += 3
        total += pts
        print("  %s %2d/12  %s" % (key, pts, label))

    pay = [b for b in blocks if re.search(r"payments-gateway", b, re.I) and re.search(r"CLAUDE_CI_KEY_PAYMENTS|cred-102|settings\.json", b)]
    reported_clean_as_bad = [b for b in pay if not re.search(r"BILLING|inventory", b)]
    clean = 0 if reported_clean_as_bad else 8
    total += clean
    print("  clean repository (payments-gateway) not reported as defective: %d/8" % clean)

    pr = [ln for ln in section(text, "Priority order").splitlines() if re.match(r"\s*\d+\.\s+\S", ln)]
    pts = 8 if len(pr) >= 4 and all(re.search(r"because|since|reason|so |which|:|;|,", ln, re.I) for ln in pr) else (4 if len(pr) >= 3 else 0)
    total += pts
    print("  prioritized with reasons (suggested top: cred-101 departed owner, then the shared CI key): %d/8" % pts)

    table = section(text, "Rotation and ownership plan")
    covered = sum(1 for c in ids if c in table)
    pts = round(12 * covered / max(1, len(ids)))
    total += pts
    print("  rotation and ownership plan covers %d of %d credentials: %d/12" % (covered, len(ids), pts))

    print("\nKEYWORD SCORE: %d / 100 (first pass; read the findings and adjust)" % total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
