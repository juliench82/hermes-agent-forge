# Invoice summary

## Scope

- 5 invoices processed.
- Suppliers: Acme Office Supplies, Contoso Legal Services, Northwind Traders.
- Statuses present: paid, unpaid, overdue.
- Currency totals are kept separate; no exchange rates applied.

## By supplier

### Acme Office Supplies

| Invoice | Issue date | Due date | Status | Amount |
|---|---|---|---|---:|
| INV-2026-003 | 2026-06-01 | 2026-07-01 | overdue | 480.00 EUR |
| INV-2026-004 | 2026-07-05 | 2026-08-05 | unpaid | 320.00 EUR |

Supplier total: **800.00 EUR**

### Contoso Legal Services

| Invoice | Issue date | Due date | Status | Amount |
|---|---|---|---|---:|
| INV-2026-005 | 2026-07-25 | 2026-08-25 | unpaid | 3,600.00 CHF |

Supplier total: **3,600.00 CHF**

### Northwind Traders

| Invoice | Issue date | Due date | Status | Amount |
|---|---|---|---|---:|
| INV-2026-001 | 2026-07-15 | 2026-08-15 | unpaid | 2,400.00 EUR |
| INV-2026-002 | 2026-07-20 | 2026-08-20 | paid | 1,250.50 EUR |

Supplier total: **3,650.50 EUR**

## By status

| Status | Count | Total |
|---|---:|---:|
| Paid | 1 | 1,250.50 EUR |
| Unpaid | 2 | 2,720.00 EUR |
| Unpaid | 1 | 3,600.00 CHF |
| Overdue | 1 | 480.00 EUR |

## Totals by currency

| Currency | Invoice count | Total |
|---|---:|---:|
| EUR | 4 | 4,450.50 EUR |
| CHF | 1 | 3,600.00 CHF |

## Notes

- No external action was taken.
- CHF and EUR were not combined because no exchange rate was provided.
- The supplied invoice statuses were used as authoritative input.
