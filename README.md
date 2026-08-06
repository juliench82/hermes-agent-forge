![Hermes Control Room](hero.png)

# Hermes Control Room

**A public reference implementation for designing dependable business automations with Hermes.**

A customer should be able to say, “Every Friday, prepare our unpaid-invoice summary and send it to finance,” without needing to install tools, understand agents, or maintain infrastructure. Hermes Control Room is the runtime design behind that experience: a default Hermes profile that orchestrates multiple focused native Hermes profiles to turn a business outcome into a safe, verified automation.

This repository is built in public. It demonstrates the architecture, policies, lifecycle contracts, and automation patterns behind a future managed Control Room offering.

> The product is the completed work—not the agent topology, YAML, or terminal commands behind it.

## What it is

Hermes Control Room is a multi-agent operating model for repeatable business work:

- A customer describes the result they want in ordinary language.
- The **default Hermes profile** acts as the orchestrator and coordinates specialist native profiles.
- Specialists convert the request into a plan, choose an implementation, build it, validate it, and return a usable outcome.
- Clear approval and safety gates prevent the system from silently taking sensitive or irreversible actions.

The repository is a reference runtime, not a hosted SaaS product. It contains no customer credentials, data, billing system, or shared production tenant.

## Architecture

The default profile is the customer-facing entry point and orchestrator. It routes work across the native Hermes profiles below; roles are deliberately separate so that planning, building, validation, and improvement do not collapse into one unbounded agent.

| Profile | Responsibility |
|---|---|
| **Orchestrator** | Receives requests, coordinates handoffs, enforces workflow state, and delivers outcomes |
| **Product Strategist** | Turns customer language into a concise automation brief |
| **Architect** | Selects deterministic, agentic, or hybrid implementation approaches |
| **Builder** | Implements the approved workflow and required integrations |
| **Quality Guardian** | Tests results, checks policy compliance, and blocks unsafe activation |
| **Self Improver** | Proposes small, reviewable improvements from operational evidence |

Profiles communicate through explicit handoffs and shared policy contracts. The default profile remains responsible for the customer experience and for enforcing final approval gates.

## Runtime lifecycle

```text
Customer outcome
  → Orchestrator intake
  → Product brief
  → Architecture plan
  → Build
  → Quality validation
  → Customer approval where required
  → Delivered outcome / scheduled automation
  → Reviewable improvement proposal
```

Example:

> “When a support ticket arrives, classify it, route it to the right team, and show me the draft before anything is sent.”

The result is not merely code. It is a scoped workflow with defined permissions, a validation path, an approval mode, and an observable outcome.

## What this demonstrates

This project is both a working reference implementation and a public development portfolio. It demonstrates:

- Multi-agent orchestration using native Hermes profiles
- Clear role and credential boundaries
- Prompt-first, Markdown-based runtime contracts
- Safe automation design: approvals, auditability, honest failure handling, and scoped access
- Cloud-portable runtime thinking: the same Control Room contract can run locally, on a managed Hermes Cloud tenant, or on self-hosted infrastructure
- An automation-pack model that turns successful bespoke workflows into repeatable products

## Repository map

```text
BOOTSTRAP.md          # Bootstrap instructions for the Control Room
README.md             # Public architecture and product positioning
buzz-handoff.md       # Inter-profile handoff contract

profiles/             # Native Hermes profile definitions
  orchestrator/
  product-strategist/
  architect/
  builder/
  quality-guardian/
  self-improver/

shared/               # Policies applied across the profile topology
  workflows.md
  safety-gates.md
  context-policy.md
  obsidian-policy.md

scripts/              # Optional setup and integration helpers
  profiles.sh
  buzz.sh
  obsidian.sh
```

## Data and safety model

Hermes Control Room follows several non-negotiable rules:

- Customer credentials, API keys, and private data never belong in this repository or in Markdown memory.
- External actions are gated by an explicit approval policy: draft-only, approval-required, or approved automatic execution.
- Profiles receive the minimum context, access, and credentials needed for their role.
- The quality guardian must be able to block activation when acceptance criteria or policy requirements are not met.
- Failures are surfaced honestly with actionable diagnostics; the system must never claim an action succeeded when it did not.
- Any future managed deployment must isolate each customer’s data, secrets, schedules, memory, and audit trail.

The optional Obsidian integration uses a scoped vault folder and explicit read/write boundaries; see `shared/obsidian-policy.md`.

## Deployment stance

The Control Room architecture is deliberately runtime-agnostic:

- **Reference/local:** a developer runs Hermes and provisions the profile topology from this repository.
- **Managed cloud:** a provider operates dedicated customer tenants, handles maintenance, and exposes a simple customer-facing activation flow.
- **Self-hosted:** a customer or partner deploys the same profile topology inside their own infrastructure.

The public repository defines the runtime and its contracts. A future private platform would handle customer identity, tenant provisioning, OAuth, encrypted secret storage, billing, operations, and support.

## Roadmap

Current foundation:

- Native multi-profile Control Room coordinated by the default Hermes profile
- Buzz handoff and profile provisioning helpers
- Optional scoped Obsidian integration
- Shared workflow, safety, and context policies

Next:

1. Customer onboarding contracts: a durable Customer Blueprint, connector authorisation flow, activation review, and acceptance criteria
2. Tenant/runtime contracts: cloud and self-hosted provider-neutral lifecycle definitions
3. Demonstrable automation packs with fixtures, validation, and safe demo modes
4. Tenant operations: audit events, upgrades, rollback, support boundaries, and data lifecycle policies

## Building in public

Each change is intended to be inspectable and useful:

- Read the architecture and profile contracts.
- Follow individual branches and pull requests as the product evolves.
- Reuse the ideas for your own Hermes deployment.
- Use issues and discussions to challenge the design, especially around safety, tenant isolation, and operational reliability.

If you are a business user, the eventual experience should be much simpler: connect the tools you already use, describe the job that keeps recurring, review the plan, and let the Control Room handle it.
