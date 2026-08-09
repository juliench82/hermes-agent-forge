# Output contract

## Successful result

Return a Markdown document with these sections, in order:

1. `# Invoice summary`
2. `## Scope`
3. `## By supplier`
4. `## By status`
5. `## Totals by currency`
6. `## Notes`

The result must include every input invoice exactly once, grouped alphabetically by supplier. Monetary values must show two decimal places and their currency code.

## Failure result

Return a validation report instead of a partial summary. It must include:

- `status: failed`
- Each invalid record's position, field, and reason.
- A statement that no totals were calculated.

## Non-goals

The pack does not send email or chat messages, write to accounting systems, approve payments, alter invoice records, deduplicate automatically, or translate currencies.
