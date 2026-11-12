#!/usr/bin/env python3
"""PreToolUse hook for Bash. Rule 1: no pushes, no forced deletes. Rule 3: every block is logged.

Exit code 2 blocks the command and sends the stderr text back to Claude.
Reads only tool_name and tool_input from stdin.
"""
import datetime
import json
import os
import re
import sys

log = os.environ.get("CLAUDE_TOOL_LOG") or os.path.join(os.path.expanduser("~"), "claude-tool-calls.log")

PUSH = re.compile(r"\bgit\s+push\b")
# rm with both -r and -f in any order or any split form: -rf, -fr, -r -f, -Rf, --recursive --force
RM = re.compile(r"\brm\b(?=[^;&|]*?(?:\s-[a-zA-Z]*[rR]|\s--recursive))(?=[^;&|]*?(?:\s-[a-zA-Z]*f|\s--force))")


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    command = (data.get("tool_input") or {}).get("command", "")
    rule = "no-push" if PUSH.search(command) else ("no-force-delete" if RM.search(command) else None)
    if rule is None:
        return 0
    entry = {"ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "event": "blocked", "rule": rule, "tool": data.get("tool_name"), "input": data.get("tool_input")}
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    print("Blocked by team rule 1 (%s). Commit locally and ask a person to push, and delete files one at a time." % rule, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
