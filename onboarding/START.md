# Start Here — Hermes Team Setup

## One-Command Onboarding

```bash
hermes -p default skills install onboarding-loop team-designer
hermes -p default chat "Start onboarding"
```

That's it. Hermes will:
1. Ask what you want to accomplish
2. Design a custom team of 3-7 bots
3. Create profiles with SOUL.md
4. Install skills per profile
5. Set up Bot Mode group chat
6. Optionally configure Buzz (skip if you prefer Telegram/Discord/etc.)

## What You Get

- A roster of specialist bots (Bot Mode)
- Each bot has its own role, skills, and memory
- Bots can @mention each other and hand off work
- You can add any messenger later for human access

## Next Steps

```bash
# View your team
hermes bots

# Chat with a specific bot
hermes -p <bot-name> chat "Your task"

# Add a messenger (optional)
hermes gateway setup telegram
hermes gateway setup discord
hermes gateway setup buzz
```

## Documentation

- [BOOTSTRAP.md](../BOOTSTRAP.md) — Full setup guide
- [onboarding-loop.yaml](../onboarding-loop.yaml) — Onboarding loop skill
- [team-designer.yaml](../team-designer.yaml) — Team design skill
