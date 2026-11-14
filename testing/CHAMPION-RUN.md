# Claude Champion test run — RVC, all six labs

**This is your brief.** You are a Claude Code session on an ROI Virtual Classroom (RVC)
instance — an Ubuntu class machine, reached through a browser. You are testing this
course the way a student will use it next week.

Read **[`HANDOFF.md`](HANDOFF.md)** first. It holds the rules, the verdict vocabulary and
the logging format, and it governs everything below.

---

## 0. What is already done, so you do not redo it

Six labs and ten demos, with five fix passes behind them — see `FIXES-APPLIED.md`.

**Labs 1, 2, 5 and 6 have been exercised on Windows**, including live runs of
`claude plugin validate`, `plugin details` and `plugin eval`. Their scorers discriminate:
`python3 testing/smoke.py` shows the untouched starter low and the answer key full on all
six labs.

**Labs 3 and 4 have never been run at all**, because their sandbox halves need
`bubblewrap`, which does not exist on Windows. **That is the main reason this run
exists.** Lab 4 is the weakest link in the whole course: it ships no answer key, so
nothing can regress it, and its live behaviour has never been observed by anyone.

Everything else you are doing is a dress rehearsal on the real image — the machine
differences that a Windows run cannot see.

---

## 1. Prove the machine first

```bash
bash demo-files/setup/check_env.sh
bash demo-files/setup/classroom-sandbox.sh --check
python3 testing/smoke.py
python3 testing/check_refs.py .
claude --version && claude auth status
```

Write all of it into `testing/results/00-setup.md`.

**If `smoke.py` reports NOT OK, stop and report that first.** It means a scorer no longer
separates an untouched starter from the answer key, so every lab result after it would be
measuring the wrong thing.

### What the RVC image is known to be, from the sister course's testing

Check each and record what you actually find — these are expectations, not facts about
your instance:

| Expectation | Why it matters here |
|---|---|
| Ubuntu 26.04, kernel `…-gcp` | |
| Claude Code is the **apt package** at `/usr/bin/claude` | `~/.local/bin` does not exist. `SETUP.md` tells students to check before installing; confirm that reads correctly |
| `sudo` is passwordless | needed for the sandbox step |
| `python3` present, `python` resolves | every scorer |
| **`jq` may be missing** | `check_env.sh` requires it, and Lab 1 and Demo 6 use it. If it is absent, that is a finding about the image, not about the lab |
| **`bubblewrap` and `socat` may be missing** | Labs 3 and 4 need them. Same: record it |
| `bwrap-userns-restrict` AppArmor profile **on by default** | this is what stops the sandbox |

### The sandbox

The operator runs this **before** your session starts, and `--off` after:

```bash
bash demo-files/setup/classroom-sandbox.sh --on
```

**Do not run it yourself.** In three runs on the sister course, the testing session's own
permission layer refused exactly this command. Your job is to detect which state you are
in and say so:

- **Probe PASSES** — you are the first run anywhere with a working sandbox. Run Labs 3
  and 4 against it and report full scores, not fallback ones.
- **Probe FAILS** — say so plainly, take each lab's fallback path, and expect Lab 3 at 85.
  Do not try to switch it on.

---

## 2. Order, and what each lab is for

| # | Lab | Why here |
|---|---|---|
| 1 | **Lab 3** — Harden a Sample Repository | The sandbox half has never run. Part B is 40 points nobody has observed |
| 2 | **Lab 4** — Prompt Injection Detection | Weakest link: no answer key, never run, four configurations, spends model requests |
| 3 | **Lab 2** — Build a Plugin With a Hook | Largest model spend. Worked on Windows; confirm on the class image |
| 4 | **Lab 1** — Rule to Control | Fast, no model spend. Confirms hooks behave on this OS |
| 5 | **Labs 5 and 6** | Take-home, paper and measurement |
| 6 | **Demos 1–10** | Never performed. Demo 9 is the one most likely to fail |

### Lab 3 — what to settle

Does a hardened configuration actually block attempts 1, 2 and 3 with a live sandbox?
Nobody has seen it. Also: does `sandbox.allowUnsandboxedCommands: false` stop an
unsandboxed retry on a sandbox that **works**? The sister course settled it only for a
sandbox that fails at runtime.

### Lab 4 — what to settle

Run all four configurations. Record the permission mode you were actually in. Build a
complete record sheet and run `check_record.py` — **and keep that sheet**, because the
lab ships no answer key and yours would become the first one.

Expect the model to refuse the payload often. That is a result, not a failure: record
what happened, not what should have happened. Flagging is **not** reproducible across
runs — the lab says so now — so do not re-run hoping for a different answer.

### Lab 2 — one thing that was broken until yesterday

Its eval cases could not pass: five of six grade a file on disk while granting no `Write`
tool, and the runner gates `Write`/`Bash` separately. The hint now carries
`--allow-tools Write Bash`. Measured on Windows, same case one flag apart: **1.00 with
the grant, 0.00 without.** Confirm that holds on Linux, and keep the run inside the cap.

---

## 3. Test the scorer, not only the lab

Required for every scored lab, and where almost every real defect here has come from.
`HANDOFF.md` section 6 has the method; the result template has a table for it.

Take your working answer and rewrite parts the way another competent student would — a
different variable spelling, a YAML block list instead of an inline one, a synonym, a
valid alternative path. **Does the score hold?** Then feed it junk and an empty answer.
**Does anything pass?**

---

## 4. Hard rules

- **The environment is ground truth. The material is the thing under test.**
- **Do not edit a lab, demo or scorer.** Report it. Project files a lab tells you to
  create go in a scratch directory outside the repository.
- **A deviation is a FAIL or a BLOCKED**, with the deviation recorded.
- **Do not change this machine.** The operator handles the sandbox before and after.
- **Never push. Never raise a spend cap. Never write a credential into a result file.**
- **Do not loop on a failing command.** A clear blocker is a useful result; a fabricated
  pass is worse than no result.

---

## 5. Finishing

Write `testing/results/99-summary.md`: the verdict table, which of the five fix passes
held, the blockers in the order they should be fixed, and **everything about the RVC
image that `SETUP.md` or `check_env.sh` should say and does not**. That last one is worth
as much as the lab verdicts — it is the part a Windows run can never produce.

Then run `python3 testing/smoke.py` once more and paste the result, so the next reader
knows the repository was in a working state when you left it.
