"""Check that every $FILES/... path named in the labs and demos actually exists.

A lab that tells a student to open a file that was never shipped fails in the room,
and nothing else in the repo catches it.
"""
import os
import re
import sys

REPO = sys.argv[1]
FILES = os.path.join(REPO, "demo-files")

# $FILES/a/b/c.md  or  `$FILES/a/b`  - stop at whitespace, backtick, comma, or sentence end
REF = re.compile(r"\$FILES/([A-Za-z0-9._/\-]+)")

missing = {}
checked = 0
for sub in ("labs", "demos"):
    d = os.path.join(REPO, sub)
    for name in sorted(os.listdir(d)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(d, name)
        text = open(path, encoding="utf-8").read()
        for m in REF.finditer(text):
            ref = m.group(1).rstrip(".,;:)`")
            checked += 1
            target = os.path.join(FILES, *ref.split("/"))
            if not os.path.exists(target):
                missing.setdefault("%s/%s" % (sub, name), set()).add(ref)

print("checked %d $FILES references" % checked)
if not missing:
    print("all resolve")
else:
    print("MISSING:")
    for f in sorted(missing):
        for ref in sorted(missing[f]):
            print("  %-46s $FILES/%s" % (f, ref))
