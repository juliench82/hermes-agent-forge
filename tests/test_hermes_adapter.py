import json
import tempfile
import unittest
from pathlib import Path

from compiler.hermes_adapter import CONTRACT_VERSION, LEGACY_PROFILES, STAGES, render_hermes
from compiler.planner import build_plan
from runtime.tenant_spec import validate_file

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "examples" / "solo-founder-app-builder.tenant-spec.json"
EXPECTED_STAGES = [stage for stage, _ in STAGES]


class HermesAdapterTests(unittest.TestCase):
    def test_compatibility_spec_validates_and_preserves_legacy_profiles(self):
        validate_file(SPEC)
        plan = build_plan(SPEC)
        with tempfile.TemporaryDirectory() as tmp:
            root = render_hermes(plan, Path(tmp), ROOT)
            runtime = json.loads((root / "runtime.json").read_text())
            coordination = json.loads((root / "coordination.json").read_text())
            self.assertEqual(runtime["routingMode"], "skill-routed")
            self.assertEqual(runtime["rootAgent"], "orchestrator")
            self.assertEqual(
                [stage["id"] for stage in coordination["stages"]],
                EXPECTED_STAGES,
            )
            self.assertEqual(
                [agent["legacyProfile"] for agent in runtime["agents"]],
                list(LEGACY_PROFILES),
            )
            for name in LEGACY_PROFILES:
                self.assertEqual(
                    (ROOT / "profiles" / name / "profile.yaml").read_text(),
                    (root / "profiles" / name / "profile.yaml").read_text(),
                )
                self.assertEqual(
                    (ROOT / "profiles" / name / "skill.md").read_text(),
                    (root / "profiles" / name / "skill.md").read_text(),
                )
            runtime_text = (root / "runtime.json").read_text().lower()
            self.assertNotIn("password", runtime_text)
            self.assertNotIn('"token"', runtime_text)

    def test_render_is_deterministic(self):
        plan = build_plan(SPEC)
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            a = render_hermes(plan, Path(first), ROOT)
            b = render_hermes(plan, Path(second), ROOT)
            self.assertEqual((a / "runtime.json").read_bytes(), (b / "runtime.json").read_bytes())
            self.assertEqual(
                (a / "coordination.json").read_bytes(),
                (b / "coordination.json").read_bytes(),
            )
            self.assertEqual(
                (a / "fingerprint.sha256").read_bytes(),
                (b / "fingerprint.sha256").read_bytes(),
            )

    def test_contract_version_and_status(self):
        plan = build_plan(SPEC)
        with tempfile.TemporaryDirectory() as tmp:
            root = render_hermes(plan, Path(tmp), ROOT)
            runtime = json.loads((root / "runtime.json").read_text())
            manifest = json.loads((root / "manifest.json").read_text())
            self.assertEqual(runtime["contractVersion"], CONTRACT_VERSION)
            self.assertEqual(runtime["contractStatus"], "compatibility")
            self.assertEqual(manifest["contractVersion"], CONTRACT_VERSION)
            self.assertIs(manifest["secretValuesIncluded"], False)

    def test_profile_identity_version_skills_io_routing_approval_namespace(self):
        plan = build_plan(SPEC)
        with tempfile.TemporaryDirectory() as tmp:
            root = render_hermes(plan, Path(tmp), ROOT)
            runtime = json.loads((root / "runtime.json").read_text())
            by_profile = {agent["legacyProfile"]: agent for agent in runtime["agents"]}
            for name in LEGACY_PROFILES:
                with self.subTest(profile=name):
                    agent = by_profile[name]
                    self.assertEqual(agent["id"], name)
                    self.assertEqual(agent["legacyProfile"], name)
                    self.assertTrue(str(agent["profileVersion"]).strip())
                    self.assertIsInstance(agent["inputs"], list)
                    self.assertIsInstance(agent["outputs"], list)
                    self.assertIsInstance(agent["skills"], list)
                    self.assertIsInstance(agent["requiresApprovalFor"], list)
                    self.assertTrue(str(agent["namespace"]).startswith("solo-founder."))
                    self.assertEqual(agent["profilePath"], f"profiles/{name}/profile.yaml")
                    self.assertEqual(agent["skillPath"], f"profiles/{name}/skill.md")
            self.assertEqual(runtime["routingMode"], "skill-routed")

    def test_delegation_and_handoff_structure(self):
        plan = build_plan(SPEC)
        with tempfile.TemporaryDirectory() as tmp:
            root = render_hermes(plan, Path(tmp), ROOT)
            coordination = json.loads((root / "coordination.json").read_text())
            self.assertEqual(coordination["workflow"], "solo-founder-app-builder")
            self.assertEqual(coordination["handoffContract"], "shared/profile-contract.md")
            self.assertIn("shared/workflows.md", coordination["policyContracts"])
            self.assertIn("shared/safety-gates.md", coordination["policyContracts"])
            self.assertIn("shared/safety-enforcement.md", coordination["policyContracts"])
            self.assertIsInstance(coordination["delegation"], list)
            for edge in coordination["delegation"]:
                self.assertIn("from", edge)
                self.assertIn("to", edge)

    def test_stage_agent_mapping(self):
        plan = build_plan(SPEC)
        with tempfile.TemporaryDirectory() as tmp:
            root = render_hermes(plan, Path(tmp), ROOT)
            coordination = json.loads((root / "coordination.json").read_text())
            self.assertEqual(
                [(s["id"], s["agent"]) for s in coordination["stages"]],
                list(STAGES),
            )


if __name__ == "__main__":
    unittest.main()
