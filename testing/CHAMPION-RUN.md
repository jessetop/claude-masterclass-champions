# Claude Champion test run — brief

**This is your brief.** You are a Claude Code session on a Linux class machine, testing
this course the way a student would use it.

Read **[`HANDOFF.md`](HANDOFF.md)** first. It holds the rules, the verdict vocabulary and
the logging format, and it governs everything below.

---

## 0. What has already been done, so you do not redo it

Six labs and ten demos, built from a supplied `labs.md` and `demos.md`. Before this run:

- **Lab 1 was tested by hand** and four scorer defects fixed. Starter scores 15/100, the
  answer key 100/100.
- **Labs 2 to 6 were audited by agents**, 65 findings raised, 45 confirmed and 20 refuted,
  and the confirmed ones fixed. See `FIXES-APPLIED.md` pass 3.
- **The demos were corrected** where they repeated a sandbox story that three earlier test
  rounds on a sister course had already disproved.
- **Nothing has been run against a live model.** Every result so far is static: scorers,
  file checks, documentation reads. **That is the gap this run exists to close.**

---

## 1. Prove the machine first

```bash
bash demo-files/setup/check_env.sh
bash demo-files/setup/classroom-sandbox.sh --check
python3 testing/smoke.py
python3 testing/check_refs.py .
```

Write all four outputs into `testing/results/00-setup.md`, with `claude --version`,
`claude auth status` and whether you have `sudo`.

**If `smoke.py` reports NOT OK, stop and report that before anything else.** It means a
scorer no longer separates an untouched starter from the answer key, so every lab result
measured after it would be measuring the wrong thing.

**The sandbox.** On Ubuntu 24.04 and later the `bwrap-userns-restrict` AppArmor profile
is on by default and stops the sandbox. Labs 3 and 4, and Demos 3 and 9, need it.
`classroom-sandbox.sh --on` switches it off and `--off` restores it — read Lab 3 Step 1
first, because it is machine-wide. If your own permission layer refuses that command,
**say so in the log and take each lab's fallback path.** Do not work around the refusal.

---

## 2. What this run must establish

In priority order. The first two are the whole point.

1. **Does a live model actually complete these labs?** Labs 2 and 4 spend model requests
   and have never been run. Lab 2's eval suite (`claude plugin eval`) and Lab 4's four
   defence configurations are the two places where the material could be wrong in a way
   no static check can see.
2. **Do the demos work when performed?** Ten demos, none of them ever run. Demo 2 and
   Demo 5 write files as root — confirm their remove scripts leave the machine clean.
   Demo 9 is the one most likely to fail; see the sandbox note above.
3. **Does each lab's rubric match what its scorer awards?** Add the published rows, run
   the scorer, compare.
4. **Timings.** Every lab states a duration. Note yours, and say plainly that agent time
   is not student time — the sessions skip the reading and deliberation that are most of
   a student's work.

---

## 3. Test the scorer, not only the lab

Required for every scored lab, and it is where almost every real defect in this
repository has come from. `HANDOFF.md` section 6 has the method; the result template has
a table for it.

Briefly: take your working answer and rewrite parts of it the way another competent
student would — a different variable spelling, a YAML block list instead of an inline
list, a synonym, a valid alternative path form. **Does the score hold?** Then feed the
scorer junk and an empty answer. **Does anything pass?**

Recently fixed examples, to show the shape of it: writing `$CLAUDE_PLUGIN_ROOT` without
braces cost 30 of 100 in Lab 2; setting `allowWrite` to the exact path Lab 3 tells you to
create was rejected; eight rows of placeholder junk scored a perfect 65/65 in Lab 4.

---

## 4. Order

| # | What | Why here |
|---|---|---|
| 1 | Lab 1 | Fastest, no model spend, confirms the fixes held |
| 2 | Lab 3 | Needs the sandbox decision made early |
| 3 | Lab 2 | Largest model spend; the eval suite is the unknown |
| 4 | Lab 4 | Model spend, and depends on the same sandbox as Lab 3 |
| 5 | Labs 5 and 6 | Take-home, no model spend, paper and measurement |
| 6 | Demos 1 to 10 | Perform each; note what an instructor would hit |

---

## 5. Hard rules

- **The environment is ground truth. The material is the thing under test.**
- **Do not edit a lab, demo or scorer.** Report it; a human decides the fix. Project files
  a lab tells you to create go in a scratch directory outside the repository.
- **A deviation is a FAIL or a BLOCKED**, with the deviation recorded. Never PASS because
  you found a way to make it work that the material never told the student to do.
- **Never push. Never raise a spend cap. Never write a credential into a result file.**
- **Do not loop on a failing command.** A clear blocker is a useful result; a fabricated
  pass is worse than no result.

---

## 6. Finishing

Write `testing/results/99-summary.md`: the verdict table, which of the recent fixes held,
the blockers in the order they should be fixed, and anything about the class machine that
`SETUP.md` should say and does not.

Then run `python3 testing/smoke.py` once more and paste the result, so the next reader
knows the repository was in a working state when you left it.
