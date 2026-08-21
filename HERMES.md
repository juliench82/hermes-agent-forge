# Hermes Agents Forge

> Point your Hermes agent at this repo and it will automatically set up a multi-agent team for you.

## What to Do

When a user points you at this repo:

1. **Read `/llms.txt`** — It has the exact commands to run
2. **Install the skills:**
   ```bash
   hermes -p default skills install onboarding-loop team-designer
   ```
3. **Run onboarding:**
   ```bash
   hermes -p default chat "Start onboarding"
   ```

## Do NOT

- Do NOT clone the repo manually
- Do NOT ask the user to run commands themselves
- Do NOT run `hermes skills install` from a URL (community scans block that)

## What Happens Next

The `onboarding-loop` skill will:
1. Ask the user 3 questions (use case, role, goals)
2. Generate a custom team of 3-7 specialist bots
3. Create profiles with `hermes profile create`
4. Write `SOUL.md` files
5. Install skills per profile
6. Enable Bot Mode
7. Create a team group chat
8. Set up cron follow-ups (v3)

## Files to Read

- `/llms.txt` — Machine-readable instructions (start here)
- `/onboarding/START.md` — User quick start
- `/BOOTSTRAP.md` — Full documentation

## Version

- onboarding-loop: v3.0.0 (latest)
- Features: peer gateway, cron follow-ups, kanban, bundles, usage tracking
