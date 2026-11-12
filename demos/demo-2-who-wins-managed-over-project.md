# Demo 2: Who Wins? Managed Over Project

**Course:** AI Champions Training: Claude Code for Engineering Teams

> Part of **[AI Champions Training: Demos](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites and cost notes before you start.

---

**Learning objective:** Show that a managed settings file beats a project settings file, and prove it with behavior, not with a screen that lists files. Time: about 12 minutes.

**Files:** `$FILES/demo2-managed`: `managed-settings.json`, `project/.claude/settings.json`, `install-managed.sh`, `remove-managed.sh`, `install-managed.ps1`, `remove-managed.ps1`.

**Context:** The project file asks for a small model and allows `git push`. The managed file pins a different model and denies `git push` and reading `.env`. The overall order, highest first, is managed settings, command line, project local, shared project, user. A managed file is read at startup and reloaded when it changes.

**Steps:**

1. Show the two files side by side. Point at `model` and `permissions` in each.
2. Prepare the project: `cd $FILES/demo2-managed/project && git init -q && git commit -q --allow-empty -m init`.
3. Before installing the managed file, start `claude` in `project`. Run `/status` and note the `Setting sources` line, then `/model` to see the model in use. It should be the project's choice. Exit.
4. Install the managed file (Linux: `sudo bash ../install-managed.sh`). See the Instructor note for Windows and macOS.
5. Start `claude` in `project` again. Run `/status`. The `Setting sources` line now lists the managed settings file (its label ends in `(file)`). Run `/model`: it should show the pinned model.
6. Ask: `Run git push origin main`. Claude Code should refuse, even though the project settings allow it.
7. Ask: `Show me the contents of .env`. The Read tool should be denied.
8. Say plainly what `/status` proves and what it does not: it lists the files that were read, not which file supplied each key. The behavior in steps 5 to 7 is the proof.
9. Remove the managed file (Linux: `sudo bash ../remove-managed.sh`) and exit.

**Expected result:** With the managed file in place, the model matches the managed file and `git push` is refused despite the project's allow rule. After removal, the project's choices apply again.

**Instructor note:** Linux and WSL: the file goes to `/etc/claude-code/managed-settings.json` and needs `sudo`. macOS: `sudo mkdir -p "/Library/Application Support/ClaudeCode" && sudo cp managed-settings.json "/Library/Application Support/ClaudeCode/managed-settings.json"`; remove it with `sudo rm`. Windows: run `install-managed.ps1` from an elevated PowerShell; the target is `C:\Program Files\ClaudeCode\managed-settings.json`. A `model` change from managed settings applies at the next launch, so restart `claude` after installing. Within the managed tier, only the first source that delivers a key is used, so if your own account also receives server-managed settings, they can shadow the file. Run `claude doctor` before class to check for rejected entries. Unconfirmed: the exact text `/model` shows for a pinned model, and whether `/model` or `/status` is the clearer view. Rehearse and use the one that is clearer. Do not claim that deny rules hold in every permission mode: that is a Demo 3 test, not a fact. Fallback (no administrator rights, or no model): show screenshots from your rehearsal. As a weaker second fallback, start with `claude --settings managed-settings.json` in `project`: the command line also ranks above the project file, but say clearly that this is not a managed file and does not show the file path.

**Why this matters:** A rule that a project can override is a default, not a control. Managed settings are the one place a team can set a floor that a developer's own settings cannot lower.
