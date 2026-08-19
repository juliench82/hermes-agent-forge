---
name: forge
description: Onboard a focused Hermes agent team from the user's goal. Use when the user wants to set up, configure, activate, or design a team of Hermes agents, or mentions Forge.
version: 0.1.0
author: juliench82
license: MIT
compatibility: Hermes CLI or Hermes Desktop. User-space only (~/.hermes). No sudo, no repository cloning, no browser automation for install.
metadata:
  homepage: https://hermes-agents-forge.vercel.app
  source: https://github.com/juliench82/hermes-agents-forge
  start: https://hermes-agents-forge.vercel.app/start.md
---

# Forge — Hermes team activation

Forge turns one stated goal into a validated team of Hermes profiles.
This skill is the procedure. Run it whenever it is loaded or the user asks to set up a team.
Do not require `/forge`. Never treat `/goal` as an alias — that is a built-in Hermes Ralph loop.
Never present `/bootstrap` to the user.

## Hard rules — never violate

1. Never ask the user to clone a GitHub repository. The Forge repo is source code, not the installer.
2. Never run `sudo` or any privileged command. Everything happens in user space (`~/.hermes`).
3. Never create or modify profiles, skills, files, or `config.yaml` before the user explicitly approves the presented plan.
4. Never claim success without verifying the result, and report exactly what was created.
5. Never ask for, store, or embed API keys or secrets. If a proposed skill needs credentials, name it and let the user configure them afterwards.
6. Gate every external side effect (third-party skill installs, network services, messages, purchases) behind its own explicit approval.
7. Never pipe downloaded content into a shell. Skills are installed through `hermes skills install` only.
8. Never use `browser`, `browser_use`, `browser_exec`, or Chrome remote debugging to fetch Forge artifacts. Use the terminal (`hermes skills install` or `curl`) or `web_extract` only.

## Install target

Canonical command:

```bash
hermes skills install https://hermes-agents-forge.vercel.app/SKILL.md --name forge
```

After install, the skill must live at:

```text
~/.hermes/skills/<category>/forge/SKILL.md
```

A lone `forge.md` file is invalid. If you find one, move it into that directory layout, then continue.

## Flow

### 1. Detect environment
- Determine whether the user runs Hermes CLI or Hermes Desktop: probe for the `hermes` binary on PATH and config under `~/.hermes`; if ambiguous, ask.
- Inspect the current profile and capabilities (`hermes profile show`, `hermes skills list`). Summarize what you found in one or two lines before proceeding.
- If this skill is not installed yet, install it with the canonical command above using the terminal tool, then continue.

### 2. Collect the goal
Ask: "What do you want Hermes to accomplish for you?" Accept free-form text.
Then ask for — or infer and state — the user's role, constraints (time, tools, budget), the tools and accounts in scope, and what a successful outcome looks like. Ask at most three follow-up questions; infer the rest and label inferences as inferences.

### 3. Propose the team
Recommend a size and say why:
- 3 profiles — default for simple, single-domain workflows.
- 5 profiles — multi-channel or multi-stage workflows.
- 7 profiles — advanced or enterprise workflows needing strict separation of duties.

Present the complete plan as a table: profile name, responsibility, proposed skills (2–4 each, hard cap of ~10 heavy skills per profile), and collaboration boundaries (who hands off to whom).

Plan rules:
- The existing main/orchestrator profile is the only hard-coded baseline. Extend it; never replace it.
- Generate every other profile dynamically from the user's actual use case. No industry presets, no fixed mappings, no example-driven shortcuts.
- Generate role descriptions and `SOUL.md` content for the specific use case — from validated templates if the local profile assets provide them, otherwise write them directly.

### 4. Confirm, then write
Show the full plan and request explicit confirmation (e.g. "Create these 5 profiles?"). Accept revisions and re-present the plan. Only after approval:
- Create each profile: `hermes profile create <name> --description "<generated description>"`.
- Generate each profile's `SOUL.md` and role assets.
- Install only the approved skills: `hermes -p <name> skills install <skill> ...`.
- Write or update `config.yaml` only with values the user supplied or explicitly accepted, and show the exact diff before writing.
- Optionally run `hermes kanban init` if the user wants the team to work as a board.

### 5. Validate and report
- Re-list profiles and skills; confirm each new profile loads.
- Report precisely: profiles created, skills installed per profile, files written, anything skipped or failed.
- If validation fails, say so plainly and propose the fix. Never declare success on unverified state.

## Trust boundaries
Before the first write, remind the user once, in one sentence: installing this skill came from a stable URL; what happens next creates local profiles and configuration; any third-party skills or external services will be named and approved separately.

## Progressive disclosure
Keep the conversation concise. Extended onboarding rules live at `https://hermes-agents-forge.vercel.app/start.md` — fetch it with `web_extract` or `curl`, never with the browser, and only if this file does not cover the ambiguity.
