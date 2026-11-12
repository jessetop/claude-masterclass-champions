# demo-files: AI Champions Training, Claude Code for Engineering Teams

Hands-on files for the demos (`demos.md`) and labs (`labs.md`). ROI Training. Everything is fictional. Every planted secret is a placeholder (`FAKE-TOKEN-DO-NOT-USE` and similar). Students work on Linux class machines with bash and Python 3.11. Instructors may demo from Windows or macOS (each demo gives the differences).

Run `bash setup/check_env.sh` on a Linux machine first. It checks Python, `jq`, `git`, `claude`, `bubblewrap`, `socat` and the AppArmor setting, and prints install commands.

Remove `facilitator/` (and the Facilitator notes in `labs.md`) before you share this folder with students.

## Index

| Folder or file | Used by | What it holds |
|---|---|---|
| `setup/check_env.sh` | all labs | Linux environment check (reads only) |
| `templates/intake-checklist.md` | Demo 1 | Generic ten-section intake checklist (a team replaces it with its own) |
| `templates/risk-tiers.md` | Demo 1 | Generic three-tier example |
| `templates/team-practices-charter.md` | Lab 1 | Generic one-page charter with a status column (Enforced, Reviewed, Undecided) |
| `templates/mcp-server-review.md` | Demo 5 | Checklist for reviewing an MCP server before adding it |
| `templates/plugin-review.md` | Demo 7, Lab 2 | Checklist for reviewing a plugin before trusting it |
| `tools/plugin_lint.py` | Demo 8, Lab 2 | Free local plugin checks (not a replacement for `claude plugin validate`) |
| `demo1-intake/` | Demo 1 | Fictional use case brief |
| `demo2-managed/` | Demo 2 | Managed settings file, a conflicting project file, install and remove scripts (Linux, macOS, Windows) |
| `demo3-rule-vs-request/` | Demo 3 | Sample project, four configurations (request only, Read deny, deny plus sandbox, bypass-mode test), `apply_config.sh` |
| `demo4-exit-codes/` | Demo 4 | A hook that exits 1 and the fixed version that exits 2, a no-model test script |
| `demo5-mcp/` | Demo 5 | Two local MCP servers (approved and unapproved), a managed MCP file installer, a test script |
| `demo6-logging/` | Demo 6 | Block-and-log hook, tool-call logger (shell and Python versions), log summaries, a sample log |
| `demo7-marketplace/champions-tools/` | Demos 7 and 8 | A marketplace with one plugin, `branch-guard`, that has a hook, a command and an eval suite |
| `demo9-sandbox/` | Demo 9 | Sandbox configurations and a harmless probe script |
| `demo10-credential-smells/` | Demo 10 | A small project with planted credential smells and a scanner |
| `lab1-rule-to-control/` | Lab 1 | Rules, the `ledgerlite` project with planted traps, a charter working copy, `check_lab1.py` |
| `lab2-plugin/` | Lab 2 | The `relnotes-starter` plugin with a six-case eval suite, a marketplace template, `score_lab2.py` |
| `lab3-harden/` | Lab 3 | The `report-archiver` project, `attack_simulation.py`, `check_settings.py` |
| `lab4-injection/` | Lab 4 | The `shipping-notes` project, four defense configurations, canary listener, injection scan, record sheet, `check_record.py` |
| `lab5-audit/` | Lab 5 | The `harbor-org` sample, findings template, `check_findings_format.py` |
| `lab6-context/` | Lab 6 | The `shopkit` project with a bloated `CLAUDE.md`, a plugin with long descriptions, the worksheet, `check_lab6.py` |
| `facilitator/` | facilitators only | Answer keys, solutions, sample answers, a keyword scorer for Lab 5, the rehearsal list |

## Rules for these files

- Never put a real key, token or password in any file here.
- Scripts that write to a system path (`/etc/claude-code/`, `/Library/Application Support/ClaudeCode/`, `C:\Program Files\ClaudeCode\`) need root or administrator rights and have a matching remove script. Run the remove script when you finish.
- Nothing here needs access to any organization or administrator console. Every score comes from a local script.
- Several labs and demos use model requests on your own seat. Each says where to cap them.
