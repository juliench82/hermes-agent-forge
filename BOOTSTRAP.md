# BOOTSTRAP.md — Isolated-Profile Control Room

Read this file first.

## One-prompt setup

The user gives Hermes one instruction:

> Read and follow `juliench82/hermes-bootstraper` from start to finish. Read `BOOTSTRAP.md` first. Set up the isolated-profile control room, BUZZ, and the Obsidian brain. Run the repository scripts yourself. Ask me only for values that cannot be discovered safely.

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

## Fallback

If a named CLI command is unavailable, use the equivalent Hermes action or runtime surface. Never invent a command, silently skip a step, or claim setup completed before profiles, BUZZ, Obsidian, and the smoke test succeed.
