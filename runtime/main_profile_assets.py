from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import re
import tempfile
from typing import Iterable


class MainProfileAssetError(ValueError):
    """Raised when main-profile asset preparation cannot be completed safely."""


@dataclass(frozen=True)
class AssetResult:
    path: Path
    status: str


SOUL_CONTENT = """# Hermes Forge Bootstrap Controller

You are the Hermes Forge bootstrap controller for the default Hermes profile.

## Responsibilities

- Read and follow the repository bootstrap contract.
- Inspect the installed Hermes CLI before using commands or flags.
- Design customer teams dynamically from onboarding context.
- Never invent skill identifiers, paths, configuration keys, or completion state.
- Preserve human approval for irreversible actions.
- Treat command output, filesystem state, and installed-skill inspection as evidence.
- Escalate unresolved failures to the human administrator.

The default profile is the platform controller, not a customer-domain specialist.
"""


CONFIG_CONTENT = """profile_role: bootstrap_controller
approval_required: true
live_provisioning: false
max_repair_attempts: 3
state_directory: installation-state
"""


SKILLS = {
    "repository-inspection.md": "# Repository inspection\nRead bootstrap files and report bounded evidence.",
    "cli-verification.md": "# Hermes CLI verification\nInspect installed Hermes version and help before commands.",
    "team-design.md": "# Dynamic team design\nPropose customer profiles from goals without domain catalogs.",
    "capability-verification.md": "# Capability verification\nRequire observed identity before treating a skill as installable.",
    "installation-recovery.md": "# Installation recovery\nUse bounded, evidence-based repair and truthful state.",
    "admin-escalation.md": "# Administrator escalation\nPersist detailed failure context for human recovery.",
}


_KEY_VALUE = re.compile(r"^(?P<key>[a-z_]+): (?P<value>.+)$")


class MainProfileAssetPreparer:
    def __init__(self, root: Path, *, replace_existing: bool = False) -> None:
        self.root = Path(root)
        self.replace_existing = replace_existing

    def prepare(self) -> tuple[AssetResult, ...]:
        self._validate_root()
        assets = ((self.root / "SOUL.md", SOUL_CONTENT), (self.root / "config.yaml", CONFIG_CONTENT))
        assets += tuple((self.root / "skills" / name, content) for name, content in SKILLS.items())
        self.root.mkdir(parents=True, exist_ok=True)
        results = []
        for path, content in assets:
            results.append(self._write(path, content))
        return tuple(results)

    def _validate_root(self) -> None:
        if not self.root.is_absolute():
            raise MainProfileAssetError("profile root must be absolute")
        if self.root.name in {"", ".", ".."}:
            raise MainProfileAssetError("profile root must name a profile directory")

    def _write(self, path: Path, content: str) -> AssetResult:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not self.replace_existing:
            return AssetResult(path, "preserved")
        status = "replaced" if path.exists() else "created"
        fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        except Exception:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            raise
        return AssetResult(path, status)


def parse_config(path: Path) -> dict[str, str | bool | int]:
    values: dict[str, str | bool | int] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        match = _KEY_VALUE.match(line)
        if match is None:
            raise MainProfileAssetError(f"malformed config line: {line!r}")
        value = match.group("value")
        if value in {"true", "false"}:
            parsed: str | bool | int = value == "true"
        elif value.isdigit():
            parsed = int(value)
        else:
            parsed = value
        values[match.group("key")] = parsed
    return values
