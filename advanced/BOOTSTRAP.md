# advanced/BOOTSTRAP.md — Isolated-Profile Control Room

Read this file after the root `BOOT.md` when the user selects **advanced mode**.
This is the contract for v2 of the control room: one native Hermes profile per role,
BUZZ as the task bus, and the Obsidian brain as shared persistent memory.

## Topology

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

Each profile has its own `HERMES_HOME`, config, memory, sessions, credentials,
and **its own BUZZ identity** (one scoped lock per relay+pubkey pair — two profiles
cannot drive one Buzz identity).

## Startup sequence

1. Read root `BOOT.md`, `SOUL.MD`, `manifest.md`, `installation-modes.md`.
2. Verify Hermes core is installed and a working provider is configured
   (`hermes --version`, provider key present).
3. Run `advanced/scripts/obsidian.sh` — verify/seed the shared vault.
4. Run `advanced/scripts/buzz.sh` — verify the BUZZ adapter and relay reachability.
5. Run `advanced/scripts/profiles.sh` — create the seven profiles idempotently
   and install each role's skill + the three shared policy files.
6. Read `advanced/buzz-handoff.md` and configure the handoff channels.
7. Provision one BUZZ identity per profile (`BUZZ_PRIVATE_KEY` in each profile's
   `.env`; never committed, never shared between profiles).
8. Smoke test: orchestrator posts a `handoff` envelope to the `strategist`
   channel and receives an acknowledgement.
9. Begin runtime orchestration from the orchestrator profile.

## Role-to-profile map

| Profile | Skill source | BUZZ channels |
|---------|--------------|----------------|
| `hermes-orchestrator` | `profiles/orchestrator/skill.md` | all |
| `hermes-product-strategist` | `profiles/product-strategist/skill.md` | `cr-brief` |
| `hermes-architect` | `profiles/architect/skill.md` | `cr-design` |
| `hermes-builder` | `profiles/builder/skill.md` | `cr-build` |
| `hermes-quality-guardian` | `profiles/quality-guardian/skill.md` | `cr-review` |
| `hermes-self-improver` | `profiles/self-improver/skill.md` | `cr-improve` |

## Rules

- Scripts are idempotent; re-running the bootstrap must be safe and fast.
- Scripts never print secrets. BUZZ keys live only in per-profile `.env` files.
- The Obsidian vault is the only shared writable memory; profiles do not share
  `HERMES_HOME`.
- If a required value is missing (relay URL, vault path, key), ask one short
  question — do not guess.
