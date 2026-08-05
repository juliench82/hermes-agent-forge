# advanced/BOOTSTRAP.md — Isolated-Profile Control Room

This branch is **isolated-profile only**. There is no v1 fallback here. The control room itself is the bootstrap contract: Hermes reads the prompt, understands the topology, and provisions the advanced system without relying on a separate installer scaffold.

## What this branch contains
- One native Hermes profile per role.
- BUZZ as the inter-profile transport layer.
- The Obsidian brain as the shared memory layer.
- Prompt-first orchestration with fallback instructions when a command or surface does not exist.

## Operating principle
The control room should not force a specific CLI shape unless the runtime actually exposes it. Instead, it tells Hermes what outcome to achieve, what to verify, and what to do when a preferred command is unavailable.

## Prompt-first startup sequence
1. Read the branch root intention: isolated-profile only.
2. Verify Hermes core and the current role context.
3. Ask Hermes to create the isolated profiles it needs, one per role.
4. Ask Hermes to provision BUZZ identities and channels for those profiles.
5. Ask Hermes to initialize the Obsidian brain and seed the shared vault.
6. Ask Hermes to install the role skills and shared policy files into each profile.
7. Ask Hermes to configure handoff channels and validate the task bus.
8. If a preferred CLI command does not exist, Hermes must fall back to the next clearly stated method in the prompt.
9. Begin runtime orchestration only after the topology is verified.

## Fallback rule
If Hermes cannot find a CLI command named in a step, it should:
- search for the equivalent built-in action,
- otherwise perform the task through the most direct available Hermes surface,
- otherwise ask one short clarification question.

Never invent a hidden command. Never silently skip a bootstrap step.

## Success criteria
- The branch stays isolated-profile only.
- The advanced topology can be understood and executed from the prompt itself.
- BUZZ and Obsidian are initialized as part of the control room flow, not as a sidecar project.
- Fallback behavior is explicit and safe.
