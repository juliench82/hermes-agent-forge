"""Tool-policy proxy: authorize tool calls per agent/connector/scope/effect."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


class EffectLevel(str, Enum):
    READ = "read"
    WRITE_LIMITED = "write_limited"
    IRREVERSIBLE = "irreversible"


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


@dataclass
class PolicyDecision:
    decision: Decision
    reason: str
    effect_level: Optional[EffectLevel] = None
    approval_metadata: Optional[Dict[str, Any]] = field(default_factory=dict)


@dataclass
class ToolCall:
    agent_id: str
    tool_name: str
    arguments: Dict[str, Any]
    effect: EffectLevel
    connector_id: Optional[str] = None
    scope: Optional[str] = None


@dataclass
class AuditEvent:
    timestamp: str
    tenant_id: str
    agent_id: str
    tool_name: str
    decision: Decision
    reason: str
    arguments_hash: str
    connector_id: Optional[str] = None
    scope: Optional[str] = None
    approval_id: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps(
            {
                "timestamp": self.timestamp,
                "tenantId": self.tenant_id,
                "agentId": self.agent_id,
                "toolName": self.tool_name,
                "decision": self.decision.value,
                "reason": self.reason,
                "argumentsHash": self.arguments_hash,
                "connectorId": self.connector_id,
                "scope": self.scope,
                "approvalId": self.approval_id,
            },
            sort_keys=True,
        )


def _hash_args(args: Dict[str, Any]) -> str:
    import hashlib
    return hashlib.sha256(json.dumps(args, sort_keys=True).encode()).hexdigest()


class PolicyProxy:
    """Enforce tool-policy decisions outside the LLM."""

    def __init__(
        self,
        tenant_id: str,
        agents_policy: Dict[str, Dict[str, Any]],
        tools_allowlist: Dict[str, List[str]],
        effects_map: Dict[str, EffectLevel],
        approval_required_for: Set[str],
        audit_sink: Callable[[AuditEvent], None],
    ):
        self.tenant_id = tenant_id
        self.agents_policy = agents_policy
        self.tools_allowlist = tools_allowlist
        self.effects_map = effects_map
        self.approval_required_for = approval_required_for
        self.audit_sink = audit_sink

    def authorize(self, call: ToolCall) -> PolicyDecision:
        agent_cfg = self.agents_policy.get(call.agent_id, {})
        max_effect_str = agent_cfg.get("maxEffect", EffectLevel.READ.value)
        max_effect = EffectLevel(max_effect_str)

        # Default-deny if tool not in allowlist
        allowed_tools = self.tools_allowlist.get(call.agent_id, [])
        if call.tool_name not in allowed_tools:
            decision = PolicyDecision(
                decision=Decision.DENY,
                reason=f"tool {call.tool_name} not in allowlist for agent {call.agent_id}",
                effect_level=call.effect,
            )
            self._audit(call, decision)
            return decision

        # Effect enforcement: agent's maxEffect must cover call.effect
        effect_order = {EffectLevel.READ: 0, EffectLevel.WRITE_LIMITED: 1, EffectLevel.IRREVERSIBLE: 2}
        if effect_order.get(call.effect, 0) > effect_order.get(max_effect, 0):
            decision = PolicyDecision(
                decision=Decision.DENY,
                reason=f"effect {call.effect.value} exceeds agent maxEffect {max_effect.value}",
                effect_level=call.effect,
            )
            self._audit(call, decision)
            return decision

        # Confirmation gate for irreversible actions
        if call.effect == EffectLevel.IRREVERSIBLE or call.tool_name in self.approval_required_for:
            decision = PolicyDecision(
                decision=Decision.REQUIRE_APPROVAL,
                reason="irreversible effect or tool requires approval",
                effect_level=call.effect,
                approval_metadata={"required": True, "reason": "irreversible"},
            )
            self._audit(call, decision)
            return decision

        decision = PolicyDecision(
            decision=Decision.ALLOW,
            reason="authorized",
            effect_level=call.effect,
        )
        self._audit(call, decision)
        return decision

    def _audit(self, call: ToolCall, decision: PolicyDecision) -> None:
        event = AuditEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            tenant_id=self.tenant_id,
            agent_id=call.agent_id,
            tool_name=call.tool_name,
            decision=decision.decision,
            reason=decision.reason,
            arguments_hash=_hash_args(call.arguments),
            connector_id=call.connector_id,
            scope=call.scope,
            approval_id=decision.approval_metadata.get("approval_id") if decision.approval_metadata else None,
        )
        self.audit_sink(event)


# Helper to build a simple in-memory audit log
class InMemoryAuditLog:
    def __init__(self) -> None:
        self.events: List[AuditEvent] = []

    def append(self, event: AuditEvent) -> None:
        self.events.append(event)

    def to_jsonl(self) -> str:
        return "\n".join(e.to_json() for e in self.events)
