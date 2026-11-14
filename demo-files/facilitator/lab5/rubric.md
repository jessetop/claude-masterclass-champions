# Lab 5 rubric (100 points) and answer key

Hold back until the audit is submitted. A sample answer is `solution-findings.md`. `score_audit.py` gives a first-pass keyword score, and you read the findings and adjust.

## Planted problems (12 points each: identified 6, location 3, fix 3)

| Id | Problem | Where | Acceptable fix |
|---|---|---|---|
| C1 | A key in a settings file | `repos/billing-service/.claude/settings.json`, `env.ANTHROPIC_API_KEY` | Remove it and rotate it. Supply credentials at run time from a secret store or the user's own login. Do not move it to another file in the repository. |
| C2 | An `apiKeyHelper` that only echoes a fixed key | `repos/inventory-service/.claude/get_key.sh`, named in `.claude/settings.json` | The helper must fetch a short-lived credential from a broker or secret store. A static echo is a key in a script. Rotate the key. |
| C3 | A CI secret shared across repositories | `org/ci_secrets_inventory.csv` (`SHARED_CLAUDE_CI_KEY` for two repositories) and the two `claude-review.yml` files that use it | One repository-scoped secret per repository, each with its own owner and rotation date. |
| C4 | A service account key owned by a person who left | `org/credentials_inventory.csv` `cred-101` (owner `p.nakamura@example.org`, no expiry, never rotated, used after the 2026-06-30 departure in `org/hr_departures.csv`) | Replace under a team-owned identity, revoke `cred-101`, set an expiry, and add a departure step to offboarding. |
| C5 | No deny rules for `.env` | `repos/inventory-service/.claude/settings.json` has no `permissions.deny`, and the repository has a `.env` | Add `Read` deny rules for `.env` and `.env.*`, and add sandbox `denyRead` so shell commands are covered too. |
| C6 | A personal key owned by a person who left, in `.env` | `org/credentials_inventory.csv` `cred-104` (owner `j.alvarez@example.org`, left 2026-03-15, last used 2026-10-05) and `repos/inventory-service/.env` | Revoke `cred-104`, give each developer their own sign-in, keep personal keys out of the project folder. |

## Other points

| Item | Points |
|---|---|
| `payments-gateway` is not reported as defective (the clean repository: repository-scoped secret with an owner, expiry and recent rotation, deny rules, sandbox with fail-closed) | 8 |
| Findings are prioritized with a stated reason (a reason, not the finding's name or rank restated). Suggested order: C4 and C6 (live credentials of people who left), C3 (widest reach), C1, C2, C5 | 8 |
| The rotation and ownership plan covers every credential in the inventory (`cred-101` to `cred-104`) | 12 |

## Notes

- Personal key versus service account key: C6 is a personal key (it dies with its owner and should never be in a project folder). C4 is a service account key that was left under a person (it needs a team owner). Give credit for saying which is which.
- `billing-service` has correct `.env` deny rules. Reporting it for C5 is a false positive.
- The `none` expiry and `never` rotation values are scenario data. Do not teach them as product defaults. A `claude setup-token` token is a one-year token per the docs read, and none appears in the inventory.
- Federation for automation: only the credential precedence list is in the docs read. Details of setting it up are unconfirmed, so a student answer on federation must say so.
- Lab step 5 (the three-options paragraph, written in the template's `## Credential options for automation` section) carries no points in the 100 above. Read it and discuss it: the thing to look for is whether the student marked the federation details `unconfirmed`. Do not add or subtract points for it.
- What `score_audit.py` does and does not look at, so you know where to adjust it by hand:
  - It accepts `## Finding N`, `### Finding N` and titled headings (`## Finding 1: departed owner`), and both `**Fix:**` and `**Fix**:` label spellings.
  - Fix credit (3 of the 12) comes only from the **Fix** and **Rotation step** fields, so a fix word that appears only in **What is wrong** earns nothing. For an answer with no bold labels at all it falls back to the whole block.
  - The 8 points for the clean repository are lost only when a finding's **File and line** field points at `payments-gateway` or `cred-102`. Naming payments-gateway elsewhere in a block (as the clean comparison) is not penalised.
  - Identification is word-blind about *how* a problem is described: it takes "ex-employee", "no longer with us", "a former employee whose last day was 30 June 2026" or a citation of `org/hr_departures.csv` for C4/C6, and "organization-scoped" or "used by both repositories" for C3. If a student identifies a problem in words it still misses, award the points by hand and say so on the sheet.
  - It is not word-blind about *what* C4 and C6 are: those are the two findings that need the join with `org/hr_departures.csv`, so the block has to name the departure, its date, or the HR file. "cred-101 has no expiry and was never rotated" alone scores C4 0/12 on purpose, and so does "cred-104 sits in `.env`" alone for C6. That is the lab's core lesson, not a formatting trip-up: the no-expiry half is worth saying so on the sheet, but it is not the finding. Fix verbs are deliberately not accepted as identification, so "terminate the key", "do not leave a key without an expiry", "give each developer their own key" and "rotate every 180 days" earn nothing by themselves. Two words read both ways and are handled accordingly: a *person* leaves, but a *key* is also "left without an expiry", so bare "left" only counts next to a person ("the owner left Harbor", "she left in March", "who left on 2026-06-30"); and "retire" never counts, because retiring a key is a fix (the sample answer's own rotation step says "retire it").
  - A priority line needs a reason clause after the finding name: a break (`,` `:` `;` ` - ` ` (` `. `) or a connective, then at least five words, at least two of which say something beyond the finding's own name or its rank. So "1. Finding 1, because it is a live credential owned by a former employee" and "1. Finding 1 - live credential of a former employee" count; "1. Finding 1 - highest", "1. Finding 1: the shared CI key" and "1. cred-101 service account key in credentials_inventory" do not. Known blind spot: a true but very terse reason of four words or fewer ("1. Finding 2, two repositories fail together") is indistinguishable by length from a restated name and is scored 4/8. Read the list; if every line gives a real reason, award the 8 by hand. `lab5-audit/check_findings_format.py` applies the same predicate, so the student sees the same verdict you do.
