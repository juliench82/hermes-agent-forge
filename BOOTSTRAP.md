# Bootstrap Guide — Hermes Team Setup

## Quick Start

```bash
# 1. Install the onboarding skills
hermes -p default skills install onboarding-loop team-designer

# 2. Run onboarding
hermes -p default chat "Start onboarding"
```

This launches an interactive flow that:
1. Asks about your use case, role, and goals
2. Generates a custom team of 3–7 specialist bots
3. Creates profiles with `SOUL.md` and installs skills
4. Sets up a team group chat (Bot Mode)
5. Optionally configures Buzz (or skip for later)

## What Gets Created

- **Profiles**: `~/.hermes/profiles/<bot-name>/` with:
  - `config.yaml` (bot_mode enabled)
  - `SOUL.md` (role description + skills)
- **Group chat**: `team-main` with all bots as members
- **Skills**: Installed per profile based on the team design

## Post-Onboarding

```bash
# View your bot roster
hermes bots

# Chat with a specific bot
hermes -p <bot-name> chat "Your task"

# Add a messenger (optional, after onboarding)
hermes gateway setup telegram
hermes gateway setup discord
hermes gateway setup buzz
```

## Buzz is Optional

Buzz is **not required**. Your bots communicate via Bot Mode group chat by default.

Add Buzz later if you want a human+agent Nostr workspace:

```bash
hermes gateway setup buzz
```

Or use any other messenger:

```bash
hermes gateway setup telegram
hermes gateway setup slack
```

## Architecture

```
onboarding-loop.yaml
  - Collects use case, role, goals
  - Calls team-designer skill
  - Creates profiles + SOUL.md
  - Installs skills per profile
  - Sets up group chat (Bot Mode)
  - Optional Buzz gateway

team-designer.yaml
  - LLM prompt to generate JSON team spec
  - Validates 3–7 profiles
  - Returns structured output
```

## Next Steps

1. Run onboarding
2. Test bot-to-bot handoffs in group chat
3. Add a messenger for human access
4. Start assigning real tasks to your team
