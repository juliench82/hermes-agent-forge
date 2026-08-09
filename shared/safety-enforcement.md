# Safety Enforcement

Shared safety guidance is enforced at the profile and workflow boundary.

## Action classes

| Class | Examples | Default policy |
|---|---|---|
| read-only | inspect files, git status, metadata queries | allowed |
| local-write | edit files, create branch, install dependency | allowed within workspace |
| external-write | push, issue comment, PR review, connector mutation | explicit approval |
| high-impact | merge, delete, deploy, credential or production change | explicit approval plus review |

## Required controls

- Validate profile permissions before dispatching a tool.
- Require explicit approval immediately before every external or high-impact write.
- Run secret scanning over changed content before external writes.
- Record the target, exact content, actor, approval, and result in the task audit log.
- Fail closed when a tool, target, branch, or permission is ambiguous.
- Never place tokens, passwords, or private keys in task records, skills, or handoffs.

## Review gate

The quality guardian verifies scope, acceptance criteria, tests, secret scan results, and approval evidence. It must return `review` or `done`; it cannot silently waive a failed gate.
