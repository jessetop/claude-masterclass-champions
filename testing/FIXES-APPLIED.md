# Fixes Applied — Claude Champion

One section per testing pass. Each records what was tested, what broke, and what was
changed, so a later reader can see why a file looks the way it does.

The method is the one that worked on the other courses in this program: **do the lab from
the student pack, then probe the scorer with correct answers that differ from the shipped
solution.** Most defects in a scored lab are not "the solution fails" — it is that a
different right answer fails, or that a wrong answer passes.

---

## Pass 0 — porting verified findings into Labs 3, 4 and 5 (2026-11-14)

Recorded in the commit `Port the verified sandbox and credential findings into Labs 3, 4
and 5`. Summary: Lab 3's AppArmor guidance named a sysctl that does nothing and has no
effect on the profile; Lab 3 had no fallback scoring, so a machine that cannot sandbox
cost 40 points with no path; Lab 4's troubleshooting described the wrong failure mode for
a blocked sandbox; Lab 5 had no rotation policy to measure "never rotated" against. All
four came from three test rounds on the Enterprise Deployment course, which shares this
material's lineage.

---

## Pass 1 — Lab 1: Rule to Control (2026-11-14)

**Verdict: the lab works.** The starter scores **15/100** with every planted trap
detected, the shipped facilitator solution scores **100/100**, and the hook in that
solution is robust well past what is tested — it blocks `rm -r -f`, `rm -Rf`,
`rm --recursive --force` and `sudo rm -rf /`, none of which the scorer exercises.

Four defects, all in the scorer, all of the same family: a correct answer that differs
from the shipped solution was punished, and an empty answer was rewarded.

### 1.1 `$CLAUDE_PROJECT_DIR` without braces cost 50 points, not 10

The worst of the four. The scorer required the literal string `${CLAUDE_PROJECT_DIR}`.
A student writing `python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard.py"` — valid shell,
and it locates the script from the project exactly as the lab asks — lost the 10-point
wiring check **and then lost the 30 points of exit-code tests and the 10-point log
check**, because the path could no longer be resolved to find the script. Half the lab,
for a brace.

Measured: 100 → 50. Now 100. The scorer substitutes both spellings, and the wiring check
asks whether `CLAUDE_PROJECT_DIR` is used at all rather than matching one rendering of it.

### 1.2 A matcher of `*` scored zero for the wiring

`*` fires for every tool, Bash included, so a hook wired that way genuinely runs before
Bash and satisfies the lab's acceptance criterion. It scored 0/10.

Measured: 100 → 90. Now 100. Still worth a word in class — `*` also fires for `Read` and
`Edit`, so it is broader than the rule needs — but it is not wrong, and the scorer should
not say it is.

### 1.3 Partial credit was promised and never paid

Both the lab rubric and the scorer's own docstring say the charter count carries
"partial credit below 6". The code computed the partial figure and then threw it away:

```python
award(20 if n >= 6 else int(20 * n / 6), n >= 6, ...)   # got = points if ok else 0
```

With `n = 5` that computes 16 and awards **0**. It also printed `[FAIL] 0/6`, which reads
as though the item were worth 6 points rather than 20.

Measured: 5 of 10 decided scored 80, identically to 3 of 10. Now 96 and 90. Added an
`award_partial` helper and a `PART` tag so a partial award is legible.

### 1.4 FALSE PASS: an untouched charter collected the full 15

The mirror of the other three, and the reason to probe in both directions. The check
"every Enforced row names a control that exists" passes **vacuously** when there are no
Enforced rows, so a charter with nothing filled in scored the full 15.

Measured: a charter with 0 of 10 decided scored 80. Now 65. The check requires at least
one Enforced row, which is reasonable in a lab whose previous three steps build a hook
and two deny rules — there is something to point at. An honest charter that marks
everything Reviewed loses this 15 and keeps the 20, which is the right shape: Reviewed is
a legitimate status, but it is not evidence of a control.

### Not changed

- **`rm -r -f` is taught but not scored.** The hints ask which `rm` spellings the starter
  misses and the facilitator note lists `rm -r -f` as a trap, but the scorer tests only
  `rm -rf` and `rm -fr`. A student can pass both and still miss the third. Left alone
  because adding a case changes the published point totals; noted in the Facilitator note
  as something to ask about rather than score.
- **The two pre-marked trap rows count toward "decided".** Rows 6 and 9 ship marked
  Enforced with no real control, so an untouched charter earns 6 partial points for them
  while correctly scoring 0 on the control check. Generous by 6 points, and the overall
  discrimination (15 against 100) is unaffected.

---

## Pass 2 — demos, and the claim everything else rests on (2026-11-14)

**Demo 9 would have failed live in front of a class.** Its Context said the AppArmor
setting on Ubuntu 24.04 and later "is off by default". It is on by default, and it is
what stopped the sandbox on the class image this program tested three times. Its
Instructor note then sent the instructor to the sysctl and to "add an AppArmor profile
for `/usr/bin/bwrap`" - both tested, both dead ends. Demo 9 and Demo 3 now point at
`classroom-sandbox.sh`. `check_env.sh` had the same flaw and printed `[ ok ]` when the
sysctl was 0 and the profile was still blocking, and that output is shown to the class in
Demo 9 step 1. It now reports the profile.

**Verified, so nobody re-litigates it:** exit 2 blocks and exit 1 does not. Lab 1 stakes
30 points of exit-code tests on it and Demo 4 is built entirely on it, so it was worth
reading in the page rather than trusting the course text. Verbatim from the hooks
reference: *"Exit with code 2 to block the action... a `PreToolUse` hook blocks the tool
call... The message that comes with the block is your hook's stderr."* Exit 1 without
valid JSON is a non-blocking error. Two refinements are now in Demo 4's instructor note
for the student who asks: a hook that exits 1 but prints valid JSON can still decide the
outcome through that JSON, and `onFailure: "block"` makes a failing hook block. Neither
affects the lab, whose starter exits 1 with plain stderr and no JSON.

**Checked and found sound:** all 46 Python files, 31 shell scripts and 38 JSON files
parse; all 52 `$FILES` references and all 74 relative markdown links resolve; both
root-writing demos (2 and 5) have symmetric install and remove scripts that back up and
restore a pre-existing file and clean up the server directory; and every demo marks its
own unconfirmed items, which is better discipline than the labs started with.

