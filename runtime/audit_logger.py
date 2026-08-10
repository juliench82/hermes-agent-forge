"""
audit_logger.py — Append-only audit logging for installation mutations.
"""

import json
from pathlib import Path
from datetime import datetime, timezone

RUNTIME_DIR = Path("runtime")
AUDIT_LOG_FILE = RUNTIME_DIR / "audit_log.jsonl"

def log_audit(event: str, details: dict):
    """Append an audit record to the audit log file."""
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "details": details,
    }
    with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
