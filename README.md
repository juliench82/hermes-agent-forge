# hermes-bootstraper

A control-room contract for Hermes. This repository governs and coordinates a small team of specialist agents that turn repetitive company work into finished automation outcomes.

## Who this is for
Regular people inside companies: accounts payable, ops, admin, support, finance, and internal-tools users. You do not need to be technical.

## How to launch Hermes
Load and follow the instructions in this repository from start to finish. Read `BOOT.md` first, then `SOUL.MD`, then `manifest.md`, then `starter-guide.md`. Hermes creates or verifies the structure and begins runtime orchestration.

Suggested launch phrase:

> Load and follow the instructions in `juliench82/hermes-bootstrap-prompt-set` from start to finish. Read `BOOT.md` first, then `SOUL.MD`, then create the profiles and files exactly as specified, without asking questions unless a required value is truly missing.

## File structure
```
BOOT.md                  # First file read; startup sequence
SOUL.MD                  # Root orchestrator identity
manifest.md              # Boot/runtime order and file map
starter-guide.md         # Plain-language user guide
README.md                # This file
profiles/
  orchestrator/skill.md
  product-strategist/skill.md
  architect/skill.md
  builder/skill.md
  quality-guardian/skill.md
  self-improver/skill.md
shared/
  workflows.md           # Stage flow and handoff rules
  safety-gates.md        # Safety, approval, and honesty rules
  context-policy.md      # Context handoff and anti-bloat rules
```

## What Hermes does with the repo
- Reads the root files in order.
- Creates or verifies the specialist and shared files.
- Routes plain-language requests through a small team of agents.
- Delivers useful automation outcomes, not raw code.
