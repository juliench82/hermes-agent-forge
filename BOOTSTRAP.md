# BOOTSTRAP.md — Isolated-Profile Control Room

Read this file first.

This repository is an isolated-profile control-room contract for Hermes. It governs and coordinates a team of specialist roles that turn repetitive company work into finished automation outcomes.

## Architecture

This branch is **isolated-profile only**. There is no skill-routed fallback.

- One native Hermes profile per role.
- BUZZ as the inter-profile transport layer.
- The Obsidian brain as the shared memory layer.
- Prompt-first orchestration with deterministic scripts for fragile provisioning operations.

## Operating principle

The control room tells Hermes what outcome to achieve and what to verify. Where a step is fragile or requires deterministic behavior (profile creation, gateway config writes, vault init, key uniqueness checks), scripts under `scripts/` handle it. Where Hermes can be instructed directly, the prompt carries the contract.

If a preferred CLI command does not exist, Hermes should:
- search for the equivalent built-in action,
- otherwise perform the task through the most direct available Hermes surface,
- otherwise ask one short clarification question.

Never invent a hidden command. Never silently skip a bootstrap step.

## Startup sequence

1. Read `BOOTSTRAP.md`.
2. Read `buzz-handoff.md`.
3. Read `README.md`.
4. Verify Hermes core is installed and a working provider is configured (`hermes --version`, provider key present).
5. Run `scripts/obsidian.sh` — verify/seed the shared Obsidian vault.
6. Run `scripts/buzz.sh` — verify the BUZZ adapter and relay reachability.
7. Run `scripts/profiles.sh` — create the seven profiles idempotently and install each role's skill + shared policy files.
8. Read `buzz-handoff.md` and configure the handoff channels.
9. Provision one BUZZ identity per profile (`BUZZ_PRIVATE_KEY` in each profile's `.env`; never committed, never shared between profiles).
10. Smoke test: orchestrator posts a `handoff` envelope to the strategist channel and receives an acknowledgement.
11. Begin runtime orchestration from the orchestrator profile.

## Role-to-profile map

| Profile | Skill source | BUZZ channels |
|---------|--------------|----------------|
| `hermes-orchestrator` | `profiles/orchestrator/skill.md` | all |
| `hermes-product-strategist` | `profiles/product-strategist/skill.md` | `cr-brief` |
| `hermes-architect` | `profiles/architect/skill.md` | `cr-design` |
| `hermes-builder` | `profiles/builder/skill.md` | `cr-build` |
| `hermes-quality-guardian` | `profiles/quality-guardian/skill.md` | `cr-review` |
| `hermes-self-improver` | `profiles/self-improver/skill.md` | `cr-improve` |

## Rules

- Scripts are idempotent; re-running the bootstrap must be safe and fast.
- Scripts never print secrets. BUZZ keys live only in per-profile `.env` files.
- The Obsidian vault is the only shared writable memory; profiles do not share `HERMES_HOME`.
- If a required value is missing (relay URL, vault path, key), ask one short question — do not guess.

## Core rule

Do not skip this repository. Do not improvise a different startup sequence. Read the control-room files first, then continue with the runtime flow defined in `buzz-handoff.md`.
