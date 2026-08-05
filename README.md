![Hero image](https://raw.githubusercontent.com/juliench82/hermes-bootstraper/main/hero.png)

# Hermes Control Room — Isolated Profiles

Hermes Control Room turns recurring company work into finished automation outcomes through a team of focused, isolated Hermes profiles.

## Goal prompt

The cleanest way to start is:

> `/goal Read and follow `juliench82/hermes-bootstraper` from start to finish. Set up the isolated-profile control room, install BUZZ and the Obsidian brain, create the isolated profiles, install each role's skill and shared policies, and make hermes-orchestrator the default user-facing profile. Ask me only for values that cannot be discovered safely.`

This keeps the user experience simple while still telling Hermes exactly what needs to be completed.

## Start with one prompt

Non-technical users do not run commands or configure agents. Give Hermes this:

> Read and follow `juliench82/hermes-bootstraper` from start to finish. Read `BOOTSTRAP.md` first. Set up the isolated-profile control room, BUZZ, and the Obsidian brain. Run the repository scripts yourself. Ask me only for values that cannot be discovered safely.

Hermes provisions the profiles, shared Obsidian brain, and BUZZ task bus itself. When bootstrap succeeds, **`hermes-orchestrator`** is the default and only profile the user talks to; it routes work to the specialist team.

## Architecture

- One native Hermes profile per role, with separate config, memory, sessions, and credentials.
- BUZZ is the inter-profile task bus.
- Obsidian is the durable shared context layer.
- `scripts/` contains Hermes-run, idempotent helpers for profile, BUZZ, and vault provisioning.

## Team

- Orchestrator: receives user requests, routes work, and delivers results.
- Product strategist: request to automation brief.
- Architect: deterministic, agentic, or hybrid design.
- Builder: implementation.
- Quality guardian: validation.
- Self improver: safe improvement proposals.

## Repository map

```text
BOOTSTRAP.md       # one-prompt setup contract
buzz-handoff.md    # BUZZ channel and envelope contract
scripts/           # Hermes-run provisioning helpers
profiles/          # specialist role contracts
shared/            # workflow, safety, and context policies
```

Hermes asks short questions only for genuinely missing values, requests approval for irreversible actions, never exposes secrets, and returns useful outcomes rather than raw code.
