# Hermes Agents Forge

This file is the source of truth for an Hermes agent onboarding this repository.

## Repository

- Repository: https://github.com/juliench82/hermes-agents-forge
- Default branch: `main`

## Required reading

Before running any command or changing any file, read:

1. `HERMES.md` (this file)
2. `onboarding-loop.yaml`
3. `team-designer.yaml`

The two YAML files are repository-root skills. Do not look for them under `site/public/` and do not invent alternate paths.

## Onboarding sequence

1. Inspect the repository and read the required skill files.
2. Explain the proposed onboarding actions to the user in plain language.
3. Ask for confirmation before any action with external side effects or any destructive change.
4. Run the onboarding loop defined by `onboarding-loop.yaml`.
5. Use `team-designer.yaml` when the flow requires designing or configuring an agent team.
6. Report what was completed, what remains, and any files changed.

## Path and state rules

- Do not assume a `profiles/` directory exists.
- Do not create a hardcoded `profiles/` directory.
- Discover paths from the repository and the referenced skills.
- Do not overwrite, delete, or migrate existing files unless the user explicitly asks for that change and confirms it.
- Keep onboarding changes scoped to this repository.

## Safety

- Never expose secrets, credentials, or private configuration in chat or committed files.
- Do not run destructive commands without explicit user confirmation.
- If an instruction is ambiguous, stop and ask a focused clarification question.

## Completion

When onboarding is complete, summarize:

- The team or agent configuration created or updated.
- The exact files changed.
- Any commands the user must run manually.
- Any unresolved setup or integration requirements.
