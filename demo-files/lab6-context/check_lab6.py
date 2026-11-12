#!/usr/bin/env python3
"""Local checker for Lab 6 (Context Engineering, take-home). No model calls.

Usage:  python3 check_lab6.py            (run from the lab6-context folder)

Compares your trimmed files with the untouched copies in original/ and original-plugin/.
Scores 100:
  CLAUDE.md (40): at least 40 percent fewer words (15), the five facts that must survive are still there (15),
                  no stale instruction remains (10).
  Plugin (30): every command and agent description is 200 characters or fewer (12), still 40+ characters (6),
               each still names its trigger topic (12).
  Measurements (15): measure.csv has a value in all six rows.
  Rules (15): RULES-LEARNED.md has exactly two numbered rules, each with a because clause.
It checks the files only. It cannot read your /context output; the measurement rows are self-reported.
The 200 character limit is a lab rule of thumb, not a product limit.
Standard library only.
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).parent
score = 0
out = []


def award(points, ok, label, hint=""):
    global score
    score += points if ok else 0
    out.append("[%s] %2d/%-2d %s%s" % ("PASS" if ok else "FAIL", points if ok else 0, points, label, ("  -> " + hint) if (hint and not ok) else ""))


def words(path):
    return len(re.findall(r"\S+", Path(path).read_text(encoding="utf-8")))


def description(path):
    t = Path(path).read_text(encoding="utf-8")
    m = re.search(r"^description:\s*(.+)$", t, re.M)
    return m.group(1).strip() if m else ""


def main():
    before = words(HERE / "original" / "CLAUDE.md")
    after_text = (HERE / "shopkit" / "CLAUDE.md").read_text(encoding="utf-8")
    after = len(re.findall(r"\S+", after_text))
    cut = 100 * (before - after) / before
    award(15, cut >= 40, "CLAUDE.md is at least 40 percent shorter (%d to %d words, %.0f percent)" % (before, after, cut))

    must = {
        "tests command": r"python3 -m pytest -q",
        "never commit .env": r"\.env",
        "integer cents": r"integer cents",
        "public API path": r"src/shop/api\.py",
        "4-space indentation": r"4 spaces",
    }
    missing = [k for k, p in must.items() if not re.search(p, after_text)]
    award(15, not missing, "The facts that must survive are still in CLAUDE.md", "missing: %s" % ", ".join(missing))
    stale = [k for k in ("nosetests", "Jenkins", "FTP", "ftp_upload", "Python 2") if k.lower() in after_text.lower()]
    award(10, not stale, "No stale instruction remains", "still mentions: %s" % ", ".join(stale))

    files = sorted((HERE / "shopkit-plugin" / "commands").glob("*.md")) + sorted((HERE / "shopkit-plugin" / "agents").glob("*.md"))
    topics = {"price-check": "price", "stock-report": "stock", "refund-policy": "refund", "cart-reviewer": "cart"}
    descs = {f.stem: description(f) for f in files}
    award(12, bool(descs) and all(len(d) <= 200 for d in descs.values()), "Every description is 200 characters or fewer",
          ", ".join("%s=%d" % (k, len(v)) for k, v in descs.items() if len(v) > 200))
    award(6, bool(descs) and all(len(d) >= 40 for d in descs.values()), "No description is shortened to nothing (40+ characters)")
    award(12, all(topics[k] in descs.get(k, "").lower() for k in topics), "Every description still names its trigger topic",
          "check that each still says price, stock, refund or cart")

    try:
        rows = list(csv.DictReader(open(HERE / "measure.csv", encoding="utf-8")))
    except OSError:
        rows = []
    award(15, len(rows) == 6 and all((r.get("value") or "").strip() for r in rows), "measure.csv has a value in all six rows")

    try:
        rtext = (HERE / "RULES-LEARNED.md").read_text(encoding="utf-8")
    except OSError:
        rtext = ""
    rules = [l for l in rtext.splitlines() if re.match(r"\s*\d+\.\s+\S", l)]
    ok = len(rules) == 2 and all(re.search(r"because", r, re.I) for r in rules)
    award(15, ok, "RULES-LEARNED.md has exactly two numbered rules, each with a because clause", "found %d rule(s)" % len(rules))

    print("LAB 6 SCORE (local checks)")
    print("\n".join(out))
    print("\nTOTAL: %d / 100" % score)


if __name__ == "__main__":
    main()
