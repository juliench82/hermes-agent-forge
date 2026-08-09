from __future__ import annotations

import argparse
from pathlib import Path

from .planner import build_plan
from .renderers import render_plan


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m compiler.render")
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = render_plan(build_plan(args.spec), args.output)
    print(f"RENDERED: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
