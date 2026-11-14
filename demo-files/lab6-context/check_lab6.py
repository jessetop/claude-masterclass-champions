#!/usr/bin/env python3
"""Local checker for Lab 6 (Context Engineering, take-home). No model calls.

Usage:  python3 check_lab6.py            (run from the lab6-context folder)

Measures your trimmed shopkit/CLAUDE.md against the untouched copy in original/.
original-plugin/ keeps the untouched plugin descriptions, so the FAIL lines below can show
you what each description used to cost; restore from it if you cut one too far.
Scores 100:
  CLAUDE.md (40): at least 40 percent fewer words (15), the five facts that must survive are still
                  there (15, three points per fact), no stale instruction remains (10).
  Plugin (30): every command and agent description is 200 characters or fewer (12), still 40+ characters (6),
               each still names its trigger topic (12).
  Measurements (15): measure.csv has a value in all six rows.
  Rules (15): RULES-LEARNED.md has exactly two numbered rules, each with a because clause.
It checks the files only. It cannot read your /context output; the measurement rows are self-reported.
The 200 character limit is a lab rule of thumb, not a product limit.
Wording is not graded: every check accepts any phrasing that keeps the fact.
Standard library only.
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).parent
BASELINE_WORDS = 652  # the shipped original/CLAUDE.md, for a "did you trim the baseline too?" warning
score = 0
out = []
notes = []


def award(points, ok, label, hint="", earned=None):
    """Add points. Pass earned= for a partial-credit check; ok is then ignored."""
    global score
    if earned is None:
        earned = points if ok else 0
    earned = max(0, min(points, int(earned)))
    score += earned
    tag = "PASS" if earned == points else ("PART" if earned else "FAIL")
    show_hint = hint and earned < points
    out.append("[%s] %2d/%-2d %s%s" % (tag, earned, points, label, ("  -> " + hint) if show_hint else ""))


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8-sig")
    except OSError:
        return None


def words(text):
    return len(re.findall(r"\S+", text or ""))


def description(path):
    """Return the frontmatter description as Claude would load it.

    Handles a plain value, a value wrapped onto indented continuation lines, and a YAML
    block or folded scalar (description: > or description: |), with quotes stripped.
    """
    t = read(path)
    if t is None:
        return ""
    m = re.match(r"---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", t, re.S)
    lines = (m.group(1) if m else t).splitlines()
    start = next((i for i, l in enumerate(lines) if re.match(r"description:", l)), None)
    if start is None:
        return ""
    value = lines[start].split(":", 1)[1]
    for line in lines[start + 1:]:
        if not line.strip():
            break  # a blank line ends the value
        if not re.match(r"[ \t]", line):
            break  # an unindented line is the next frontmatter key
        value += " " + line.strip()
    value = re.sub(r"^[|>][-+0-9]*[ \t]*", "", value.strip())  # drop a block/folded indicator
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1].strip()
    return value


def sentences(text):
    """Rough sentence split, so a negation in one sentence cannot excuse its neighbours."""
    return [s for s in re.split(r"(?<=[.!?;:])\s+|\n+", text or "") if s.strip()]


def numbered_rules(text):
    """Return the top-level numbered rules, each joined with its continuation lines.

    Accepts "1." and "1)". Stops at a later heading or at a new prose paragraph, so a
    numbered evidence list further down the file is not counted as a third rule.
    """
    lines = (text or "").splitlines()
    start = next((i for i, l in enumerate(lines) if re.match(r"[ \t]*\d+[.)][ \t]+\S", l)), None)
    if start is None:
        return []
    body, prev_blank = [], False
    for line in lines[start:]:
        if re.match(r"[ \t]*#{1,6}\s", line):
            break  # a heading ends the rules list
        is_item = re.match(r"[ \t]*\d+[.)][ \t]+\S", line)
        indented = re.match(r"[ \t]+\S", line)
        if prev_blank and line.strip() and not is_item and not indented \
                and not re.match(r"(?i)because\b", line.strip()):
            break  # a fresh unindented paragraph ends the rules list
        body.append(line)
        prev_blank = not line.strip()
    blocks = re.split(r"(?m)^[ \t]*\d+[.)][ \t]+(?=\S)", "\n".join(body))[1:]
    return [b for b in (re.sub(r"\s+", " ", b).strip() for b in blocks) if b]


def main():
    original_text = read(HERE / "original" / "CLAUDE.md")
    after_text = read(HERE / "shopkit" / "CLAUDE.md")
    if after_text is None:
        after_text = ""
        notes.append("shopkit/CLAUDE.md is missing. Trim that file in place; do not delete it.")
    if original_text is None:
        original_text = ""
        notes.append("original/CLAUDE.md is missing. Restore it from the demo files: the checker measures "
                     "your trimmed CLAUDE.md against it.")
    before, after = words(original_text), words(after_text)
    if before and abs(before - BASELINE_WORDS) > BASELINE_WORDS * 0.1:
        notes.append("original/CLAUDE.md is %d words but the shipped copy is about %d. It is the baseline, "
                     "so restore it and trim shopkit/CLAUDE.md only." % (before, BASELINE_WORDS))
    cut = 100.0 * (before - after) / before if before else 0.0
    if not before:
        cut_hint = "cannot measure without original/CLAUDE.md"
    elif not after:
        cut_hint = "shopkit/CLAUDE.md is empty: trim it, do not empty it"
    else:
        cut_hint = "cut more of what Claude would not act on"
    award(15, before > 0 and after > 0 and cut >= 40,
          "CLAUDE.md is at least 40 percent shorter (%d to %d words, %.0f percent)" % (before, after, cut),
          cut_hint)

    must = {
        "the test command (pytest)": r"(?i)\bpytest\b",
        "never commit .env": r"(?i)\.env\b",
        "money is integer cents":
            r"(?i)\bcents?\b[^.\n]{0,40}\bint(?:eger)?s?\b|\bint(?:eger)?s?\b[^.\n]{0,40}\bcents?\b",
        "the public API path (api.py)": r"(?i)\bapi\.py\b",
        "4-space indentation": r"(?i)\b(?:4|four)[ -]spaces?\b",
    }
    missing = [k for k, p in must.items() if not re.search(p, after_text)]
    award(15, not missing, "The facts that must survive are still in CLAUDE.md",
          "3 points each; add a line that names: %s" % ", ".join(missing),
          earned=3 * (len(must) - len(missing)))

    stale = {
        "nosetests": r"(?i)\bnosetests\b",
        "Jenkins": r"(?i)\bjenkins\b",
        "the FTP uploader": r"(?i)\bftp\b|ftp_upload",
        "Python 2": r"(?i)\bpython ?2(\.7)?\b",
    }
    # A sentence that cancels the old tool ("use pytest, not nosetests"; "Python 2 support was
    # dropped") resolves the contradiction instead of repeating it, so it is not stale.
    cancelled = (r"(?i)\b(not|no|never|dropped|removed|deleted|gone|instead|rather than|avoid|stop|"
                 r"stopped|unsupported|obsolete|stale|ignore|former|formerly|used to|don't|"
                 r"doesn't|isn't|no longer)\b")
    still = []
    for key, pat in stale.items():
        for s in sentences(after_text):
            if re.search(pat, s) and not re.search(cancelled, s):
                still.append(key)
                break
    award(10, not still, "No stale instruction remains",
          "still prescribes: %s - delete the line, or say plainly that it no longer applies"
          % ", ".join(still))

    files = sorted((HERE / "shopkit-plugin" / "commands").glob("*.md")) + \
        sorted((HERE / "shopkit-plugin" / "agents").glob("*.md"))
    topics = {"price-check": "price", "stock-report": "stock", "refund-policy": "refund", "cart-reviewer": "cart"}
    descs = {f.stem: description(f) for f in files}
    originals = {f.stem: description(f) for f in
                 sorted((HERE / "original-plugin" / "commands").glob("*.md")) +
                 sorted((HERE / "original-plugin" / "agents").glob("*.md"))}

    def was(stem, now):
        n = len(originals.get(stem, ""))
        return " (was %d)" % n if n and n != now else ""

    too_long = ["%s=%d%s" % (k, len(v), was(k, len(v))) for k, v in sorted(descs.items()) if len(v) > 200]
    absent = ["%s has no description" % k for k, v in sorted(descs.items()) if not v]
    award(12, bool(descs) and not too_long and not absent, "Every description is 200 characters or fewer",
          "; ".join(too_long + absent) or "no command or agent files found under shopkit-plugin/")
    short = ["%s=%d" % (k, len(v)) for k, v in sorted(descs.items()) if len(v) < 40]
    award(6, bool(descs) and not short, "No description is shortened to nothing (40+ characters)",
          ("too short: %s - say the job and the trigger in one sentence" % ", ".join(short)) if short
          else "no command or agent files found under shopkit-plugin/")
    off_topic = [k for k in topics if topics[k] not in descs.get(k, "").lower()]
    award(12, not off_topic, "Every description still names its trigger topic",
          "put the trigger word back into: %s"
          % ", ".join("%s (%s)" % (k, topics[k]) for k in sorted(off_topic)))

    try:
        with open(HERE / "measure.csv", newline="", encoding="utf-8-sig") as fh:
            rows = list(csv.DictReader(fh))
    except OSError:
        rows = []
        notes.append("measure.csv is missing. Restore it from the demo files and fill the value column.")
    except (UnicodeDecodeError, csv.Error):
        rows = []
        notes.append("measure.csv could not be read. Save it as comma separated CSV in UTF-8.")

    def cells(row):
        for v in row.values():  # a long unquoted note can land in a list under the rest key
            for one in (v if isinstance(v, list) else [v]):
                yield one or ""

    rows = [r for r in rows if any(c.strip() for c in cells(r))]  # ignore blank records
    filled = [r for r in rows if (r.get("value") or "").strip()]
    award(15, len(filled) >= 6, "measure.csv has a value in all six rows",
          "%d of the 6 measurements have something in the value column" % len(filled))

    rules = numbered_rules(read(HERE / "RULES-LEARNED.md"))
    no_because = [i + 1 for i, r in enumerate(rules) if not re.search(r"(?i)\bbecause\b", r)]
    if len(rules) != 2:
        hint = "found %d numbered rule(s) in the rules list; write exactly two" % len(rules)
    else:
        many = len(no_because) > 1
        hint = "rule%s %s %s no \"because\" clause: end the rule with the reason you measured" % (
            "s" if many else "", " and ".join(str(i) for i in no_because), "have" if many else "has")
    award(15, len(rules) == 2 and not no_because,
          "RULES-LEARNED.md has exactly two numbered rules, each with a because clause", hint)

    print("LAB 6 SCORE (local checks)")
    print("\n".join(out))
    for n in notes:
        print("NOTE: " + n)
    print("\nTOTAL: %d / 100" % score)


if __name__ == "__main__":
    main()
