#!/usr/bin/env python3
"""
installer_entrypoint.py — Thin wrapper Hermes can call to run the installer.
"""

import subprocess
import sys
from pathlib import Path

def main():
    installer = Path(__file__).parent.parent / "scripts" / "hermes_forge_install.py"
    if not installer.exists():
        print(f"Installer not found at {installer}", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run(["python3", str(installer)], check=False)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
