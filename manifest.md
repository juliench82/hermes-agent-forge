# manifest.md — Control-Room Map

Machine-readable map of the repository. This file makes the boot order, runtime order, installation modes, and file roles explicit.

## Canonical boot order
1. `BOOT.md`
2. `SOUL.MD`
3. `manifest.md`
4. `starter-guide.md`
5. `installation-modes.md`
6. Install specialist roles (as skills or profiles, depending on mode).
7. Install shared policy files.
8. Begin runtime orchestration.

## Canonical runtime order
1. **Intake** — root orchestrator receives a plain-language request.
2. **Product Strategist** — converts the request into an automation brief.
3. **Architect** — designs the approach; chooses deterministic, agentic, or hybrid.
4. **Builder** — implements the automation.
5. **Quality Guardian** — validates the result.
6. **Self Improver** — periodically inspects and proposes improvements.
7. **Delivery** — root orchestrator returns a useful outcome to the user.

## Installation modes

### Default: skill-routed (tested)
| Aspect | Value |
|--------|-------|
| Native Hermes profiles | One (the active profile) |
| Specialist roles installed as | Six `SKILL.md` skills under `.hermes/skills/hermes-bootstraper/` |
| Shared policies installed as | Reference files under the orchestrator skill |
| Root orchestrator | Active profile with augmented `SOUL.md` |
| Inter-agent communication | Internal skill routing within one agent |
| Status | Tested and supported |

### Advanced: isolated-profile (design target)
| Aspect | Value |
|--------|-------|
| Native Hermes profiles | Seven (one orchestrator + six specialists) |
| Specialist roles installed as | Separate Hermes profiles, each with its own skill, config, memory, sessions |
| Shared policies installed as | Distributed to every profile |
| Root orchestrator | Dedicated orchestrator profile |
| Inter-agent communication | Task bus with explicit handoff contract |
| Status | Not automated by the bootstrap prompt; requires manual provisioning |

See `installation-modes.md` for the full decision guide and advanced-mode contract.

## File map

### Root layer
| File | Role |
|------|------|
| `BOOT.md` | First file read; defines startup sequence and mode selection. |
| `SOUL.MD` | Root orchestrator identity and mode-specific behavior. |
| `manifest.md` | This file; boot/runtime order, installation modes, and file map. |
| `starter-guide.md` | Plain-language user guide. |
| `installation-modes.md` | Decision guide and advanced-mode implementation contract. |
| `README.md` | Human-readable repo explanation. |

### Specialist layer (source role specifications)
These files are source contracts. In default mode they are installed as Hermes skills. In advanced mode they are installed in separate Hermes profiles.

| File | Role |
|------|------|
| `profiles/orchestrator/skill.md` | Root orchestrator role specification. |
| `profiles/product-strategist/skill.md` | Converts requests into automation briefs. |
| `profiles/architect/skill.md` | Designs automation approach. |
| `profiles/builder/skill.md` | Implements automation. |
| `profiles/quality-guardian/skill.md` | Validates results. |
| `profiles/self-improver/skill.md` | Proposes periodic improvements. |

Note: `profiles/` is a repository source directory. These are role specifications, not native Hermes profiles. The installation mode determines how they are deployed.

### Policy layer
| File | Role |
|------|------|
| `shared/workflows.md` | Stage flow and handoff rules. |
| `shared/safety-gates.md` | Safety, approval, and honesty rules. |
| `shared/context-policy.md` | Context handoff and anti-bloat rules. |

In default mode, the root orchestrator carries and enforces these. In advanced mode, they are distributed to every profile.

## Success criteria
- Hermes reads `BOOT.md` first and selects an installation mode.
- `SOUL.MD` clearly acts as the root orchestrator in the selected mode.
- `manifest.md` makes the file map, sequence, and modes explicit.
- `starter-guide.md` speaks to non-technical users.
- `installation-modes.md` explains both modes honestly.
- Specialist role specifications are narrow and non-overlapping.
- Shared files define policy for the whole system.
- The repo supports automation delivery, not only software generation.
- The documentation does not claim six isolated Hermes profiles exist unless advanced mode is explicitly provisioned.
