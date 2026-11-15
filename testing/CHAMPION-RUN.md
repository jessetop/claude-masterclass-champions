# Claude Champion test run 5 — the pre-teach rehearsal

**This is your brief.** Read **[`HANDOFF.md`](HANDOFF.md)** for the rules, the verdict
vocabulary and the logging format. It governs everything below.

Four runs have tested this course. Nothing in it is known broken: all six labs have
answer keys, `smoke.py` reports no WARN, and the scorers have been probed in both
directions. **This run is not a re-test.** It is the rehearsal on the seat the course
will actually be taught from, and it exists to close five specific questions.

The course is taught next week. If you can only finish part of this, do sections 2 and 3
and report — they are the ones that matter.

---

## 0. First, pull

```bash
cd ~/Desktop/claude-masterclass-champions   # or wherever you cloned it
git pull        # you want b9021f7 or later
git log --oneline -1
python3 testing/smoke.py
```

If `smoke.py` reports NOT OK, stop and report that before anything else — a broken scorer
makes every other result meaningless. It should print `ok` for all six labs.

---

## 1. Get the sandbox live, and prove it

Everything below needs a working sandbox. Do this exactly as a student would, from the
lab text, not from memory.

```bash
bash $FILES/setup/classroom-sandbox.sh --check     # changes nothing
bash $FILES/setup/classroom-sandbox.sh --on        # needs sudo
bash $FILES/setup/classroom-sandbox.sh --check
```

`--check` must report **both** controls clear: the AppArmor profile `clear` **and**
`kernel.apparmor_restrict_unprivileged_userns` **0**. One without the other means
commands run **unsandboxed**, which is the worst of the four states.

**Then prove it for real, because `--check` only reads two files.** In a session, ask
Claude to run `touch ~/sandbox-probe`. It must **fail** with a read-only filesystem
error. If it succeeds, you are not sandboxed — say so and stop; sections 2 and 3 cannot
be run and nothing you measure in them would mean anything.

**Also answer this, because it changes the advice to students:** is this seat inside a
container? `systemd-detect-virt` and `cat /proc/1/cgroup` will tell you. If bubblewrap
fails with `Operation not permitted` rather than working, that is the container case, and
the fix is not in the lab text.

Run `--off` when the whole run is finished, and confirm with `--check`.

---

## 2. Lab 3 Part B, live

Run 3 scored this 100/100 on a working sandbox. **The only question is whether this seat
behaves the same.** Work through Lab 3 as a student: apply the settings, run
`attack_simulation.py`, score it.

Three things to watch, each of which is currently written in the lab as unconfirmed:

- **Attempt 2 may read `BLOCKED` with a DNS failure.** That counts — the proxy refuses the
  name before any connection. Confirm it is a DNS error and not a missing-internet error;
  the script prints `NOT REACHABLE` in the second case.
- **Relative paths in `sandbox.filesystem`.** The answer key uses `.` and
  `./config/secrets.env`. If those do not take effect, say so and report whether absolute
  paths fix it. This is in the lab as a fallback and it would be good to delete the
  hedge.
- **`sandbox.excludedCommands`.** The entry format is unconfirmed and the checker passes
  an empty or absent list. If you can establish the format from a real settings file that
  loads without error, that closes it.

Report the Part B score and which attempts blocked.

---

## 3. Lab 4 config 03, live — and the one thing nobody has ever seen

Two questions here. The second needs a human-style interactive session and is the reason
this section exists.

### 3a. Does loopback survive the sandbox network proxy?

Lab 4's canary listener sits on `127.0.0.1:8765`, and configuration 03 allows only
`pypi.org`. **Nobody has confirmed what the proxy does with loopback.** Start the listener
as the lab says, apply configuration 03, and from inside a sandboxed session try to reach
it. If the proxy lets loopback through, configuration 03 would show a network canary hit
and the lab's expected progression is wrong — that is a real finding, not a bug to route
around.

Do **not** edit the payloads. The payload itself will not fire; that is settled across 30
runs and is not what you are testing.

### 3b. What the escape dialog actually shows

This is the only genuinely unobserved thing left in the whole course, and it needs an
**interactive** session — `claude`, not `claude -p`. Headless auto-denies, which is why
four runs have missed it.

Make a copy of `03_sandbox_network.json` with `allowUnsandboxedCommands` **removed** (the
shipped config sets it to `false` deliberately — do not change the shipped file). Apply
the copy, then in an interactive session ask Claude to run a command that needs the
network to a host *not* on the allowlist, so the sandbox refuses and it retries with the
escape.

**Capture what the approval dialog looks like.** A screenshot is ideal; a careful
transcription is fine. What matters:

- Does the dialog show `dangerouslyDisableSandbox` anywhere a student would see it, or is
  the request indistinguishable from an ordinary Bash approval?
- Are you asked **twice** for near-identical commands? Run 4 saw that headlessly.
- What exactly distinguishes the escape request from the first one on screen?

**Never approve it.** Press no. Being asked is the finding, and the answer tells us
whether Lab 4 step 3's hint is teachable or whether the student has no way to tell the two
requests apart.

Write this to `testing/results/run5-escape-dialog.md`.

---

## 4. Two cheap ones, no sandbox needed

- **Lab 6:** do command descriptions count toward a plugin's projected token cost the same
  way skill descriptions do? `claude plugin details` on the lab's plugin, with and without
  the commands, settles it. The lab currently marks this unconfirmed.
- **Lab 4's key:** `python3 $FILES/lab4-injection/check_record.py $FILES/facilitator/lab4/solution-record-sheet.csv`
  must print 65/65 on this machine too. One command; it guards against a line-ending or
  locale difference.

---

## 5. Not for this run

Runs 1 to 4 covered these and repeating them spends model requests for nothing: all six
labs end to end, every scorer probe, Demos 1 to 10, Phase 0 provisioning, and any attempt
to make the Lab 4 payload fire. The image has `jq`, `bwrap`, `socat` and passwordless
sudo.

---

## 6. Logging

Write to `testing/results/run5-*.md` so earlier runs' files survive untouched. Keep
`00-INDEX.md` current. Finish with `testing/results/99-summary-run5.md`: the sandbox state
you achieved, Lab 3 Part B's score, what loopback did, what the escape dialog showed, the
two cheap answers, and anything you could not do and why.

**Two standing rules.** Do not edit a lab, demo or scorer — report it. And if your own
permission layer refuses a command, say so in the log and take the fallback rather than
working around it. That has mattered in every run so far, and it is a finding about the
harness rather than an obstacle to route around.
