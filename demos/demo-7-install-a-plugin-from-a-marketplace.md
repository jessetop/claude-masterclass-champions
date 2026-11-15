# Demo 7: Install a Plugin From a Marketplace

**Course:** AI Champions Training: Claude Code for Engineering Teams

> Part of **[AI Champions Training: Demos](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites and cost notes before you start.

---

**Learning objective:** Add a marketplace, review a plugin before trusting it, install it, and use its command and its hook. Time: about 10 minutes.

**Files:** `$FILES/demo7-marketplace/champions-tools` (a marketplace with one plugin, `branch-guard`). Review aid: `$FILES/templates/plugin-review.md`.

**Context:** A marketplace is a folder (or a git repository) with `.claude-plugin/marketplace.json`. `branch-guard` bundles a command and a PreToolUse hook that blocks force pushes and pushes to `main`. A plugin's hooks and servers run with the user's rights, outside the sandbox, so review before you install. Plugin components are namespaced `plugin:component`.

**Steps:**

1. Add the marketplace from the local folder: `claude plugin marketplace add $FILES/demo7-marketplace/champions-tools`, then `claude plugin marketplace list`. Say where a team marketplace would come from instead: a git repository (`owner/repo` or a git URL).
2. Review before you trust. Open `plugins/branch-guard/hooks/hooks.json` and `scripts/block_force_push.py`. Then list the contents: `claude --plugin-dir $FILES/demo7-marketplace/champions-tools/plugins/branch-guard plugin details branch-guard`. Read the component inventory and the projected token cost.
3. Install it for yourself only: `claude plugin install branch-guard -s local`.

   > **Create the Step 4 scratch repository first, and install from inside it.** `-s local` applies only in the folder you install from, so installing here and then moving to a new folder in Step 4 leaves the plugin unavailable — which is what happened on the class image. Either make the scratch repo before this step and run the install there, or use `-s user` so it follows you. **Give that scratch repo a `main` branch and a dummy remote** — measured 2026-11-15, the model declines to push to a repository with neither, so the hook never gets the chance to block anything.
4. In a scratch repository (`git init`, one commit), start `claude`. Run `/reload-plugins` if the plugin does not show. Run `/branch-guard:branch-status`.
5. Ask: `Run git push --force origin main`. The hook blocks it, and the message starts with `BRANCH-GUARD`.
6. Uninstall and remove: `claude plugin uninstall branch-guard -s local` and `claude plugin marketplace remove champions-tools`. **The scope flag is needed**: a bare `uninstall` assumes user scope and fails to find a local-scope install.

**Expected result:** The command reports the branch and the working tree state. The force push is blocked by the plugin's hook and Claude relays the reason.

**Instructor note:** `claude plugin install <plugin>` takes a scope with `-s user|project|local`. If the name is ambiguous or not found, the one-command form `claude plugin install branch-guard --marketplace <path>` adds the marketplace and installs together (needs a recent version). The `plugin@marketplace` name form is not in the docs read, so treat it as unconfirmed. Windows: use backslash paths, or run in Git Bash. The hook uses `python3`, so edit `hooks.json` to `python` if that is all your laptop has. macOS: no differences. No administrator rights are needed for a user or local scope install. Unconfirmed: whether `/reload-plugins` is enough on your version or you must restart `claude`. Fallback (no marketplace step, or a failed install): load the plugin for one session with `claude --plugin-dir $FILES/demo7-marketplace/champions-tools/plugins/branch-guard` and run steps 4 and 5. Keep a transcript outline: marketplace added, details read, installed, command output, blocked push.

**Why this matters:** A plugin is the unit a team ships and updates. It is also code with the user's rights. A marketplace gives one place to review, and the review must happen before the install, because the install is the trust decision.
