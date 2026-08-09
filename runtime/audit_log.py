"""Append-only audit log for runtime enforcement."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List

from .policy_proxy import AuditEvent


class FileAuditLog:
    """Append-only audit log backed by a file (newline-delimited JSON)."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

    def append(self, event: AuditEvent) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(event.to_json() + "\n")

    def read_all(self) -> List[AuditEvent]:
        events = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            data = json.loads(line)
            events.append(
                AuditEvent(
                    timestamp=data["timestamp"],
                    tenant_id=data["tenantId"],
                    agent_id=data["agentId"],
                    tool_name=data["toolName"],
                    decision=data["decision"],
                    reason=data["reason"],
                    arguments_hash=data["argumentsHash"],
                    connector_id=data.get("connectorId"),
                    scope=data.get("scope"),
                    approval_id=data.get("approvalId"),
                )
            )
        return events


def default_audit_log_path() -> Path:
    return Path(os.getenv("HERMES_AUDIT_LOG_PATH", "audit.log"))
