# Example onboarding — weekly unpaid invoice summary

## Customer request

> Every Friday morning, prepare a list of unpaid invoices grouped by supplier and send it to finance.

## Safe first version

- Trigger: Friday, 09:00, customer timezone
- Read: authorised accounting system, open-invoice records only
- Output: Markdown or spreadsheet summary in a customer-approved destination
- Action mode: `DRAFT_ONLY` for the first four successful runs
- Recipient: finance contact named in the Customer Blueprint
- Quality checks: invoice count and grouped totals reconcile with the source data
- Failure: do not send; notify the approved owner with a diagnostic summary

## Why this is a good first automation

It has a clear owner, observable output, bounded data scope, measurable correctness, and a reversible draft-first rollout. It is not activated until the acceptance checklist and customer activation review pass.
