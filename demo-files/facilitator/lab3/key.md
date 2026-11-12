# Lab 3 key: Harden a Sample Repository

Solution: `solution/report-archiver/` (settings, `.mcp.json`, fixed `app.py`). `python3 lab3-harden/check_settings.py facilitator/lab3/solution/report-archiver` prints Part A 60 of 60.

## Planted weaknesses and the fix for each

| # | Weakness | Where | Fix | Part A points |
|---|---|---|---|---|
| 1 | Sandbox off | `sandbox.enabled: false` | `true` | 7 |
| 2 | No fail-closed | `failIfUnavailable` missing | `true` | 7 |
| 3 | A command outside the sandbox on purpose | `sandbox.excludedCommands: ["python3"]` | remove | 5 |
| 4 | Wildcard domain | `sandbox.network.allowedDomains: ["*"]` | `["pypi.org", "files.pythonhosted.org"]` | 7 |
| 5 | Writes to the home folder | `sandbox.filesystem.allowWrite: ["~"]` | the project folder only | 5 |
| 6 | Nothing protected from reads | `sandbox.filesystem.denyRead: []` | the secrets file and `~/.ssh` | 5 |
| 7 | Config files writable by shell commands | `denyWrite: []` | `.claude` and `.mcp.json` | 3 |
| 8 | No Read deny rules | `permissions.deny: []` | `Read(./config/secrets.env)`, `Read(./.env)`, `Read(./.env.*)` | 4 |
| 9 | `curl` and `wget` allowed | `permissions.deny: []` | `Bash(curl *)`, `Bash(wget *)` | 3 |
| 10 | Blanket allow | `permissions.allow: ["Bash(*)", "Read(*)"]` | narrow allow rules | 4 |
| 11 | An unapproved server | `.mcp.json` `shadow-sync` | remove it | 6 |
| 12 | A hook that sends tool calls to an outside address | `hooks` in settings, `tools/report_usage.py` | remove the hook | 4 |

## Part B (live, 10 points each when blocked)

1. Write outside the working directory: blocked by the sandbox write rules.
2. A call to `example.com:80`: blocked by the network allowlist.
3. A read of `config/secrets.env` by a script run in the shell: blocked by the sandbox `denyRead`. The Read deny rule does not apply to a shell script, which is why both layers are needed.
4. Command injection through `app.py`: blocked only by the code fix (`subprocess` with an argument list, and name validation). The sandbox does not stop a command that runs inside the working directory.

Expected: with the sandbox working, the solution scores 40. If the sandbox cannot start, attempts 1 to 3 will succeed and the score is 10 (attempt 4). A student whose Part B is low because the sandbox is broken still earns Part A.

## What a good GAPS.md says

- Hooks and MCP servers run outside the sandbox, so the hook was reviewed and removed and the server list was cut by hand.
- Claude's own file tools run outside the sandbox, so the Read deny rules and the permission rules cover them.
- Plugin processes run outside the sandbox.
- The code fix closed a hole that the sandbox could not, because the injected command stayed inside the working directory.

## Unconfirmed

- The entry format of `sandbox.excludedCommands`.
- How a relative path in `sandbox.filesystem` is resolved. If the solution's `.` and `./config/secrets.env` entries do not block on your image, switch to absolute paths.
- Loopback under the sandbox network proxy. The attack script uses `example.com:80` so it does not depend on this.
- Container behavior: the docs read name a troubleshooting section for "Operation not permitted" but the fix steps were not captured.
