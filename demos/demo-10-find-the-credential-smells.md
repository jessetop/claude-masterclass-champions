# Demo 10: Find the Credential Smells

**Course:** AI Champions Training: Claude Code for Engineering Teams

> Part of **[AI Champions Training: Demos](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites and cost notes before you start.

---

**Learning objective:** Spot the common credential smells in a small project, and say for each who owns it, how long it lives and how it is rotated. Time: about 10 minutes.

**Files:** `$FILES/demo10-credential-smells`: `lakeside-api/` (a fictional project), `smell_scan.py`.

**Context:** The project holds a key in a settings file, a key helper that only echoes a fixed value, an `.env` file with no deny rule, a shared-sounding CI secret, an inventory row with no expiry, and a token set in a script. All values are placeholders. A scan finds patterns, and it cannot tell you who owns a credential.

**Steps:**

1. Open `lakeside-api/.claude/settings.json`, `.claude/token.sh`, `.github/workflows/summary.yml`, `scripts/nightly.sh` and `ops/credentials.csv`. For 3 minutes, ask the class to call each smell as you open a file.
2. Run the scan: `python3 smell_scan.py lakeside-api`. Compare its list with the class's list.
3. Ask what the scan cannot see. (Who owns `ORG_WIDE_CLAUDE_KEY`, whether `t.brandt` still works here, whether anything was ever rotated.)
4. For the top two smells, say the fix and the rotation step aloud.
5. Show where your own login is stored without opening it. On Linux: `ls -l ~/.claude/.credentials.json` (mode `-rw-------`). Run `/status` to see which credential is active.
6. Close with the three kinds of credential for automation: a personal token (tied to a person), a shared key (tied to nobody and everybody), and a federated or service identity (tied to a role the team owns).

**Expected result:** The class finds most smells by eye. The scan finds the patterns and misses the ownership problems, which only a person reading the inventory can see.

**Instructor note:** No model call and no administrator rights are needed. Facts for step 5: on Linux the credentials are stored in `~/.claude/.credentials.json` with mode 0600; on macOS they are in the Keychain (and fall back to the same file when the Keychain is locked); on Windows they are in `%USERPROFILE%\.claude\.credentials.json`. Never open or display that file. If `ANTHROPIC_API_KEY` is set alongside a login, Claude Code can use the key once it is approved, which is why `/status` matters. A long-lived token from `claude setup-token` is a one-year token, per the docs read, and it can only make model requests. The details of federation setup are not in the docs read, so keep that to a sentence and mark it as unconfirmed. Windows: run `python smell_scan.py lakeside-api`. macOS: no differences. Fallback (no machine): the five files and the scan output on a slide.

**Why this matters:** Credentials are where most real incidents start. A named owner, a lifetime and a rotation step turn a secret into something a team manages. Without them, it is a leak that has not been found yet.
