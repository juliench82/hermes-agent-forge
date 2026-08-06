# Activation Review Record — <Automation name>

> Produced by the default profile (orchestrator) and presented to the customer. Records the explicit activation decision before a workflow begins real work.

## Review summary

- Customer / tenant: <name>
- Blueprint version: <version>
- Automation brief: <path or reference>
- Quality guardian verdict: PASS | BLOCKED | NEEDS_CUSTOMER_INPUT
- Acceptance checklist: <path or reference>
- Presented by: hermes-orchestrator
- Presented at: <timestamp>

## What the customer reviewed

1. **Outcome:** <what will be delivered>
2. **Trigger:** <when it runs or what starts it>
3. **Data used:** <systems and folders it may read>
4. **Actions:** <drafts, sends, creates, updates, or deletes>
5. **Recipients/destinations:** <exact approved targets>
6. **Approval mode:** DRAFT_ONLY | APPROVAL_REQUIRED | AUTOMATIC_AFTER_ACCEPTANCE
7. **Failure behaviour:** <what happens on failure>
8. **Stop control:** <how the customer pauses the workflow>

## Decision

- Decision: ACTIVATE | KEEP_IN_DRAFT | CHANGE_REQUESTED | DECLINE
- Decided by: <customer name or authorised operator>
- Decided at: <timestamp>
- Notes: <any customer conditions or caveats>

## Approved scope

- Exact actions permitted: <list>
- Exact recipients/destinations: <list>
- Schedule: <crontab or trigger>
- Approval expiry: <date/time if applicable>

## Rules

- This record is the only valid authorisation for activation.
- Activation is not inferred from silence or a previous unrelated approval.
- Any material change to scope, recipients, schedule, data access, or approval mode invalidates this record and requires a new review.
- The self-improver may not activate or alter an active workflow.
