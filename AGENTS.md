# Hermes Agents Forge — Agent Instructions

## Project Purpose

Hermes Agents Forge is a **Hermes-native bootstrap repository** that provisions isolated multi-profile agent teams from declarative manifests. Point your Hermes agent at this repo and it can:

1. **Discover** bootstrap manifests (`bootstrap.manifest.json`) in the wild
2. **Compile** tenant specs into profile bundles with roles, connectors, triggers, and policies
3. **Provision** isolated Hermes profiles with dynamic skills, context files, and MCP integrations
4. **Onboard** users via guided workflows with acceptance criteria and audit trails

## Architecture

```
├── bootstrap.manifest.json    # Declarative team spec (schema: schemas/bootstrap-manifest.v1.schema.json)
├── compiler/                   # Bootstrap discovery, team compilation, rendering
├── runtime/                    # Profile provisioning, skill resolution, policy enforcement
├── catalog/                    # Versioned primitives (roles, connectors, triggers, memory, policies)
├── onboarding/                 # Templates, workflows, fixtures for user onboarding
├── shared/                     # Cross-cutting contracts (security, context, skill, workflow policies)
├── skills/forge/               # Project-local forge skill (SKILL.md)
└── site/                       # Public website with llms.txt for LLM discoverability
```

## Key Conventions

- **Manifests over code**: Team specs are declarative JSON/YAML, compiled by `compiler/`
- **Versioned primitives**: Catalog entries use semantic versioning (`1.0.0/primitive.yaml`)
- **Hermes-native alignment**: Connectors map to MCP servers, triggers to `cronjob`, delegation to `delegate_task`
- **Security by design**: All runtime operations reference Hermes's 8-layer security model (see `shared/safety-enforcement.md`)

## Getting Started

```bash
# Install Hermes (if not already installed)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Trust project-local skills
hermes skills trust

# Run the bootstrap compiler
python -m compiler --manifest bootstrap.manifest.json
```

## Testing

```bash
pytest tests/ -v --cov
```

## Related Docs

- `HERMES.md` — Hermes-specific context (highest priority, git-root scoped)
- `BOOTSTRAP.md` — Bootstrap manifest specification
- `README.md` — User-facing overview
- `CONTRIBUTING.md` — How to contribute
