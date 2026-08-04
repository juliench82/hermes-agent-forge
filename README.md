# Hermes Bootstrap Prompt Set

This repository is a bootstrap contract for Hermes.

## How to launch Hermes
Use this as the startup instruction:

> Load and follow the instructions in `juliench82/hermes-bootstrap-prompt-set` from start to finish. Read `SOUL.MD` first, then create the profiles and files exactly as specified, without asking questions unless a required value is truly missing.

## What this repository defines
- `SOUL.MD` — the root orchestration file for the main profile
- `profiles/orchestrator/skill.md` — the main orchestration profile instructions
- `profiles/product-strategist/skill.md` — product and market brief profile
- `profiles/architect/skill.md` — technical blueprint profile
- `profiles/builder/skill.md` — implementation profile
- `profiles/quality-guardian/skill.md` — review profile
- `profiles/self-improver/skill.md` — continuous improvement profile
- `shared/workflows.md` — workflow rules used by all profiles
- `shared/safety-gates.md` — safety and branching rules used by all profiles
- `shared/context-policy.md` — context and handoff rules used by all profiles

## Boot order
1. Read `SOUL.MD`.
2. Create the directory structure.
3. Create the shared files.
4. Create the specialist profile files.
5. Validate that the expected files exist.
6. Proceed with the workflow.

## Operating rules
- One profile = one job.
- The main profile is the root orchestrator, not a specialist.
- Specialist profiles stay narrow and focused.
- Global rules live in shared files.
- Runtime behavior should remain consistent with the bootstrap contract.

## Goal
A regular person inside a company can describe a repetitive process in plain language, point Hermes at this repository, and get back a team of agents that can design and deliver either deterministic workflows or agentic AI automations, then return a simple human-friendly result such as an email containing the completed output.
