# manifest.md — Control-Room Map

Machine-readable map of the repository. This file makes the boot order, runtime order, and file roles explicit.

## Canonical boot order
1. `BOOT.md`
2. `SOUL.MD`
3. `manifest.md`
4. `starter-guide.md`
5. Create or verify structure.
6. Create or verify specialist profile files.
7. Create or verify shared policy files.
8. Begin runtime orchestration.

## Canonical runtime order
1. **Intake** — root orchestrator receives a plain-language request.
2. **Product Strategist** — converts the request into an automation brief.
3. **Architect** — designs the approach; chooses deterministic, agentic, or hybrid.
4. **Builder** — implements the automation.
5. **Quality Guardian** — validates the result.
6. **Self Improver** — periodically inspects and proposes improvements.
7. **Delivery** — root orchestrator returns a useful outcome to the user.

## File map

### Root layer
| File | Role |
|------|------|
| `BOOT.md` | First file read; defines startup sequence. |
| `SOUL.MD` | Root orchestrator identity. |
| `manifest.md` | This file; boot/runtime order and file map. |
| `starter-guide.md` | Plain-language user guide. |
| `README.md` | Human-readable repo explanation. |

### Specialist layer
| File | Role |
|------|------|
| `profiles/orchestrator/skill.md` | Root orchestrator skill. |
| `profiles/product-strategist/skill.md` | Converts requests into automation briefs. |
| `profiles/architect/skill.md` | Designs automation approach. |
| `profiles/builder/skill.md` | Implements automation. |
| `profiles/quality-guardian/skill.md` | Validates results. |
| `profiles/self-improver/skill.md` | Proposes periodic improvements. |

### Policy layer
| File | Role |
|------|------|
| `shared/workflows.md` | Stage flow and handoff rules. |
| `shared/safety-gates.md` | Safety, approval, and honesty rules. |
| `shared/context-policy.md` | Context handoff and anti-bloat rules. |

## Success criteria
- Hermes reads `BOOT.md` first.
- `SOUL.MD` acts as the root orchestrator.
- `manifest.md` makes the file map and sequence explicit.
- `starter-guide.md` speaks to non-technical users.
- Specialist profiles are one-job-only and non-overlapping.
- Shared files define policy for the whole system.
- The repo supports automation delivery, not only software generation.
