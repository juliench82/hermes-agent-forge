# Onboarding — Hermes Team Setup

This directory contains the Hermes-native onboarding flow for dynamic team creation.

## Files

- `onboarding-loop.yaml` — Main loop that collects requirements, designs team, creates profiles
- `team-designer.yaml` — Skill that generates JSON team spec from use case
- `START.md` — Quick start for users
- `README.md` — This file
- `BOOTSTRAP.md` — Full setup guide (root)

## How It Works

1. User runs: `hermes -p default skills install onboarding-loop team-designer`
2. User runs: `hermes -p default chat "Start onboarding"`
3. Loop collects: use case, role, goals
4. Calls `team-designer` to generate 3-7 profiles
5. Creates profiles with `hermes profile create`
6. Writes `SOUL.md` per profile
7. Installs skills per profile
8. Enables Bot Mode
9. Creates team group chat
10. Optionally configures Buzz gateway

## Key Design Choices

- **Buzz is optional** — Users can skip and add any messenger later
- **Bot Mode is wired in** — Every profile gets `bot_mode: true`
- **Hermes-native** — No Python orchestrator; the loop is a skill
- **Iterative** — Users can adjust the team before creation

## Customization

Edit `onboarding-loop.yaml` to:
- Change prompts
- Add validation steps
- Customize SOUL.md template
- Add post-creation tasks

Edit `team-designer.yaml` to:
- Adjust the system prompt
- Change skill recommendations
- Enforce specific team patterns
