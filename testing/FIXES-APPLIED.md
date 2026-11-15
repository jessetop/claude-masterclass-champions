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

---

## Pass 4 — the pendulum, and stopping it by hand (2026-11-14)

A second agent pass closed 22 of the regressions from pass 3. It also made **8 checks
swing back**: correct answers rejected again. Lab 4 came back CLEAN; Labs 2, 3, 5 and 6
did not.

That is the finding, more than any individual defect. **Keyword matching over student
prose does not converge.** Each round moves the boundary and overshoots the other way,
because a word list cannot tell "terminate the credential" (a fix verb) from "the owner
was terminated" (an identification). Two automated rounds produced a net improvement and
a fresh set of errors each time, so the rest was done by hand with an explicit two-sided
test at each step.

### Fixed here, each proven in both directions

**Lab 5 — the word-count floor.** `has_reason` demanded five words after the break, so
`6. Finding 5, hygiene only.` was rejected while a longer restatement of the finding's
own name passed. Length was never the signal. The floor is gone; what remains is the
rule that already worked — at least two words that are not filler, and FILLER holds the
rank words, so `Finding 1 - highest` is a rank rather than a reason and still fails.
Seven cases tested both ways, all correct, including one that now fails for a better
reason than expected (no clause break at all).

Scoring that row is also proportional now. One terse line used to cost half the row and
make the student's own format check unreachable, which is a cliff of exactly the kind
this material keeps producing.

**Lab 6 — the clause rule.** `occurs_asserted` treated any negation in the sentence as
governing the fact, so `Avoid tabs and use 4 spaces` read as a ban on 4 spaces. A
negation now governs only its own clause, with a comma, a spaced dash, or a coordinating
conjunction ending it. The severe case still fails correctly:
`Run the tests with nosetests, not python3 -m pytest -q` does **not** count as keeping
the pytest fact, which is the lab's headline trap resolved the wrong way.

Two real bugs surfaced doing it. The double-negative guard was dead code — `neg.end()`
pointed past a 30-character lookbehind tail, so the string it searched was always empty —
and the first repair attempt doubled its backslashes inside an `r"..."` literal, turning
`` into a literal backslash and silently disabling every word boundary. Both are now
covered by the eight-case test.

**Stale bytecode.** Four `__pycache__` directories were tracked, one of them shipping a
`.pyc` older than the `.py` it shadowed, in the student-facing tree. Removed and ignored.

### Left open, deliberately

The remaining items are vocabulary arguments rather than defects — `no longer` accepting
hygiene prose, `left` matching "left the key in .env", a `terminat` adjacency firing on
credential termination. Each could be patched and each patch would reopen something else.

**The real recommendation is a design change, not another patch.** Labs 5 and 6 score
prose that a facilitator reads anyway. Their rubrics already say the written account is
facilitator-judged. These keyword rows should report rather than score — print what they
found and let the human decide — which is what the Lab 2 evidence rows already say about
themselves. That is a course-owner decision, so it is recorded here rather than taken.

---

## Pass 5 — the first LIVE run, and a lab that could not have worked (2026-11-14)

Everything before this was static. This pass ran the real commands against Claude Code
2.1.322 for **$0.20 total**, and found the worst defect in the repository — one no amount
of reading the scorer would have caught.

### Lab 2's eval suite could not pass, as shipped

Five of the six cases grade `RELEASE_NOTES.md` on disk, or ask Claude to create it.
Every one of them granted `allowed_tools: [Read, Glob, Grep(, Skill, Agent)]` — **no
`Write`**. The file is never created, so the graders that read it cannot pass, and the
PostToolUse hook the suite exists to exercise never fires.

`hook-lints-bad-notes` is the clearest: its prompt says *"Create a file named
RELEASE_NOTES.md"* and it grants `[Read, Glob, Grep]`.

This is not a planted trap. The facilitator note lists the traps and this is not among
them. Lab 2 is 75 minutes and the eval suite is its final step.

**And the grant is needed twice.** `Write`, `Bash` and `Edit` are gated at the runner as
well as declared per case, so the command line needs `--allow-tools` too. The lab's hint
did not have it. Measured, same case, same plugin, one flag apart:

```
--allow-tools Write   ->  score 1.00   hook-lints-bad-notes  100%  $0.06
(no grant)            ->  score 0.00   "pattern not found in trace"  $0.14
```

Every student would have seen 0.00 and concluded their plugin was broken.

Fixed: the five cases that need them now declare `Write`, and `Bash` where the command
reads the git log. `ignores-unrelated` deliberately still has no `Write` — its grader
asserts the file is *absent*, so granting it would weaken the one case that was correct.
The lab's hint, its troubleshooting row and its facilitator note all now carry the flag.

### Answered, by running it

The lab said: *"Unconfirmed: whether the stderr of an exit-2 PostToolUse hook is fed to
Claude. The `hook-lints-bad-notes` case exists to find out, so rehearse it."*

It does. `✓ hook-message-reached-claude (weight 1): matched RELNOTES-LINT`, score 1.00.
That is the documented behaviour confirmed in practice, for six cents.

### `claude plugin validate` scored a correct student zero

Real output has two halves: the plugin's own result, then a `Plugin directory checks
for ...` section about submitting to the public catalog, which reports missing README,
LICENSE and icon as `✘ Found 2 problems the plugin directory refuses a submission for`.
**The lab's own answer key reports them.** The tool itself closes that section with
*"These plugin directory checks do not change the result below."*

The evidence row rejected any block containing the word `fail` — and that section
contains the sentence *"To fail on problems the directory refuses a submission for..."*.
So pasting genuine, correct output scored **0 of 8**.

The row now splits the block at `Plugin directory checks for` and looks for
`Found N errors` in the first half only, which is what a genuinely broken manifest
prints there (`✘ Found 4 errors:`). Exit status is 0 in both cases and cannot be used.
Three-way tested: real good output 8/8, real broken-plugin output 0/8, and the
fabricated "it all failed" evidence from pass 3 still 0/8.

Step 1 now warns students about the two halves, because every one of them will see that
`✘`.

### Still needs the class machine

`bwrap` and `socat` do not exist on Windows, so **Lab 3's sandbox half and Lab 4's
configuration 03 cannot be exercised here at all**. Those need an RVC instance, and they
are the largest remaining untested surface.

---

## Pass 6 — the first RVC Phase 0, and two bugs in my own script (2026-11-14)

A session on the real class image ran Phase 0. **The image is in better shape than
expected:** Ubuntu 26.04.1, Claude Code 2.1.311 at `/usr/bin/claude`, and `jq`,
`bwrap` and `socat` all already installed, with passwordless sudo. `check_env.sh` reports
every required item present, so nothing needs provisioning this week. `smoke.py` reported
OK and `check_refs.py` resolved all 53 references.

Both defects it found were in `classroom-sandbox.sh`, which I wrote.

### 6.1 `--check` crashed with `FILES: unbound variable`

Porting the script from the sister course, I replaced `$0` in its messages with
`bash $FILES/setup/classroom-sandbox.sh`. `$FILES` is a **convention in the lab text**,
not an exported variable, and the script runs under `set -u` — so any message containing
it aborts.

Run exactly as the brief writes it, `--check` died at line 66 with
`FILES: unbound variable` and exit 1, swallowing the line that tells the student how to
switch the sandbox on. `--on` would have hit the same thing on its "Undo with" line
*after succeeding*, so a working run would have looked like a failure.

Messages now use `$0`, which is always defined and shows the path actually invoked. Three
expansions replaced; the header comments keep `$FILES` because the usage text is printed
literally by `sed` and never expanded. Verified on real Linux with `FILES` unset,
including the ACTIVE branch that crashed, by pointing `PROFILE` at a fixture and forcing
`loaded()` true: full message, correct path, exit 0.

### 6.2 `--check` could hang on a password prompt

Found while testing the fix. `--check` advertises *"changes nothing, no sudo"* but calls
`sudo aa-status`. On RVC sudo is passwordless so it never showed; on any machine where
sudo prompts, `--check` sits waiting for a password. It timed out at 120 seconds under
test.

Read-only probing now uses `sudo -n`, which fails immediately instead of waiting. The
profile-file test above it already answers the question where `aa-status` is unavailable.

### What this says about the method

Both bugs were in the one file no scorer covers and `smoke.py` cannot see — it tests
scorers, not setup scripts. Neither would have surfaced without someone running the
documented command on a real machine, which is the entire argument for the RVC pass.

---

## Pass 7 — the full RVC run, and the two labs that failed (2026-11-15)

A session ran all six labs and all ten demos on the class image, end to end, for about
**$2.40**. Two labs failed, three demos failed, and the thing the run existed for did not
happen: **the sandbox was never switched on.** `bwrap-userns-restrict` stayed active and
`classroom-sandbox.sh --on` was never run, so Labs 3 and 4 and Demos 3 and 9 are *still*
unobserved live. Everything sandbox-related below is the fallback path.

### Fixed here

**Lab 4 config 03 was missing `allowUnsandboxedCommands: false`** — the most important
finding in the run, because it is a teaching defect rather than a scoring one. When the
sandbox cannot start, the model retries the same command with
`dangerouslyDisableSandbox: true`. Headless, the retry was denied. **With a matching
allow rule it ran unsandboxed with no prompt at all.** Interactively, a student is asked
to approve precisely the escape the payload needs, and approving it defeats the control
they are testing. The key is in the config now, and the Context explains why it is there
and says that seeing the prompt *is* the finding.

**Lab 2's eval hint was still incomplete.** Pass 5 added `--allow-tools Write Bash` and
that held on Linux (1.00 with the grant, 0.00 without, reconfirmed). But four of the six
cases build a git repository to read, and without `--scaffold` they run in an empty
workspace and score about 0.33. The hint now carries `--scaffold`, `--trust-plugin` (a
non-interactive run otherwise stops to ask about trusting the directory) and
`--no-publish` — because **`plugin eval` publishes its HTML report to claude.ai by
default**, which students should decide about before running, not after.

**`demos.md` was stale, and that was my miss.** Pass 2 corrected the AppArmor claim in
`demos/demo-9-*.md` but not the printable copy, which still said the profile is "off by
default" — the opposite of the class image, in the document an instructor teaches from.
Rather than patch it again, `demos.md` is now **generated** from `demos/` by
`testing/build_demos_md.py`, with a `--check` mode that fails when it is stale. Two
hand-maintained copies of the same text is a defect generator; one source is not.

### Open, and needing a decision

- **The sandbox, still.** Until an operator runs `--on` before a session, Labs 3 and 4
  and Demos 3 and 9 have never been seen working. Top blocker, and not a code change.
- **Lab 4's record sheet now exists** (`testing/results/lab4-record/` on the class
  machine) — the first answer key that lab has ever had. Moving it into
  `demo-files/facilitator/` is a human's call and has not been done.
- **The payload never fired in 8 runs** on `claude-opus-5-5`: every row is "stopped by
  the model", so no row exercises a control. The lab should ship the recorded firing
  transcript its facilitator note asks for, and tell students an all-model sheet is the
  likely result.
- **Demos 6, 7 and 8 fail.** A hook with `"args": []` and an inner-quoted path gives
  `ENOENT posix_spawn`; the `-s local` plugin install does not carry into Demo 7's
  scratch repo; Demo 8 needs the same eval flags as Lab 2.
- **Lab 1, live:** started from `ledgerlite/src`, the project's settings did not apply,
  so the hook never ran and the recursive force delete executed. `$CLAUDE_PROJECT_DIR`
  does not cover starting in a subfolder. Needs a re-test before the text changes.
- Smaller scorer items in every lab, listed in the run's own results files.
