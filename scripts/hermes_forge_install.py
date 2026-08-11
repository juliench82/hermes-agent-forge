#!/usr/bin/env python3
"""Compatibility entrypoint for the Hermes-native installer."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime.adaptive_installer import main

if __name__ == "__main__":
    raise SystemExit(main())
