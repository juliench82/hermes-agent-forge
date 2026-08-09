# Skill Contract

Skills are executable Markdown SOPs. Keep the index small and load the body only when the skill is selected.

## Required front matter

```yaml
---
name: <stable-skill-name>
version: 1
triggers:
  - <situational trigger>
requires:
  - <input or capability>
produces:
  - <artifact>
risk_level: read | local-write | external-write | high-impact
---
```

## Required sections

### When to Use
State the exact conditions that activate the skill and when not to use it.

### Procedure
Give ordered, observable steps. Each step should identify its expected artifact or result.

### Pitfalls
List scope, security, approval, and reliability failure modes.

### Verification
Define commands, checks, or evidence that prove the skill completed successfully.

## Rules

- Prefer small composable skills over role-sized mega-prompts.
- Keep secrets, credentials, and user-specific state out of skills.
- Version changes and record compatibility assumptions.
- A skill may be proposed by `self-improver`, but canonical changes require review.
