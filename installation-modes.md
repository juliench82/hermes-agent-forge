# installation-modes.md — Deployment Decision Guide

This file explains the two ways to deploy the Hermes control room and helps you choose the right one.

## Default mode: skill-routed

### What it is
One active Hermes profile becomes the root orchestrator. Six specialist role specifications are installed as Hermes skills inside that profile. The orchestrator routes work through those skills internally.

### What gets installed
- The active profile's `SOUL.md` is augmented with the root orchestrator identity and runtime rules.
- Six `SKILL.md` skills are created under `.hermes/skills/hermes-bootstraper/`:
  - `bootstraper-orchestrator`
  - `bootstraper-product-strategist`
  - `bootstraper-architect`
  - `bootstraper-builder`
  - `bootstraper-quality-guardian`
  - `bootstraper-self-improver`
- Three shared policy files are installed as reference files under the orchestrator skill:
  - `references/workflows.md`
  - `references/safety-gates.md`
  - `references/context-policy.md`

### When to use it
- You want a quick, tested setup.
- You interact with one Hermes assistant that handles everything.
- You do not need strict isolation between specialist roles.
- You are testing or starting out.

### Limitations
- All specialist roles share the same agent context, memory, and credentials.
- There is no hard boundary preventing role overlap.
- The orchestrator must self-discipline to avoid collapsing into a mega-agent.
- This mode does not require BUZZ for internal skill routing.

### Status
Tested. This is the result of a real six-minute bootstrap using the launch prompt on a Hermes installation.

## Advanced mode: isolated-profile

### What it is
Each specialist role becomes a separate native Hermes profile with its own `SOUL.md`, config, memory, sessions, skills, and credentials. A dedicated orchestrator profile coordinates work via a task bus.

### What gets installed
- Seven native Hermes profiles:
  - `hermes-orchestrator`
  - `hermes-product-strategist`
  - `hermes-architect`
  - `hermes-builder`
  - `hermes-quality-guardian`
  - `hermes-self-improver`
- Each profile receives its corresponding skill from `profiles/<role>/skill.md`.
- Each profile receives copies of the three shared policy files.
- BUZZ is configured as the inter-profile transport layer.
- A task bus or inter-profile handoff mechanism is configured.

### Provisioning commands (manual)
```bash
hermes profile create hermes-orchestrator
hermes profile create hermes-product-strategist
hermes profile create hermes-architect
hermes profile create hermes-builder
hermes profile create hermes-quality-guardian
hermes profile create hermes-self-improver
```

Then install the corresponding skill and shared policies into each profile, and wire BUZZ as the messaging layer.

### When to use it
- You need strict isolation between roles (different credentials, different memory, different risk boundaries).
- You want specialist agents to run independently, including on schedules.
- You are ready to configure and maintain a task bus and inter-profile routing.

### Limitations
- More complex to set up and maintain.
- Requires a reliable handoff mechanism between profiles.
- The bootstrap prompt does not automate this mode; it must be provisioned manually or via a separate script.
- The advanced topology is only valid once BUZZ is operational.

### Status
Design target. Not automated by the bootstrap prompt. Requires manual provisioning.

## How to choose

| Question | Default if yes | Advanced if yes |
|----------|----------------|-----------------|
| Do you want a quick, tested setup? | ✓ | |
| Do you interact with one assistant? | ✓ | |
| Do you need strict role isolation? | | ✓ |
| Do specialists need separate credentials? | | ✓ |
| Do specialists need independent schedules? | | ✓ |
| Are you ready to maintain a task bus? | | ✓ |

## Recommendation
Start with default mode. Test your automations. Move to advanced mode only when you need genuine isolation, independent scheduling, or separate credential boundaries for specific roles.
