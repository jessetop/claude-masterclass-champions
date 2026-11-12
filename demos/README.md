# AI Champions Training: Claude Code for Engineering Teams. Demos

**Course:** AI Champions Training: Claude Code for Engineering Teams (Governance, Hooks, Plugins, and Secure Environments), two days, ROI Training
**Contents:** 10 instructor-led demos. Each takes 15 minutes or less and has a learning objective. The numbers and titles match the Today's Demos slide.

---

## About this guide

Run the demos in the order of the chapters. Each has the same layout: a learning objective, a time, a Files line, a short context paragraph, steps, an Expected result, an Instructor note, a fallback where the demo needs a live model or administrator rights, and a Why this matters note.

In this guide `$FILES` means the `demo-files` folder. Students run the course on Linux class machines. Instructors may demo from a Windows or macOS laptop, so each Instructor note gives the Windows and macOS differences for file paths and administrator rights. The managed file paths are:

| System | Managed settings file | Managed MCP file |
|---|---|---|
| Linux and WSL | `/etc/claude-code/managed-settings.json` | `/etc/claude-code/managed-mcp.json` |
| macOS | `/Library/Application Support/ClaudeCode/managed-settings.json` | `/Library/Application Support/ClaudeCode/managed-mcp.json` |
| Windows | `C:\Program Files\ClaudeCode\managed-settings.json` | `C:\Program Files\ClaudeCode\managed-mcp.json` |

Writing any of these needs root or administrator rights. The older Windows path `C:\ProgramData\ClaudeCode\managed-settings.json` is not read.

Demos 1 to 10 use no organization-level administrative feature. Anything that lives in an administrator console is lecture only.

Claude Code can word things differently each time. Check results against the Expected result and not against exact text. Demos that use a live model (1, 2, 3, 4, 6, 7, 8, 9) spend usage on the instructor's seat. Demos 5 and 10 need no model call to make their main point. Every person, company and value in the files is fictional, and every planted secret is a placeholder such as `FAKE-TOKEN-DO-NOT-USE`.

> **Unconfirmed items.** Each Instructor note says what is unconfirmed or needs rehearsal. If an item is marked unconfirmed, say so to the class. Do not present it as fact. Rehearse every demo once on the machine you will teach from, and recheck the model names the day before class.

> **Cleanup.** Demos 2 and 5 write a file as root or administrator. Run the matching remove script when you finish, and check with `claude mcp list` and `/status` that nothing is left on the machine.

---

---

## The demos

- **[Demo 1: Intake: One Use Case, One Tier](demo-1-intake-one-use-case-one-tier.md)**
- **[Demo 2: Who Wins? Managed Over Project](demo-2-who-wins-managed-over-project.md)**
- **[Demo 3: Rule Versus Request](demo-3-rule-versus-request.md)**
- **[Demo 4: Exit 1 Versus Exit 2](demo-4-exit-1-versus-exit-2.md)**
- **[Demo 5: A Fixed MCP Set](demo-5-a-fixed-mcp-set.md)**
- **[Demo 6: Prove It: A Logging Hook](demo-6-prove-it-a-logging-hook.md)**
- **[Demo 7: Install a Plugin From a Marketplace](demo-7-install-a-plugin-from-a-marketplace.md)**
- **[Demo 8: Evaluate a Plugin With a Test Suite](demo-8-evaluate-a-plugin-with-a-test-suite.md)**
- **[Demo 9: Block a Write and a Network Call](demo-9-block-a-write-and-a-network-call.md)**
- **[Demo 10: Find the Credential Smells](demo-10-find-the-credential-smells.md)**

---

**Related:** the [labs guide](../labs/README.md) holds the 6 labs for this course. A single printable copy of every demo is at [`../demos.md`](../demos.md).
