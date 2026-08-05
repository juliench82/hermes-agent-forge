# BOOT.md

Read this file first.

This repository is a control-room contract for Hermes. It governs and coordinates a team of specialist roles that turn repetitive company work into finished automation outcomes.

## Two installation modes

This repository supports two deployment designs. Hermes must select one before proceeding.

### Default mode: skill-routed (tested)
- Hermes keeps one active profile.
- The active profile becomes the root orchestrator via `SOUL.md`.
- Hermes installs six specialist skills under `.hermes/skills/hermes-bootstraper/`.
- The orchestrator routes work through those skills internally.
- Shared policies are carried as orchestrator reference files.
- This is the tested and supported path.

### Advanced mode: isolated-profile (design target, not automated)
- One native Hermes profile per role, each with its own config, memory, sessions, and credentials.
- Requires an explicit task bus and handoff contract between profiles.
- Must be provisioned manually; the bootstrap prompt does not automate this mode.
- See `installation-modes.md` for the full contract.

Unless the user explicitly requests advanced mode, use default mode.

## Startup order (default mode)
1. Read `BOOT.md`.
2. Read `SOUL.MD`.
3. Read `manifest.md`.
4. Read `starter-guide.md`.
5. Read `installation-modes.md`.
6. Create or verify the six specialist skills in the active Hermes profile.
7. Create or verify the shared policy reference files.
8. Update the active profile's `SOUL.md` with the root orchestrator identity.
9. Begin runtime orchestration.

## Startup order (advanced mode)
1. Read `BOOT.md`.
2. Read `SOUL.MD`.
3. Read `manifest.md`.
4. Read `starter-guide.md`.
5. Read `installation-modes.md`.
6. Bootstrap Hermes core.
7. Bootstrap the Obsidian brain as the persistent memory layer.
8. Bootstrap BUZZ as the messaging layer.
9. Create one native Hermes profile per role using `hermes profile create`.
10. Install the corresponding skill in each profile.
11. Distribute the shared policy files to every profile.
12. Configure the task bus and inter-profile handoff mechanism.
13. Begin runtime orchestration.

## What to do next
- Treat the root orchestrator as the main control point.
- Keep specialist roles narrow and execution-focused.
- Follow the shared policies before starting any work.
- Ask only simple, plain-language questions when a required value is truly missing.

## Core rule
Do not skip this repository. Do not improvise a different startup sequence. Read the control-room files first, then continue with the runtime flow defined in the manifest.
