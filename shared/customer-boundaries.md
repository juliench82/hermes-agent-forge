# Customer boundaries policy

This policy applies to every customer automation and every native Hermes profile participating in the Control Room.

## Customer / tenant boundary

- Customer data, memories, schedules, artifacts, connector metadata, and audit records must be logically and operationally scoped to one customer.
- A profile handling one customer must not retrieve or use another customer’s context, credentials, files, outputs, or operational history.
- Shared role definitions and generic templates may be reused; customer-specific state may not be shared.

## Credential boundary

- Credentials are owned by the customer or an explicitly authorised operator.
- Store credentials only in the approved secret store or connector manager.
- Profiles receive the least privilege and minimum duration needed for their assigned work.
- A profile must not export, reveal, copy, or place credentials in notes, code, logs, prompts, or handoffs.

## Execution boundary

- A workflow may read and write only within the Customer Blueprint and Integration Register allowlists.
- New external recipients, write targets, deletion, payment, access-scope changes, and policy changes require a new activation review.
- The default profile enforces the customer-facing approval decision; the quality guardian may block activation.
- The self-improver is advisory only and cannot change live behaviour without review.

## Data boundary

- Use the minimum data required to complete the stated outcome.
- Do not retain raw customer data beyond the stated retention requirement.
- Customer-visible artifacts must not include secrets or unrelated sensitive data.
- Failures must preserve only the diagnostics necessary to support recovery and audit.

## Operational boundary

- Every active workflow has a named owner, a failure notification route, and a documented pause mechanism.
- No workflow is considered active until the activation review records an explicit `ACTIVATE` decision.
- Any uncertainty about permissions, data scope, or customer intent is a blocking condition, not an invitation to infer permission.
