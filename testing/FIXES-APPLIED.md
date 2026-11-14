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

---

## Pass 3 — Labs 2 to 6, audited and fixed (2026-11-14)

Five labs audited in parallel, every finding then handed to a separate agent whose job
was to **refute** it. 65 findings raised, **45 confirmed, 20 refuted**.

The refutations are the reason the second stage exists. They included a finding built on
evidence the verifier could not reproduce at all and labelled fabricated; one whose
premise was contradicted by the lab's own text; three that reported a documented,
deliberate design as a bug; and one disproved by running the locally installed Claude
Code binary to check how permission rules actually match. Acting on those would have
broken working behaviour to fix problems that did not exist.

### The best defect in the set

Lab 2's evidence section awards 20 points for pasted output proving the student ran
`claude plugin validate`, `claude plugin details` and `claude plugin eval`. The validate
row read:

```python
re.search("claude plugin validate", text) and \
re.search("(passed|valid|success|no errors|exit(ed)? (code )?0)", text, re.I)
```

**`valid` is a substring of `validate`.** The second condition is satisfied by the exact
string the first condition requires, so the "and it passed" half of the check was dead
code and could never fail. The other two rows fell the same way: "could not compute token
cost" contains `token cost`, and "0 of 6 cases fail to even start" matches on `fail`.

Measured: an evidence file whose every line records total failure —
`ERROR: 3 errors found, plugin is broken, nothing works` — scored the full 20/20 and took
the lab to **100/100**, while the scorer printed the literally false line
`[PASS] 8/8 Evidence: validate output pasted and it passed`.

### The shape of the other 44

Almost all of them are one of two failures, and the split is roughly even:

**A correct answer that differs from the shipped solution is punished.** Writing
`$CLAUDE_PLUGIN_ROOT` without braces costs 30 of 100 in Lab 2 — the identical defect
already fixed in Lab 1, in a different file. Setting `allowWrite` to
`~/work/report-archiver`, the exact path Lab 3 Step 1 tells the student to create, is
rejected. Naming a Lab 4 configuration `01` the way the lab text and `apply_config.sh`
both name it costs up to 38 of 65. Writing a C4 finding as "ex-employee" instead of
"departed" scores 0 of 12 in Lab 5. Re-saving `measure.csv` from Excel scores 0 in Lab 6.

**A wrong or empty answer is rewarded.** Eight rows of placeholder junk score a perfect
65/65 in Lab 4, and Step 4 of that lab — fifteen minutes of work — can be skipped
entirely without losing a point. Lab 3's planted `excludedCommands` hole still makes the
checker predict all three sandbox attacks blocked. Lab 5 has one finding collecting
points for planted problems the student never reported, and a clean-repository penalty
that cannot be lost.

### The fixes, and what they cost

62 changes applied across the five scorers and their lab texts. Every lab still
discriminates: `python3 testing/smoke.py` reports the untouched starter low and the
shipped answer key full on all six.

**But the regression agents found about twenty NEW false passes**, and they are the
reason that stage existed. Closing a false fail by widening a check is easy; widening it
too far turns a scorer into a rubber stamp. Every lab came back `CONCERNS`.

The worst is Lab 5. Its matcher was widened with alternatives like `terminat`, `leave`
and `individual` — all of which are *fix* verbs carrying no identification signal. A
submission that never joins `hr_departures.csv`, never mentions a departure, and lists
four bare names as its priority order now scores **52/100**, with C4 and C6 at full
marks. The original defect was real — "ex-employee" should not score zero — but the cure
went too far.

Lab 6's is the sharpest single case: the stale-instruction check now excuses a stale term
if any prohibition word appears in the same sentence, so a student who resolves the lab's
headline trap **the wrong way** —
`Run the tests with nosetests, not python3 -m pytest -q` — scores 10/10 for "no stale
instruction remains" and 15/15 on facts, because the banned token satisfies the facts
regex too.

Lab 2 gained two: a basename fallback awards 22 points to a hook pointing at a script
that does not exist in the plugin — while `plugin_lint.py`, changed in the same batch,
correctly fails it — and grading "the best-scoring file in `commands/`" lets a scratch
cheat-sheet carry the command row while the real command is still the untouched TODO.

Lab 4 gained one (a digit anywhere in the defense cell escapes the configuration check)
and Lab 3 gained two, both defensible (commented-out code, and deliberate `exec()`
obfuscation no student would write).

These are recorded here rather than quietly fixed because the pattern matters: **this
material's scorers fail in both directions, and fixing one direction without testing the
other just moves the defect.** The next pass tightens each of them with a two-sided test —
the new wrong answer must fail, and the original right answer must still pass.

