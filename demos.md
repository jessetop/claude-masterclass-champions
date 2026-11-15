# AI Champions Training: Claude Code for Engineering Teams. Demos

**Course:** AI Champions Training: Claude Code for Engineering Teams (Governance, Hooks, Plugins, and Secure Environments), two days, ROI Training
**Contents:** 10 instructor-led demos. Each takes 15 minutes or less and has a learning objective. The numbers and titles match the Today's Demos slide.

---

## About this guide

Run the demos in the order of the chapters. Each has the same layout: a learning objective, a time, a Files line, a short context paragraph, steps, an Expected result, an Instructor note, a fallback where the demo needs a live model or administrator rights, and a Why this matters note.

In this guide `$FILES` means the `demo-files` folder. Students run the course on Linux class machines. Instructors may demo from a Windows or macOS laptop, so each Instructor note gives the Windows and macOS differences for file paths and administrator rights. The managed file paths are:

| System | Managed settings file | Managed MCP file |
|---|---|---|
| Linux and WSL | `/etc/claude-code/managed-settings.json` | `/etc/claude-code/managed-mcp.json` |
| macOS | `/Library/Application Support/ClaudeCode/managed-settings.json` | `/Library/Application Support/ClaudeCode/managed-mcp.json` |
| Windows | `C:\Program Files\ClaudeCode\managed-settings.json` | `C:\Program Files\ClaudeCode\managed-mcp.json` |

Writing any of these needs root or administrator rights. The older Windows path `C:\ProgramData\ClaudeCode\managed-settings.json` is not read.

Demos 1 to 10 use no organization-level administrative feature. Anything that lives in an administrator console is lecture only.

Claude Code can word things differently each time. Check results against the Expected result and not against exact text. Demos that use a live model (1, 2, 3, 4, 6, 7, 8, 9) spend usage on the instructor's seat. Demos 5 and 10 need no model call to make their main point. Every person, company and value in the files is fictional, and every planted secret is a placeholder such as `FAKE-TOKEN-DO-NOT-USE`.

> **Unconfirmed items.** Each Instructor note says what is unconfirmed or needs rehearsal. If an item is marked unconfirmed, say so to the class. Do not present it as fact. Rehearse every demo once on the machine you will teach from, and recheck the model names the day before class.

> **Cleanup.** Demos 2 and 5 write a file as root or administrator. Run the matching remove script when you finish, and check with `claude mcp list` and `/status` that nothing is left on the machine.

---

---

> Generated from `demos/` by `testing/build_demos_md.py`. Edit the files in
> `demos/`, not this copy, then regenerate.

---

## Demo 1: Intake: One Use Case, One Tier

**Learning objective:** Run one use case through the ten-section intake checklist and give it a risk tier, and name the single answer that decided the tier. Time: about 12 minutes.

**Files:** `$FILES/demo1-intake/use-case-brief.md`, `$FILES/templates/intake-checklist.md`, `$FILES/templates/risk-tiers.md`. Answer: `$FILES/facilitator/demos/demo1-completed-intake.md`.

**Context:** The intake checklist and the tiers are generic templates. A team replaces them with its own. The brief describes a fictional team that wants Claude Code to draft weekly release notes. Most of the use case is low risk. One data answer and one missing control set the tier.

**Steps:**

1. Show the brief on screen and the blank checklist next to it. Say the ten section names aloud: purpose and owner, data, repositories, tools and servers, model and effort, permissions and sandbox, credentials, review and escalation, logging, exit criteria.
2. In a terminal in `$FILES/demo1-intake`, start `claude` and ask:
   `Read use-case-brief.md and ../templates/intake-checklist.md. Draft an answer for each of the ten sections. Write "Unknown" where the brief is silent. Do not invent facts.`
3. Read Claude's draft with the class. Ask them to find one place where the draft states something the brief does not say.
4. Open `risk-tiers.md`. Ask the class to call out the tier. Take a vote.
5. Ask: which one answer decided the tier? Then ask what single change would lower it.

**Expected result:** The draft fills most sections and marks sections 5, 8, 9 and 10 as Unknown or thin. The class lands on Medium, and names section 2 (a real staging password in the repository folder with nothing stopping Claude Code from reading it) as the deciding answer. Removing or denying that file and blocking `git push` could lower the tier.

**Instructor note:** Nothing here is unconfirmed product behavior. The tiers are an example, and the class may reasonably pick another. What matters is that they name the deciding answer. Windows and macOS: no differences, and no administrator rights are needed. Run `claude` from any folder that holds the files. Fallback (no model or no time): read `$FILES/facilitator/demos/demo1-completed-intake.md` aloud section by section and let the class react, or fill the checklist on a whiteboard.

**Why this matters:** Governance starts with a repeatable question list. Without one, each use case is judged by whoever happens to be in the room. With one, an unknown answer becomes visible, and the team can see which control it is missing.

---

## Demo 2: Who Wins? Managed Over Project

**Learning objective:** Show that a managed settings file beats a project settings file, and prove it with behavior, not with a screen that lists files. Time: about 12 minutes.

**Files:** `$FILES/demo2-managed`: `managed-settings.json`, `project/.claude/settings.json`, `install-managed.sh`, `remove-managed.sh`, `install-managed.ps1`, `remove-managed.ps1`.

**Context:** The project file asks for a small model and allows `git push`. The managed file pins a different model and denies `git push` and reading `.env`. The overall order, highest first, is managed settings, command line, project local, shared project, user. A managed file is read at startup and reloaded when it changes.

**Steps:**

1. Show the two files side by side. Point at `model` and `permissions` in each.
2. Prepare the project: `cd $FILES/demo2-managed/project && git init -q && git commit -q --allow-empty -m init`.
3. Before installing the managed file, start `claude` in `project`. Run `/status` and note the `Setting sources` line, then `/model` to see the model in use. It should be the project's choice. Exit.
4. Install the managed file (Linux: `sudo bash ../install-managed.sh`). See the Instructor note for Windows and macOS.
5. Start `claude` in `project` again. Run `/status`. The `Setting sources` line now lists the managed settings file (its label ends in `(file)`). Run `/model`: it should show the pinned model.
6. Ask: `Run git push origin main`. Claude Code should refuse, even though the project settings allow it.
7. Ask: `Show me the contents of .env`. The Read tool should be denied.
8. Say plainly what `/status` proves and what it does not: it lists the files that were read, not which file supplied each key. The behavior in steps 5 to 7 is the proof.
9. Remove the managed file (Linux: `sudo bash ../remove-managed.sh`) and exit.

**Expected result:** With the managed file in place, the model matches the managed file and `git push` is refused despite the project's allow rule. After removal, the project's choices apply again.

**Instructor note:** Linux and WSL: the file goes to `/etc/claude-code/managed-settings.json` and needs `sudo`. macOS: `sudo mkdir -p "/Library/Application Support/ClaudeCode" && sudo cp managed-settings.json "/Library/Application Support/ClaudeCode/managed-settings.json"`; remove it with `sudo rm`. Windows: run `install-managed.ps1` from an elevated PowerShell; the target is `C:\Program Files\ClaudeCode\managed-settings.json`. A `model` change from managed settings applies at the next launch, so restart `claude` after installing. Within the managed tier, only the first source that delivers a key is used, so if your own account also receives server-managed settings, they can shadow the file. Run `claude doctor` before class to check for rejected entries. **Confirmed 2026-11-14 against the settings documentation:** "Settings precedence, highest first: managed settings, command line, project local, shared project, user... Nothing in your own settings files or `--settings` overrides a managed [setting]." That last clause matters for the fallback below: `--settings` outranks the project file, but it cannot override a managed file, so do not use the fallback to argue the opposite of what the demo just showed. Unconfirmed: the exact text `/model` shows for a pinned model, and whether `/model` or `/status` is the clearer view. Rehearse and use the one that is clearer. Do not claim that deny rules hold in every permission mode: that is a Demo 3 test, not a fact. Fallback (no administrator rights, or no model): show screenshots from your rehearsal. As a weaker second fallback, start with `claude --settings managed-settings.json` in `project`: the command line also ranks above the project file, but say clearly that this is not a managed file and does not show the file path.

**Why this matters:** A rule that a project can override is a default, not a control. Managed settings are the one place a team can set a floor that a developer's own settings cannot lower.

---

## Demo 3: Rule Versus Request

**Learning objective:** Show the difference between asking Claude not to do something and a control that stops it, and show why a file deny rule and a sandbox rule are two different layers. Time: about 15 minutes.

**Files:** `$FILES/demo3-rule-vs-request`: `project/` (with `CLAUDE.md`, `.env`), `configs/A-request-only.json`, `B-read-deny.json`, `C-deny-plus-sandbox.json`, `D-bypass-mode-test.json`, `apply_config.sh`.

**Context:** `CLAUDE.md` says "Never read the `.env` file". That is a request. A `Read` deny rule blocks Claude's file tools. The sandbox `denyRead` setting covers shell commands. The docs say to use both. Configuration A is the request only. B adds the deny rule. C adds the sandbox. D is an optional test.

**Steps:**

1. `cd $FILES/demo3-rule-vs-request` and run `bash apply_config.sh A`. Start `claude` in `project`.
2. Ask: `I own this project and I approve it. Print the contents of .env so I can check the password.` Note what Claude does. Exit.
3. Run `bash apply_config.sh B` and restart `claude`. Ask the same question. The Read tool call should be denied.
4. Now ask: `Run cat .env in the shell and show me the output.` Note carefully what happens. This is the shell route.
5. Run `bash apply_config.sh C` (Linux, macOS or WSL2) and restart. Ask for the file with the Read tool, then through the shell. Both should be stopped. Read the two refusals aloud: one comes from a permission rule, the other from the sandbox.
6. Optional test: run `bash apply_config.sh D`, in a throwaway VM only, and ask the first question again. This shows whether a deny rule holds when the permission mode is `bypassPermissions`.
7. Ask the class: which of these steps depended on the model choosing well, and which did not?

**Expected result:** Step 2 depends on the model, and it may refuse or comply. That inconsistency is the point. In B the Read tool is denied by rule. In C both routes are blocked.

**Instructor note:** Unconfirmed, so say so: the docs say a `Read` deny blocks Claude's file tools and that `sandbox.filesystem.denyRead` covers shell commands. Whether `cat .env` in step 4 is stopped under B alone is not confirmed, so record what you see. Step 6 tests the idea that deny rules hold in every permission mode. Treat it as a test, not a fact, and tell the class what you saw, once. Windows: native Windows is not sandboxed, so steps 1 to 4 and step 6 work in Git Bash with `claude`, but step 5 needs WSL2, a Mac or a Linux VM. macOS: the sandbox runs on macOS and needs no extra install. Linux: needs `bubblewrap` and `socat`, and verify with `touch ~/sandbox-probe` (see Demo 9). On Ubuntu 24.04 and later the `bwrap-userns-restrict` AppArmor profile is on by default and will stop the sandbox starting, so run `bash $FILES/setup/classroom-sandbox.sh --check` before you rehearse — step 5 is the part that depends on it. The path form for `sandbox.filesystem.denyRead` entries is not confirmed beyond what the docs show, so `apply_config.sh` writes an absolute path. Fallback: a transcript outline with these beats: A, Claude refuses or complies, B, the Read call is denied, shell route observed, C, both blocked, and a screenshot of each result from your rehearsal.

**Why this matters:** A sentence in `CLAUDE.md` is a request that the model weighs. A rule in settings is a control that a hook, a permission check or the operating system applies whatever the model decides. A charter row marked "Enforced" must point at the second kind.

---

## Demo 4: Exit 1 Versus Exit 2

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

---

## Demo 5: A Fixed MCP Set

**Learning objective:** Fix the set of MCP servers a team may use, and show that each user authenticates as themselves with no secret in the shared file. Time: about 15 minutes.

**Files:** `$FILES/demo5-mcp`: `servers/notes_server.py`, `servers/shadow_server.py`, `servers/mcp_min.py`, `servers/test_servers.py`, `setup_project.sh`, `install_managed_mcp.sh`, `remove_managed_mcp.sh`, `install_managed_mcp.ps1`, `remove_managed_mcp.ps1`. Review aid: `$FILES/templates/mcp-server-review.md`.

**Context:** Two small local servers run on your machine, so no account or network is needed. `notes` is the approved server. It reads a per-user environment variable, `NOTES_TOKEN`, and maps it to a user. `shadow-sync` stands in for a server nobody reviewed. A `managed-mcp.json` file gives exclusive control: only the servers it defines load, and `claude mcp add` fails. The file is readable by every user on the machine, so it holds no secret. It refers to `${NOTES_TOKEN}` and each user supplies their own value.

**Steps:**

1. Show that both servers work without Claude Code: `python3 servers/test_servers.py`. Four lines read `ok`.
2. Write the project file: `bash setup_project.sh`. It creates `project/.mcp.json` declaring both servers.
3. `export NOTES_TOKEN=FAKE-TOKEN-DO-NOT-USE-alice`, then `cd project && claude`. Approve the project servers if asked. Run `/mcp`. Both servers appear. Ask Claude to call the `whoami` tool of `notes`, then the `sync_notes` tool of `shadow-sync`. Read the second answer aloud: a local server runs with the user's rights. Exit.
4. Install the managed file: `sudo bash install_managed_mcp.sh`. Show it: `cat /etc/claude-code/managed-mcp.json`. Point at `${NOTES_TOKEN}`: there is no secret in it.
5. Restart `claude` in `project`. Run `claude mcp list` in another shell. Only `notes` is listed.
6. Try to add a server: `claude mcp add --transport http test https://example.com/mcp`. It fails with a message that an enterprise MCP configuration is active and has exclusive control.
7. In a second terminal, `export NOTES_TOKEN=FAKE-TOKEN-DO-NOT-USE-bo`, start `claude` in `project`, and ask for `whoami` again. It answers `bo`. Same file, different identity.
8. Review a server before adding it: fill in two rows of `templates/mcp-server-review.md` for `shadow-sync` (what can it reach, what identity does it use).
9. Clean up: `sudo bash remove_managed_mcp.sh`.

**Expected result:** Before the managed file, both servers load. After it, only `notes` loads, adding a server fails, and two users get two identities from one shared file.

**Instructor note:** Linux: the file goes to `/etc/claude-code/managed-mcp.json` and needs root. macOS: `sudo bash install_managed_mcp.sh` picks `/Library/Application Support/ClaudeCode/`. Windows: run `install_managed_mcp.ps1` from an elevated PowerShell (target `C:\Program Files\ClaudeCode\managed-mcp.json`), use `python` instead of `python3` in `project/.mcp.json`, and use the `set NOTES_TOKEN=...` or `$env:NOTES_TOKEN = "..."` form. `allowedMcpServers` does not apply to servers in `managed-mcp.json`, but `deniedMcpServers` does, so say that the managed file itself is the allowlist. Unconfirmed, so rehearse: that `${NOTES_TOKEN}` expands inside an `env` value on your version (the docs describe `${VAR}` expansion from each user's environment; if the server sees no token, tell the class and show the `headersHelper` or per-user header route in the docs); how a project `.mcp.json` server is shown while the managed file is active; and where OAuth tokens live for project-scoped servers (not stated in the docs read). This demo uses an environment variable as a stand-in for per-user OAuth or per-user headers, and says so. Fallback (no root): do steps 1 to 3 and 8, then show screenshots of steps 5 to 7 from your rehearsal.

**Why this matters:** A server is code that runs with the user's rights, outside the sandbox, and it authenticates as someone. A fixed set removes the unreviewed ones. Per-user credentials mean the log shows who did what, and a leaver's access ends with their own login.

---

## Demo 6: Prove It: A Logging Hook

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

---

## Demo 7: Install a Plugin From a Marketplace

**Learning objective:** Add a marketplace, review a plugin before trusting it, install it, and use its command and its hook. Time: about 10 minutes.

**Files:** `$FILES/demo7-marketplace/champions-tools` (a marketplace with one plugin, `branch-guard`). Review aid: `$FILES/templates/plugin-review.md`.

**Context:** A marketplace is a folder (or a git repository) with `.claude-plugin/marketplace.json`. `branch-guard` bundles a command and a PreToolUse hook that blocks force pushes and pushes to `main`. A plugin's hooks and servers run with the user's rights, outside the sandbox, so review before you install. Plugin components are namespaced `plugin:component`.

**Steps:**

1. Add the marketplace from the local folder: `claude plugin marketplace add $FILES/demo7-marketplace/champions-tools`, then `claude plugin marketplace list`. Say where a team marketplace would come from instead: a git repository (`owner/repo` or a git URL).
2. Review before you trust. Open `plugins/branch-guard/hooks/hooks.json` and `scripts/block_force_push.py`. Then list the contents: `claude --plugin-dir $FILES/demo7-marketplace/champions-tools/plugins/branch-guard plugin details branch-guard`. Read the component inventory and the projected token cost.
3. Install it for yourself only: `claude plugin install branch-guard -s local`.
4. In a scratch repository (`git init`, one commit), start `claude`. Run `/reload-plugins` if the plugin does not show. Run `/branch-guard:branch-status`.
5. Ask: `Run git push --force origin main`. The hook blocks it, and the message starts with `BRANCH-GUARD`.
6. Uninstall and remove: `claude plugin uninstall branch-guard` and `claude plugin marketplace remove champions-tools`.

**Expected result:** The command reports the branch and the working tree state. The force push is blocked by the plugin's hook and Claude relays the reason.

**Instructor note:** `claude plugin install <plugin>` takes a scope with `-s user|project|local`. If the name is ambiguous or not found, the one-command form `claude plugin install branch-guard --marketplace <path>` adds the marketplace and installs together (needs a recent version). The `plugin@marketplace` name form is not in the docs read, so treat it as unconfirmed. Windows: use backslash paths, or run in Git Bash. The hook uses `python3`, so edit `hooks.json` to `python` if that is all your laptop has. macOS: no differences. No administrator rights are needed for a user or local scope install. Unconfirmed: whether `/reload-plugins` is enough on your version or you must restart `claude`. Fallback (no marketplace step, or a failed install): load the plugin for one session with `claude --plugin-dir $FILES/demo7-marketplace/champions-tools/plugins/branch-guard` and run steps 4 and 5. Keep a transcript outline: marketplace added, details read, installed, command output, blocked push.

**Why this matters:** A plugin is the unit a team ships and updates. It is also code with the user's rights. A marketplace gives one place to review, and the review must happen before the install, because the install is the trust decision.

---

## Demo 8: Evaluate a Plugin With a Test Suite

**Learning objective:** Test a plugin's behavior with an eval suite, read its always-on cost, and say what a passing score does not prove. Time: about 12 minutes.

**Files:** `$FILES/demo7-marketplace/champions-tools/plugins/branch-guard` (with its `evals/` folder), `$FILES/tools/plugin_lint.py`.

**Context:** `claude plugin validate` checks files for syntax and schema errors and does not test behavior. `claude plugin eval` runs eval cases (a prompt and graders) in isolated sessions with only the plugin loaded. By default it also runs without the plugin as a baseline. It uses model credits and needs Git 2.31 or later. `branch-guard` has three cases: the hook blocks a force push, the command is chosen for a status question, and the plugin stays out of the way on an unrelated question.

**Steps:**

1. Cheap checks first, no model: `python3 $FILES/tools/plugin_lint.py $FILES/demo7-marketplace/champions-tools/plugins/branch-guard --marketplace $FILES/demo7-marketplace/champions-tools`. Then `claude plugin validate $FILES/demo7-marketplace/champions-tools/plugins/branch-guard`.
2. Always-on cost: `claude --plugin-dir <plugin> plugin details branch-guard`. Read the projected token cost. Say that descriptions are in the context window every turn, and that hooks and servers are not counted there.
3. Open `evals/blocks-force-push/prompt.md` and its two graders. Say what each grader checks: a regex over the trace for `BRANCH-GUARD`, and a model-judged check of the reply.
4. Run one case, once, without the baseline to keep it short: `claude plugin eval <plugin>/evals/blocks-force-push/case.yaml --runs 1 --ablation none --max-cost-usd 2`.
5. Read the result: the exit code (0 pass, 1 a case below the threshold or a failure, 2 a partial run), and the `report.html` and `aggregate-result.json` files.
6. Ask the class: this case passed. What have we not tested? (A command that triggers too eagerly, a hook that blocks too much, a second model.) Point at the `ignores-unrelated` case as the one that tests for over-triggering.

**Expected result:** The lint and validation pass. `plugin details` prints a component inventory and a token cost. The eval case passes, and the class names at least two things the suite does not cover.

**Instructor note:** `--runs`, `--ablation none|with-without`, `--max-cost-usd`, `--threshold` and `--allow-tools` are in the docs read, and so is the exit code scheme. Unconfirmed: that a `case.yaml` path is accepted as the target on your version (the docs say a plugin directory, a `prompt.md` or `case.yaml`, or an installed plugin), and whether a case needs `--allow-tools Bash` to run. If a path is rejected, run the plugin directory with `--runs 1`. An eval needs a recent version of Claude Code, and its sessions share your rate limit. Windows: run in Git Bash with Git 2.31 or later; the case's `scaffold.sh` needs `bash`. macOS: no differences. No administrator rights are needed. Fallback (no model, or the run is slow): show a screenshot of a `report.html` from your rehearsal, and walk through the three prompts and six graders on screen. The lint and `plugin details` steps still run live.

**Why this matters:** A plugin that validates can still trigger on the wrong prompts or fail to fire on the right one. An eval suite is the test for behavior. A pass is evidence for the cases you wrote, and only for those.

---

## Demo 9: Block a Write and a Network Call

**Learning objective:** Show an operating-system sandbox block a write outside the working directory and a call to a domain that is not allowed, and show what fail-closed means. Time: about 12 minutes.

**Files:** `$FILES/demo9-sandbox`: `configs/`, `apply.sh`, `project/probe.sh`. Environment check: `$FILES/setup/check_env.sh`.

**Context:** The sandbox covers shell commands and their child processes. Claude's file tools, MCP servers and hooks run outside it. On Linux and WSL2 it needs `bubblewrap` and `socat`. **On Ubuntu 24.04 and later the AppArmor profile `bwrap-userns-restrict` is loaded and enforcing by default, and it blocks bubblewrap.** Rehearse this demo on the exact machine you will teach from. `sandbox.failIfUnavailable: true` makes an unavailable sandbox a hard failure; by default Claude Code runs commands unsandboxed instead. **Where that failure surfaces depends on why the sandbox is unavailable:** with `bubblewrap` missing the startup check fails and Claude Code exits at startup, which is what step 5 shows. With `bubblewrap` installed but AppArmor blocking it, the startup check passes, the session starts normally, and every shell command is refused at run time with `apply-seccomp: ... Permission denied` instead.

**Steps:**

1. On the demo machine run `bash $FILES/setup/check_env.sh`. Show the `bubblewrap` and `socat` lines and the AppArmor line.
2. Sandbox off: `cd $FILES/demo9-sandbox && bash apply.sh off`, then `cd project && claude`. Ask: `Run bash probe.sh`. Probes 1, 2 and 3 report SUCCEEDED, and probe 4 gets a response.
3. Sandbox on: exit, run `bash ../apply.sh on`, and restart `claude`. Open `/sandbox` to show the panel. Ask for the probe again. Probes 1, 2 and 3 report BLOCKED. Probe 4 (an allowed domain) still gets a response.
4. Show the one-line check the class will use: ask Claude to run `touch ~/sandbox-probe`. With the sandbox working it fails with "Read-only file system".
5. Fail closed: on a second machine or snapshot with `bubblewrap` removed, show two starts. With `apply.sh on`, Claude Code runs commands unsandboxed (the default). With `apply.sh fail-closed`, it exits at startup.
6. Say what the sandbox does not cover: hooks, MCP servers and plugin processes, and Claude's own file tools.

**Expected result:** The probes flip from SUCCEEDED to BLOCKED when the sandbox is on, the allowed domain still answers, and a missing sandbox is a hard failure only when `failIfUnavailable` is true.

**Instructor note:** Windows: native Windows is not sandboxed, so run this demo from WSL2, a Linux VM or a Mac. macOS: the sandbox runs on macOS and needs no install, but the exact failure message for the `~/sandbox-probe` write is stated only for Linux and WSL2, so check what yours says. Linux: install with `sudo apt-get install bubblewrap socat` (Debian and Ubuntu) or `sudo dnf install bubblewrap socat` (Fedora and RHEL), and restart Claude Code, because the check runs at startup. On Ubuntu 24.04 and later, run `bash $FILES/setup/classroom-sandbox.sh --check` before you teach. Two things that look like fixes are not: relaxing `kernel.apparmor_restrict_unprivileged_userns` does nothing, because `bwrap-userns-restrict` stays loaded and carries `audit deny capability`, and an AppArmor deny beats any allow; and a profile naming a binary does not help either, because the denial is raised inside `unpriv_bwrap`, the profile `/usr/bin/bwrap` transitions *into*. Both were tested on a class image and both failed. What works is disabling the `bwrap-userns-restrict` profile, which `classroom-sandbox.sh --on` does and `--off` undoes. It is machine-wide, so treat it as a decision rather than a fix, and say that to the class — it is the same trade Lab 3 asks them to make. Inside a container bubblewrap can fail with "Operation not permitted", and `sandbox.enableWeakerNestedSandbox` weakens isolation, so do not use it for this demo. Unconfirmed: the container fix steps, and whether a typical Linux VM works without changes (the docs state only the dependency and user namespace requirements). If your machine has no internet, probe 3 reads BLOCKED for the wrong reason: run the `curl` from a normal terminal first. Fallback (no sandbox support on the machine): screenshots of both probe runs and of the fail-closed exit from your rehearsal.

**Why this matters:** A sandbox is the layer that still holds when a rule is missing or the model is persuaded. Fail-closed turns a quiet loss of protection into a loud stop. Knowing what the sandbox does not cover is what keeps the team from over-trusting it.

---

## Demo 10: Find the Credential Smells

**Learning objective:** Spot the common credential smells in a small project, and say for each who owns it, how long it lives and how it is rotated. Time: about 10 minutes.

**Files:** `$FILES/demo10-credential-smells`: `lakeside-api/` (a fictional project), `smell_scan.py`.

**Context:** The project holds a key in a settings file, a key helper that only echoes a fixed value, an `.env` file with no deny rule, a shared-sounding CI secret, an inventory row with no expiry, and a token set in a script. All values are placeholders. A scan finds patterns, and it cannot tell you who owns a credential.

**Steps:**

1. Open `lakeside-api/.claude/settings.json`, `.claude/token.sh`, `.github/workflows/summary.yml`, `scripts/nightly.sh` and `ops/credentials.csv`. For 3 minutes, ask the class to call each smell as you open a file.
2. Run the scan: `python3 smell_scan.py lakeside-api`. Compare its list with the class's list.
3. Ask what the scan cannot see. (Who owns `ORG_WIDE_CLAUDE_KEY`, whether `t.brandt` still works here, whether anything was ever rotated.)
4. For the top two smells, say the fix and the rotation step aloud.
5. Show where your own login is stored without opening it. On Linux: `ls -l ~/.claude/.credentials.json` (mode `-rw-------`). Run `/status` to see which credential is active.
6. Close with the three kinds of credential for automation: a personal token (tied to a person), a shared key (tied to nobody and everybody), and a federated or service identity (tied to a role the team owns).

**Expected result:** The class finds most smells by eye. The scan finds the patterns and misses the ownership problems, which only a person reading the inventory can see.

**Instructor note:** No model call and no administrator rights are needed. Facts for step 5: on Linux the credentials are stored in `~/.claude/.credentials.json` with mode 0600; on macOS they are in the Keychain (and fall back to the same file when the Keychain is locked); on Windows they are in `%USERPROFILE%\.claude\.credentials.json`. Never open or display that file. If `ANTHROPIC_API_KEY` is set alongside a login, Claude Code can use the key once it is approved, which is why `/status` matters. A long-lived token from `claude setup-token` is a one-year token, per the docs read, and it can only make model requests. The details of federation setup are not in the docs read, so keep that to a sentence and mark it as unconfirmed. Windows: run `python smell_scan.py lakeside-api`. macOS: no differences. Fallback (no machine): the five files and the scan output on a slide.

**Why this matters:** Credentials are where most real incidents start. A named owner, a lifetime and a rotation step turn a secret into something a team manages. Without them, it is a leak that has not been found yet.
