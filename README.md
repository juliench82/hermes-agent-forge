# Hermes Bootstrap Prompt Set

This repository is a control-room contract for Hermes.

## What it is
A sidecar repository that documents, governs, and coordinates a small team of specialist agents.

## How to launch Hermes
Use this as the startup instruction:

> Load and follow the instructions in `juliench82/hermes-bootstrap-prompt-set` from start to finish. Read `BOOT.md` first, then `SOUL.MD`, then create the profiles and files exactly as specified, without asking questions unless a required value is truly missing.

## What this repository defines
- `BOOT.md` — startup entrypoint
- `SOUL.MD` — root orchestration profile
- `manifest.md` — machine-readable file map and sequence
- `starter-guide.md` — plain-language guide for end users
- `profiles/orchestrator/skill.md` — root orchestration profile instructions
- `profiles/product-strategist/skill.md` — intake and problem-shaping profile
- `profiles/architect/skill.md` — solution design profile
- `profiles/builder/skill.md` — implementation profile
- `profiles/quality-guardian/skill.md` — review profile
- `profiles/self-improver/skill.md` — continuous improvement profile
- `shared/workflows.md` — workflow rules used by all profiles
- `shared/safety-gates.md` — safety and branching rules used by all profiles
- `shared/context-policy.md` — context and handoff rules used by all profiles

## Boot order
1. Read `BOOT.md`.
2. Read `SOUL.MD`.
3. Read `manifest.md`.
4. Read `starter-guide.md` if you need plain-language context.
5. Create or verify the directory structure.
6. Create the shared files.
7. Create the specialist profile files.
8. Validate that the expected files exist.
9. Proceed with runtime orchestration.

## Operating rules
- One profile = one job.
- The main profile is the root orchestrator, not a specialist.
- Specialist profiles stay narrow and focused.
- Global rules live in shared files.
- Runtime behavior should remain consistent with the control-room contract.

## Audience
Regular people inside companies who want to automate repetitive work in plain language.
