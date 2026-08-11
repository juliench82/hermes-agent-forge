# Hermes Agents Forge

Hermes Agents Forge is a Hermes-native bootstrap repository. It does not install a preselected business team or predict a customer’s domain. Instead, the fresh Hermes default profile prepares the Hermes environment, then Hermes discovers the customer-specific team from free-text goals.

## The key idea

There are two different kinds of profiles:

1. **Bootstrap controller** — the fresh Hermes default/main profile. This is the platform control plane that reads this repository, prepares and verifies its own assets, runs onboarding, supervises provisioning, and escalates unresolved failures to the human administrator.
2. **Customer team** — profiles designed dynamically by Hermes after onboarding. Names, roles, descriptions, capabilities, and skills are generated from the customer’s objective and are never selected from a repository-side domain catalog.

The fixed bootstrap controller is not a fixed customer team. It exists so Hermes can set itself up safely before it designs any customer-specific specialists.

The detailed architecture and roadmap are documented in [`REVISED_PLAN_V2.md`](REVISED_PLAN_V2.md).

## Target lifecycle

```text
fresh Hermes install
  -> read BOOTSTRAP.md and bootstrap.manifest.json
  -> prepare the default/main profile
  -> inspect the installed Hermes CLI and version
  -> create or update verified bootstrap assets
  -> configure administrator notification policy
  -> collect free-text customer onboarding
  -> Hermes designs the required team
  -> validate the proposal
  -> resolve or create capabilities
  -> show a complete reviewable plan
  -> require approval of that exact plan
  -> create dynamic profiles
  -> install and verify skills
  -> generate and verify SOUL.md/config.yaml
  -> run bounded repair loops when needed
  -> notify the administrator on unresolved failure
  -> report truthful state
```

The repository orchestrates and verifies this lifecycle. Hermes performs the domain reasoning and proposes the team.

## Bootstrap controller

The default Hermes profile is instructed to act as the Forge bootstrap controller. Its generic responsibilities include:

- repository and manifest inspection;
- actual Hermes CLI/version discovery;
- main-profile asset preparation;
- semantic team design;
- skill resolution and post-install verification;
- installation-ledger analysis;
- bounded recovery;
- human-administrator escalation.

The controller must not invent commands, configuration keys, profile paths, or skill identifiers. It must use command output, filesystem state, and installed-skill inspection as evidence.

Main-profile files are generated or updated according to an explicit preservation policy. Existing `SOUL.md` and `config.yaml` files are not silently overwritten.

## Dynamic customer teams

Onboarding collects:

- what the user wants to accomplish;
- the user’s role;
- free-text goals and workflows;
- optional team-size preference;
- constraints and approval expectations as needed.

Hermes then proposes a team. The repository validates safe names, unique profiles, descriptions, and non-empty capabilities. The current lifecycle supports teams of three, five, or seven profiles, but contains no predefined team for any customer category.

Each profile may have one to ten capabilities or skills. One is valid; ten is the upper complexity bound. Semantic capability labels are not automatically treated as installable skills.

## Skills and verification

A capability is a semantic requirement. An installable skill is an observed Hermes artifact, a validated bootstrap skill, or a validated local/custom skill.

The resolution sequence is:

```text
semantic capability
  -> Hermes searches or designs a candidate
  -> exact identity is checked against observed output
  -> candidate appears in the approval plan
  -> approved candidate is installed or created
  -> Hermes and machine checks verify the result
```

The repository does not guess catalog slugs. A display name is not sufficient evidence of an installable identity. If Hermes cannot resolve or verify a capability, provisioning stops safely.

## Approval and recovery

No customer profile, skill, or asset side effect occurs before the complete plan is displayed and explicitly approved. Approval must eventually be bound to the exact plan, not merely to a general installation request.

Failures are recorded per profile, skill, and asset. Hermes may diagnose and repair within bounded iteration limits. If recovery is exhausted, the state becomes `admin_action_required`; the customer receives a simple paused-setup message while the human administrator receives the detailed ledger and remediation context.

Completion is based on observed evidence, including subprocess results, filesystem checks, installed-skill inspection, and semantic consistency review. A command invocation alone is never success.

## Repository contract

- [`BOOTSTRAP.md`](BOOTSTRAP.md) — canonical human bootstrap instructions.
- [`bootstrap.manifest.json`](bootstrap.manifest.json) — machine-readable discovery contract.
- [`REVISED_PLAN_V2.md`](REVISED_PLAN_V2.md) — current architecture and phased implementation plan.
- [`onboarding/`](onboarding/) — generic onboarding material and templates.
- [`compiler/`](compiler/) — prompt generation, response parsing, and structural validation.
- [`runtime/`](runtime/) — orchestration, provisioning, skill resolution, state, policy, and verification boundaries.
- [`profiles/`](profiles/) — repository reference material only; not a customer-domain team catalog.
- [`tests/`](tests/) — deterministic compatibility and lifecycle coverage.

## Safety rules

- No customer-domain mappings or predefined customer teams.
- No guessed skill identifiers.
- No shell interpolation or `shell=True`.
- No secrets in prompts, plans, generated assets, or logs.
- No unbounded model, command, or repair loops.
- No silent overwrites of existing profile assets.
- No claim of completion without verification.
- Live Hermes tests are opt-in and isolated; ordinary CI remains deterministic.

## Current status

PR #43 wired the generic onboarding lifecycle into the canonical installer path. The next implementation phase is the bootstrap controller: main-profile preparation, evidence-based skill verification, durable approval/state binding, bounded recovery, and administrator escalation.

Live Hermes provisioning has not been claimed as validated until the opt-in acceptance suite passes against the installed Hermes version.

## Validation

Deterministic tests can be run with:

```bash
python -m unittest discover
```

Live acceptance is deliberately opt-in:

```bash
HERMES_LIVE_TESTS=1 python -m unittest discover
```

Use an isolated Hermes home/profile root for live runs and review the resulting state ledger before treating the installation as complete.
