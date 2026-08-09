"""Tests for Sprint 3 runtime enforcement: policy, audit, isolation, secrets, approval."""
from __future__ import annotations

import unittest
from pathlib import Path

from runtime.policy_proxy import PolicyProxy, ToolCall, EffectLevel, Decision, InMemoryAuditLog
from runtime.isolation import IsolationConfig, NetworkPolicy, FilesystemPolicy, MemoryPolicy, apply_isolation
from runtime.secrets import SecretsPolicy, SecretRef, build_secrets_policy
from runtime.confirmation import ApprovalGateway


class TestPolicyProxy(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLog()
        agents_policy = {
            "builder": {"maxEffect": "irreversible"},
            "reader": {"maxEffect": "read"},
        }
        tools_allowlist = {"builder": ["git.push", "github.write"], "reader": ["filesystem.read"]}
        effects_map = {"git.push": EffectLevel.IRREVERSIBLE, "github.write": EffectLevel.WRITE_LIMITED, "filesystem.read": EffectLevel.READ}
        approval_required_for = {"git.push"}
        self.proxy = PolicyProxy(
            tenant_id="test",
            agents_policy=agents_policy,
            tools_allowlist=tools_allowlist,
            effects_map=effects_map,
            approval_required_for=approval_required_for,
            audit_sink=self.audit.append,
        )

    def test_allow_authorized_tool_within_effect(self):
        call = ToolCall(agent_id="builder", tool_name="github.write", arguments={}, effect=EffectLevel.WRITE_LIMITED)
        decision = self.proxy.authorize(call)
        self.assertEqual(decision.decision, Decision.ALLOW)
        self.assertEqual(len(self.audit.events), 1)

    def test_deny_tool_not_in_allowlist(self):
        call = ToolCall(agent_id="reader", tool_name="git.push", arguments={}, effect=EffectLevel.IRREVERSIBLE)
        decision = self.proxy.authorize(call)
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("not in allowlist", decision.reason)

    def test_deny_effect_exceeds_max_effect(self):
        call = ToolCall(agent_id="reader", tool_name="filesystem.read", arguments={}, effect=EffectLevel.IRREVERSIBLE)
        decision = self.proxy.authorize(call)
        self.assertEqual(decision.decision, Decision.DENY)
        self.assertIn("exceeds", decision.reason)

    def test_require_approval_for_irreversible(self):
        call = ToolCall(agent_id="builder", tool_name="git.push", arguments={"ref": "main"}, effect=EffectLevel.IRREVERSIBLE)
        decision = self.proxy.authorize(call)
        self.assertEqual(decision.decision, Decision.REQUIRE_APPROVAL)
        self.assertTrue(decision.approval_metadata.get("required"))


class TestIsolation(unittest.TestCase):
    def test_apply_isolation_default_deny(self):
        cfg = IsolationConfig(network=NetworkPolicy.DEFAULT_DENY, filesystem=FilesystemPolicy.ISOLATED, memory=MemoryPolicy.PRIVATE, data_namespace="test.agent")
        env = apply_isolation(cfg, Path("/tmp"))
        self.assertEqual(env["HERMES_NETWORK_POLICY"], "deny")
        self.assertEqual(env["HERMES_FILESYSTEM_POLICY"], "isolated")
        self.assertEqual(env["HERMES_MEMORY_POLICY"], "private")
        self.assertIn("HERMES_WORKDIR", env)


class TestSecretsPolicy(unittest.TestCase):
    def test_can_access(self):
        policy = build_secrets_policy([{"agent": "builder", "secret_ref": "vault:secret/github/token"}])
        self.assertTrue(policy.can_access("builder", "vault:secret/github/token"))
        self.assertFalse(policy.can_access("reader", "vault:secret/github/token"))


class TestApprovalGateway(unittest.TestCase):
    def test_request_approve_deny(self):
        gw = ApprovalGateway()
        req = gw.request("t1", "builder", "git.push", "deploy", "abc123")
        self.assertEqual(req.status, "pending")
        approved = gw.approve(req.id)
        self.assertEqual(approved.status, "approved")
        denied = gw.deny(req.id)
        self.assertEqual(denied.status, "denied")


if __name__ == "__main__":
    unittest.main()
