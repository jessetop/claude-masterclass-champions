# Demo 1: Completed Example (facilitator only)

Do not share with students. This is one reasonable answer. Accept other answers that reach the same tier for a stated reason.

## 1. Purpose and owner
Draft weekly release notes for `tally-api`. Owner: Dana Okafor. Backup: Ravi Menon. Owner approves and can stop it.

## 2. Data
Source code and commit messages. Most sensitive item in reach: `config/staging.env` (a real staging database password). Customer ticket numbers appear in commit messages. No customer data stored in the repository. Data can leave the machine through shell commands and a push.

## 3. Repositories
In scope: `tally-api`. Out of scope: `billing-core`. Today Claude Code can push. Branch protection: unknown.

## 4. Tools and servers
File tools and shell. A ticket MCP server is proposed and authenticates as a shared service account. That is a finding: users would act as one shared identity. Fix before approval: per-user sign-in.

## 5. Model and effort
Unknown, default account model. Needs a decision, low impact for this use case.

## 6. Permissions and sandbox
Everyone clicks allow. No deny rules. `git push` allowed. Gap: no deny rule for `config/staging.env`, no block on push.

## 7. Credentials
Own seats: good. A personal key in a `.env` file in the repository folder: a finding. Move it out of the repository folder and add a deny rule.

## 8. Review and escalation
One reviewer on the pull request. No escalation path written.

## 9. Logging
Only git history. Cannot prove any rule from a log today.

## 10. Exit criteria
Not discussed.

## Tier
Medium. The deciding answer is section 2: a real staging password sits in the repository folder and nothing stops Claude Code from reading it, pushing, or using it. Remove or deny the file and block the push, and the tier could drop to Low. A shared service account on the ticket server would push it toward High if that server could change tickets.

## Teaching points
- Most of the use case is low risk. One data answer and one missing control set the tier.
- "Unknown" in sections 5, 8, 9 and 10 is itself a result: the team has not decided.
