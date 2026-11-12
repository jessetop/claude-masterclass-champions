# Demo 9: Block a Write and a Network Call

**Course:** AI Champions Training: Claude Code for Engineering Teams

> Part of **[AI Champions Training: Demos](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites and cost notes before you start.

---

**Learning objective:** Show an operating-system sandbox block a write outside the working directory and a call to a domain that is not allowed, and show what fail-closed means. Time: about 12 minutes.

**Files:** `$FILES/demo9-sandbox`: `configs/`, `apply.sh`, `project/probe.sh`. Environment check: `$FILES/setup/check_env.sh`.

**Context:** The sandbox covers shell commands and their child processes. Claude's file tools, MCP servers and hooks run outside it. On Linux and WSL2 it needs `bubblewrap` and `socat`. Ubuntu 24.04 and later can block bubblewrap through an AppArmor setting. It is off by default. With `sandbox.failIfUnavailable` set to true, Claude Code exits at startup if the sandbox cannot start. By default it runs commands unsandboxed when the sandbox is unavailable.

**Steps:**

1. On the demo machine run `bash $FILES/setup/check_env.sh`. Show the `bubblewrap` and `socat` lines and the AppArmor line.
2. Sandbox off: `cd $FILES/demo9-sandbox && bash apply.sh off`, then `cd project && claude`. Ask: `Run bash probe.sh`. Probes 1, 2 and 3 report SUCCEEDED, and probe 4 gets a response.
3. Sandbox on: exit, run `bash ../apply.sh on`, and restart `claude`. Open `/sandbox` to show the panel. Ask for the probe again. Probes 1, 2 and 3 report BLOCKED. Probe 4 (an allowed domain) still gets a response.
4. Show the one-line check the class will use: ask Claude to run `touch ~/sandbox-probe`. With the sandbox working it fails with "Read-only file system".
5. Fail closed: on a second machine or snapshot with `bubblewrap` removed, show two starts. With `apply.sh on`, Claude Code runs commands unsandboxed (the default). With `apply.sh fail-closed`, it exits at startup.
6. Say what the sandbox does not cover: hooks, MCP servers and plugin processes, and Claude's own file tools.

**Expected result:** The probes flip from SUCCEEDED to BLOCKED when the sandbox is on, the allowed domain still answers, and a missing sandbox is a hard failure only when `failIfUnavailable` is true.

**Instructor note:** Windows: native Windows is not sandboxed, so run this demo from WSL2, a Linux VM or a Mac. macOS: the sandbox runs on macOS and needs no install, but the exact failure message for the `~/sandbox-probe` write is stated only for Linux and WSL2, so check what yours says. Linux: install with `sudo apt-get install bubblewrap socat` (Debian and Ubuntu) or `sudo dnf install bubblewrap socat` (Fedora and RHEL), and restart Claude Code, because the check runs at startup. On Ubuntu 24.04 and later, check `sysctl kernel.apparmor_restrict_unprivileged_userns` (1 means restricted) and add an AppArmor profile for `/usr/bin/bwrap` as the docs describe. Inside a container bubblewrap can fail with "Operation not permitted", and `sandbox.enableWeakerNestedSandbox` weakens isolation, so do not use it for this demo. Unconfirmed: the container fix steps, and whether a typical Linux VM works without changes (the docs state only the dependency and user namespace requirements). If your machine has no internet, probe 3 reads BLOCKED for the wrong reason: run the `curl` from a normal terminal first. Fallback (no sandbox support on the machine): screenshots of both probe runs and of the fail-closed exit from your rehearsal.

**Why this matters:** A sandbox is the layer that still holds when a rule is missing or the model is persuaded. Fail-closed turns a quiet loss of protection into a loud stop. Knowing what the sandbox does not cover is what keeps the team from over-trusting it.
