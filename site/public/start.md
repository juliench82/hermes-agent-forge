# Hermes Agents Forge — start

Forge is an onboarding layer for Hermes. It turns a user's stated goal into a
small, validated team of Hermes agent profiles. This file is machine-readable
guidance for agents; it is not marketing material.

## Canonical activation

- The activation command is `/forge`, typed inside Hermes (CLI or Desktop).
- `/goal` may be treated as an alias. Never surface `/bootstrap` to users.
- The GitHub repository (github.com/juliench82/hermes-agents-forge) is source
  code. It is not the activation trigger and never needs to be cloned.

## Install

```bash
hermes skills install https://hermes-agents-forge.vercel.app/SKILL.md
```

Then open Hermes and type `/forge`. Installing the skill registers the slash
command automatically in both CLI and Desktop.

## What /forge does

1. Detects CLI vs Desktop and inspects the current profile and capabilities.
2. Asks what the user wants to accomplish (free text), plus role, constraints,
   tools in scope, and desired outcomes.
3. Proposes a team of 3, 5, or 7 profiles with names, responsibilities,
   skills, and collaboration boundaries, sized to workflow complexity.
4. Shows the complete plan and requests explicit approval before any write.
5. On approval: creates profiles dynamically (the main/orchestrator profile is
   the only hard-coded baseline), generates `SOUL.md` role assets, installs the
   approved skills (cap of ~10 heavy skills per profile), and writes
   `config.yaml` only with values the user supplied or explicitly accepted.
6. Validates the result and reports exactly what was created, skipped, or
   failed. Success is never claimed without verification.

## Trust and safety

- The agent must present a plan and obtain explicit approval before creating
  or modifying profiles, files, or configuration.
- External side effects (third-party skills, network services, messages)
  require separate, individual approval.
- No API keys are collected by the website or this document. No secrets belong
  in the skill, examples, or generated files.
- Installation is user-space only (`~/.hermes`); no sudo, no privileged shell,
  no piping remote content into a shell.

## Artifacts

- `/SKILL.md` — canonical installable skill (primary artifact).
- `/start.md` — this file.
- `/llms.txt` — short agent-readable index.
- `/.well-known/skills/index.json` — machine-readable skill index, when the
  Hermes version supports it.
- `/install.sh` — optional compatibility wrapper only; never the preferred
  install path.
