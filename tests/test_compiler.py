import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from compiler.errors import CatalogResolutionError, CompilerError
from compiler.planner import build_plan

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "invoice-collections.tenant-spec.json"


class CompilerTests(unittest.TestCase):
    def test_builds_deterministic_plan(self):
        first = build_plan(EXAMPLE)
        second = build_plan(EXAMPLE)
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertEqual(len(first.fingerprint), 64)
        self.assertEqual(first.tenantId, "acme-fr")
        self.assertEqual([agent["id"] for agent in first.agents], ["collections-supervisor", "receivables-analyst"])

    def test_rejects_unknown_primitive(self):
        from compiler.catalog import Catalog
        with self.assertRaises(CatalogResolutionError):
            Catalog().resolve("unknown@1.0.0")

    def test_rejects_unresolved_connector_binding(self):
        spec = json.loads(EXAMPLE.read_text())
        spec["agents"][0]["connectors"][0]["connectorId"] = "missing"
        path = ROOT / "tests" / ".tmp-invalid-spec.json"
        path.write_text(json.dumps(spec))
        try:
            with self.assertRaises(CompilerError):
                build_plan(path)
        finally:
            path.unlink()

    def test_cli_plan_outputs_json(self):
        result = subprocess.run([sys.executable, "-m", "compiler", "plan", str(EXAMPLE)], cwd=ROOT, text=True, capture_output=True, check=True)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["tenantId"], "acme-fr")
        self.assertIn("fingerprint", payload)


if __name__ == "__main__":
    unittest.main()
