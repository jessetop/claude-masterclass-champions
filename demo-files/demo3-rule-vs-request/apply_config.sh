#!/usr/bin/env bash
# Copies one of the demo configs into project/.claude/settings.json.
# Usage: bash apply_config.sh A|B|C|D      (then restart Claude Code in project/)
set -e
here="$(cd "$(dirname "$0")" && pwd)"
case "$1" in
  A) src=A-request-only.json ;;
  B) src=B-read-deny.json ;;
  C) src=C-deny-plus-sandbox.json ;;
  D) src=D-bypass-mode-test.json ;;
  *) echo "Usage: bash apply_config.sh A|B|C|D"; exit 2 ;;
esac
mkdir -p "$here/project/.claude"
sed "s#__PROJECT__#$here/project#g" "$here/configs/$src" > "$here/project/.claude/settings.json"
echo "Applied $src to $here/project/.claude/settings.json"
echo "Restart Claude Code in $here/project and run /status to confirm."
