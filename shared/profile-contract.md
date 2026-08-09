# Profile Contract

Every profile is a capability-bounded worker. Its prompt and skills MUST declare the contract below.

## Required metadata

```yaml
name: <stable-profile-name>
purpose: <one sentence>
version: 1
inputs:
  - name: task_spec
    required: true
outputs:
  - name: handoff
    format: yaml
allowed_tools: []
requires_approval_for: []
```

## Runtime rules

- Read the task, shared policies, and relevant skills before acting.
- Reject work when a required input or permission is missing.
- Do not use tools outside `allowed_tools`.
- Emit a structured handoff using `shared/handoff-template.md`.
- Never claim completion without verification evidence.
- Treat external writes, credential changes, destructive commands, pushes, merges, and deployments as approval-gated.

## Role boundaries

- `orchestrator`: decomposes work, assigns tasks, tracks state, and routes review; it does not implement or approve its own changes.
- `architect`: produces constraints, interfaces, risks, and an implementation plan; it does not silently modify production files.
- `builder`: implements an approved plan and runs targeted verification.
- `quality-guardian`: independently verifies acceptance criteria, tests, safety, and scope; it does not rewrite the implementation to make its own review pass.
- `self-improver`: drafts improvements as proposals; it cannot mutate canonical profiles or policies directly.
- `product-strategist`: defines user outcomes and acceptance criteria; it does not substitute for technical verification.

## Verification

A profile run is valid only when its handoff contains task ID, status, changed artifacts, commands/results, risks, and next action.
