# Customer onboarding

This package turns a customer's plain-language request into a reviewed, durable automation contract. It is provider-neutral: the same artifacts apply to a managed cloud runtime or a self-hosted deployment.

## Read order

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
