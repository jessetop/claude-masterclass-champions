# Claude Champion

**AI Champions Training: Claude Code for Engineering Teams**
*Governance, Hooks, Plugins, and Secure Environments* — two days, ROI Training.

Ten instructor-led demos and six labs. Everything runs on a student's own Linux class
machine with their own Claude Code sign-in. No lab or demo needs access to an
organization, an administrator console, or a shared account, and every score comes from a
script the student runs locally.

---

## Contents

| Path | What it holds |
|---|---|
| **[`labs/`](labs/)** | Six labs, one file each, plus the guide preamble and index in [`labs/README.md`](labs/README.md) |
| **[`demos/`](demos/)** | Ten demos, one file each, plus the preamble and index in [`demos/README.md`](demos/README.md) |
| [`demos.md`](demos.md) | Every demo in one printable document, for teaching from |
| [`demo-files/`](demo-files/) | The assets the labs and demos refer to as `$FILES` |
| [`SETUP.md`](SETUP.md) | Install and sign-in, and the environment check to run before Lab 1 |

In every lab and demo, **`$FILES` means the `demo-files` folder.**

## The labs

| # | Lab | Time |
|---|---|---|
| 1 | [Rule to Control](labs/lab-1-rule-to-control.md) | 30 min |
| 2 | [Build a Plugin With a Hook](labs/lab-2-build-a-plugin-with-a-hook.md) | 75 min |
| 3 | [Harden a Sample Repository](labs/lab-3-harden-a-sample-repository.md) | 90 min |
| 4 | [Prompt Injection Detection](labs/lab-4-prompt-injection-detection.md) | 75 min |
| 5 | [Credential Audit](labs/lab-5-credential-audit-take-home.md) | take-home |
| 6 | [Context Engineering](labs/lab-6-context-engineering-take-home.md) | take-home |

## The demos

| # | Demo | Time |
|---|---|---|
| 1 | [Intake: One Use Case, One Tier](demos/demo-1-intake-one-use-case-one-tier.md) | ~12 min |
| 2 | [Who Wins? Managed Over Project](demos/demo-2-who-wins-managed-over-project.md) | ~12 min |
| 3 | [Rule Versus Request](demos/demo-3-rule-versus-request.md) | ~15 min |
| 4 | [Exit 1 Versus Exit 2](demos/demo-4-exit-1-versus-exit-2.md) | ~10 min |
| 5 | [A Fixed MCP Set](demos/demo-5-a-fixed-mcp-set.md) | ~15 min |
| 6 | [Prove It: A Logging Hook](demos/demo-6-prove-it-a-logging-hook.md) | ~12 min |
| 7 | [Install a Plugin From a Marketplace](demos/demo-7-install-a-plugin-from-a-marketplace.md) | ~10 min |
| 8 | [Evaluate a Plugin With a Test Suite](demos/demo-8-evaluate-a-plugin-with-a-test-suite.md) | ~12 min |
| 9 | [Block a Write and a Network Call](demos/demo-9-block-a-write-and-a-network-call.md) | ~12 min |
| 10 | [Find the Credential Smells](demos/demo-10-find-the-credential-smells.md) | ~10 min |

---

## Before you hand anything to students

Run the pack builder. It copies `demo-files/` and removes the answer keys:

```bash
./demo-files/make-student-pack.sh /path/to/output
./demo-files/make-student-pack.sh --list     # show what would be removed, change nothing
```

It refuses to finish if anything instructor-only survives the prune, so adding a new
answer key and forgetting the list fails loudly rather than shipping it.

**Also strip the Facilitator notes from the lab and demo files you share.** Each lab ends
with one and each demo carries an Instructor note. They name where the traps are planted.

## Conventions

Everything is fictional — every person, company, domain and value. Every planted secret
is an obvious placeholder such as `FAKE-TOKEN-DO-NOT-USE`, and no file holds a real
credential. Claude Code words things differently from run to run, so every lab is scored
against its acceptance criteria rather than against exact output text.

Where a lab or demo depends on product behavior that has not been verified against
current documentation, it says so in place rather than asserting it. Treat an item marked
unconfirmed as unconfirmed when you teach it.
