# Acceptance Checklist — <Automation name>

The quality guardian completes this checklist before a workflow can enter `READY_FOR_REVIEW`.

## Outcome

- [ ] The delivered output matches the Customer Blueprint’s stated outcome.
- [ ] The trigger or schedule is correct in the customer timezone.
- [ ] Expected success and failure outputs are understandable to a non-technical customer.

## Permissions and safety

- [ ] Every integration is listed as authorised in the Integration Register.
- [ ] Actual permissions are no broader than required.
- [ ] No secret appears in prompts, artifacts, logs intended for the customer, or repository files.
- [ ] All denied paths, systems, and actions are rejected.
- [ ] Approval mode is implemented exactly as specified.
- [ ] Material-change detection returns the workflow to review.

## Reliability

- [ ] A representative safe test has passed.
- [ ] Failure behaviour preserves diagnostics and notifies the approved recipient.
- [ ] Duplicate-run and retry behaviour is defined.
- [ ] A pause or kill-switch procedure is documented.
- [ ] Rollback or recovery steps are documented where the workflow writes externally.

## Activation decision

- Result: PASS | BLOCKED | NEEDS_CUSTOMER_INPUT
- Quality guardian notes: <notes>
- Verified at: <timestamp>
- Customer review required: yes / no
