# Hermes Control Room

Most repetitive work does not need another meeting, another spreadsheet tab, or a developer ticket that quietly ages like milk in the fridge.

**Hermes Control Room** is a repository for turning everyday company chores into useful automations. It gives Hermes a clear operating model: understand a request in plain language, delegate the work to focused specialist agents, check the result, and deliver something useful back to the person who asked.

The point is not to impress anyone with code. The point is to make work disappear.

## The idea

AI is often presented as a clever assistant that can write code, explain jargon, or produce a very confident paragraph about almost anything. That is useful — but regular people at work usually need a different kind of help.

They need things like:
- “Collect the invoices and send me a summary every Friday.”
- “When a support request arrives, sort it and alert the right person.”
- “Prepare this month’s expense report and send it to finance.”
- “Watch this folder and keep the filenames sensible.”

Those are not software projects in the user’s mind. They are small pieces of work that keep coming back. Hermes is designed to turn those recurring requests into reliable outcomes.

## Why this repository exists

The starting problem is simple: people should not have to become developers just to stop doing the same administrative task for the fiftieth time.

A normal user does not want a tutorial on APIs, a half-finished script, or the thrilling instruction “run this in your terminal.” They want the invoices compiled, the report ready, the right person notified, or the follow-up sent. This repository was created to make that expectation explicit: Hermes should deliver an outcome, not merely generate code and wave goodbye.

It also avoids the opposite problem: one enormous “do everything” AI prompt. That tends to become a digital junk drawer — impressive at first glance, hard to trust, and somehow full of mystery cables. Instead, this repo operates like a small control room: one central coordinator and several focused specialists, each with a clear job.

## Who it is for

This is for regular people inside companies, including:
- Accounts payable and finance teams
- Operations and admin teams
- Support teams
- Internal-tools users
- Anyone who repeatedly thinks: “Surely a computer could do this part.”

Technical teams can use it too, but the experience is deliberately written for people who do not speak in YAML before coffee.

## What happens when you ask Hermes

1. You describe the task in ordinary language.
2. Hermes turns it into a clear automation brief.
3. A specialist designs whether the task should be deterministic, agentic, or a hybrid of both.
4. Another specialist builds the automation.
5. A quality guardian checks that the result is safe, complete, and useful.
6. Hermes gives you the finished outcome.

If a required detail is missing, Hermes asks a short, simple question. It should not make you translate your task into technical language.

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
| “Every Friday, send me unpaid invoices grouped by supplier.” | A scheduled summary email with the requested invoice list. |
| “When a new support ticket arrives, tell the correct team.” | A categorized ticket and a clear notification to the responsible team. |
| “Prepare the monthly expenses for finance.” | A compiled expense report ready for finance to use. |
| “Rename files added to this folder using the date.” | Newly added files renamed consistently, without a manual clean-up session. |

## How the control room works

Hermes is not one giant agent trying to do everything. It is a coordinated team:

- **Orchestrator** receives the request, routes the work, and delivers the result.
- **Product Strategist** turns the request into a clear automation brief.
- **Architect** chooses the most suitable approach: deterministic, agentic, or hybrid.
- **Builder** implements the automation.
- **Quality Guardian** checks the result before delivery.
- **Self Improver** periodically suggests small, safe improvements.

The shared policy files set the rules for handoffs, safety, approvals, secret handling, honesty, and keeping context compact.

## How to start Hermes

Use this launch instruction, or something close to it:

> Load and follow the instructions in `juliench82/hermes-bootstraper` from start to finish. Read `BOOT.md` first, then `SOUL.MD`, then `manifest.md`, then `starter-guide.md`. Create or verify the specified files and profiles without asking questions unless a required value is truly missing.

Hermes must read the repository in this order:

1. `BOOT.md` — startup instructions
2. `SOUL.MD` — root orchestrator identity
3. `manifest.md` — the file map and runtime sequence
4. `starter-guide.md` — user-facing expectations
5. Specialist profiles and shared policy files

## Repository map

```text
BOOT.md                  # Start here: the required boot sequence
SOUL.MD                  # The root orchestrator’s identity and boundaries
manifest.md              # Canonical file map and runtime flow
starter-guide.md         # Simple guide for non-technical users
README.md                # You are here

profiles/
  orchestrator/skill.md        # Intake, routing, and delivery
  product-strategist/skill.md  # Request → automation brief
  architect/skill.md           # Automation approach
  builder/skill.md             # Implementation
  quality-guardian/skill.md    # Validation
  self-improver/skill.md       # Improvement proposals

shared/
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
- Keep specialists focused on one job each.
- Deliver a useful result instead of stopping at raw code.

## In one sentence

Hermes Control Room is a practical way to turn “I do this every week and I hate it” into “it is handled.”