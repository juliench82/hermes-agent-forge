# Self-Improvement Policy

Self-improvement is proposal generation, not unrestricted self-modification.

## Pipeline

```text
completed task -> recurring signal -> proposal -> quality review -> approval -> versioned change
```

## Allowed proposals

- New or clarified skills.
- Better verification steps.
- Reusable troubleshooting guidance.
- Handoff and workflow improvements.

## Prohibited direct mutations

`self-improver` must not directly change credentials, safety gates, tool permissions, profile boundaries, canonical orchestrator behavior, or production configuration.

## Proposal format

```yaml
proposal_id: IMP-<id>
source_task: TASK-<id>
problem: <recurring failure or opportunity>
proposed_change: <exact file and change>
evidence: []
regression_risk: low | medium | high
verification_plan: []
status: proposed
```

Proposals become canonical only through a reviewed, versioned change. Stale or rejected proposals remain auditable and are not silently retried.
