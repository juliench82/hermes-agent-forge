# Hermes Control Room — Isolated Profiles Only

This branch is the long-term control-room architecture. It is not a v1 compatibility branch, and it does not present a skill-routed fallback.

The repository exists to let Hermes bootstrap a multi-agent control room directly:
- one native profile per role,
- BUZZ as the inter-profile transport layer,
- the Obsidian brain as the shared memory layer,
- prompt-first startup instructions with explicit fallback behavior when a surface or CLI command does not exist.

## What the control room does

Hermes reads the control-room prompt and provisions the topology it needs:
1. create or verify the isolated profiles,
2. configure BUZZ identities and channels,
3. seed the Obsidian brain,
4. install each role's skill and shared policy files,
5. validate the task bus,
6. begin orchestration only after the topology is verified.

## Design rules

- The branch is isolated-profile only.
- Do not reintroduce v1 root docs or a skill-routed alternative.
- Do not hardcode a CLI shape if Hermes can be instructed to do the job directly.
- If a preferred command does not exist, fall back to the next clear method in the prompt.
- Never invent hidden commands and never silently skip a bootstrap step.

## Branch layout

```text
BOOTSTRAP.md        # Root control-room contract for the branch
buzz-handoff.md     # BUZZ task-bus contract and envelope shape
scripts/            # Optional deterministic helpers for fragile operations
profiles/           # Role skill source contracts
shared/             # Shared policy files
```

## Why this shape

The early v1 control room taught a useful lesson: the docs should describe the intended system plainly, and the runtime should only be forced to use deterministic helpers where the environment is actually fragile. That keeps the control room readable while still making the advanced path executable.

## Status

Active branch: isolated-profile only.
