# Start customer onboarding

This is the customer-facing activation entry point for Hermes Control Room.

The customer does not need to understand profiles, tools, models, prompts, or infrastructure. Ask only for the information needed to design one useful first automation.

## Install prerequisite (shared brain)

If Control Room install is still in progress, resolve the Obsidian vault **first** via
`workflows/vault-path.md` (path prompt + OS suggestion, or SKIP). Do not mix the
vault-path question with the automation discovery question below.

If install already recorded `SKIPPED` for the vault, continue; automations that need
local notes can revisit vault-path later.

## Desired outcome

Begin with this question:

> What repeated piece of work would you most like to stop doing?

Use the answer to propose a narrow first outcome. Prefer a workflow that is frequent, measurable, reversible, and safe to run in draft mode.

Examples:

- “Every Friday, prepare unpaid invoices grouped by supplier.”
- “Sort incoming support requests and prepare the right team notification.”
- “Compile monthly expenses into a report for finance.”

## Activation rules

1. Do not ask the customer to install Hermes, use a terminal, create profiles, or edit configuration files.
2. Do not request passwords, API keys, session cookies, or other secrets in chat or Markdown. Use the approved credential-authorisation flow.
3. Do not enable an external action during discovery.
4. Create a Customer Blueprint from `templates/customer-blueprint.md` before any build work begins.
5. The default Hermes profile coordinates the native specialist profiles. Customer-facing communication remains with the default profile.
6. The quality guardian must complete the acceptance checklist before activation is offered.

## Next artifacts

- `workflows/vault-path.md` (install-time only, if vault not yet resolved)
- `templates/customer-blueprint.md`
- `templates/integration-register.md`
- `templates/approval-policy.md`
- `workflows/connector-authorisation.md`
- `workflows/activation-review.md`
