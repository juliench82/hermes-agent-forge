"""Tests comparing adapter output against hermes_kernel.py expectations."""

import unittest
import hashlib

class TestAdapterKernelCompatibility(unittest.TestCase):
    """Test adapter output structure against kernel expectations."""

    def _get_sample_bundle(self):
        """Get a sample bundle structure."""
        return {
            "contract_version": "v1-draft",
            "contract_status": "compatibility",
            "fingerprint": hashlib.sha256(b"test").hexdigest(),
            "runtime": {"agents": [{"name": "orchestrator", "profile": "orchestrator", "profile_version": "1.0.0", "skills": ["product-vision"], "mode": "skill-routed", "isolation_namespace": "orchestrator-ns", "secrets": []}]},
            "coordination": {"delegation": [], "handoff": {}},
            "manifest": {"isolation": {"network": "default-deny", "filesystem": "isolated", "memory": "private"}, "secrets_policy": [], "tools_policy": []}
        }

    def test_bundle_has_required_top_level_fields(self):
        bundle = self._get_sample_bundle()
        for field in ["contract_version", "contract_status", "fingerprint", "runtime", "coordination", "manifest"]:
            with self.subTest(field=field):
                self.assertIn(field, bundle)

    def test_runtime_has_agents_array(self):
        bundle = self._get_sample_bundle()
        self.assertIn("agents", bundle["runtime"])
        self.assertIsInstance(bundle["runtime"]["agents"], list)

    def test_agents_have_required_fields(self):
        bundle = self._get_sample_bundle()
        for agent in bundle["runtime"]["agents"]:
            for field in ["name", "profile", "skills", "mode"]:
                with self.subTest(agent=agent.get("name"), field=field):
                    self.assertIn(field, agent)

    def test_agents_have_isolation_namespace(self):
        bundle = self._get_sample_bundle()
        for agent in bundle["runtime"]["agents"]:
            with self.subTest(agent=agent.get("name")):
                self.assertIn("isolation_namespace", agent)

    def test_mode_is_skill_routed(self):
        bundle = self._get_sample_bundle()
        for agent in bundle["runtime"]["agents"]:
            with self.subTest(agent=agent.get("name")):
                self.assertEqual(agent["mode"], "skill-routed")

    def test_coordination_has_delegation(self):
        bundle = self._get_sample_bundle()
        self.assertIn("delegation", bundle["coordination"])
        self.assertIsInstance(bundle["coordination"]["delegation"], list)

    def test_coordination_has_handoff(self):
        bundle = self._get_sample_bundle()
        self.assertIn("handoff", bundle["coordination"])
        self.assertIsInstance(bundle["coordination"]["handoff"], dict)

    def test_manifest_has_isolation(self):
        bundle = self._get_sample_bundle()
        self.assertIn("isolation", bundle["manifest"])

    def test_manifest_has_secrets_policy(self):
        bundle = self._get_sample_bundle()
        self.assertIn("secrets_policy", bundle["manifest"])
        self.assertIsInstance(bundle["manifest"]["secrets_policy"], list)

    def test_manifest_has_tools_policy(self):
        bundle = self._get_sample_bundle()
        self.assertIn("tools_policy", bundle["manifest"])
        self.assertIsInstance(bundle["manifest"]["tools_policy"], list)

    def test_no_secret_values_in_bundle(self):
        bundle = self._get_sample_bundle()
        for agent in bundle["runtime"]["agents"]:
            for secret in agent.get("secrets", []):
                with self.subTest(secret=secret.get("name")):
                    self.assertNotIn("value", secret)
                    self.assertIn("ref", secret)

    def test_isolation_network_is_default_deny(self):
        bundle = self._get_sample_bundle()
        self.assertEqual(bundle["manifest"]["isolation"]["network"], "default-deny")

    def test_isolation_filesystem_is_isolated(self):
        bundle = self._get_sample_bundle()
        self.assertEqual(bundle["manifest"]["isolation"]["filesystem"], "isolated")

    def test_isolation_memory_is_private(self):
        bundle = self._get_sample_bundle()
        self.assertEqual(bundle["manifest"]["isolation"]["memory"], "private")

    def test_delegation_is_acyclic(self):
        bundle = self._get_sample_bundle()
        delegation = bundle["coordination"]["delegation"]
        graph = {}
        for edge in delegation:
            src, tgt = edge["from"], edge["to"]
            graph.setdefault(src, []).append(tgt)
        visited, rec_stack = set(), set()
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor): return True
                elif neighbor in rec_stack: return True
            rec_stack.remove(node)
            return False
        for node in graph:
            if node not in visited:
                self.assertFalse(has_cycle(node))

if __name__ == "__main__":
    unittest.main()
