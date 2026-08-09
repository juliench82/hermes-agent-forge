# .hermes.md — vault map template

Copy to the vault root as `.hermes.md` when the user accepts seeding.
Edit folder names to match the real vault. Keep this file free of secrets.

```markdown
# Shared brain map (Hermes)

This Obsidian vault is the local knowledge layer for Hermes Control Room.
Notes stay on this machine. Do not put passwords, API keys, or tokens in notes.

## Folders

- /Hermes — agent-writable control-room artifacts (scoped)
- /projects — project status and working notes
- /notes — general notes
- /templates — draft templates
- /daily — daily notes
- /meetings — meeting notes (prefer YYYY-MM-DD names)
- /crm — people and account notes
- /sops — standard operating procedures (candidates for /learn)

## Routing

- When asked about a project, check /projects first.
- When asked about a person or account, check /crm.
- Meeting notes live in /meetings, sorted by date.
- For runbooks and repeatable processes, check /sops then offer /learn.
- For drafts, start from /templates.
- Write agent-generated control-room task notes under /Hermes only unless the user asks otherwise.

## Control-room layout (if present)

- /Hermes or control-room seed folders may include Inbox, Tasks, Decisions, RunLog, Reference.
- BUZZ handoffs reference vault paths via payload_ref; keep those notes under the scoped tree.

## Learn candidates

Stable notes under /sops and gold-path /templates may be promoted with `/learn`
into permanent Hermes skills after user approval.
```
