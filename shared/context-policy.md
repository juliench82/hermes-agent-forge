# Context Policy

This document defines how context files are discovered, loaded, and validated in Hermes Agents Forge.

## Alignment with Hermes Native Context File Handling

Hermes Agent automatically discovers and loads context files from your working directory.

See: https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files

### Context File Priority (Hermes Native)

1. **`HERMES.md`** / **`.hermes.md`** — Highest priority, walks to git root
2. **`AGENTS.md`** / **`.agents.md`** — Cross-tool standard
3. **`SOUL.md`** — Global to Hermes instance only
4. **Project skills** — Require `hermes skills trust`

### This Project's Context Files

| File | Location | Purpose |
|------|----------|---------|
| `HERMES.md` | Repo root | Hermes-specific instructions |
| `AGENTS.md` | Repo root | Cross-tool agent instructions |
| `skills/forge/SKILL.md` | Project skills | Forge skill definition |

## Context File Scanning (Hermes Layer 6)

Hermes scans all context files for prompt injection before loading (automatic).

See: https://hermes-agent.nousresearch.com/docs/user-guide/security

## Project-Local Skills

This project uses `skills/forge/SKILL.md` as a project-local skill.

**Required step for users**:
```bash
hermes skills trust
```

This is documented in `onboarding/START.md`, `HERMES.md`, and `AGENTS.md`.

## Related Docs

- `shared/safety-enforcement.md` — Security model overview
- `runtime/profile_assets.py` — Profile asset generation
