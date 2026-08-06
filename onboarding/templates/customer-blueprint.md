# Customer Blueprint — <Customer name>

> This is the durable source of truth for one customer automation. Do not include credentials, API keys, personal secrets, or raw customer exports.

## Identity

- Customer / tenant: <name>
- Business owner: <name and approved contact channel>
- Timezone: <IANA timezone>
- Blueprint version: <version>
- Status: DISCOVERY | BLUEPRINTED | AUTHORISED | DESIGNED | BUILT | VALIDATED | READY_FOR_REVIEW | ACTIVE

## Desired outcome

- Customer statement: <plain-language request>
- Delivered outcome: <specific report, draft, notification, file, or completed action>
- Frequency / trigger: <schedule or event>
- Success measure: <observable business result>

## Data boundaries

- Allowed read sources: <systems, folders, datasets>
- Allowed write destinations: <systems, folders, recipients>
- Explicitly denied sources/destinations: <systems, folders, actions>
- Retention / deletion expectation: <policy>

## Approval and risk

- Approval mode: DRAFT_ONLY | APPROVAL_REQUIRED | AUTOMATIC_AFTER_ACCEPTANCE
- Actions requiring explicit approval: <list>
- Failure notification recipient: <approved channel>
- Human escalation condition: <list>

## Integration summary

Reference the Integration Register. Record service names, permitted operations, owner, and scope—not secret values.

## Acceptance criteria

- [ ] <criterion 1>
- [ ] <criterion 2>
- [ ] <criterion 3>

## Native-profile handoff

- Product brief: <path or reference>
- Architecture plan: <path or reference>
- Build artifact: <path or reference>
- Quality result: <path or reference>
- Activation review: <path or reference>
