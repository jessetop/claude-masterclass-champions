#!/usr/bin/env bash
# Build the student pack: a copy of demo-files with the answer keys removed.
#
#   ./make-student-pack.sh /path/to/output      write the pack there
#   ./make-student-pack.sh --list               show what would be removed, change nothing
#
# In this course every scoring script is a STUDENT tool -- each lab's steps tell the
# student to run it, and none of them names a planted trap. The only instructor-only
# material is facilitator/, which holds the worked solutions and the answer keys.
#
# If you add a new answer key, add it to WITHHOLD. Anything not on this list ships, so
# the failsafe at the end exists to catch exactly that mistake.
set -eu

WITHHOLD="
facilitator
"

SRC="$(cd "$(dirname "$0")" && pwd)"

if [ "${1:-}" = "--list" ]; then
  echo "Withheld from the student pack:"
  for p in $WITHHOLD; do
    if [ -e "$SRC/$p" ]; then echo "  [present] $p"; else echo "  [MISSING] $p  <- check the list"; fi
  done
  echo
  echo "Shipped to students (each lab tells them to run it):"
  echo "  setup/check_env.sh                 environment check, before Lab 1"
  echo "  lab1-rule-to-control/check_lab1.py"
  echo "  lab2-plugin/score_lab2.py          and tools/plugin_lint.py"
  echo "  lab3-harden/check_settings.py"
  echo "  lab4-injection/check_record.py"
  echo "  lab5-audit/check_findings_format.py"
  echo "  lab6-context/check_lab6.py"
  exit 0
fi

DEST="${1:-}"
[ -z "$DEST" ] && { sed -n '2,6p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
[ -e "$DEST" ] && { echo "Refusing to overwrite an existing path: $DEST"; exit 1; }

mkdir -p "$DEST"
cp -R "$SRC/." "$DEST/"
rm -f "$DEST/make-student-pack.sh"

for p in $WITHHOLD; do
  if [ -e "$DEST/$p" ]; then
    rm -rf "$DEST/$p"
    echo "  removed  $p"
  else
    echo "  WARNING  $p was not in the copy - the withheld list may be stale"
  fi
done

# Belt and braces: no facilitator folder, and nothing calling itself a solution or key,
# should survive. A new answer key added without updating WITHHOLD fails here.
# Note: eval graders legitimately have names like answers-the-question.md, so match
# only the names this repo actually uses for answer keys.
LEFT="$(find "$DEST" \( -name 'facilitator' -o -name 'solution' -o -name 'solution-*' -o -name 'key.md' \) -print 2>/dev/null || true)"
if [ -n "$LEFT" ]; then
  echo
  echo "REFUSING TO FINISH - instructor material is still present:"
  echo "$LEFT" | sed 's/^/    /'
  echo "  Add it to WITHHOLD in this script, delete $DEST, and run it again."
  exit 1
fi

echo
echo "Student pack written to $DEST"
echo
echo "Still to do by hand: remove the Facilitator note from the end of each lab file,"
echo "and the Instructor note from each demo, before you share those documents."
