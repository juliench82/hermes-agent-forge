# Hermes Agent Forge

Build, package, and operate domain-specific AI agents and multi-agent workflows.

Hermes Agent Forge is a modular framework for turning reusable agent profiles, capability packs, tool integrations, and tenant configuration into deployable automation systems.

## What it provides

- Reusable agent profiles and behavioral contracts
- Capability packs for domain-specific workflows
- Multi-tenant configuration and isolation
- Compilation and validation of agent definitions
- Runtime orchestration across models and tools
- Deployment patterns for local, VPS, and cloud environments
- Structured schemas, examples, and test fixtures
- Human-supervised automation with explicit governance and auditability

## Architecture

```text
Profiles + Packs + Tenant Configuration
                  |
                  v
              Compiler
                  |
                  v
       Validated Agent Bundles
                  |
                  v
       Runtime / Cloud Deployment
```

## Example use cases

Hermes can support agents for:

- Customer support and ticket triage
- E-commerce order monitoring and anomaly handling
- Appointment scheduling
- Lead qualification and CRM updates
- Document collection and administrative follow-up
- IT support and L1 ticket automation
- Reporting, notifications, and operational workflows

The goal is not to replace every business system. Hermes coordinates the systems already in use and gives operators a controlled, conversational interface to them.

## Repository structure

| Directory | Purpose |
|---|---|
| `profiles/` | Reusable agent identities, roles, and behavior |
| `packs/` | Capabilities and domain workflows |
| `tenants/` | Tenant-specific configuration |
| `compiler/` | Validation and bundle generation |
| `runtime/` | Agent execution and orchestration |
| `cloud/` | Deployment and infrastructure concerns |
| `schemas/` | Configuration and contract definitions |
| `examples/` | Reference implementations |
| `onboarding/` | Setup and adoption flows |
| `tests/` | Validation and regression coverage |

## Design principles

- Modular over monolithic
- Configuration over hard-coded behavior
- Human supervision over uncontrolled autonomy
- Portable deployments over vendor lock-in
- Explicit contracts over implicit prompt behavior
- Observable execution over black-box automation

## Status

Hermes Agent Forge is under active development. The repository currently focuses on the foundational architecture, schemas, profiles, packs, compilation workflow, and runtime integration needed to build production-oriented agents.

## Contributing

Contributions, experiments, feedback, and domain-specific agent packs are welcome. Please open an issue before making large architectural changes.