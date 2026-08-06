# invoice-summary

This pack turns a set of invoice records into a review-ready summary grouped by supplier and status. It is intentionally deterministic: it does not send messages, modify source data, call external services, or convert currencies.

## User request

> Summarize these invoices by supplier, show paid/unpaid/overdue status, and give me totals by currency.

## Delivery

The pack produces a Markdown report containing:

- Invoice count and reporting scope.
- Supplier sections with invoice details and supplier totals.
- Status totals, separated by currency.
- Grand totals, separated by currency.
- Explicit notes for missing or inconsistent fields.

## Safety boundary

This demonstration is read-only. Any future connector-based delivery or payment action must be a separate approved workflow; it is not part of this pack.
