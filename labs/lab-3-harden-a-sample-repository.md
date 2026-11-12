# Lab 3: Harden a Sample Repository

**Course:** AI Champions Training: Claude Code for Engineering Teams

> Part of **[AI Champions Training: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites and cost notes before you start.

---

**Learning objective:** Harden a deliberately weak project with a sandbox, network and file rules, deny rules and a fixed MCP list, then prove it with an attack script, and say what a sandbox does not cover. Time: 90 minutes.

**Files:** `$FILES/lab3-harden`: `report-archiver/` (the project, with `attack_simulation.py`), `check_settings.py`. Environment check: `$FILES/setup/check_env.sh`.

**Context:** The sandbox limits shell commands and their child processes. It needs `bubblewrap` and `socat` on Linux, and Ubuntu 24.04 and later may need an AppArmor change. `sandbox.failIfUnavailable: true` makes a missing sandbox a hard failure, where the default is to run unsandboxed. A `Read` deny rule blocks Claude's file tools, and `sandbox.filesystem.denyRead` covers shell commands, so you use both. Hooks, MCP servers and plugin processes run outside the sandbox. `report-archiver` is a tiny tool with a command injection in `app.py`. Its settings are wide open, a hook reports every tool call to an outside address, and `.mcp.json` declares a server nobody approved. `check_settings.py` scores the files (60 points). `attack_simulation.py` makes four harmless attempts and scores the outcomes (40 points). Both run on your machine.

**Steps:**

1. **Make the sandbox work (about 15 minutes).** Goal: a sandbox that really blocks a write, shown by the probe.
   - Run `bash $FILES/setup/check_env.sh`. Install `bubblewrap` and `socat` if it says so. On Ubuntu 24.04 and later, check `sysctl kernel.apparmor_restrict_unprivileged_userns`, and if it is 1, follow your instructor's AppArmor instructions.
   - Copy `report-archiver` to `~/work/report-archiver`. Run `python3 attack_simulation.py --baseline` in a normal terminal outside Claude Code, and check it says REACHABLE.
   - Acceptance criteria: inside a Claude Code session in the project, with the sandbox on, `touch ~/sandbox-probe` fails with "Read-only file system". Then take a baseline: with the sandbox off, run `python3 attack_simulation.py` from the Bash tool and note the score.
   - Hints: Restart Claude Code after installing the dependencies, because the check runs at startup. The `/sandbox` panel has a Dependencies tab. If the probe file appears, delete it and fix the sandbox before you go on.

2. **Static baseline (about 5 minutes).** Goal: a table of what `check_settings.py` finds.
   - Run `python3 check_settings.py ~/work/report-archiver`. Acceptance criteria: every FAIL with one sentence on the risk.

3. **Harden the settings (about 30 minutes).** Goal: Part A scores 60 of 60, and the project still works for its job.
   - Acceptance criteria:
     - The sandbox is on and a missing sandbox is a hard failure.
     - Nothing is excluded from the sandbox on purpose.
     - Network access is limited to a short list of approved domains: `pypi.org` and `files.pythonhosted.org`.
     - Writes are limited to the project, and `.claude` and `.mcp.json` cannot be written by shell commands.
     - The secrets file and `~/.ssh` are protected from reads by shell commands, and the secrets file and `.env` are also protected from Claude's file tools.
     - `curl` and `wget` are denied, and there is no blanket Bash allow.
     - Only the two approved servers (`docs-search`, `ticket-bridge`) remain in `.mcp.json`.
     - No hook sends data to the network.
     - `python3 app.py q3.txt` and `python3 -m pytest -q` still run.
   - Hints: Read the settings file top to bottom and ask of each line what it grants. A wildcard in a domain list defeats the list. A command in `excludedCommands` is a hole in the wall. A hook is code that runs outside the sandbox, so reading it matters more than sandboxing it. Run the checker after each change and not once at the end.

4. **Fix the code (about 10 minutes).** Goal: the command injection is closed in `app.py`.
   - Acceptance criteria: a report name such as `q3.txt ; echo injected > INJECTED_MARKER` is rejected or treated as a plain file name, and `python3 app.py q3.txt` still prints a checksum.
   - Hints: a sandbox does not stop a command that runs inside the working directory. Where does the name reach a shell? Prefer fixing the call over cleaning the text.

5. **Prove it (about 20 minutes).** Goal: Part B at 40 of 40, observed live.
   - Start `claude` in the project with the sandbox on. Ask Claude to run `python3 attack_simulation.py`. Save the output.
   - Acceptance criteria: the sandbox probe line says the sandbox looks active; attempts 1, 2 and 3 are BLOCKED; attempt 4 is BLOCKED by your code fix; the score is 40.
   - Hints: if attempt 2 reads BLOCKED with the sandbox off, the machine has no internet. Use the baseline. If attempt 3 is not blocked, check the sandbox `denyRead` entry, not just the Read deny rule. Restart Claude Code after each settings change.

6. **Write what it does not cover (about 10 minutes).** Goal: five sentences, in a file called `GAPS.md`.
   - Acceptance criteria: it names at least three things the sandbox does not limit (for example hooks, MCP servers, plugin processes and Claude's file tools), says which of your controls covers each one, and says what the code fix did that the sandbox could not.

**Checkpoint:** Part A is 60, the attack script reports at least three BLOCKED attempts with the sandbox on, and `GAPS.md` exists.

**Common problems:**

- The probe write succeeds: the sandbox is not running. A missing dependency, an AppArmor restriction on Ubuntu 24.04 and later, or a container that blocks user namespaces. The default behavior is to run unsandboxed when it cannot start, which is why `failIfUnavailable` matters.
- Claude Code exits at startup after you set `failIfUnavailable`: the sandbox cannot start on this machine. Fix the dependency. That is the setting working.
- You blocked everything and the tool no longer runs: `allowWrite` must still allow the project folder, and `python3` must still run.
- Attempt 3 still succeeds: only the `Read` deny rule is set. It covers Claude's file tools and not a script run by the shell.
- Part A stays below 60 after you fixed a line: the checker looks for the words `secrets` and `.ssh` in `denyRead`, and a `Read` deny for `.env`. Compare your spelling.
- A server stays in `.mcp.json`: check the name against the approved list.

**Scoring rubric (100 points):**

| Item | Points |
|---|---|
| Part A: `check_settings.py` (twelve checks, 60 points) | 60 |
| Part B: each attack BLOCKED live is 10 points (write outside, disallowed domain, secrets read, injection) | 40 |

A missing `GAPS.md` or a Part B result with no saved output caps the total at 90. Zeroing the Claude-facing features to pass, for example deleting the tool or the tests, scores 0 for the lab.

**Facilitator note:** Remove before sharing. The answer key is `facilitator/lab3/solution/report-archiver` (a settings file, a fixed `app.py` and a two-server `.mcp.json`). It scores 60 on Part A, and 20 to 40 on Part B depending on the sandbox on the machine. Traps planted in `report-archiver`:

| Trap | Where | Check |
|---|---|---|
| Sandbox off, no fail-closed | `.claude/settings.json` `sandbox.enabled`, no `failIfUnavailable` | 7 + 7 |
| A command that runs outside the sandbox on purpose | `sandbox.excludedCommands: ["python3"]` | 5 |
| A wildcard domain | `sandbox.network.allowedDomains: ["*"]` | 7 |
| Writes allowed to the home folder | `sandbox.filesystem.allowWrite: ["~"]` | 5 |
| Empty read and write protections | `denyRead`, `denyWrite` empty | 5 + 3 |
| No deny rules, blanket allow | `permissions.allow: ["Bash(*)", "Read(*)"]`, `deny: []` | 4 + 3 + 4 |
| An unapproved server | `.mcp.json`, `shadow-sync` | 6 |
| A hook that sends every tool call to an outside address (runs outside the sandbox) | `.claude/settings.json` hooks, `tools/report_usage.py` | 4 |
| Command injection | `app.py`, `os.system` with the name pasted in | attack 4 |

The attack script's network target is `example.com:80`, a harmless public name. Unconfirmed: the entry format of `sandbox.excludedCommands` (the checker passes an empty or absent list), how a relative path in `sandbox.filesystem` is resolved (the answer key uses `.` and `./config/secrets.env`; if it fails on your image, use absolute paths), and how loopback traffic behaves under the sandbox's network proxy (which is why the default target is not loopback). Rehearse the whole lab on the class image, including the AppArmor step on Ubuntu 24.04 and later and a container check. If the image runs in a container, bubblewrap may fail with "Operation not permitted", the fix steps are not in the docs read, and `enableWeakerNestedSandbox` weakens isolation, so decide before class. Part A can always be scored without a working sandbox, because it only reads files. Watch for students who raise the score by removing the hook script but leave the hook entry (the checker follows the script, so an entry pointing at a missing script passes: ask why), and for students who treat the checker's predictions as observations.
