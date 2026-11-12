# Demo 1: Intake: One Use Case, One Tier

**Course:** AI Champions Training: Claude Code for Engineering Teams

> Part of **[AI Champions Training: Demos](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites and cost notes before you start.

---

**Learning objective:** Run one use case through the ten-section intake checklist and give it a risk tier, and name the single answer that decided the tier. Time: about 12 minutes.

**Files:** `$FILES/demo1-intake/use-case-brief.md`, `$FILES/templates/intake-checklist.md`, `$FILES/templates/risk-tiers.md`. Answer: `$FILES/facilitator/demos/demo1-completed-intake.md`.

**Context:** The intake checklist and the tiers are generic templates. A team replaces them with its own. The brief describes a fictional team that wants Claude Code to draft weekly release notes. Most of the use case is low risk. One data answer and one missing control set the tier.

**Steps:**

1. Show the brief on screen and the blank checklist next to it. Say the ten section names aloud: purpose and owner, data, repositories, tools and servers, model and effort, permissions and sandbox, credentials, review and escalation, logging, exit criteria.
2. In a terminal in `$FILES/demo1-intake`, start `claude` and ask:
   `Read use-case-brief.md and ../templates/intake-checklist.md. Draft an answer for each of the ten sections. Write "Unknown" where the brief is silent. Do not invent facts.`
3. Read Claude's draft with the class. Ask them to find one place where the draft states something the brief does not say.
4. Open `risk-tiers.md`. Ask the class to call out the tier. Take a vote.
5. Ask: which one answer decided the tier? Then ask what single change would lower it.

**Expected result:** The draft fills most sections and marks sections 5, 8, 9 and 10 as Unknown or thin. The class lands on Medium, and names section 2 (a real staging password in the repository folder with nothing stopping Claude Code from reading it) as the deciding answer. Removing or denying that file and blocking `git push` could lower the tier.

**Instructor note:** Nothing here is unconfirmed product behavior. The tiers are an example, and the class may reasonably pick another. What matters is that they name the deciding answer. Windows and macOS: no differences, and no administrator rights are needed. Run `claude` from any folder that holds the files. Fallback (no model or no time): read `$FILES/facilitator/demos/demo1-completed-intake.md` aloud section by section and let the class react, or fill the checklist on a whiteboard.

**Why this matters:** Governance starts with a repeatable question list. Without one, each use case is judged by whoever happens to be in the room. With one, an unknown answer becomes visible, and the team can see which control it is missing.
