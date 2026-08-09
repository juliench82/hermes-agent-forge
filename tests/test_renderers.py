import json
import tempfile
import unittest
from pathlib import Path

from compiler.planner import build_plan
from compiler.renderers import render_plan

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "invoice-collections.tenant-spec.json"


class RendererTests(unittest.TestCase):
    def test_render_is_deterministic_and_contains_fingerprint(self):
        plan = build_plan(EXAMPLE)
        with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
            first = render_plan(plan, Path(first_dir))
            second = render_plan(plan, Path(second_dir))
            first_files = sorted(path.relative_to(first) for path in first.rglob("*"))
            second_files = sorted(path.relative_to(second) for path in second.rglob("*"))
            self.assertEqual(first_files, second_files)
            self.assertEqual(json.loads((first / "manifest.json").read_text())["sourcePlanFingerprint"], plan.fingerprint)
            self.assertEqual((first / "agents" / "collections-supervisor" / "system-prompt.md").read_text(), (second / "agents" / "collections-supervisor" / "system-prompt.md").read_text())

    def test_renders_each_agent_and_isolation_manifest(self):
        plan = build_plan(EXAMPLE)
        with tempfile.TemporaryDirectory() as output:
            root = render_plan(plan, Path(output))
            for agent in plan.agents:
                agent_root = root / "agents" / agent["id"]
                self.assertTrue((agent_root / "hermes.json").is_file())
                self.assertTrue((agent_root / "tools-policy.json").is_file())
                self.assertTrue((agent_root / "system-prompt.md").is_file())
            isolation = json.loads((root / "isolation" / "agents.json").read_text())
            self.assertEqual(len(isolation["agents"]), len(plan.agents))

    def test_secret_manifest_contains_references_only(self):
        plan = build_plan(EXAMPLE)
        with tempfile.TemporaryDirectory() as output:
            root = render_plan(plan, Path(output))
            manifest = json.loads((root / "secrets.manifest.json").read_text())
            self.assertFalse(manifest["valuesIncluded"])
            self.assertIn("acme-fr/finance-mailbox/credentials", manifest["references"])


if __name__ == "__main__":
    unittest.main()
