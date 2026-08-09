# Customer onboarding manifest

## Purpose

This package turns a customer's plain-language request into a reviewed, durable automation contract. It is provider-neutral: the same artifacts apply to a managed cloud runtime or a self-hosted deployment.

Install-time vault resolution is part of this package but **outside** the customer automation state machine.

## Install-time vault (before customer discovery)

| Step | Artifact / workflow |
|------|---------------------|
| Resolve vault path | `workflows/vault-path.md` |
| Record choice | `templates/vault-register.md` |
| Optional map seed | `templates/hermes-md.md` → vault `/.hermes.md` |
| Wire + smoke | `scripts/obsidian.sh` when not SKIPPED |

Statuses: `PENDING` → `ACCEPTED` | `CREATED` | `SKIPPED`

## Profile participation

| Profile | Onboarding responsibility |
|---|---|
| Default profile / Orchestrator | Owns customer communication, state, handoffs, and final delivery; runs install-time vault prompt |
| Product Strategist | Converts discovery into an automation brief and measurable outcome |
| Architect | Selects an implementation approach and defines permissions, dependencies, and rollback |
| Builder | Implements only after the blueprint and approval policy are complete |
| Quality Guardian | Verifies acceptance criteria and blocks activation when requirements are unmet |
| Self Improver | May propose later improvements; cannot enable, alter, or expand a workflow unilaterally |

## Required artifacts (customer automation)

1. Customer Blueprint
2. Integration Register
3. Approval Policy
4. Automation Brief
5. Acceptance Checklist
6. Activation Review record

## Required artifacts (install vault)

1. Vault Register (or explicit SKIP record)
2. `OBSIDIAN_VAULT_PATH` in env when not skipped

## State machine

```text
DISCOVERY → BLUEPRINTED → AUTHORISED → DESIGNED → BUILT → VALIDATED → READY_FOR_REVIEW → ACTIVE
                                      ↘ BLOCKED / NEEDS_CUSTOMER_INPUT
```

Only the customer or an explicitly authorised operator may move a workflow from `READY_FOR_REVIEW` to `ACTIVE`. Any material change to data access, external actions, recipients, schedule, or approval mode requires a new review.

## Non-negotiable rules

- No secrets in repository files, notes, messages, or agent memory.
- No external action before the approval policy permits it.
- Every artifact is tenant/customer scoped.
- Every handoff references the current artifact version and outstanding decisions.
- Automation claims must be testable against stated acceptance criteria.
- Do not run `scripts/obsidian.sh` until vault-path workflow finishes with ACCEPTED or CREATED.
