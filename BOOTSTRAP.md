# BOOTSTRAP.md — Multi-Agent Control Room

Read this file first.

## Goal prompt

A good kickoff prompt for Hermes is:

> `/goal Read and follow `juliench82/hermes-bootstraper` from start to finish. Set up the multi-agent control room, install BUZZ and the Obsidian brain, create the native profiles, install each role's skill and shared policies, and make hermes-orchestrator the default user-facing profile. Ask me only for values that cannot be discovered safely.`

## One-prompt setup

The user gives Hermes one instruction:

> Read and follow `juliench82/hermes-bootstraper` from start to finish. Read `BOOTSTRAP.md` first. Set up the multi-agent control room, BUZZ, and the Obsidian brain. Run the repository scripts yourself. Ask me only for values that cannot be discovered safely.

The user does not run commands, create profiles, edit YAML, configure BUZZ, or wire Obsidian. Hermes owns bootstrap.

## Required outcome

- Create one native Hermes profile per role.
- Make `hermes-orchestrator` the active/default and only user-facing profile.
- Run `scripts/obsidian.sh` to seed and verify the shared vault.
- Run `scripts/profiles.sh` to create/verify profiles and install skills and policies.
- Configure one distinct BUZZ identity per profile; keep secrets only in each profile `.env`.
- Configure BUZZ from `buzz-handoff.md`, then run `scripts/buzz.sh`.
- Smoke-test an orchestrator-to-strategist handoff before declaring success.

Ask only for an Obsidian vault choice, BUZZ relay/community endpoint, or identity creation/location when Hermes cannot discover them safely.

## Customer onboarding

When a customer requests an automation, follow the onboarding contracts in `onboarding/`:

1. Read `onboarding/START.md` — the customer-facing activation entry point.
2. Create a Customer Blueprint from `onboarding/templates/customer-blueprint.md` before any build work begins.
3. The Product Strategist produces an Automation Brief from `onboarding/templates/automation-brief.md`.
4. Connect integrations per `onboarding/workflows/connector-authorisation.md` and record them in `onboarding/templates/integration-register.md`.
5. The Quality Guardian completes `onboarding/templates/acceptance-checklist.md` before activation.
6. Present an Activation Review using `onboarding/workflows/activation-review.md` and record the decision in `onboarding/templates/activation-review-record.md`.
7. No external action runs until the customer explicitly activates the workflow.

The default profile owns all customer-facing communication. Specialist profiles participate through defined handoffs only.

## Fallback

If a named CLI command is unavailable, use the equivalent Hermes action or runtime surface. Never invent a command, silently skip a step, or claim setup completed before profiles, BUZZ, Obsidian, and the smoke test succeed.
