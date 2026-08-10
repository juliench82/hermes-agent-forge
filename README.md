# Hermes Agent Forge

> Bootstrap repository for Hermes: discover the bootstrap contract, run onboarding, and provision isolated multi-profile agent teams for real-world workflows.

## Purpose

This repository is not primarily an application repository that Hermes should modify. It is the bootstrap source that Hermes reads when it starts the Hermes Agent Forge experience.

The intended entry point is the repository itself:

`https://github.com/juliench82/hermes-agent-forge`

When Hermes is given this repository link, it must read the bootstrap files and start the onboarding flow. The repository describes how to determine a user's objective, select the right specialist profiles, define their permissions and isolation boundaries, and provision a usable agent team.

This distinction is essential:

- **Bootstrap repository:** this repository. It defines Hermes Agent Forge, its profiles, onboarding rules, schemas, examples, policies, and reference workflows.
- **User project repository:** an optional repository belonging to the user or the user's company. It may be connected later when the selected use case requires code inspection or implementation work.

The bootstrap repository must never be confused with the SaaS or application repository that a team may eventually operate on.

## Intended experience

The target user experience is:

1. The user starts Hermes and provides the Hermes Agent Forge repository link.
2. Hermes reads the root bootstrap instructions and discovers the repository structure.
3. Hermes starts an interactive onboarding instead of asking the user to edit JSON or write prompts manually.
4. The user describes their objective, business, project stage, tools, constraints, and desired level of autonomy.
5. Hermes identifies the required capabilities and proposes a team of specialized profiles.
6. Hermes shows the proposed profiles, responsibilities, tools, permissions, isolation model, workflows, and approval gates.
7. The user approves or adjusts the proposed team.
8. Hermes creates the runtime team from the generated configuration.
9. The user interacts primarily with the orchestrator, which delegates work to the isolated specialist profiles.

The bootstrap link is therefore a product activation mechanism. It is not a request to work on this repository and it is not equivalent to connecting a customer's codebase.

## Bootstrap reading contract

Hermes should treat the repository as a discoverable bootstrap contract and inspect the following areas in this order:

1. `BOOTSTRAP.md` — activation and bootstrap instructions.
2. `bootstrap.manifest.json` — machine-readable bootstrap discovery contract.
3. `README.md` — product purpose, operating model, and expected experience.
4. `onboarding/` — onboarding questions, activation flow, connector authorization, templates, and examples.
5. `profiles/` — available specialist roles and their boundaries.
6. `schemas/` — machine-readable contracts for tenants, bundles, runtime configuration, and compatibility.
7. `catalog/` — available primitives and supported capabilities.
8. `packs/` — reusable workflow packs.
9. `examples/` — reference tenant specifications, including the solo-founder app-builder scenario.
10. `runtime/` — enforcement concepts such as policies, confirmations, audit logging, secrets, and isolation.
11. `tests/` — compatibility, golden, renderer, adapter, and runtime expectations.

The implementation may evolve, but these conceptual boundaries must remain discoverable. Hermes should prefer the machine-readable schemas and examples for provisioning and use the Markdown files for human-readable instructions and onboarding context.

Sprint 4 status: discovery is implemented via `bootstrap.manifest.json` and `compiler/bootstrap_discovery.py`. Recognition of this repository as a bootstrap source does **not** yet mean a team has been provisioned.

## Onboarding model

The onboarding must be adaptive. Users should describe the outcome they want; they should not need to know the names of internal profiles or manually construct a `TenantSpec`.

The onboarding should discover at least:

- the user's business or product objective;
- the type of workflow to automate;
- whether the user is a solo founder, a small team, or an agency;
- the project stage: idea, validation, MVP, growth, maintenance, or operations;
- whether an existing user project repository must be inspected;
- the application stack and infrastructure, when relevant;
- required connectors such as GitHub, Supabase, Google Drive, email, finance, or messaging;
- the data sensitivity and secrets involved;
- which actions are read-only, reversible, or irreversible;
- the desired autonomy level;
- human approval requirements;
- escalation and reporting preferences.

The onboarding output is a generated team manifest. Conceptually, it contains:

```json
{
  "team": {
    "name": "my-saas-team",
    "profiles": [
      "orchestrator",
      "product-strategist",
      "architect",
      "builder",
      "quality-guardian"
    ]
  },
  "integrations": ["github", "supabase"],
  "permissions": {
    "read_repository": true,
    "create_branch": true,
    "create_pull_request": true,
    "merge_pull_request": false,
    "deploy_production": false
  },
  "isolation": {
    "workspace_per_agent": true,
    "shared_context": "controlled"
  },
  "approval_policy": "human-in-the-loop"
}
```

This example is conceptual. The canonical field names and validation rules must come from the schemas in this repository.

## Initial target: solo-founder SaaS/apps

The first complete end-to-end onboarding target is a solo founder building a SaaS or application.

The recommended baseline team is:

| Profile | Responsibility | Default authority |
|---|---|---|
| `orchestrator` | Understand the request, plan work, delegate, consolidate results | High coordination authority; no unapproved side effects |
| `product-strategist` | Clarify the problem, users, priorities, scope, and acceptance criteria | Analysis and specification |
| `architect` | Propose technical design, boundaries, data flows, and trade-offs | Read-only analysis and design |
| `builder` | Implement approved work, add tests, and prepare changes | Isolated workspace and branch |
| `quality-guardian` | Test, review, check regressions, security, and release readiness | Read/test/review; no merge by default |

Optional profiles such as `self-improver` should be added only when evaluation, audit, and rollback behaviour are reliable enough to justify them.

The expected first workflow is:

```text
founder request
  -> orchestrator
  -> product strategist: brief and acceptance criteria
  -> architect: technical proposal
  -> builder: isolated implementation and tests
  -> quality guardian: validation report
  -> human approval
  -> optional external action
```

The founder should normally interact with the orchestrator rather than manually coordinating every specialist.

## Isolation and safety

Every profile must have an explicit identity, workspace, context boundary, tool policy, and approval policy. Profiles should share only the minimum context required for collaboration.

The default policy for a newly provisioned team is:

- reading is allowed only for explicitly authorised sources;
- implementation happens in an isolated workspace or branch;
- external writes require an approval gate unless explicitly classified as safe;
- merges, production deployments, production migrations, financial actions, and external communications are not automatic by default;
- all important actions and decisions are auditable;
- secrets are referenced through the runtime secret mechanism and must not be placed in prompts, Markdown, or tenant specifications.

The runtime enforcement layer is responsible for policy proxying, confirmations, audit logging, isolation, and secret handling. Profiles must not bypass those controls.

## User project repositories

Connecting a user project repository is a separate capability from bootstrapping Hermes Agent Forge.

It becomes relevant only after onboarding has determined that the selected use case needs repository work, for example:

- inspect an existing SaaS codebase;
- analyse architecture or technical debt;
- implement a feature;
- create tests or migrations;
- open a pull request;
- maintain an application over time.

In that situation, the user project repository is an input to the provisioned team. It must not replace or obscure the bootstrap repository. Hermes should first read and apply the bootstrap contract, then request authorisation for any additional repository or connector required by the selected workflow.

## Use-case library

The same onboarding and team-provisioning mechanism must support multiple real-world use cases. The team should vary according to the objective rather than always loading every available profile.

Reference categories include:

- solo-founder SaaS/app development;
- e-commerce customer support and order anomaly handling;
- appointment scheduling for local services;
- quotes, invoice follow-up, and payment administration;
- medical-office administration with appropriate privacy boundaries;
- legal or consulting case and deadline tracking;
- real-estate lead qualification and dossier follow-up;
- restaurant reservations and review handling;
- accounting document collection and reporting;
- marketing outbound and nurturing;
- freelancer back-office administration;
- training cohort management;
- IT/MSP level-one support.

Each use case should eventually define onboarding questions, recommended profiles, allowed connectors, workflow packs, approval policies, isolation requirements, and evaluation tasks.

## Product boundaries

This repository is intended to define and bootstrap an agent-team product. It is not intended to require the user to:

- clone the repository manually as the normal onboarding experience;
- edit profile files by hand;
- write a custom system prompt for every agent;
- construct a tenant manifest from scratch;
- understand internal compiler or runtime modules before starting;
- point Hermes at this repository as if it were the user's application code.

Manual editing remains useful for development, fixtures, tests, and advanced operators, but it is not the target user experience.

The project should not assume that new custom Hermes commands can be added. The preferred activation mechanism is repository discovery and bootstrap-file reading through Hermes' existing capabilities. If a native Hermes command already exists for repository or bootstrap ingestion, this repository should document and use that mechanism rather than inventing a parallel command interface.

## Current implementation direction

The repository contains the main conceptual building blocks:

- specialist profile definitions;
- onboarding documentation and workflow artifacts;
- tenant and bundle schemas;
- platform/catalog primitives;
- deterministic planning and rendering concepts;
- Hermes adapter and solo-founder compatibility path;
- golden compatibility and adapter tests;
- runtime enforcement concepts for policy, audit, confirmation, isolation, and secrets;
- **Sprint 4 bootstrap discovery contract** (`bootstrap.manifest.json`, schema, loader, tests).

The remaining product-level goal is to connect these pieces into the user experience described above: repository-triggered bootstrap, adaptive onboarding, team recommendation, explicit approval, team provisioning, and immediate interaction through the orchestrator.

The existence of a profile, schema, example, or runtime module must not be presented as proof that the complete end-to-end onboarding is already available. The README, `BOOTSTRAP.md`, schemas, tests, and actual runtime behaviour must stay aligned.

## Definition of done

The project reaches its primary goal when a user can:

1. give Hermes the URL of this repository;
2. have Hermes discover and read the bootstrap contract;
3. complete an adaptive onboarding without hand-editing configuration;
4. receive a proposed team tailored to the selected use case;
5. review profiles, tools, permissions, isolation, and approval gates;
6. approve the configuration;
7. start the team;
8. speak to the orchestrator;
9. have isolated specialists collaborate on the selected workflow;
10. connect a separate user project repository only when the workflow requires it;
11. observe auditable, reviewable results and safely stop or reconfigure the team.

The solo-founder SaaS/apps scenario should be the first complete acceptance test before expanding the catalogue to additional business use cases.

## Repository map

- `BOOTSTRAP.md` — bootstrap activation instructions.
- `bootstrap.manifest.json` — machine-readable bootstrap discovery contract.
- `onboarding/` — onboarding flow, templates, connector authorization, activation review, and examples.
- `profiles/` — specialist agent profiles.
- `schemas/` — machine-readable contracts.
- `catalog/` — supported platform primitives.
- `packs/` — reusable workflow packs.
- `examples/` — reference tenant specifications.
- `runtime/` — runtime policy, confirmation, audit, isolation, and secret-handling components.
- `compiler/` — deterministic planning, rendering, and bootstrap discovery.
- `tests/` — compatibility and enforcement expectations.

## Guiding principle

Hermes Agent Forge should make the creation of a useful, safe, specialised agent team feel like onboarding a product—not like assembling a software repository by hand.
