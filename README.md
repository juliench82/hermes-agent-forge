# Hermes Bootstrap Prompt Set

This repository defines the bootstrap instructions Hermes should follow to build itself from the ground up.

## Structure
- `SOUL.MD` — main orchestrator identity and routing rules
- `profiles/orchestrator/skill.md` — orchestrator profile instructions
- `profiles/product-strategist/skill.md` — market and product brief profile
- `profiles/architect/skill.md` — technical blueprint profile
- `profiles/builder/skill.md` — implementation profile
- `profiles/quality-guardian/skill.md` — review profile
- `profiles/self-improver/skill.md` — continuous improvement profile
- `shared/workflows.md` — global workflow rules
- `shared/safety-gates.md` — safety and branching rules
- `shared/context-policy.md` — context and handoff rules

## How Hermes should use this repo
1. Read `SOUL.MD` first.
2. Read the relevant specialist `skill.md` for the current task.
3. Use the shared files for workflow, safety, and context rules.
4. Keep each profile focused on one job.
5. Do not duplicate global rules inside every specialist profile.

## Goal
A solo founder can provide a SaaS idea, and Hermes coordinates a small specialist team to turn it into a production-ready GitHub repository that can be deployed and improved over time.