"""Semantic validation for the versioned TenantSpec v1 contract."""
from __future__ import annotations
from typing import Any

class TenantSpecValidationError(ValueError):
    """Raised when a TenantSpec violates a mandatory platform invariant."""

def _fail(message: str) -> None:
    raise TenantSpecValidationError(message)

def _assert_no_literal_secrets(value: Any, path: str = "$") -> None:
    forbidden = {"password", "token", "secret", "api_key", "apikey", "private_key"}
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in forbidden:
                _fail(f"{path}.{key}: literal secrets are forbidden; use secretRefs")
            _assert_no_literal_secrets(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _assert_no_literal_secrets(child, f"{path}[{index}]")

def _assert_acyclic_delegation(agents: list[dict[str, Any]]) -> None:
    graph = {agent["id"]: set(agent.get("delegates", {}).get("allow", [])) for agent in agents}
    for source, targets in graph.items():
        unknown = targets - graph.keys()
        if unknown:
            _fail(f"agent {source}: delegates to unknown agents: {sorted(unknown)}")
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> None:
        if node in visiting:
            _fail(f"delegation graph contains a cycle at agent {node}")
        if node in visited:
            return
        visiting.add(node)
        for target in graph[node]:
            visit(target)
        visiting.remove(node)
        visited.add(node)
    for agent_id in graph:
        visit(agent_id)

def validate_tenant_spec(spec: dict[str, Any]) -> None:
    required = {"apiVersion", "kind", "metadata", "business", "security", "connectors", "agents"}
    missing = required - spec.keys()
    if missing:
        _fail(f"missing required top-level fields: {sorted(missing)}")
    if spec["apiVersion"] != "hermes.platform/v1" or spec["kind"] != "TenantSpec":
        _fail("unsupported TenantSpec apiVersion or kind")
    security = spec["security"]
    audit = security.get("audit", {})
    if security.get("baseline") != "mandatory-baseline@1.0.0":
        _fail("mandatory baseline cannot be replaced or removed")
    if security.get("secretsProvider") not in {"docker-secrets", "vault"}:
        _fail("secretsProvider must be docker-secrets or vault")
    if audit.get("enabled") is not True or audit.get("immutable") is not True:
        _fail("immutable audit logging is mandatory")
    if not isinstance(audit.get("retentionDays"), int) or audit["retentionDays"] < 30:
        _fail("audit retentionDays must be at least 30")
    if security.get("network", {}).get("defaultDenyEgress") is not True:
        _fail("default-deny egress is mandatory")
    _assert_no_literal_secrets(spec)
    connectors = {connector["id"]: set(connector.get("allowedOperations", [])) for connector in spec["connectors"]}
    if len(connectors) != len(spec["connectors"]):
        _fail("connector ids must be unique")
    agent_ids: set[str] = set()
    for agent in spec["agents"]:
        agent_id = agent.get("id")
        if not agent_id or agent_id in agent_ids:
            _fail("agent ids must be present and unique")
        agent_ids.add(agent_id)
        isolation = agent.get("isolation", {})
        if not isolation.get("dataNamespace") or isolation.get("networkPolicy") != "strict" or isolation.get("filesystem") != "read_only":
            _fail(f"agent {agent_id}: strict data, network and filesystem isolation is mandatory")
        for binding in agent.get("connectors", []):
            connector_id = binding.get("connectorId")
            if connector_id not in connectors:
                _fail(f"agent {agent_id}: unknown connector {connector_id}")
            unknown_scopes = set(binding.get("scopes", [])) - connectors[connector_id]
            if unknown_scopes:
                _fail(f"agent {agent_id}: scopes not granted by {connector_id}: {sorted(unknown_scopes)}")
        permissions = agent.get("permissions", {})
        if permissions.get("maxEffect") == "irreversible" and permissions.get("confirmation", {}).get("required") is not True:
            _fail(f"agent {agent_id}: irreversible actions require confirmation")
    _assert_acyclic_delegation(spec["agents"])
