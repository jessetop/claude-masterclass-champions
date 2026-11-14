# Rehearsal checklist — before you teach

Every item the course marks unconfirmed or needs-rehearsal, gathered from all six labs
and all ten demos into one list. Work through it on **the exact machine you will teach
from**, because most of these differ by operating system or by Claude Code version.

The course convention is that an unconfirmed item is said aloud as unconfirmed. This
page exists so you know which ones those are before a student finds them for you.

---

## Do this first, or the sandbox demos fail in the room

**Ubuntu 24.04 and later ship the `bwrap-userns-restrict` AppArmor profile loaded and
enforcing, and it stops the Claude Code sandbox starting.** This is the single most
likely thing to break, and it affects **Demo 3 step 5, Demo 9 in full, Lab 3 and Lab 4
configuration 03**.

```bash
bash demo-files/setup/check_env.sh                      # reports the profile, not the sysctl
bash demo-files/setup/classroom-sandbox.sh --check
bash demo-files/setup/classroom-sandbox.sh --on         # needs sudo; --off afterwards
```

Two things that look like fixes and are not, both tested on a class image: relaxing
`kernel.apparmor_restrict_unprivileged_userns` does nothing, because the profile stays
loaded and carries `audit deny capability`; and a profile naming a binary does not work,
because the denial is raised inside `unpriv_bwrap`, which `/usr/bin/bwrap` transitions
*into*. Disabling the profile is what works, and it is machine-wide — Lab 3 Step 1 frames
it for students as a decision rather than a fix, and you should frame it the same way.

**Know which failure you are looking at.** With `bubblewrap` missing, `failIfUnavailable:
true` makes Claude Code exit at startup — that is Demo 9 step 5. With `bubblewrap`
installed but AppArmor blocking it, the startup check passes, the session starts
normally, and every shell command is refused at run time with `apply-seccomp: ...
Permission denied`. The two look nothing alike and students hit the second one.

---

## Settled — do not re-litigate these

Checked against the documentation and recorded in `testing/FIXES-APPLIED.md`.

| Claim | Status |
|---|---|
| Exit 2 blocks a `PreToolUse` call; exit 1 does not | **Confirmed.** "The message that comes with the block is your hook's stderr" |
| A `PostToolUse` hook that exits 2 cannot block, but its stderr reaches Claude | **Confirmed.** Per-event table: `PostToolUse / No / Shows stderr to Claude; the tool already ran` |
| Managed settings beat project settings | **Confirmed.** "highest first: managed settings, command line, project local, shared project, user" |
| `--settings` outranks the project file but cannot override a managed file | **Confirmed**, same sentence |
| `claude setup-token` produces a one-year token, used through `CLAUDE_CODE_OAUTH_TOKEN` | **Confirmed** |
| Credentials: macOS Keychain, Linux `~/.claude/.credentials.json` mode 0600 | **Confirmed** |

Two refinements worth knowing if a student asks, neither of which changes any lab: a hook
that exits 1 but prints valid JSON can still decide the outcome through that JSON, and a
hook configured with `onFailure: "block"` blocks when it fails.

---

## Still unconfirmed, by session

Rehearse each once and note what your version did.

### Demos

| Demo | What to check |
|---|---|
| 2 | The exact text `/model` shows for a pinned model, and whether `/model` or `/status` reads more clearly. Use whichever is clearer |
| 3 | Whether `cat .env` in step 4 is stopped under configuration B alone. The path form for `sandbox.filesystem.denyRead` entries — `apply_config.sh` writes an absolute path to be safe |
| 4 | Whether the non-blocking-error notice shows the first line of stderr as described on your version |
| 5 | That `${NOTES_TOKEN}` expands inside an `env` value on your version. If the server sees no token, show the `headersHelper` or per-user header route instead |
| 6 | That hooks inherit your shell's environment. Leave `CLAUDE_TOOL_LOG` unset and use the default `~/claude-tool-calls.log` |
| 7 | The `plugin@marketplace` name form. Whether `/reload-plugins` is enough or you must restart `claude` |
| 8 | Whether a `case.yaml` path is accepted as the eval target, and whether a case needs `--allow-tools Bash` |
| 9 | The container fix steps, and whether a plain Linux VM works unchanged |
| 10 | Federation setup details are not in the documentation read — keep it to a sentence and mark it unconfirmed |

### Labs

| Lab | What to check |
|---|---|
| 1 | Whether a `Read` deny also stops `cat .env` in the shell. It should not — deny rules cover Claude's file tools, shell reads need the sandbox — and the charter note should say so. Shares its answer with Demo 3 |
| 2 | Whether a plugin agent honors `permissionMode`; the linter reports it as WARN only. Run the `hook-lints-bad-notes` eval case once |
| 3 | The entry format of `sandbox.excludedCommands`. How a relative path in `sandbox.filesystem` resolves — the answer key uses `.` and `./config/secrets.env`; switch to absolute paths if that fails on your image. Rehearse the whole lab on the class image |
| 4 | How loopback traffic to the listener behaves under the sandbox network proxy. If the proxy lets loopback through, configuration 03 shows a hit: either pick another canary host with `set_canary_host.sh` or teach that result as the lesson |
| 5 | Nothing product-dependent. Students mark the federation part unconfirmed themselves |
| 6 | Whether command descriptions count toward a plugin's projected cost the way skill descriptions do |

---

## Cost, before you run anything

Labs 2 and 4 and Demos 1, 2, 3, 4, 6, 7, 8 and 9 spend model requests on the seat that
runs them. Labs 1, 5 and 6 and Demos 5 and 10 need almost none.

Check your own shell before rehearsing: if `ANTHROPIC_API_KEY` is set it is used in
preference to your sign-in, and the rehearsal bills against that key.

```bash
echo $ANTHROPIC_API_KEY     # if it prints anything: unset ANTHROPIC_API_KEY
```

## Clean up after Demos 2 and 5

Both write a file as root. Each has a matching remove script that restores any file it
backed up:

```bash
sudo bash demo-files/demo2-managed/remove-managed.sh
sudo bash demo-files/demo5-mcp/remove_managed_mcp.sh
claude mcp list        # confirm nothing of the demo's is left
```

And if you ran `classroom-sandbox.sh --on`, run `--off`.
