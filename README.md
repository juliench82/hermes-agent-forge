![Hero image](https://raw.githubusercontent.com/juliench82/hermes-bootstraper/main/hero.png)

# Hermes Control Room — Isolated Profiles

Turn recurring company work into finished automation outcomes with a team of focused, isolated Hermes profiles.

## One prompt. Full control room.

Give Hermes this:

> `/goal Read and follow juliench82/hermes-bootstraper from start to finish. Set up the isolated-profile control room, install BUZZ and the Obsidian brain, create the isolated profiles, install each role's skill and shared policies, and make hermes-orchestrator the default user-facing profile. Ask me only for values that cannot be discovered safely.`

Hermes does the rest:
- Creates one native profile per role (orchestrator, strategist, architect, builder, quality, self-improver)
- Installs skills and policies
- Wires BUZZ as the task bus
- Seeds Obsidian as the shared brain
- Makes `hermes-orchestrator` the only profile you talk to

## Why this exists

Most AI assistants are one generic brain trying to do everything. This repo turns Hermes into a **control room**: a coordinated team of specialists that work together behind the scenes.

- **BUZZ** is the inter-agent task bus: profiles pass jobs, share status, and finish work without you juggling conversations.
- **Obsidian** is the shared brain: important context, notes, and decisions live in one place that all profiles can read and update.

You get a real automation team, not a chatbot.

## Architecture

- One native Hermes profile per role, with separate config, memory, sessions, and credentials
- BUZZ as the inter-profile task bus
- Obsidian as the durable shared context layer
- `scripts/` contains Hermes-run, idempotent helpers for profile, BUZZ, and vault provisioning

## Team

- **Orchestrator**: receives your requests, routes work, and delivers results
- **Product strategist**: turns requests into clear automation briefs
- **Architect**: designs deterministic, agentic, or hybrid solutions
- **Builder**: implements the solution
- **Quality guardian**: validates the work
- **Self improver**: proposes safe improvements

## Repository map

```text
BOOTSTRAP.md       # one-prompt setup contract
buzz-handoff.md    # BUZZ channel and envelope contract
scripts/           # Hermes-run provisioning helpers
profiles/          # specialist role contracts
shared/            # workflow, safety, and context policies
```

## For builders

This repo is a **power pack** for Hermes: it bootstraps the whole system, not just the idea. It's built on top of the Hermes framework and the BUZZ task bus protocol, so it works with the same foundation that companies already use.

Hermes asks short questions only for genuinely missing values, requests approval for irreversible actions, never exposes secrets, and returns useful outcomes rather than raw code.
