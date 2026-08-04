# Shared Safety Gates

## Non-negotiable rules
- Inspect repository structure and instructions before making changes.
- Verify the default branch before creating work branches.
- Never edit, commit, push, or open a PR on the default branch.
- Stage only exact files.
- Never use `git add .` or `git add -A`.
- Do not change credentials, secrets, auth, or deployment settings without explicit approval.
- Never claim tests or reviews succeeded unless they actually did.

## Destructive operations
Never run destructive actions without explicit approval for that exact action.

## Secrets
Never print or commit secret values.

## Honesty
Report failures plainly and precisely.