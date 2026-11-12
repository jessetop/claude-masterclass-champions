# Lab 6: Context Engineering (take-home)

**Course:** AI Champions Training: Claude Code for Engineering Teams

> Part of **[AI Champions Training: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites and cost notes before you start.

---

**Learning objective:** Measure what loads into the context window at startup, trim a `CLAUDE.md` and a plugin's descriptions, measure again, and write two rules for your team. Time: take-home, no set time.

**Files:** `$FILES/lab6-context`: `shopkit/` (a sample project with a bloated `CLAUDE.md`), `shopkit-plugin/` (a plugin with long descriptions), `original/` and `original-plugin/` (untouched copies for the checker), `measure.csv`, `RULES-LEARNED.md`, `check_lab6.py`.

**Context:** At startup, before you type anything, `CLAUDE.md`, auto memory, MCP tool names and skill descriptions are already in the context window, and each file Claude reads adds to it. `/context` shows a live breakdown by category with suggestions, including which `CLAUDE.md` and memory files loaded. `/memory` opens and edits them. `/compact` replaces the conversation with a summary, and `/clear` starts fresh. Every enabled plugin puts the names and descriptions of its commands, skills and agents in the context window on every turn, and `claude plugin details <name>` prints a projected token cost. A shorter description can stop a command being chosen, so test it after you shorten it. This lab does not quote any size, threshold or limit. For how `CLAUDE.md` files are found and loaded, read the memory documentation (https://code.claude.com/docs/en/memory). For model and context options, read the model configuration documentation (https://code.claude.com/docs/en/model-config). For what fills the window, see https://code.claude.com/docs/en/context-window.

**Steps:**

1. **Measure before (about 10 minutes).** Goal: three numbers recorded.
   - In `$FILES/lab6-context/shopkit`, start `claude` and run `/context`. Record the startup total and the `CLAUDE.md` line in `measure.csv` as the tool shows them (tokens or percent). Then run `claude --plugin-dir ../shopkit-plugin plugin details shopkit-helpers` and record the projected token cost.
   - Hints: copy the numbers exactly as displayed and do not convert them.

2. **Trim `CLAUDE.md` (about 20 minutes).** Goal: a `CLAUDE.md` at least 40 percent shorter that keeps what Claude needs.
   - Acceptance criteria: the five facts that matter survive (the test command, never committing `.env`, integer cents for money, the public API path, and the indentation rule); stale and duplicated instructions are gone; no motivational text remains.
   - Hints: for each line, ask whether Claude would behave differently without it. Two of the instructions contradict each other, and some describe a tool that no longer exists. A rule that must persist belongs in the project-root `CLAUDE.md`.

3. **Trim the plugin (about 15 minutes).** Goal: every command and agent description is short and still says when to use it.
   - Acceptance criteria: each description is 200 characters or fewer (a lab rule of thumb and not a product limit), at least 40 characters, and still names its topic (price, stock, refund, cart).
   - Hints: lead with the job and the trigger, and cut the filler. Test that the commands are still chosen: ask a matching question and an unrelated one in a session with the plugin loaded.

4. **Measure after (about 10 minutes).** Goal: the same three numbers again.
   - Restart `claude`, run `/context`, and run `plugin details` again. Record all three in `measure.csv`.
   - Hints: use the same session setup as in step 1 so that the comparison is fair.

5. **Write two rules (about 10 minutes).** Goal: two rules for your own team in `RULES-LEARNED.md`.
   - Acceptance criteria: exactly two numbered rules, each starting with a verb and ending with a "because" clause that points at something you measured.

6. **Check it.** From `$FILES/lab6-context`, run `python3 check_lab6.py`.

**Checkpoint:** The checker reports at least 85, and `measure.csv` shows a lower number after than before for at least two of the three measurements.

**Common problems:**

- You cut the facts that matter: the checker names the missing ones.
- The numbers did not change: compare like with like. `/context` also counts other files that loaded.
- A description is shorter and the command stopped being chosen: add the trigger back in fewer words.
- You wrote rules with no measurement behind them: change the because clause to what you saw.
- You quote a number from memory in your rules: remove it, or link to the documentation.

**Scoring rubric (100 points, from `check_lab6.py`):**

| Item | Points |
|---|---|
| `CLAUDE.md` at least 40 percent shorter | 15 |
| The five facts that matter are still there | 15 |
| No stale instruction remains | 10 |
| Every description 200 characters or fewer | 12 |
| No description shortened to nothing | 6 |
| Every description still names its topic | 12 |
| `measure.csv` complete | 15 |
| Two rules, each with a because clause | 15 |

An untouched project scores about a third of the points. The checker cannot read `/context` output, so the measurement rows are self-reported, and the facilitator may ask to see a screen.

**Facilitator note:** Remove before sharing. The model answer is `facilitator/lab6/solution/` (a trimmed `CLAUDE.md`, four short descriptions, a sample `measure.csv` and sample rules), and it scores 100. Traps planted: two contradictory test commands (`nosetests` and `python3 -m pytest -q`), the stale Python 2.7, Jenkins and FTP uploader instructions, duplicated rules (indentation, integer cents, `.env`), a file tree and a style guide that Claude can read from the code, motivational filler, and four plugin descriptions of 400 to 500 characters that read as keyword stuffing. Only claim what the verified facts support: the contents of `/context`, `/memory`, `/compact` and `/clear`, that the startup load includes `CLAUDE.md`, memory, MCP tool names and skill descriptions, and that `plugin details` prints a projected token cost. Do not quote token counts, auto-compact thresholds or the `CLAUDE.md` load hierarchy: those are not in the docs read, and the lab links to the memory and model configuration pages instead. Unconfirmed: whether command descriptions count toward the plugin's projected cost in the same way as skill descriptions (the docs read say names and descriptions of skills, agents and commands). Watch for students who shorten a description until the command no longer triggers, and who delete every rule to hit the percentage: the five facts check catches the second.
