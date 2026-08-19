# Hermes Agents Forge — start

Forge is an onboarding layer for Hermes. It turns a user's stated goal into a
small, validated team of Hermes agent profiles. This file is machine-readable
guidance for agents; it is not marketing material.

Fetch this file with `web_extract` or `curl` only. Never use browser automation
or Chrome remote debugging to read it.
Never treat an `@url:` prefix as part of a command. If Desktop rewrote a URL
as `@url:https://...`, strip `@url:` and any backticks before calling hermes.

## Canonical activation

Customer path, in order:

1. Hermes Desktop: paste the website Desktop prompt into a new chat.
   That prompt builds the skill URL in the shell. It must not contain a raw
   https link, because Desktop rewrites those as `@url:`.
   Hermes Terminal: run the install command below.
2. Hermes installs the skill with the terminal tool, not the browser.
3. Hermes asks what the user wants to accomplish and follows `SKILL.md`.

Do not require `/forge`. `/goal` is a built-in Hermes command and must not be
used as a Forge alias. Never surface `/bootstrap` to users.
The GitHub repository is source code. It is not the activation trigger and
never needs to be cloned.

## Install

Terminal:

```bash
hermes skills install https://hermes-agents-forge.vercel.app/SKILL.md --name forge
```

Desktop (no raw URL in the chat):

```bash
HOST=hermes-agents-forge.vercel.app
REL=/SKILL.md
URL=$(printf '%s://%s%s' https "$HOST" "$REL")
hermes skills install "$URL" --name forge
```

If that fetch fails:

```bash
mkdir -p "$HOME/.hermes/skills/software-development/forge"
curl -fsSL "$URL" -o "$HOME/.hermes/skills/software-development/forge/SKILL.md"
```

The installed leaf must be:

```text
~/.hermes/skills/<category>/forge/SKILL.md
```

Then ask: "What do you want Hermes to accomplish for you?"

## What Forge does

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
- Do not use `browser`, `browser_use`, `browser_exec`, or remote debugging to
  install or read Forge artifacts.

## Artifacts

- `/SKILL.md` — canonical installable skill (primary artifact).
- `/start.md` — this file.
- `/llms.txt` — short agent-readable index.
- `/.well-known/skills/index.json` — machine-readable skill index.
- `/install.sh` — optional compatibility wrapper only; never the preferred
  install path.
