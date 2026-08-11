# Hermes Agents Forge — Revised Plan v2

## Status and intent

This document supersedes the previous strategic plan for the next implementation phase. It preserves the core principle that Hermes sets itself up, while making one platform-level distinction explicit:

- The fresh Hermes default/main profile is the bootstrap controller.
- Customer-specific specialist profiles are discovered and created dynamically after onboarding.
- The repository must never encode customer-domain-to-team mappings.

The bootstrap controller is a fixed platform role, not a fixed customer team. It exists so a fresh Hermes installation has a trustworthy entrypoint capable of reading this repository, preparing the local Hermes environment, supervising onboarding, and escalating failures to the human administrator.

The current repository has merged the generic onboarding lifecycle and installer wiring in PR #43. The next work must close the gap between deterministic mocked orchestration and a verified, recoverable, Hermes-native bootstrap.

## Core architecture

The system has two layers.

### Layer A: bootstrap controller

The default Hermes profile is responsible for:

1. Reading `BOOTSTRAP.md`, `bootstrap.manifest.json`, `README.md`, and this plan.
2. Inspecting the installed Hermes version and actual CLI help before using commands.
3. Preparing its own profile assets and generic bootstrap skills.
4. Verifying its own configuration, skills, workspace, and runtime health.
5. Collecting administrator notification preferences and safety constraints.
6. Collecting generic customer onboarding answers in free text.
7. Asking Hermes to analyze the customer context and propose a team.
8. Resolving, creating, or rejecting capabilities using observed Hermes evidence.
9. Displaying a complete plan and obtaining explicit approval.
10. Creating and configuring the discovered profiles.
11. Verifying files, installed skills, profile isolation, and command results.
12. Running bounded repair loops when verification fails.
13. Escalating unresolved failures to the human administrator.
14. Reporting only observed installation state.

The controller may use Hermes reasoning for analysis, diagnosis, repair, and semantic verification. Machine completion state must still be grounded in subprocess results, filesystem evidence, and installed-skill inspection.

### Layer B: dynamically discovered customer team

After onboarding, Hermes proposes the smallest effective team for the user’s objective. The repository does not know the customer’s sector, workflow, role, or required specialists in advance.

For each generated profile, Hermes supplies:

- a safe unique profile name;
- a role description;
- collaboration and handoff expectations;
- one to ten semantic capability labels;
- optional constraints and verification criteria.

The repository validates structure and safety, but does not translate customer categories into profile names. The team may contain three, five, or seven profiles under the current lifecycle contract; this is a provisioning constraint, not a catalog of fixed teams.

## Bootstrap sequence

The target fresh-install experience is:

```text
fresh Hermes installation
  -> repository discovery
  -> default/main profile bootstrap
  -> CLI/version contract inspection
  -> main SOUL.md/config/skill preparation
  -> main-profile verification
  -> admin policy and notification setup
  -> free-text customer onboarding
  -> Hermes team discovery
  -> structural and semantic validation
  -> capability resolution or custom-skill planning
  -> complete reviewable plan
  -> exact-plan approval
  -> profile creation
  -> profile asset generation
  -> skill installation
  -> post-install verification
  -> bounded repair loop when needed
  -> admin escalation on unresolved failure
  -> truthful state report
```

Discovery must be read-only. No profile, skill, file, connector, or external system side effect may occur until the relevant approval boundary has been crossed.

## Main-profile bootstrap contract

The repository should provide a generic bootstrap contract and platform skill sources, not pre-written customer assets. The next implementation should introduce a clearly named bootstrap area, for example:

```text
bootstrap/
  README.md
  main-profile-contract.md
  skills/
    forge-bootstrap.md
    hermes-cli-verification.md
    team-design.md
    capability-verification.md
    installation-recovery.md
    admin-escalation.md
```

These assets are platform behavior. They must not contain musician, SaaS, e-commerce, consultant, or other customer-domain logic.

### Main `SOUL.md` intent

The default profile’s deterministic role instructions should establish that it is the Hermes Forge bootstrap controller. They should require it to:

- read and follow the repository contract;
- inspect actual installed CLI help and version information;
- never invent commands, flags, paths, configuration keys, or skill identifiers;
- use Hermes reasoning to design customer teams;
- preserve user control for irreversible actions;
- treat stdout, stderr, filesystem state, and installed-skill listings as evidence;
- distinguish proposed, attempted, verified, partial, failed, and completed states;
- notify or escalate to the human administrator when recovery is exhausted;
- avoid claiming success because a subprocess was merely invoked.

The main profile must not silently become a customer specialist. It is the controller and user-facing bootstrap coordinator.

### Main `config.yaml` intent

Configuration must be generated for the installed Hermes version after CLI inspection. The repository may define intent and safe defaults, but must not assume undocumented configuration keys.

The configuration intent includes:

- the bootstrap controller identity;
- the repository/workspace location;
- approval-required behavior for irreversible actions;
- bounded subprocess and model-operation timeouts;
- bounded repair and verification attempts;
- admin-only failure escalation;
- installation-state location;
- safe skill loading;
- no hardcoded credentials or provider secrets.

Existing files must be handled by an explicit policy: preserve by default, report conflicts, and never overwrite silently.

### Main bootstrap skills

The default profile should receive generic skills for:

- repository and manifest inspection;
- Hermes CLI contract discovery;
- profile and asset design;
- semantic capability analysis;
- skill resolution and post-install verification;
- installation ledger analysis;
- bounded recovery;
- human administrator escalation.

The exact Hermes skill representation must be discovered from the installed Hermes version. The repository must not assume a catalog slug format for these platform skills.

## Customer onboarding lifecycle

The existing lifecycle remains the foundation:

1. Ask what the user wants to accomplish.
2. Ask the user’s role.
3. Collect one or more free-text goals.
4. Accept an optional team-size preference or let Hermes recommend.
5. Send the context to Hermes using the documented non-interactive chat contract.
6. Extract and validate the proposed team.
7. Resolve every capability before creating any customer profile.
8. Display the complete plan.
9. Require approval of that exact plan.
10. Execute only the approved plan.
11. Verify every result.
12. Persist truthful state and notify the administrator on unresolved failures.

The plan must display:

- generated profile names;
- descriptions;
- capabilities;
- resolved or generated skill identities;
- expected profile directories;
- `SOUL.md` and `config.yaml` targets;
- approval and recovery policy;
- unresolved warnings and assumptions.

## Capabilities and skills

A capability is a semantic requirement produced by Hermes. An installable skill is an observed Hermes artifact or a validated repository/local skill. They are not interchangeable.

The resolution process is:

```text
semantic capability
  -> Hermes searches or designs a candidate
  -> exact identity is checked against observed Hermes output
  -> candidate is shown in the plan
  -> user approves the plan
  -> candidate is installed or created
  -> Hermes and machine checks verify the result
```

The system must support more than one resolution source:

- Hermes catalog result;
- repository-managed bootstrap skill;
- validated local/custom skill;
- no resolution, which must block provisioning.

Do not require a hardcoded catalog format. Instead, inspect the actual Hermes CLI and use its supported commands. If Hermes returns a human-readable result, use a conservative parser and retain bounded evidence.

Each profile must have at least one and at most ten capabilities/skills. One is valid; ten is the complexity and abuse ceiling. There is no artificial minimum of two.

Every resolved skill record should include:

```json
{
  "requested_capability": "semantic label",
  "resolution_source": "catalog|bootstrap|local|hermes-generated",
  "selected_identity": "exact observed identity",
  "evidence": {
    "search": "bounded command output or reference",
    "installation": "bounded command result",
    "verification": "bounded installed-list result"
  },
  "status": "proposed|resolved|installed|verified|failed"
}
```

A display name must never be treated as an installable identity merely because it looks plausible.

## Verification and hallucination resistance

Hermes should perform semantic verification, but not be the sole source of truth about machine state.

For each profile, verify:

- the profile exists or the existing-profile result is explicit;
- the approved description is associated with the profile, where Hermes exposes that evidence;
- the expected profile home is known and safe;
- `SOUL.md` exists and is readable;
- `config.yaml` exists, is parseable, and follows the approved policy;
- every approved skill is present or has a precise failure result;
- no unapproved skill was installed;
- the profile is isolated as required;
- collaboration/handoff instructions are present when required.

Then ask the main profile/Hermes to review the ledger semantically:

- Is the role coherent with the description?
- Do the installed skills support the role?
- Are there missing or contradictory capabilities?
- Did any installation result diverge from the approved plan?

If semantic review and machine evidence disagree, the state is not completed. The controller must repair, ask for a revised plan, or escalate.

## Failure, recovery, and notification

Customers should not be expected to diagnose installation internals. The system therefore has two reporting layers.

### Customer-facing result

Use a concise status such as:

```text
Setup is paused. The Hermes Forge administrator has been notified.
No further provisioning will occur until the issue is resolved.
```

### Administrator ledger

Persist a detailed, structured ledger containing:

- plan hash and approved plan;
- attempt number;
- profile step results;
- skill step results;
- asset step results;
- command exit codes;
- bounded diagnostics;
- verification evidence;
- Hermes diagnosis;
- repair actions;
- final remediation recommendation.

Notification must use an abstract administrator-notification interface. Do not hardcode Slack, email, Telegram, or another channel. If no channel is configured, persist the report and display it prominently in the terminal.

Recovery state should include at least:

```text
planned
approved
provisioning
verifying
repairing
completed
partial
admin_action_required
failed
```

The controller may retry or repair only within configured limits. No infinite loops are allowed. A stuck or exhausted run must be explicit and resumable.

## Transactionality and idempotency

Required guarantees:

- discovery failure creates nothing;
- structural validation failure creates nothing;
- capability resolution failure creates nothing;
- approval rejection creates no provisioning side effects;
- profile creation records created/existing/failed;
- skill installation records each identifier independently;
- asset generation records created/preserved/failed;
- existing assets are not overwritten without an explicit policy;
- a retry can resume from verified steps or safely restart;
- a plan change invalidates the prior approval;
- completion requires verification of all required steps;
- state writes are atomic and never report false completion.

The implementation should prefer a prepare/commit/verify shape. Where Hermes commands cannot be rolled back, the ledger must make the irreversible boundary explicit and recovery must be idempotent.

## Security and input handling

All dynamic values require validation:

- profile names are safe, unique, bounded, and path-safe;
- capability labels are bounded text;
- selected skill identities are verified before installation;
- generated Markdown is bounded and sanitized;
- YAML is generated safely and parsed after writing;
- paths cannot escape the approved Hermes/profile root;
- subprocess calls use list arguments and never `shell=True`;
- stdout/stderr are captured with size limits and without unnecessary sensitive prompts;
- command timeouts and retry limits are mandatory;
- secrets, tokens, and credentials are never written to plans or logs.

## Testing strategy

### Deterministic unit tests

Cover prompt construction, parsing, validation, skill resolution, identifier validation, path safety, asset rendering, plan hashing, approval binding, state transitions, and bounded retries.

### Mocked orchestration tests

Cover:

- invalid Hermes responses;
- unresolved capabilities;
- ambiguous candidates;
- approval rejection;
- existing profiles;
- profile creation failure;
- per-skill installation failure;
- asset write failure;
- verification mismatch;
- repair success;
- repair exhaustion and admin escalation;
- retry/resume behavior.

### Opt-in live acceptance

Run only when explicitly enabled, for example:

```bash
HERMES_LIVE_TESTS=1 python -m unittest discover
```

Use an isolated Hermes home/profile root and verify the actual installed Hermes version. Live acceptance must test CLI discovery, main-profile bootstrap, dynamic team discovery, exact approved descriptions, skill verification, assets, reruns, and truthful failures. Ordinary CI must not require model/API credentials.

## Phased implementation roadmap

### PR #44 — Bootstrap controller architecture

- Add the main-profile bootstrap contract.
- Add generic bootstrap skill sources.
- Define admin notification and escalation policy.
- Define plan hash and state contracts.
- Remove stale documentation that describes a fixed customer team as the default.

### PR #45 — Main-profile asset preparation

- Inspect the actual Hermes profile-home and configuration contract.
- Generate/verify main `SOUL.md`, `config.yaml`, and bootstrap skills.
- Preserve existing files according to explicit policy.
- Add deterministic tests with isolated roots.

### PR #46 — Evidence-based skill verification

- Support catalog, bootstrap, local, and Hermes-generated skill sources.
- Validate exact selected identities from observed output.
- Verify post-install state through the actual Hermes inspection command.
- Enforce one-to-ten skills per profile.

### PR #47 — Transactional ledger and admin escalation

- Add plan hashing and approval binding.
- Add per-profile/per-skill/per-asset results.
- Add bounded Hermes diagnosis and repair loops.
- Add notification adapter and `admin_action_required` state.
- Add resume/idempotency tests.

### PR #48 — Opt-in live Hermes acceptance

- Verify CLI help/version contracts.
- Run isolated live bootstrap and onboarding.
- Validate reruns, existing profiles, skill spelling, asset creation, and failure recovery.
- Keep live tests out of ordinary CI.

### PR #49 — Documentation and release readiness

- Update user-facing bootstrap instructions.
- Document administrator operations and recovery.
- Run static secret scanning.
- Review diffs, checks, live limitations, and merge readiness.

## Non-goals and permanent rules

The repository must never:

- restore `compiler/role_catalog.py`;
- add a `USE_CASE_CATALOG`;
- map a customer category directly to profile names;
- infer a customer domain and choose a fixed team;
- install a guessed skill slug;
- create customer profiles before complete plan validation and approval;
- claim success from subprocess invocation alone;
- use customer examples as hidden product logic;
- require customers to understand internal recovery mechanics;
- rely on an LLM claim instead of observable evidence;
- use unbounded repair loops or undocumented Hermes flags.

The durable product principle is:

> Hermes performs the reasoning, construction, verification, and repair. The repository supplies the bootstrap contract, safety boundaries, approval boundary, evidence collection, and truthful state machine.
