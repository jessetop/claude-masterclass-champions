# Credential Audit: Findings (facilitator sample answer)

Audit target: `harbor-org` (fictional sample). Auditor: Facilitator  Date: 2026-10-12

## Finding 1

- **File and line:** `org/credentials_inventory.csv` cred-101 (and `org/hr_departures.csv`)
- **What is wrong:** cred-101, a service account key used by CI for two repositories, is owned by p.nakamura, who left on 2026-06-30. It has no expiry, was never rotated, and was used on 2026-10-09.
- **Risk:** a live credential tied to a former employee. Nobody on the team owns it.
- **Severity:** high
- **Fix:** replace it with a team-owned identity, revoke cred-101, set an expiry, and add a departure step to offboarding.
- **Rotation step:** create the replacement, update the CI secrets, revoke cred-101, confirm CI still runs.
- **Owner:** platform-team

## Finding 2

- **File and line:** `org/ci_secrets_inventory.csv` SHARED_CLAUDE_CI_KEY, and `repos/billing-service/.github/workflows/claude-review.yml`, `repos/inventory-service/.github/workflows/claude-review.yml`
- **What is wrong:** one organization-scoped CI secret is shared by two repositories (billing-service and inventory-service) and backed by cred-101.
- **Risk:** the widest blast radius: a leak from either repository exposes both, and one rotation breaks both.
- **Severity:** high
- **Fix:** one repository-scoped secret per repository, each with its own owner and rotation date.
- **Rotation step:** create separate secrets, switch each workflow, then retire the shared one.
- **Owner:** platform-team

## Finding 3

- **File and line:** `repos/billing-service/.claude/settings.json`, `env.ANTHROPIC_API_KEY`
- **What is wrong:** an API key sits in a committed settings file.
- **Risk:** everyone with the repository has the key, and it lives in git history.
- **Severity:** high
- **Fix:** remove it from the file and from history, and supply credentials at run time from a secret store or the user's own login. Do not move it to another file in the repository.
- **Rotation step:** rotate the key now, because it has been exposed.
- **Owner:** billing-service team

## Finding 4

- **File and line:** `repos/inventory-service/.claude/get_key.sh` (referenced by `.claude/settings.json` apiKeyHelper)
- **What is wrong:** the key helper only echoes a static key, so it is a hard-coded key in a script.
- **Risk:** a helper is meant to return a short-lived credential; this one never changes.
- **Severity:** medium
- **Fix:** make the helper fetch a short-lived credential from a broker or secret store.
- **Rotation step:** rotate the echoed key and retire it.
- **Owner:** inventory-service team

## Finding 5

- **File and line:** `repos/inventory-service/.claude/settings.json` (no `permissions.deny`) and `repos/inventory-service/.env`
- **What is wrong:** the repository holds a `.env` file and the settings have no Read deny rules for it.
- **Risk:** Claude's file tools can read the secrets in `.env`.
- **Severity:** medium
- **Fix:** add `Read(./.env)` and `Read(./.env.*)` deny rules, and add sandbox `denyRead` so shell commands are covered too.
- **Rotation step:** rotate any value Claude may already have read.
- **Owner:** inventory-service team

## Finding 6

- **File and line:** `repos/inventory-service/.env` and `org/credentials_inventory.csv` cred-104
- **What is wrong:** cred-104, a personal API key, belongs to j.alvarez, who left on 2026-03-15. It sits in `.env`, has no expiry, and was used on 2026-10-05.
- **Risk:** a personal key outliving its owner. Someone is still using a departed person's key.
- **Severity:** high
- **Fix:** revoke cred-104, give developers their own seats, and keep personal keys out of the repository folder.
- **Rotation step:** revoke now and confirm who used it on 2026-10-05.
- **Owner:** inventory-service team

## Not a finding

- `repos/payments-gateway`: a repository-scoped secret with an owner, an expiry and a recent rotation, deny rules for `.env` and `curl`, and a sandbox with `failIfUnavailable`.
- `repos/billing-service` Read deny rules for `.env`: correct, so no finding there.
- `org/managed-settings.json`: it only disables bypass mode, which is sound.

## Priority order

1. Finding 1, because it is a live credential owned by a former employee.
2. Finding 6, because it is also a departed person's key and it was used recently.
3. Finding 2, because it has the widest reach: two repositories fail together.
4. Finding 3, because the key is exposed to everyone with the repository.
5. Finding 4, since the helper is a static key, though contained in one repository.
6. Finding 5, since it only matters while a secret sits in `.env`.

## Rotation and ownership plan

| Credential | Owner | Lifetime | Where used | Rotation | If the owner leaves |
|---|---|---|---|---|---|
| cred-101 | platform-team | 90 days | CI for billing-service and inventory-service | replace with two repository-scoped keys, then revoke | no change, a team owns it |
| cred-102 | platform-team | until 2027-02-20 | CI for payments-gateway | rotate before expiry | no change |
| cred-103 | platform-team | until 2026-11-02 | nightly report job | rotate before 2026-11-02 | no change |
| cred-104 | revoke, no owner | none | local developer sessions | revoke, use own seats | not applicable after revoke |
