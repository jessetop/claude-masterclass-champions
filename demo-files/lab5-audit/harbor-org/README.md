# Harbor Example Co: Claude Code credential audit sample

Fictional. Every secret in this tree is a placeholder (`FAKE-KEY-DO-NOT-USE-NNNN`, `FAKE-TOKEN-DO-NOT-USE`). Report the pattern, not the value.

Layout:

- `org/` holds a managed settings file and three inventories: credentials, CI secrets and departures. The audit date is 2026-10-12.
- `repos/billing-service`, `repos/inventory-service`, `repos/payments-gateway` each hold a `.claude/` folder and a CI workflow. Two of them also hold a `.env` file or a key helper.

Your task and the findings layout are in Lab 5 of `labs.md`. Use `../findings-template.md`.
