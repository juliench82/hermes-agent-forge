import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from runtime.adaptive_installer import provision_profile


class ProfileAssetIntegrationTests(unittest.TestCase):
    def test_missing_repository_assets_are_reported_in_profile_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            completed = type("Completed", (), {"returncode": 0, "stderr": ""})()
            with patch("runtime.adaptive_installer.subprocess.run", return_value=completed):
                result = provision_profile(root, "builder", "nous", "default")
            self.assertFalse(result["verified"])
            self.assertEqual(result["assets"]["status"], "missing_source")
            self.assertIn("assets", result)

    def test_repository_assets_are_required_for_verified_profile(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "profiles" / "builder" / "skills"
            source.mkdir(parents=True)
            (root / "profiles" / "builder" / "SOUL.md").write_text("role\n")
            (source / "role.md").write_text("skill\n")
            completed = type("Completed", (), {"returncode": 0, "stderr": ""})()
            with patch("runtime.adaptive_installer.subprocess.run", return_value=completed):
                result = provision_profile(root, "builder", "nous", "default")
            self.assertTrue(result["verified"])
            self.assertEqual(result["assets"]["status"], "completed")


if __name__ == "__main__":
    unittest.main()
