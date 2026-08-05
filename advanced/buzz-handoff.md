# advanced/buzz-handoff.md — Task-Bus Contract

How isolated profiles talk to each other through BUZZ. The orchestrator is the
only profile allowed to start a handoff chain; specialists reply on their own
channel and never talk to each other directly.

## Channels

| Channel | Purpose | Writer | Reader |
|---------|---------|--------|--------|
| `cr-intake` | user request normalized by orchestrator | orchestrator | orchestrator (log) |
| `cr-brief` | automation brief | product-strategist | orchestrator, architect |
| `cr-design` | approach decision (deterministic / agentic / hybrid) | architect | orchestrator, builder |
| `cr-build` | implementation result | builder | orchestrator, quality-guardian |
| `cr-review` | validation verdict | quality-guardian | orchestrator |
| `cr-improve` | improvement proposals (async, non-blocking) | self-improver | orchestrator |
| `cr-delivery` | final outcome to user | orchestrator | user |

## Message envelope

Every handoff message is a single JSON object posted to the target channel:

```json
{
  "v": 1,
  "task_id": "uuid",
  "stage": "brief | design | build | review | improve | delivery",
  "from": "hermes-orchestrator",
  "to": "hermes-product-strategist",
  "summary": "one-sentence summary (<= 280 chars)",
  "payload_ref": "obsidian://10-Tasks/<task_id>.md",
  "needs_approval": false,
  "created_at": "ISO-8601"
}
```

- `payload_ref` points to the full artifact in the Obsidian vault, not inline
  content. This keeps BUZZ messages compact per `shared/context-policy.md`.
- `needs_approval: true` freezes the chain until the orchestrator relays a
  user approval, per `shared/safety-gates.md`.

## Handoff rules

1. One task = one `task_id` for the whole chain; every message reuses it.
2. The reader acknowledges by writing its own envelope with `stage` advanced.
   Silence beyond `poll_interval * 5` is a timeout: orchestrator retries once,
   then reports failure honestly.
3. Specialists never skip stages and never message each other directly — the
   orchestrator is the only router.
4. Secrets never appear in envelopes. If a payload needs a credential, the
   consuming profile reads it from its own `.env`.
5. The self-improver channel is advisory: it may propose, never merge.

## Gateway configuration

Each profile carries the same relay but its own identity:

```yaml
# <profile HERMES_HOME>/config.yaml
gateway:
  platforms:
    buzz:
      enabled: true
      extra:
        relay_url: <BUZZ_RELAY_URL>
        channels: [<channels from the role-to-profile map>]
        poll_interval: 4
```

```env
# <profile HERMES_HOME>/.env  (chmod 600)
BUZZ_PRIVATE_KEY=nsec1...   # unique per profile
BUZZ_RELAY_URL=<community relay URL>
```
