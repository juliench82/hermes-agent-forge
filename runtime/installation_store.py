from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
import json
import os

from runtime.approval import ApprovalRecord

SCHEMA_VERSION = "installation-ledger.v1"

class ApprovalRequiredError(PermissionError):
    pass

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _atomic_write(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    encoded = json.dumps(value, sort_keys=True, indent=2) + "\n"
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)

class InstallationLedger:
    def __init__(self, path: Path):
        self.path = path

    def initialize(self, bootstrap: Mapping[str, Any]) -> dict[str, Any]:
        if self.path.exists():
            return self.load()
        ledger = {"schema_version": SCHEMA_VERSION, "bootstrap": dict(bootstrap), "approval": None, "events": []}
        self.append(ledger, "discovered", {"bootstrap": dict(bootstrap)})
        return ledger

    def load(self) -> dict[str, Any]:
        value = json.loads(self.path.read_text(encoding="utf-8"))
        if value.get("schema_version") != SCHEMA_VERSION:
            raise ValueError("unsupported installation ledger schema")
        if not isinstance(value.get("events"), list):
            raise ValueError("installation ledger events are missing")
        return value

    def append(self, ledger: dict[str, Any], event: str, details: Mapping[str, Any] | None = None) -> None:
        ledger["events"].append({"at": _now(), "event": event, "details": dict(details or {})})
        _atomic_write(self.path, ledger)

    def record_approval(self, ledger: dict[str, Any], approval: ApprovalRecord) -> None:
        ledger["approval"] = approval.to_dict()
        self.append(ledger, "approval-recorded", {"manifest_hash": approval.manifest_hash, "action": approval.action, "actor": approval.actor})

    def require_approval(self, ledger: Mapping[str, Any], manifest: Mapping[str, Any], action: str = "provision-and-start") -> None:
        raw = ledger.get("approval")
        if not raw:
            raise ApprovalRequiredError("no durable approval record exists")
        record = ApprovalRecord(**raw)
        if not record.validates(manifest, action):
            raise ApprovalRequiredError("approval does not match the exact manifest and action")
