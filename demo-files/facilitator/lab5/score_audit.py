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

# Each ISSUES entry has five elements:
#   label  - what the issue is, printed next to the score
#   ident  - identification: the block must match ALL of these
#   why    - identification, second half: the block must match ANY of these
#            (the evidence that the student saw *this* problem and not a neighbouring one)
#   fix    - acceptable fix: ANY of these, matched against the Fix and Rotation step
#            fields only, so a fix word borrowed from "What is wrong" earns nothing
#   loc    - location: ANY of these, matched against the whole block
ISSUES = {
    "C1": ("Key in a settings file (billing-service .claude/settings.json env.ANTHROPIC_API_KEY)",
           [r"billing"], [r"settings\.json|settings file|settings\.local\.json|\.claude/settings"],
           [r"remove|rotate|secret store|run time|runtime|own login|own sign-in|own seat"], [r"settings\.json"]),
    "C2": ("apiKeyHelper that echoes a static key (inventory-service get_key.sh)",
           [r"get_key|apikeyhelper|helper"],
           [r"echo|static|hard-?coded|fixed|constant|same key|never changes|does not change|does not rotate"],
           [r"short-lived|broker|secret store|fetch|rotate|replace"], [r"get_key\.sh|settings\.json"]),
    "C3": ("Shared CI secret across repositories (SHARED_CLAUDE_CI_KEY)",
           [r"shared|share|SHARED_CLAUDE_CI_KEY|organi[sz]ation-scoped|organi[sz]ation-wide|org-scoped|org-wide|org-level|re-?used|same secret|single secret|common secret|across repositor|used by both|used in both|used by two|used across"],
           [r"SHARED_CLAUDE_CI_KEY|ci_secrets|two repositor|both repositor|two repos\b|both repos\b|billing.*inventory|inventory.*billing"],
           [r"per-repo|per repo|one .*per repo|repository-scoped|repository scoped|own secret|separate"], [r"ci_secrets_inventory|claude-review\.yml"]),
    "C4": ("Long-lived key owned by a departed person (cred-101, p.nakamura)",
           [r"cred-101|nakamura"],
           [r"left|leave|depart|former|ex-?employ|no longer|resign|terminat|offboard|last day|2026-06-30|30 june|june 2026|180"],
           [r"revoke|replace|re-?issue|team-owned|team owned|team identity|expiry|expire|offboarding"],
           [r"credentials_inventory|hr_departures"]),
    "C5": ("No deny rules for .env (inventory-service)",
           [r"inventory"],
           [r"permissions\.deny", r"deny rule", r"denyRead", r"deny entr", r"deny list",
            r"\b(no|not|without|missing|lack\w*|absent|never|nothing)\b[^\n]{0,60}deny",
            r"deny[^\n]{0,40}\b(missing|absent|not set|not configured)\b"],
           [r"deny"], [r"inventory-service.*settings|settings\.json|\.env"]),
    "C6": ("Personal key of a departed person in .env (cred-104, j.alvarez)",
           [r"cred-104|alvarez"],
           [r"left|leave|depart|former|ex-?employ|no longer|resign|terminat|personal|individual|2026-03-15|15 march|march 2026"],
           [r"revoke|rotate|replace|remove"], [r"\.env|credentials_inventory"]),
}

# A block is "about" the clean repository when its File and line field points there.
PAYMENTS = r"payments-gateway|payments_gateway|cred-102|CLAUDE_CI_KEY_PAYMENTS"


def norm(text):
    """Accept both **Field:** and **Field**: spellings of the template's bold labels."""
    return re.sub(r"\*\*([^*\n]+?)\*\*[ \t]*:", r"**\1:**", text)


def field(block, name):
    """The text of one template field, or "" when the block does not use that label."""
    m = re.search(r"\*\*%s:\*\*[ \t]*(.*)" % re.escape(name), norm(block))
    return m.group(1).strip() if m else ""


def fix_text(block):
    """What the student actually proposes: the Fix and Rotation step fields.

    Falls back to the whole block for an answer that does not use the template labels,
    so free-form prose is not scored at zero for formatting.
    """
    proposed = " ".join(p for p in (field(block, "Fix"), field(block, "Rotation step")) if p)
    return proposed or block


def blocks_of(text):
    parts = re.split(r"^#{2,3}[ \t]*Finding[ \t]*\d+\b.*$", text, flags=re.M)[1:]
    return [re.split(r"^#{2,3}[ \t]", b, flags=re.M)[0] for b in parts]


def section(text, title):
    m = re.search(r"^## %s\s*\n(.*?)(?=^## |\Z)" % re.escape(title), text, re.S | re.M)
    return m.group(1) if m else ""


def priority_items(text):
    return [ln for ln in section(text, "Priority order").splitlines() if re.match(r"\s*\d+[.)]\s+\S", ln)]


def has_reason(line):
    """True when a priority line says *why* it sits where it does.

    Shared with lab5-audit/check_findings_format.py: keep the two in step.
    Accepts a connective ("because", "since", ...), a punctuation break after the
    finding name (", " / " - " / ": "), or a substantial clause of plain prose.
    """
    body = re.split(r"^\s*\d+[.)]\s+", line, maxsplit=1)[-1].strip()
    if re.search(r"because|since|reason|so that|\bso\b|as it|as the|which|due to|given|in order", body, re.I):
        return True
    if re.search(r"[:;,\u2014]|\s[-\u2013]\s", body):
        return True
    return len(body) >= 40


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
            if any(re.search(p, fix_text(hit), re.I) for p in fix):
                pts += 3
        total += pts
        print("  %s %2d/12  %s" % (key, pts, label))

    reported_clean_as_bad = [b for b in blocks if re.search(PAYMENTS, field(b, "File and line") or b, re.I)]
    clean = 0 if reported_clean_as_bad else 8
    total += clean
    print("  clean repository (payments-gateway) not reported as defective: %d/8" % clean)

    pr = priority_items(text)
    pts = 8 if len(pr) >= 4 and all(has_reason(ln) for ln in pr) else (4 if len(pr) >= 3 else 0)
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
