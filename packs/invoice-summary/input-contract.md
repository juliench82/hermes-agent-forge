# Input contract

## Accepted input

A JSON array of invoice objects. Each object must contain:

| Field | Type | Required | Rules |
|---|---|---:|---|
| `invoice_number` | string | yes | Non-empty identifier. |
| `supplier` | string | yes | Non-empty supplier name. |
| `issue_date` | string | yes | ISO date: `YYYY-MM-DD`. |
| `due_date` | string | yes | ISO date: `YYYY-MM-DD`. |
| `amount` | number | yes | Zero or greater; no implicit currency conversion. |
| `currency` | string | yes | Three-letter uppercase currency code, such as `EUR` or `CHF`. |
| `status` | string | yes | One of `paid`, `unpaid`, or `overdue`. |

## Validation

Reject the complete input if any required field is missing, a date is not ISO-formatted, an amount is negative or non-numeric, a currency is not a three-letter uppercase code, or a status is outside the allowed set. Do not silently repair records.

Duplicate invoice numbers are reported as a validation error because this pack cannot determine which record is authoritative.

## Processing assumptions

- Amounts are summed only when the currency matches.
- Supplier names are grouped by exact value after trimming surrounding whitespace.
- The supplied `status` is treated as authoritative; the pack does not infer status from dates.
- No exchange rates are used.
