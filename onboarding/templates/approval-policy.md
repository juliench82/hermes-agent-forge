# Approval Policy — <Customer name / automation name>

## Default principle

Start with the least permissive mode that can demonstrate useful value. New workflows default to `DRAFT_ONLY` unless the customer explicitly approves another mode.

## Modes

| Mode | Behaviour | Suitable for |
|---|---|---|
| `DRAFT_ONLY` | Hermes prepares output but does not send, publish, modify, or delete anything external | First runs, high-risk workflows, unclear requirements |
| `APPROVAL_REQUIRED` | Hermes proposes an action and waits for a named approver | External messages, record updates, payments, or sensitive changes |
| `AUTOMATIC_AFTER_ACCEPTANCE` | Hermes executes only the reviewed action within approved scope | Stable, low-risk, repeatedly validated workflows |

## Policy

- Current mode: <mode>
- Named approver(s): <approved contact/channel>
- Approval expiry: <for example, 24 hours>
- Automatic action scope: <exact actions, recipients, and schedule>
- Always require approval for: <new recipient, deletion, payment, credential change, scope expansion, policy change>
- Pause / kill-switch owner: <customer/operator>

## Change rule

Changing recipients, write destinations, schedule, data sources, permission scope, or action type is a material change. Return the workflow to `READY_FOR_REVIEW` and obtain approval before activation.
