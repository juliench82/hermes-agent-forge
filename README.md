![Hero image](https://raw.githubusercontent.com/juliench82/hermes-bootstraper/main/hero.png)

# Hermes Control Room — Isolated Profiles

Most repetitive work does not need another meeting, another spreadsheet tab, or a developer ticket that quietly ages like milk in the fridge.

**Hermes Control Room** is a repository for turning everyday company chores into useful automations. It gives Hermes a clear operating model: understand a request in plain language, delegate the work to focused specialist roles, check the result, and deliver something useful back to the person who asked.

The point is not to impress anyone with code. The point is to make work disappear.

## The idea

AI is often presented as a clever assistant that can write code, explain jargon, or produce a very confident paragraph about almost anything. That is useful — but regular people at work usually need a different kind of help.

They need things like:
- "Collect the invoices and send me a summary every Friday."
- "When a support request arrives, sort it and alert the right person."
- "Prepare this month's expense report and send it to finance."
- "Watch this folder and keep the filenames sensible."

Those are not software projects in the user's mind. They are small pieces of work that keep coming back. Hermes is designed to turn those recurring requests into reliable outcomes.

## Why this repository exists

The starting problem is simple: people should not have to become developers just to stop doing the same administrative task for the fiftieth time.

A normal user does not want a tutorial on APIs, a half-finished script, or the thrilling instruction "run this in your terminal." They want the invoices compiled, the report ready, the right person notified, or the follow-up sent. This repository was created to make that expectation explicit: Hermes should deliver an outcome, not merely generate code and wave goodbye.

It also avoids the opposite problem: one enormous "do everything" AI prompt. That tends to become a digital junk drawer — impressive at first glance, hard to trust, and somehow full of mystery cables. Instead, this repo operates like a small control room: one central coordinator and several focused specialists, each with a clear job.

## Architecture: isolated profiles only

This repository deploys **one native Hermes profile per role**. Each profile has its own config, memory, sessions, and credentials. A dedicated orchestrator profile coordinates work via **BUZZ**, Block's open-source human+agent messaging platform. The **Obsidian brain** provides shared persistent memory across all profiles.

### Topology

```text
                +------------------------+
                |   Obsidian brain       |  shared vault (memory layer)
                +-----------+------------+
                            |
   +----------------+  BUZZ |  +----------------+
   | orchestrator   |<------>|  | BUZZ relay     |
   | profile        |<------>|  | (task bus)     |
   +-------+--------+        +--+-------+-------+
           ^                      ^       ^
           | handoff channels    |       |
   +-------+--------+   +--------+--+   +-+-------------+
   | strategist etc. |   | architect |   | builder ...   |
   | (own profile)   |   | (profile) |   | (profiles)    |
   +-----------------+   +-----------+   +---------------+
```

Each profile has its own `HERMES_HOME`, config, memory, sessions, credentials, and **its own BUZZ identity** (one scoped lock per relay+pubkey pair — two profiles cannot drive one Buzz identity).

## What happens when you ask Hermes

1. You describe the task in ordinary language.
2. The orchestrator profile receives it and posts a handoff to the strategist channel via BUZZ.
3. The product-strategist profile converts the request into an automation brief and writes it to the Obsidian brain.
4. The architect profile designs the approach: deterministic, agentic, or hybrid.
5. The builder profile implements the automation.
6. The quality-guardian profile validates the result before delivery.
7. The orchestrator profile returns the finished outcome to the user.

All handoffs travel through BUZZ channels. All shared context lives in the Obsidian vault. If a required detail is missing, the orchestrator asks a short, simple question.

## What you receive

Hermes is designed to return results people can use, for example:
- An email containing compiled invoices
- A report ready to review or share
- A notification sent to the right team
- A completed workflow result
- A background automation that finishes without needing babysitting

Raw code may exist behind the scenes, but it is not the product. The useful result is the product.

## A few examples

| You say | Hermes aims to deliver |
|---|---|
| "Every Friday, send me unpaid invoices grouped by supplier." | A scheduled summary email with the requested invoice list. |
| "When a new support ticket arrives, tell the correct team." | A categorized ticket and a clear notification to the responsible team. |
| "Prepare the monthly expenses for finance." | A compiled expense report ready for finance to use. |
| "Rename files added to this folder using the date." | Newly added files renamed consistently, without a manual clean-up session. |

## How the control room works

Hermes is not one giant agent trying to do everything. It is a coordinated team of roles:

- **Orchestrator** receives the request, routes the work, and delivers the result.
- **Product Strategist** turns the request into a clear automation brief.
- **Architect** chooses the most suitable approach: deterministic, agentic, or hybrid.
- **Builder** implements the automation.
- **Quality Guardian** checks the result before delivery.
- **Self Improver** periodically suggests small, safe improvements.

The shared policy files set the rules for handoffs, safety, approvals, secret handling, honesty, and keeping context compact.

## How to start Hermes

Use this launch instruction, or something close to it:

> Load and follow the instructions in `juliench82/hermes-bootstraper` from start to finish. Read `BOOTSTRAP.md` first, then `buzz-handoff.md`, then `README.md`. Run the scripts under `scripts/` to provision the isolated profiles, BUZZ transport, and Obsidian brain. Create or verify the specified files and skills without asking questions unless a required value is truly missing.

Hermes must read the repository in this order:

1. `BOOTSTRAP.md` — startup sequence and bootstrap contract
2. `buzz-handoff.md` — BUZZ task-bus contract and message envelope
3. `README.md` — this file
4. Specialist role specifications and shared policy files
5. `scripts/` — deterministic helpers for fragile provisioning operations

## Repository map

```text
BOOTSTRAP.md             # Start here: bootstrap sequence and contract
buzz-handoff.md          # BUZZ task-bus contract and message envelope
README.md                # You are here
hero.png                 # Hero image

scripts/                 # Deterministic helpers for fragile operations
  profiles.sh            # Idempotent 7-profile creation + skill/policy install
  buzz.sh                # BUZZ prerequisites + key-uniqueness guard
  obsidian.sh           # Vault verify/seed + per-profile wiring

profiles/                # Source role specifications
  orchestrator/skill.md        # Intake, routing, and delivery
  product-strategist/skill.md  # Request -> automation brief
  architect/skill.md           # Automation approach
  builder/skill.md             # Implementation
  quality-guardian/skill.md    # Validation
  self-improver/skill.md       # Improvement proposals

shared/                  # Cross-agent operating policy
  workflows.md           # Stage flow and handoff rules
  safety-gates.md        # Approvals, safety, and honest reporting
  context-policy.md      # Compact handoffs and anti-bloat rules
```

## Guardrails

Hermes should:
- Use plain language unless the user is clearly technical.
- Ask only for genuinely missing information.
- Request approval before irreversible or sensitive actions.
- Never expose secrets or pretend a failed workflow succeeded.
- Keep specialist roles focused on one job each.
- Deliver a useful result instead of stopping at raw code.

## In one sentence

Hermes Control Room is a practical way to turn "I do this every week and I hate it" into "it is handled."
