#!/usr/bin/env python3
"""Validate and render the invoice-summary demonstration pack."""
import argparse
import json
import math
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATUS_ORDER = ("paid", "unpaid", "overdue")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CURRENCY_RE = re.compile(r"^[A-Z]{3}$")
REQUIRED_FIELDS = ("invoice_number", "supplier", "issue_date", "due_date", "amount", "currency", "status")

class ValidationError(ValueError):
    pass

def fail(index, message):
    raise ValidationError(f"record {index}: {message}")

def validate(invoices):
    if not isinstance(invoices, list):
        raise ValidationError("input must be a JSON array")
    seen = set()
    normalized = []
    for index, invoice in enumerate(invoices, start=1):
        if not isinstance(invoice, dict):
            fail(index, "must be an object")
        for field in REQUIRED_FIELDS:
            if field not in invoice:
                fail(index, f"missing required field '{field}'")
        number = invoice["invoice_number"]
        if not isinstance(number, str) or not number.strip():
            fail(index, "invoice_number must be a non-empty string")
        if number in seen:
            fail(index, f"duplicate invoice_number '{number}'")
        seen.add(number)
        supplier = invoice["supplier"]
        if not isinstance(supplier, str) or not supplier.strip():
            fail(index, "supplier must be a non-empty string")
        for field in ("issue_date", "due_date"):
            value = invoice[field]
            if not isinstance(value, str) or not DATE_RE.fullmatch(value):
                fail(index, f"{field} must be a valid ISO date")
            try:
                date.fromisoformat(value)
            except ValueError:
                fail(index, f"{field} must be a valid ISO date")
        amount = invoice["amount"]
        if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not math.isfinite(amount) or amount < 0:
            fail(index, "amount must be a non-negative number")
        currency = invoice["currency"]
        if not isinstance(currency, str) or not CURRENCY_RE.fullmatch(currency):
            fail(index, "currency must be a three-letter uppercase code")
        status = invoice["status"]
        if status not in STATUS_ORDER:
            fail(index, "status must be one of: paid, unpaid, overdue")
        normalized.append({**invoice, "invoice_number": number.strip(), "supplier": supplier.strip()})
    return normalized

def money(amount, currency):
    return f"{amount:,.2f} {currency}"

def render(invoices):
    invoices = validate(invoices)
    suppliers = defaultdict(list)
    by_status = defaultdict(list)
    by_currency = defaultdict(list)
    for invoice in invoices:
        suppliers[invoice["supplier"]].append(invoice)
        by_status[invoice["status"]].append(invoice)
        by_currency[invoice["currency"]].append(invoice)
    lines = ["# Invoice summary", "", "## Scope", "", f"- {len(invoices)} invoices processed.", f"- Suppliers: {', '.join(sorted(suppliers)) or 'none'}.", f"- Statuses present: {', '.join(status for status in STATUS_ORDER if by_status[status]) or 'none'}.", "- Currency totals are kept separate; no exchange rates applied.", "", "## By supplier", ""]
    for supplier in sorted(suppliers):
        records = sorted(suppliers[supplier], key=lambda item: item["invoice_number"])
        lines.extend([f"### {supplier}", "", "| Invoice | Issue date | Due date | Status | Amount |", "|---|---|---|---|---:|"])
        for invoice in records:
            lines.append(f"| {invoice['invoice_number']} | {invoice['issue_date']} | {invoice['due_date']} | {invoice['status']} | {money(invoice['amount'], invoice['currency'])} |")
        totals = defaultdict(float)
        for invoice in records:
            totals[invoice["currency"]] += invoice["amount"]
        lines.extend(["", "Supplier total: " + "; ".join(f"**{money(totals[currency], currency)}**" for currency in sorted(totals)), ""])
    lines.extend(["## By status", "", "| Status | Count | Total |", "|---|---:|---:|"])
    for status in STATUS_ORDER:
        records = by_status[status]
        for currency in dict.fromkeys(record["currency"] for record in records):
            matched = [record for record in records if record["currency"] == currency]
            lines.append(f"| {status.title()} | {len(matched)} | {money(sum(record['amount'] for record in matched), currency)} |")
    lines.extend(["", "## Totals by currency", "", "| Currency | Invoice count | Total |", "|---|---:|---:|"])
    for currency in by_currency:
        records = by_currency[currency]
        lines.append(f"| {currency} | {len(records)} | {money(sum(record['amount'] for record in records), currency)} |")
    lines.extend(["", "## Notes", "", "- No external action was taken.", "- CHF and EUR were not combined because no exchange rate was provided.", "- The supplied invoice statuses were used as authoritative input.", ""])
    return "\n".join(lines)

def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)

def run_tests():
    fixtures = ROOT / "tests" / "fixtures"
    expected = (ROOT / "tests" / "expected-output.md").read_text(encoding="utf-8")
    actual = render(load_json(fixtures / "invoices.json"))
    if actual != expected:
        raise AssertionError("rendered output does not match tests/expected-output.md")
    for case in load_json(fixtures / "invalid-invoices.json"):
        try:
            validate(case["input"])
        except ValidationError as error:
            if case["error"] not in str(error):
                raise AssertionError(f"{case['name']}: expected {case['error']!r}, got {error!s}")
        else:
            raise AssertionError(f"{case['name']}: validation unexpectedly passed")
    print("invoice-summary tests passed")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test:
        run_tests()
    elif args.input:
        print(render(load_json(args.input)), end="")
    else:
        parser.error("provide an input JSON file or --test")

if __name__ == "__main__":
    try:
        main()
    except (ValidationError, AssertionError, OSError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
