import json
import tempfile
import unittest
from pathlib import Path

from compiler.hermes_adapter import render_hermes
from compiler.planner import build_plan
from runtime.tenant_spec import validate_file

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "examples" / "solo-founder-app-builder.tenant-spec.json"


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
            self.assertEqual([stage["id"] for stage in coordination["stages"]], ["intake", "brief", "design", "build", "validate", "deliver", "improve"])
            self.assertEqual([agent["legacyProfile"] for agent in runtime["agents"]], ["orchestrator", "product-strategist", "architect", "builder", "quality-guardian", "self-improver"])
            for name in ("orchestrator", "product-strategist", "architect", "builder", "quality-guardian", "self-improver"):
                self.assertEqual((ROOT / "profiles" / name / "profile.yaml").read_text(), (root / "profiles" / name / "profile.yaml").read_text())
                self.assertEqual((ROOT / "profiles" / name / "skill.md").read_text(), (root / "profiles" / name / "skill.md").read_text())
            self.assertNotIn("password", (root / "runtime.json").read_text().lower())
            self.assertNotIn("token", (root / "runtime.json").read_text().lower())

    def test_render_is_deterministic(self):
        plan = build_plan(SPEC)
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            a = render_hermes(plan, Path(first), ROOT)
            b = render_hermes(plan, Path(second), ROOT)
            self.assertEqual((a / "runtime.json").read_bytes(), (b / "runtime.json").read_bytes())
            self.assertEqual((a / "coordination.json").read_bytes(), (b / "coordination.json").read_bytes())
            self.assertEqual((a / "fingerprint.sha256").read_bytes(), (b / "fingerprint.sha256").read_bytes())


if __name__ == "__main__":
    unittest.main()
