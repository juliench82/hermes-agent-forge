# Workflow

1. Receive the invoice array as an untrusted input payload.
2. Validate the payload shape and every required field against `input-contract.md`.
3. Check invoice-number uniqueness and stop with a validation report if duplicates exist.
4. Normalize only presentation-safe values: trim supplier names and render amounts to two decimals; never alter business values.
5. Sort invoices by supplier name, then invoice number.
6. Group records by supplier and calculate per-currency supplier subtotals.
7. Group records by status and calculate per-currency counts and subtotals.
8. Calculate grand totals per currency without exchange-rate conversion.
9. Render the result according to `output-contract.md`.
10. Run the fixture assertions in `tests/` and verify that every input invoice appears once.
11. Present the result as a draft, with no external send or write action.

## Stop conditions

Stop before calculation when input validation fails, duplicate invoice numbers exist, or a currency/amount combination is ambiguous. Report the exact issue; do not guess.
