# Claude Champion test run 3 — RVC, with the sandbox ACTUALLY on

**This is your brief.** Read **[`HANDOFF.md`](HANDOFF.md)** for the rules, the verdict
vocabulary and the logging format. It governs everything below.

Runs 1 and 2 (2026-11-14/15) tested all six labs and ten demos on this image. **Keep
their result files.** This run is not a repeat: it exists for the one thing neither run
could do.

---

## 0. First, pull

```bash
cd ~/Desktop/claude-masterclass-champions   # or wherever you cloned it
git pull        # you want 4c05db2 or later
git log --oneline -1
```

Run 2 was at `3819968`. Every defect it found is now fixed upstream, including all three
failing demos, so this run confirms those and then does the sandbox work.

---

## 1. The sandbox — the whole reason for this run

**Twice now this has not happened.** Run 2 was told the operator had run `--on`, and
found `--check` reporting ACTIVE, `apparmor_restrict_unprivileged_userns = 1` and the
probe failing with `apply-seccomp`. So **Labs 3 and 4 and Demos 3 and 9 have still never
been observed with a working sandbox**, and every sandbox result so far is fallback.

If the probe shows no sandbox a third time, **stop and report that first** — do not
spend the run re-confirming fallback behaviour that two runs already recorded.

**The operator switches it on before your session starts.** Do not run `--on` yourself.
Your first job is to establish which state you are in and record it:

```bash
bash demo-files/setup/classroom-sandbox.sh --check
python3 testing/smoke.py
```

Then the probe the labs use — inside a Claude Code session in a scratch project, with the
sandbox on, ask it to run `touch ~/sandbox-probe`:

- **It fails with "Read-only file system"** → the sandbox is live. Go to section 2. This
  is the first time anyone has run these labs that way.
- **A command fails with `apply-seccomp ... Permission denied`** → the sandbox is *not* live either. The
  profile is still blocking and every shell call will fail. Treat this exactly like the case below, and say
  so explicitly — run 2 was told `--on` had been run, found `--check` reporting ACTIVE and this error, and
  reporting the discrepancy was the single most useful thing it did.
- **It succeeds** → there is still no sandbox. Say so plainly at the top of your summary,
  take the fallback paths, and **skip section 2** — do not spend the run re-confirming
  what run 1 already recorded.

---

## 2. What only a working sandbox can settle

In priority order. These are the open questions, not whole labs — run 1 covered the rest.

1. **Lab 3 Step 5, live.** Does a correctly hardened configuration actually block
   attempts 1, 2 and 3? Part B is 40 points nobody has ever observed. Run 1 scored 85 on
   the fallback; a working sandbox should make 100 reachable.
2. **Lab 3's open question.** Does `allowUnsandboxedCommands: false` stop an unsandboxed
   retry on a sandbox that *works*? Run 1 showed it holding when the sandbox failed at
   runtime, which is not the same thing.
3. **Lab 4 runs 3 and 8** (`readme` and `tool_result` under configuration 03). Run 1 found
   the model retrying with `dangerouslyDisableSandbox: true`, and in run 8 — with a
   matching allow rule — it **ran unsandboxed with no prompt at all**.
   **Config 03 now carries `allowUnsandboxedCommands: false`.** Confirm the retry is now
   refused. If you are prompted to approve the escape, **that is the finding — record it,
   do not approve it.**
4. **Demo 3 step 5** and **Demo 9 in full**. Both were blocked in run 1.

---

## 3. Confirm the four fixes from run 1

Each came directly from your own findings. Check each and say held or not held.

| Fix | What to check |
|---|---|
| **Lab 2 Step 5 hint** | now has `--scaffold --trust-plugin --no-publish` alongside `--allow-tools Write Bash`. Re-run the suite: do the four scaffolded cases now score properly instead of ~0.33? |
| **Lab 4 config 03** | `allowUnsandboxedCommands: false` is in the file, and the Context explains why. See section 2 item 3 |
| **`demos.md`** | regenerated from `demos/`, so the "off by default" AppArmor line is gone. `python3 testing/build_demos_md.py --check` must say it is current |
| **`classroom-sandbox.sh`** | already confirmed in run 1 — no need to retest |

---

## 4. Confirm the three demo fixes

All three are fixed from run 2's own diagnoses. Perform each and say held or not held.

- **Demo 6** — `"args": []` removed, so the command runs through a shell and the quoted
  path resolves. Does a `tool_call` line now appear in the log? Note run 2's caveat: the
  model often chains `ls && git push` into one call, so the listing is not logged
  separately — the Step 3 prompt may need splitting.
- **Demo 7** — Step 3 now says to create the scratch repo first and install inside it (or
  use `-s user`), and Step 6 uninstalls with `-s local`. Does the corrected flow block the
  force push with `BRANCH-GUARD`?
- **Demo 8** — now carries `--allow-tools Bash --no-publish`, and the note says the Step 1
  lint FAIL is expected because it is a Lab 2 rule firing on the wrong plugin.

---

## 5. Lab 1's subfolder note

Run 2 settled the cause: Claude Code reads project settings from the folder it starts in,
not the git root, so from `src/` the root settings are never read at all. Lab 1 Step 3
now carries that as a note. Just read it and say whether it states the case correctly —
no re-test needed unless you think it is wrong.

---

## 6. Not for this run

Run 1 already covered these. Do not redo them: Labs 5 and 6 end to end, Lab 1 and Lab 2's
scorer probes, Demos 1, 2, 4, 5 and 10, and Phase 0 provisioning — the image has `jq`,
`bwrap`, `socat` and passwordless sudo, and nothing needs installing.

---

## 7. Logging

Write to `testing/results/run2-*.md` so run 1's files survive untouched. Keep
`00-INDEX.md` current.

Finish with `testing/results/99-summary-run2.md`: what the sandbox state was, what a
working sandbox settled, which of the four fixes held, the three demos' diagnoses, and
anything still unobserved. Then run `python3 testing/smoke.py` once more and paste it.

**Two standing rules worth repeating.** Do not edit a lab, demo or scorer — report it.
And if your own permission layer refuses a command, say so in the log and take the
fallback path rather than working around it; that is a finding about the harness and the
operator needs to know.
