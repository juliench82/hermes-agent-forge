# Activation review workflow

## Goal

Give the customer one short, unambiguous decision before a workflow begins real work.

## Review format

The default profile presents:

1. **Outcome:** what will be delivered
2. **Trigger:** when it runs or what starts it
3. **Data used:** systems/folders it may read
4. **Actions:** drafts, sends, creates, updates, or deletes it may perform
5. **Recipients/destinations:** exact approved targets
6. **Approval mode:** draft-only, approval-required, or automatic-after-acceptance
7. **Failure behaviour:** what happens when a source, integration, or validation fails
8. **Stop control:** how the customer pauses the workflow

## Decision

- `ACTIVATE`: enable only the reviewed scope and approval mode
- `KEEP_IN_DRAFT`: retain draft-only operation
- `CHANGE_REQUESTED`: return to the relevant profile with the requested change
- `DECLINE`: close the activation attempt without enabling anything

## Rules

- Activation is not inferred from silence or from a previous unrelated approval.
- A customer request that materially expands scope triggers a new architecture and quality review.
- The self-improver may recommend changes but cannot activate or alter an active workflow.
