# Demo 6: Prove It: A Logging Hook

**Course:** AI Champions Training: Claude Code for Engineering Teams

> Part of **[AI Champions Training: Demos](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites and cost notes before you start.

---

**Learning objective:** Show how a rule is decided, enforced and proved, using a hook that blocks a push and a log that records it. Time: about 12 minutes.

**Files:** `$FILES/demo6-logging`: `project/.claude/settings.json`, `project/.claude/hooks/log-tool.sh`, `block-push.py`, `log-tool.py`, `settings.windows-or-no-jq.json`, `summarize_log.sh`, `summarize_log.py`, `sample-log.jsonl`.

**Context:** The rule is "Claude Code never pushes". Decide: it is written in the team charter. Enforce: a PreToolUse hook exits 2 on `git push`. Prove: a log records every attempt. A PostToolUse hook logs each tool call using only `tool_name` and `tool_input`. The blocked push never ran, so the blocking hook writes its own log line.

**Steps:**

1. Prepare the project: `cd $FILES/demo6-logging/project && git init -q && git commit -q --allow-empty -m init`. Check `jq --version`. If `jq` is missing, copy `../settings.windows-or-no-jq.json` over `.claude/settings.json`.
2. `chmod +x .claude/hooks/*` and show the three pieces: the rule on a slide, `block-push.py`, and `log-tool.sh`.
3. Start `claude` in `project` and ask: `List the files here, then run git push origin main.`
4. Claude lists the files and the push is blocked. Claude reports the reason from standard error.
5. Exit and read the log: `bash ../summarize_log.sh` (or `python3 ../summarize_log.py`). It shows calls by tool and a `blocked` line with the rule name and the command.
6. Put the three words on the board next to the three artifacts: decide (the charter row), enforce (the hook), prove (the log line).
7. Ask: what could this log not prove? (For example, a rule nobody wrote a hook for, or a command run outside Claude Code.)

**Expected result:** The log has a `tool_call` line for the listing and a `blocked` line with `rule: no-push`. The summary reports one blocked push.

**Instructor note:** The hook reads only `tool_name` and `tool_input`. The fields that are specific to PostToolUse, such as a tool result, are not stated in the docs read, so do not claim any, and do not read a result field. The logging pattern with `jq` and `args: []` comes from the docs. Unconfirmed: that hooks inherit your shell's environment, so leave `CLAUDE_TOOL_LOG` unset and use the default `~/claude-tool-calls.log`. Windows: no `jq` by default, so use the Python version of the logger (`settings.windows-or-no-jq.json`) and `summarize_log.py`; use `python` if there is no `python3`. macOS: `brew install jq`, otherwise the same. No administrator rights are needed. Fallback (no model): `python3 summarize_log.py sample-log.jsonl` shows the shape of a proof without a live call.

**Why this matters:** A rule nobody can prove held is an opinion. The log turns "we never push" into evidence an auditor can read, and it shows the exact moment a rule saved a push.
