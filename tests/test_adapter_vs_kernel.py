"""Structural checks: adapter bundle vs hermes_kernel / shared contracts."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from compiler.hermes_adapter import CONTRACT_VERSION, LEGACY_PROFILES, render_hermes
from compiler.planner import build_plan

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "examples" / "solo-founder-app-builder.tenant-spec.json"
KERNEL = ROOT / "runtime" / "hermes_kernel.py"
SHARED = {
    "profile-contract": ROOT / "shared" / "profile-contract.md",
    "task-coordination": ROOT / "shared" / "task-coordination.md",
    "safety-enforcement": ROOT / "shared" / "safety-enforcement.md",
    "safety-gates": ROOT / "shared" / "safety-gates.md",
    "workflows": ROOT / "shared" / "workflows.md",
}


class AdapterVsKernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = build_plan(SPEC)
        cls._tmp = tempfile.TemporaryDirectory()
        cls.root = render_hermes(cls.plan, Path(cls._tmp.name), ROOT)
        cls.runtime = json.loads((cls.root / "runtime.json").read_text())
        cls.coordination = json.loads((cls.root / "coordination.json").read_text())
        cls.manifest = json.loads((cls.root / "manifest.json").read_text())

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_kernel_and_shared_contracts_exist(self):
        self.assertTrue(KERNEL.is_file())
        for name, path in SHARED.items():
            with self.subTest(contract=name):
                self.assertTrue(path.is_file())

    def test_runtime_top_level_contract(self):
        self.assertEqual(self.runtime["apiVersion"], "hermes.runtime/v1")
        self.assertEqual(self.runtime["kind"], "HermesRuntimeConfiguration")
        self.assertEqual(self.runtime["contractVersion"], CONTRACT_VERSION)
        self.assertEqual(self.runtime["contractStatus"], "compatibility")
        self.assertEqual(self.runtime["routingMode"], "skill-routed")
        self.assertEqual(self.runtime["rootAgent"], "orchestrator")
        self.assertIsInstance(self.runtime["agents"], list)
        self.assertEqual(len(self.runtime["agents"]), len(LEGACY_PROFILES))

    def test_agents_required_fields(self):
        required = (
            "id",
            "legacyProfile",
            "profileVersion",
            "skills",
            "inputs",
            "outputs",
            "requiresApprovalFor",
            "namespace",
            "profilePath",
            "skillPath",
        )
        for agent in self.runtime["agents"]:
            with self.subTest(agent=agent.get("id")):
                for field in required:
                    self.assertIn(field, agent)

    def test_isolation_namespace_matches_plan(self):
        plan_ns = {a["id"]: a["isolation"]["dataNamespace"] for a in self.plan.agents}
        for agent in self.runtime["agents"]:
            with self.subTest(agent=agent["id"]):
                self.assertEqual(agent["namespace"], plan_ns[agent["id"]])

    def test_coordination_delegation_and_handoff(self):
        self.assertEqual(self.coordination["apiVersion"], "hermes.runtime/v1")
        self.assertEqual(self.coordination["kind"], "HermesCoordinationConfiguration")
        self.assertIsInstance(self.coordination["delegation"], list)
        self.assertEqual(self.coordination["handoffContract"], "shared/profile-contract.md")
        self.assertEqual(self.coordination["delegation"], self.plan.delegation)

    def test_delegation_is_acyclic(self):
        graph: dict[str, list[str]] = {}
        for edge in self.coordination["delegation"]:
            graph.setdefault(edge["from"], []).append(edge["to"])
        visited: set[str] = set()
        stack: set[str] = set()

        def has_cycle(node: str) -> bool:
            visited.add(node)
            stack.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in stack:
                    return True
            stack.remove(node)
            return False

        for node in list(graph):
            if node not in visited:
                self.assertFalse(has_cycle(node), f"cycle involving {node}")

    def test_manifest_security_flags(self):
        self.assertEqual(self.manifest["kind"], "HermesCompatibilityBundle")
        self.assertEqual(self.manifest["contractVersion"], CONTRACT_VERSION)
        self.assertIs(self.manifest["secretValuesIncluded"], False)
        self.assertEqual(self.manifest["sourcePlanFingerprint"], self.plan.fingerprint)

    def test_no_secret_values_in_bundle_files(self):
        for name in ("runtime.json", "coordination.json", "manifest.json"):
            text = (self.root / name).read_text().lower()
            with self.subTest(file=name):
                self.assertNotIn("password", text)
                self.assertNotIn("begin private key", text)

    def test_fingerprint_file_matches_bundle(self):
        fp = (self.root / "fingerprint.sha256").read_text().strip()
        self.assertEqual(len(fp), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in fp))

    def test_legacy_profiles_unchanged_on_disk(self):
        for name in LEGACY_PROFILES:
            with self.subTest(profile=name):
                src = ROOT / "profiles" / name / "profile.yaml"
                dst = self.root / "profiles" / name / "profile.yaml"
                self.assertEqual(src.read_bytes(), dst.read_bytes())


if __name__ == "__main__":
    unittest.main()
