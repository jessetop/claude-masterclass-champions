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
| Findings are prioritized with a stated reason. Suggested order: C4 and C6 (live credentials of people who left), C3 (widest reach), C1, C2, C5 | 8 |
| The rotation and ownership plan covers every credential in the inventory (`cred-101` to `cred-104`) | 12 |

## Notes

- Personal key versus service account key: C6 is a personal key (it dies with its owner and should never be in a project folder). C4 is a service account key that was left under a person (it needs a team owner). Give credit for saying which is which.
- `billing-service` has correct `.env` deny rules. Reporting it for C5 is a false positive.
- The `none` expiry and `never` rotation values are scenario data. Do not teach them as product defaults. A `claude setup-token` token is a one-year token per the docs read, and none appears in the inventory.
- Federation for automation: only the credential precedence list is in the docs read. Details of setting it up are unconfirmed, so a student answer on federation must say so.
