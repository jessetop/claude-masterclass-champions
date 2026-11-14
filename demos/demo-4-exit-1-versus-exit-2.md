# Demo 4: Exit 1 Versus Exit 2

**Course:** AI Champions Training: Claude Code for Engineering Teams

> Part of **[AI Champions Training: Demos](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites and cost notes before you start.

---

**Learning objective:** Show that a hook that exits 1 does not block and a hook that exits 2 does, and send the block reason back to Claude. Time: about 10 minutes.

**Files:** `$FILES/demo4-exit-codes`: `project/.claude/hooks/block_rm.py`, `project/.claude/settings.json`, `hooks-source/block_rm_broken.py`, `hooks-source/block_rm_fixed.py`, `fix_hook.sh`, `test_exit_codes.sh`.

**Context:** A hook script reads the tool call as JSON on standard input. Exit code 0 means success. Exit code 2 is a blocking error: on a PreToolUse hook the tool call is blocked and the text on standard error is the reason. Any other exit code is a non-blocking error: the action proceeds. The starter hook prints a good message and then exits 1.

**Steps:**

1. Show `project/.claude/hooks/block_rm.py`. Point at `sys.exit(1)` and at the matcher `Bash` in `settings.json`.
2. Run the hook by hand, no model needed: `bash test_exit_codes.sh`. The dangerous command prints the message and reports exit code 1.
3. Start `claude` in `project` and ask: `Delete the build folder with rm -rf build`. A notice appears, and the folder is deleted anyway. Check with `ls`.
4. Restore the file: `echo "stale build output" > build/old-output.txt` (create `build` first if needed with `mkdir -p build`).
5. Fix the hook: `bash ../fix_hook.sh fixed`. The script is read on each call, so no restart is needed. Run `bash ../test_exit_codes.sh` again. It now reports exit code 2.
6. Ask the same question again. The call is blocked, and Claude reports the reason from standard error.
7. Show the three-line rule on a slide: 0 allows, 2 blocks, anything else only warns.
8. Switch back for the next class: `bash ../fix_hook.sh broken`.

**Expected result:** With exit 1 the command runs and the folder is gone. With exit 2 the command does not run, the folder stays, and Claude explains the block.

**Instructor note:** Steps 2 and 5 need no model call and always work, so they are the fallback. Windows: run the scripts in Git Bash; the hook command uses `python3`, so if your laptop has only `python`, edit `project/.claude/settings.json` to say `python`. macOS: no differences. No administrator rights are needed. **Confirmed 2026-11-14 against the hooks reference:** "Exit with code 2 to block the action... a `PreToolUse` hook blocks the tool call... The message that comes with the block is your hook's stderr." Exit 1 without valid JSON is a non-blocking error. Two refinements if a student asks, neither needed for the demo: a hook that exits 1 but prints JSON that passes validation can still decide the outcome through that JSON, and a hook configured with `onFailure: "block"` blocks when it fails rather than passing through. The starter here exits 1 with plain stderr and no JSON, so it genuinely does not block. Unconfirmed: whether the notice for a non-blocking error shows the first line of standard error exactly as the docs describe on your version, so check once. Fallback if the live model call fails: run only steps 2, 5 and the second half of step 7, and show a recorded transcript outline: command, notice, folder deleted, fix, command, block message, folder kept.

**Why this matters:** The most common hook bug is an exit code of 1. The author sees the message, believes the rule works, and ships it. The rule never held. This is why every rule needs a test that proves it.
