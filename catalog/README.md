# Primitive catalog

The catalog contains immutable, versioned building blocks resolved by a `TenantSpec`.

- Tenant specs reference exact versions: `name@MAJOR.MINOR.PATCH`.
- Published primitive versions are immutable; breaking changes require a new major version.
- Primitives never grant implicit permissions.
- Tenant specs may restrict, but never weaken, `mandatory-baseline@1.0.0`.
- Secrets are references only and resolve through Docker secrets or Vault at deployment time.

The first catalog slice supports invoice collections: REST accounting APIs, IMAP/SMTP mail, executor and supervisor roles, cron scheduling, and immutable audit logging.
