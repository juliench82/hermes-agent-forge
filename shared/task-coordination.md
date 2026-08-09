# Task Coordination Contract

Use a durable task record instead of relying on conversational context between profiles.

## Lifecycle

```text
todo -> claimed -> in_progress -> review -> done
                    \-> blocked
review -> in_progress
```

## Required task fields

```yaml
id: TASK-<unique-id>
objective: <one sentence>
acceptance_criteria:
  - <testable criterion>
dependencies: []
assigned_profile: <profile>
status: todo
artifacts: []
verification: []
risks: []
created_at: <timestamp>
updated_at: <timestamp>
audit_log: []
```

## Read / Claim / Execute

1. Read the task and all dependencies.
2. Claim only tasks matching the profile contract and available permissions.
3. Set `in_progress` before mutation.
4. Attach artifacts and verification evidence as work proceeds.
5. Set `review` with a handoff; only the quality guardian can set `done` after independent verification.
6. Set `blocked` with a concrete reason and required next action when progress cannot continue.

## Concurrency and ownership

- A task has at most one active owner.
- Do not modify another profile's in-progress task without an explicit takeover record.
- Dependencies must be satisfied before claiming.
- Every state transition records actor, timestamp, reason, and evidence.
