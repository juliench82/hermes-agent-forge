# BOOTSTRAP.md — Hermes Agent Forge

Read this file first.

## What this repository is

This repository is a **Hermes bootstrap source**, not a user application repository.

When Hermes is given:

`https://github.com/juliench82/hermes-agent-forge`

it must treat the repository as a product activation contract for **Hermes Agent Forge**.

It must **not**:

- treat this repository as the user's SaaS or application codebase;
- begin feature implementation against this repository by default;
- invent custom Hermes commands;
- provision a multi-profile team before onboarding and explicit approval;
- connect a separate user project repository until onboarding determines that one is required.

## Machine-readable entrypoint

Canonical human entrypoint: `BOOTSTRAP.md` (this file).

Canonical machine-readable entrypoint: `bootstrap.manifest.json`

Schema: `schemas/bootstrap-manifest.v1.schema.json`

Discovery loader (read-only): `compiler/bootstrap_discovery.py`

```text
sourceType: hermes-bootstrap
role: bootstrap
userProjectRepository: false
nextStep: onboarding
provisionTeam: false
```

## Discovery order

Hermes should inspect the repository in this order:

1. `BOOTSTRAP.md` — activation and bootstrap instructions (this file)
2. `bootstrap.manifest.json` — machine-readable bootstrap contract
3. `README.md` — product purpose and operating model
4. `onboarding/` — onboarding questions, activation flow, templates, examples
5. `profiles/` — available specialist roles and boundaries
6. `schemas/` — machine-readable contracts
7. `catalog/` — platform primitives and capabilities
8. `packs/` — reusable workflow packs
9. `examples/` — reference tenant specifications (including solo-founder SaaS)
10. `runtime/` — policy proxy, confirmation gates, audit log, isolation, secrets
11. `tests/` — compatibility and contract expectations

Prefer machine-readable schemas, manifests, and examples for validation. Prefer Markdown for human-readable instructions and onboarding context.

## Sprint 4 expected behaviour

After successful discovery, Hermes should be able to conclude:

```text
Repository recognised: hermes-bootstrap
Bootstrap repository: juliench82/hermes-agent-forge
Entrypoint: BOOTSTRAP.md
Onboarding entrypoints: onboarding/START.md, onboarding/manifest.md
Required profiles discoverable:
  - orchestrator
  - product-strategist
  - architect
  - builder
  - quality-guardian
Optional profiles (not enabled by default):
  - self-improver
User project repository: not connected
Team status: not provisioned
Next step: onboarding
```

Sprint 4 stops here. Discovery must not start specialists, create workspaces, write external systems, or activate connectors.

## What comes next

1. **Sprint 5 — Adaptive onboarding**
   Read `onboarding/START.md` and run a business-oriented decision flow.
   Output: a proposed team manifest for user review.
2. **Sprint 6 — Team compiler and provisioning**
   Compile the approved onboarding result into isolated profile instances using Sprint 3 runtime primitives.
3. **Sprint 7 — Hermes activation path**
   Prove the full repository-link experience through orchestrator startup.

Until those stages are implemented and validated, Hermes must not claim that end-to-end team activation is complete merely because profiles, schemas, or examples exist.

## Baseline team (reference only)

The first target use case is a solo founder building SaaS products or applications.

Default enabled profiles after a future approved onboarding:

| Profile | Responsibility |
|---|---|
| `orchestrator` | Receive founder requests, plan, delegate, consolidate |
| `product-strategist` | Users, problems, priorities, scope, acceptance criteria |
| `architect` | Technical design, boundaries, data flows, trade-offs |
| `builder` | Implement approved work in an isolated workspace or branch |
| `quality-guardian` | Tests, regressions, security, readiness |

`self-improver` remains optional and disabled by default.

## Safety rules

- No secrets in Markdown, manifests, examples, or prompts.
- No external writes, merges, deployments, migrations, financial actions, or external communication without an explicit approval gate.
- Runtime enforcement (policy proxy, confirmation, audit, isolation, secrets) remains authoritative once a team is provisioned in later sprints.
- The bootstrap repository stays read-oriented during discovery.

## Validation

Run:

```bash
python -m unittest tests.test_bootstrap_discovery
```

Successful tests confirm that the bootstrap manifest exists, referenced paths exist, onboarding entrypoints exist, required profiles are discoverable, required schemas are present, and at least one use-case example exists.

## Core rule

Do not improvise a different product path.

1. Read this file.
2. Load `bootstrap.manifest.json`.
3. Validate discovery.
4. Identify the repository as `hermes-bootstrap`.
5. Stop before team provisioning until onboarding is completed and approved.
