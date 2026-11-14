# Lab Testing Handoff — Claude Champion

**Read this first. You are starting with no prior context.**

You are a Claude Code session on a Linux class machine. Your job is to work through this
repository's labs and demos as a student would, record what actually happens, and write
the results to files a reviewer can read.

You are **testing the material**, not completing a course. Nobody is grading your lab
output. The deliverable is the log.

---

## 1. The one rule that matters

**The environment is ground truth. The lab text is the thing under test.**

When a lab says something the machine contradicts — a command that does not exist, a flag
that has moved, a version that is too old, a score that does not match the rubric — that
is a **defect in the lab**, and you record it.

Do **not**:

- Edit a lab file to match what you found. Report it; a human decides the fix.
- Work around a blocker silently and carry on as if it passed.
- Mark something PASS because you found a way to make it work that the lab never told
  the student to do.

If you had to deviate from the written steps to proceed, that is a **FAIL** or a
**BLOCKED**, with the deviation recorded.

---

## 2. Safety constraints

- **Never write a credential into a result file.** Not a key, not a token, not a
  password. Replace it with `REDACTED` and check every file before you save it.
- **Never push to any remote.** No `git push`, no pull request. Results are local files.
  Labs that say to commit mean commit locally.
- **Spend caps are results, not obstacles.** Labs 2 and 4 spend model requests. If a lab
  stops because it hit a cap, log it and move on. Do not raise the cap.
- **The only change you may make to the machine** is `classroom-sandbox.sh --on`, and you
  run `--off` before you finish. Nothing else. If your own permission layer refuses it,
  **say so in the log and take the fallback path** rather than working around the refusal.

---

## 3. Where things are

```
<repo root>/
├── README.md              what the course is, and the index
├── SETUP.md               install, sign-in, and the pre-Lab-1 environment check
├── REHEARSAL.md           every unconfirmed item, and what is already settled
├── labs/                  one file per lab, plus README.md (preamble and index)
├── demos/                 one file per demo, plus README.md
├── demos.md               every demo in one printable document
├── demo-files/            the assets the labs call $FILES
│   ├── setup/             check_env.sh, classroom-sandbox.sh
│   ├── facilitator/       answer keys — NOT in the student pack
│   └── make-student-pack.sh
└── testing/
    ├── HANDOFF.md         this file
    ├── CHAMPION-RUN.md    the brief for the current run
    ├── FIXES-APPLIED.md   what has been tested and changed, one section per pass
    ├── smoke.py           one command: do all the scorers still discriminate?
    ├── check_refs.py      do all $FILES references resolve?
    └── results/
        ├── _TEMPLATE.md   copy this per lab
        └── <slug>.md      your logs
```

In every lab, **`$FILES` means the `demo-files` folder.**

Each lab states a goal, acceptance criteria, a **Checkpoint** and a **Scoring rubric**.
Those are your test plan: confirm the prerequisites, run the lab, check every Checkpoint
item, and run the scorer.

---

## 4. Before any lab: prove the machine

```bash
bash demo-files/setup/check_env.sh
bash demo-files/setup/classroom-sandbox.sh --check
python3 testing/smoke.py
```

`check_env.sh` reads the machine and changes nothing. `smoke.py` runs every lab's scorer
against both the untouched starter and the shipped answer key, and asserts that the
starter scores low and the key scores full marks. **If smoke.py reports NOT OK, stop and report
that before testing anything else** — it means a scorer is broken, and every lab result
after it would be measuring the wrong thing.

Record the output of all three in `testing/results/00-setup.md`, along with
`claude --version`, `claude auth status`, and whether you have `sudo`.

---

## 5. How to log

Copy `testing/results/_TEMPLATE.md` to `testing/results/<lab-file-slug>.md`.

Use these verdicts, and only these:

| Verdict | Means |
|---|---|
| `PASS` | Every step worked as written; every Checkpoint item satisfied |
| `PASS WITH NOTES` | Completed as written, but something is worth fixing |
| `FAIL` | A step did not work as written, or a Checkpoint item could not be satisfied |
| `BLOCKED` | Could not start or continue for an environmental reason |
| `REVIEWED` | Paper lab assessed by reading, not executed |
| `NOT TESTED` | Deliberately skipped — say why |

**Record verbatim output for every failure.** The actual command and the actual error,
not a paraphrase. A reviewer cannot reproduce it and is relying on what you captured.

Also record, for every lab:

- **The score you got**, and whether it matches what the rubric says it should.
- **Wall-clock time** against the lab's stated duration, and say plainly if your time is
  agent time rather than student time — they are not comparable.
- **Anything a student would ask** that the lab does not answer.

**Save after each lab, not at the end.** Keep `testing/results/00-INDEX.md` current so
the state of the run is readable from one file.

---

## 6. Test the scorer, not only the lab

This is what has found almost every real defect in this repository, so do it for every
scored lab. After you have the lab working:

1. **Probe for false fails.** Take the working answer and rewrite parts of it the way
   another competent student would — a different variable spelling, a block list instead
   of an inline list, a synonym, a different but valid path form. Does the score hold? A
   correct answer that scores zero is the most damaging defect this material has.
2. **Probe for false passes.** Feed the scorer an empty or junk answer. Does anything
   pass? A check of the form "every X is valid" passes trivially when there are no X.
3. **Check the rubric against the scorer.** Do the published point totals sum to the
   stated maximum, and does each row award what the table says?

Report these in the Defects table like any other finding.

---

## 7. When you finish, or get stuck

Write `testing/results/99-summary.md` with the verdict table, the blockers in the order
they should be fixed, and anything about the class machine the setup guide should say and
does not.

If you hit something you cannot resolve — ambiguous instructions, a failure you cannot
interpret — **stop, write it up, and say so plainly.** Do not guess your way forward and
do not loop on a failing command. A clear blocker is a useful result; a fabricated pass
is worse than no result.
