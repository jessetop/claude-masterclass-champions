# Facilitator folder

Do not share this folder with students. `make-student-pack.sh` removes it for you. Also strip the Facilitator note at the end of each file in `labs/` and the Instructor note in each file in `demos/` before you hand those documents out.

## Where each answer key is

| Item | Key |
|---|---|
| Demo 1 | `demos/demo1-completed-intake.md` |
| Lab 1 | `lab1/solution/` (`ledgerlite/.claude/settings.json`, `ledgerlite/.claude/hooks/guard.py`, `charter.md`) |
| Lab 2 | `lab2/solution-marketplace/` (a marketplace named `team-tools` holding the finished `relnotes` plugin) |
| Lab 3 | `lab3/solution/report-archiver/` and `lab3/key.md` |
| Lab 4 | `lab4/key.md`, `lab4/solution-record-sheet.csv` (a real run, 65/65; the payload never fired - read the key before using it) |
| Lab 5 | `lab5/rubric.md`, `lab5/solution-findings.md`, `lab5/score_audit.py` |
| Lab 6 | `lab6/solution/` |

## Check that every key still scores before class

Run these from the `demo-files` folder. Each should print the score shown.

```
python3 lab1-rule-to-control/check_lab1.py facilitator/lab1/solution/ledgerlite facilitator/lab1/solution/charter.md     # 100
python3 lab2-plugin/score_lab2.py facilitator/lab2/solution-marketplace/plugins/relnotes --marketplace facilitator/lab2/solution-marketplace    # 80 without an evidence file, 100 with one
python3 lab3-harden/check_settings.py facilitator/lab3/solution/report-archiver     # Part A 60
python3 facilitator/lab5/score_audit.py facilitator/lab5/solution-findings.md lab5-audit/harbor-org/org/credentials_inventory.csv     # 100
```

For Lab 6, copy `lab6-context` to a temporary folder, copy the files in `lab6/solution/` over the matching student files, and run `python3 check_lab6.py` there. It should print 100.

## Rehearsal list (nothing here has been run against a live model)

These were built without model calls. Rehearse each on the class image the day before.

1. Every live demo (1 to 4, 6 to 9): the prompts, and the wording Claude Code shows.
2. Demo 2: how `/model` and `/status` show a managed value.
3. Demo 3: whether `cat .env` is stopped by the Read deny rule alone. Record what you see.
4. Demo 5: that `${NOTES_TOKEN}` expands inside the `env` block of `managed-mcp.json`, and how project servers are listed while the managed file is active.
5. Demos 7 and 8: the install name form, `/reload-plugins` versus a restart, and whether `claude plugin eval` accepts a `case.yaml` path.
6. Demo 9 and Lab 3: the sandbox on the class image, including Ubuntu 24.04 and later (AppArmor), containers, and `failIfUnavailable`.
7. Lab 2: whether an exit-2 PostToolUse hook's message reaches Claude (the `hook-lints-bad-notes` case).
8. Lab 4: run each payload under configuration 01 on the model the class will use, and check loopback behaviour under the sandbox network proxy. **Do not plan on a transcript of the payload firing** - 30 runs across 7 models produced none, and `lab4/solution-record-sheet.csv` is the completed sheet to teach from instead. Read `lab4/key.md` on what that sheet does and does not show.
9. Model names and aliases change quickly. Recheck the model-config page the day before class.
