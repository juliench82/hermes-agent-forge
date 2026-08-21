# Hermes Agents Forge

> Point your Hermes agent at this repo and provision isolated multi-profile agent teams that can implement real-world workflows.

## Quick Start

### Option A: Two-Command Onboarding (Recommended)

```bash
# 1. Install the onboarding skills
hermes -p default skills install onboarding-loop team-designer

# 2. Run onboarding
hermes -p default chat "Start onboarding"
```

Hermes will:
1. Ask what you want to accomplish
2. Design a custom team of 3–7 specialist bots
3. Create profiles with `SOUL.md` and install skills
4. Set up Bot Mode group chat
5. Optionally configure Buzz (or skip for later)

### Option B: Manual Setup

```bash
# Clone the repo
git clone https://github.com/juliench82/hermes-agents-forge.git
cd hermes-agents-forge

# Run the installer
./install.sh
```

## What You Get

- A roster of specialist bots (Bot Mode)
- Each bot has its own role, skills, and memory
- Bots can @mention each other and hand off work
- You can add any messenger later for human access

## Documentation

- [BOOTSTRAP.md](./BOOTSTRAP.md) — Full setup guide
- [onboarding/START.md](./onboarding/START.md) — Onboarding quickstart
- [onboarding/README.md](./onboarding/README.md) — Onboarding architecture

## Features

- **Dynamic team creation** — Hermes analyzes your use case and proposes an optimal team
- **Bot Mode wired in** — Every profile gets `bot_mode: true`, group chat created automatically
- **Buzz optional** — Use any messenger (Telegram, Discord, Slack, WhatsApp) or skip entirely
- **Hermes-native** — Everything runs as Hermes loop skills, no external orchestrator
- **Secure skill installs** — Skills are scanned with NVIDIA SkillEvaluator before install

## Example Use Cases

- **E-commerce** — Customer service, order management, anomaly detection
- **Artisans** — Appointment scheduling, invoice/quote management
- **Professionals** — Medical secretariat, legal case tracking, real estate lead management
- **Marketing** — Outbound campaigns, content creation, analytics
- **Freelancers** — Back-office admin, invoicing, tax reminders

See [Bibliothèı¨que de cas d'usage](./Bibliothèı¨que de cas d'usage.md) for detailed workflows.

## License

MIT
