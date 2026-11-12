# Demo 8: Evaluate a Plugin With a Test Suite

**Course:** AI Champions Training: Claude Code for Engineering Teams

> Part of **[AI Champions Training: Demos](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites and cost notes before you start.

---

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
