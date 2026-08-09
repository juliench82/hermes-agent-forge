from __future__ import annotations

import argparse
import json
from pathlib import Path

from .planner import build_plan


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m compiler")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("spec", type=Path)
    plan = subparsers.add_parser("plan")
    plan.add_argument("spec", type=Path)
    args = parser.parse_args()
    if args.command == "validate":
        from runtime.tenant_spec import validate_file
        validate_file(args.spec)
        print(f"VALID: {args.spec}")
        return 0
    print(json.dumps(build_plan(args.spec).to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
