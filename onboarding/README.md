# Customer onboarding

This package turns a customer's plain-language request into a reviewed, durable automation contract. It is provider-neutral: the same artifacts apply to a managed cloud runtime or a self-hosted deployment.

It also holds **install-time** vault onboarding (Obsidian shared brain path), which runs during `BOOTSTRAP.md` before customer automation discovery.

## Two entry points

| Phase | Entry | Purpose |
|-------|-------|---------|
| Install | `workflows/vault-path.md` | Resolve local Obsidian vault path (prompt + OS suggestion, CREATE/SKIP) |
| Customer automation | `START.md` | First useful automation after install |

## Read order

### Install-time (vault / shared brain)

1. `workflows/vault-path.md` — resolve `OBSIDIAN_VAULT_PATH`
2. `templates/vault-register.md` — record the choice
3. `templates/hermes-md.md` — optional vault-root `.hermes.md` map
4. Then `scripts/obsidian.sh` (from repo root) if not skipped

### Customer automation

1. `START.md` — customer-facing activation entry point
2. `manifest.md` — lifecycle, profile participation, and required artifacts
3. `templates/customer-blueprint.md` — durable source of truth for one automation
4. `templates/automation-brief.md` — Product Strategist handoff to Architect
5. `templates/integration-register.md` — credential-free integration and scope register
6. `templates/approval-policy.md` — approval modes and material-change rules
7. `templates/acceptance-checklist.md` — Quality Guardian pre-activation verification
8. `templates/activation-review-record.md` — customer activation decision record
9. `workflows/connector-authorisation.md` — OAuth and credential authorisation flow
10. `workflows/activation-review.md` — customer activation review workflow

## Examples

- `examples/invoice-summary.md` — safe weekly unpaid invoice summary

## Rules

- No secrets in any onboarding artifact.
- No external action before the approval policy permits it.
- The default Hermes profile owns all customer-facing communication.
- The quality guardian must pass the acceptance checklist before activation is offered.
- Vault path SKIP is allowed at install time; do not block the whole bootstrap solely for skipping Obsidian.
