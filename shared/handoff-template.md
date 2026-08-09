# Structured Handoff

Copy this template for every profile result.

```yaml
task_id: TASK-<id>
profile: <profile-name>
status: ready_for_review | blocked | completed
summary: <concise result>
objective: <original objective>
acceptance_criteria:
  - criterion: <text>
    result: passed | failed | not_run
    evidence: <command, artifact, or explanation>
files_changed: []
artifacts: []
tests:
  - command: <command>
    result: passed | failed | not_run
    notes: <short notes>
risks: []
approvals_required: []
next_action: <single concrete action>
```

## Handoff rules

- Use paths relative to the repository or workspace.
- Include failed and skipped checks; never omit them.
- Keep evidence reproducible and avoid claims based only on intent.
- A `completed` handoff is not sufficient for task closure; independent review is required.
