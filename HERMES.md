# Hermes Agents Forge — Hermes-Specific Context

> This file (`HERMES.md`) is the highest-priority context file for Hermes Agent.

## Project Overview

Hermes-native bootstrap repository for provisioning isolated multi-profile agent teams.

## Quick Start

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup --portal
hermes skills trust
python -m compiler --manifest bootstrap.manifest.json
```

## Key Hermes Features Used

| Feature | Usage | Docs |
|---------|-------|------|
| Profiles | Multi-profile team provisioning | [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) |
| Skills | `skills/forge/SKILL.md` | [Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) |
| MCP | Connectors map to MCP servers | [MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) |
| Cron | Triggers use native `cronjob` | [Cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) |
| Delegation | Orchestrator uses `delegate_task` | [Delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation) |
| Context Files | `HERMES.md`, `AGENTS.md`, `SOUL.md` | [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files) |
| Security | All 8 layers enforced | [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security) |

## Skills Trust (Important!)

This project uses project-local skills. **You must run**:

```bash
hermes skills trust
```

Without this, the forge skill won't load.

## Security Alignment

All runtime operations reference Hermes's 8-layer security model.

See: `shared/safety-enforcement.md`, `shared/safety-gates.md`

## Related Docs

- `AGENTS.md` — Cross-tool agent instructions
- `README.md` — User-facing overview
- `BOOTSTRAP.md` — Bootstrap manifest spec
- `CONTRIBUTING.md` — How to contribute
