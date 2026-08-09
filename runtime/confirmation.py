"""Confirmation gates for irreversible actions."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class ApprovalRequest:
    id: str
    tenant_id: str
    agent_id: str
    tool_name: str
    reason: str
    arguments_hash: str
    created_at: str
    status: str = "pending"  # pending | approved | denied
    metadata: Dict[str, Any] = field(default_factory=dict)


class ApprovalGateway:
    """Gate requiring explicit approval before executing irreversible actions."""

    def __init__(self) -> None:
        self.requests: Dict[str, ApprovalRequest] = {}

    def request(self, tenant_id: str, agent_id: str, tool_name: str, reason: str, arguments_hash: str) -> ApprovalRequest:
        req = ApprovalRequest(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            agent_id=agent_id,
            tool_name=tool_name,
            reason=reason,
            arguments_hash=arguments_hash,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self.requests[req.id] = req
        return req

    def approve(self, request_id: str) -> Optional[ApprovalRequest]:
        req = self.requests.get(request_id)
        if not req:
            return None
        req.status = "approved"
        return req

    def deny(self, request_id: str) -> Optional[ApprovalRequest]:
        req = self.requests.get(request_id)
        if not req:
            return None
        req.status = "denied"
        return req

    def get(self, request_id: str) -> Optional[ApprovalRequest]:
        return self.requests.get(request_id)
