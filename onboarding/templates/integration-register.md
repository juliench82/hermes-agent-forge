# Integration Register — <Customer name>

> Record metadata and approved scopes only. Never write a password, API key, OAuth refresh token, cookie, or connection string in this document.

| Integration | Purpose | Allowed operations | Allowed data scope | Credential owner | Status |
|---|---|---|---|---|---|
| <service> | <business purpose> | read / draft / send / create / update | <folders, queues, entities> | <customer/operator> | requested / authorised / revoked |

## Authorisation record

For each integration, record:

- Customer-approved purpose
- Minimum required scopes
- Authorised user or service account identity
- Date authorised and review date
- Revocation procedure
- Any excluded folders, teams, mailboxes, records, or recipients

## Rules

- The builder may use only integrations marked `authorised`.
- The architect must reject broader scopes when a narrower scope meets the business requirement.
- The quality guardian verifies that actual use matches this register before activation.
- Credentials live in the approved secret store or provider connection manager, never in this repository.
