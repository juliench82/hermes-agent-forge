from pathlib import Path
import json
import unittest


ROOT = Path(__file__).parents[1]


class BootstrapDiscoveryTests(unittest.TestCase):
    def test_activation_file_is_hermes_md(self):
        self.assertTrue((ROOT / "HERMES.md").is_file())
        self.assertFalse((ROOT / "BOOTSTRAP.md").exists())

    def test_manifest_is_readable_and_does_not_require_bootstrap_md(self):
        manifest_path = ROOT / "bootstrap.manifest.json"
        self.assertTrue(manifest_path.is_file())
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertIsInstance(payload, dict)
        encoded = json.dumps(payload)
        self.assertNotIn("BOOTSTRAP.md", encoded)

    def test_discovery_does_not_mean_provisioned(self):
        self.assertTrue((ROOT / "HERMES.md").is_file())
        self.assertTrue((ROOT / "bootstrap.manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
