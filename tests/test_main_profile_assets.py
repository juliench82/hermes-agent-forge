import tempfile
from pathlib import Path
import unittest

from runtime.main_profile_assets import (
    MainProfileAssetPreparer,
    MainProfileAssetError,
    parse_config,
)


class MainProfileAssetPreparerTests(unittest.TestCase):
    def test_creates_generic_controller_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "main"
            results = MainProfileAssetPreparer(root).prepare()
            self.assertTrue((root / "SOUL.md").exists())
            self.assertTrue((root / "config.yaml").exists())
            self.assertEqual(len(list((root / "skills").glob("*.md"))), 6)
            self.assertTrue(all(result.status == "created" for result in results))
            config = parse_config(root / "config.yaml")
            self.assertEqual(config["profile_role"], "bootstrap_controller")
            self.assertFalse(config["live_provisioning"])

    def test_preserves_existing_assets_by_default(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "main"
            root.mkdir()
            soul = root / "SOUL.md"
            soul.write_text("operator-owned", encoding="utf-8")
            results = MainProfileAssetPreparer(root).prepare()
            self.assertEqual(soul.read_text(encoding="utf-8"), "operator-owned")
            self.assertEqual(results[0].status, "preserved")

    def test_explicit_replace_updates_existing_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "main"
            root.mkdir()
            soul = root / "SOUL.md"
            soul.write_text("old", encoding="utf-8")
            result = MainProfileAssetPreparer(root, replace_existing=True).prepare()[0]
            self.assertEqual(result.status, "replaced")
            self.assertIn("bootstrap controller", soul.read_text(encoding="utf-8").lower())

    def test_config_parser_rejects_malformed_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            path.write_text("malformed\n", encoding="utf-8")
            with self.assertRaises(MainProfileAssetError):
                parse_config(path)


if __name__ == "__main__":
    unittest.main()
