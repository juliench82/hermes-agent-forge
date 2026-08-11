import tempfile
import unittest
from pathlib import Path

from runtime.profile_assets import provision_profile_assets, provision_selected_profiles


class ProfileAssetTests(unittest.TestCase):
    def make_repo(self, root: Path, profile: str = "builder") -> Path:
        source = root / "profiles" / profile
        (source / "skills").mkdir(parents=True)
        (source / "SOUL.md").write_text("repository soul\n", encoding="utf-8")
        (source / "skills" / "role.md").write_text("repository skill\n", encoding="utf-8")
        return root

    def test_copies_role_assets_and_verifies_them(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repo(Path(directory))
            result = provision_profile_assets(root, "builder", root / "homes" / "builder")
            self.assertTrue(result["verified"])
            self.assertEqual((root / "homes/builder/SOUL.md").read_text(), "repository soul\n")
            self.assertTrue((root / "homes/builder/skills/role.md").exists())

    def test_preserves_existing_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repo(Path(directory))
            home = root / "homes/builder"
            home.mkdir(parents=True)
            (home / "SOUL.md").write_text("user soul\n", encoding="utf-8")
            result = provision_profile_assets(root, "builder", home)
            self.assertTrue(result["verified"])
            self.assertEqual((home / "SOUL.md").read_text(), "user soul\n")
            self.assertIn("preserved", [item["action"] for item in result["actions"]])

    def test_missing_source_is_truthful(self):
        with tempfile.TemporaryDirectory() as directory:
            result = provision_profile_assets(Path(directory), "missing", Path(directory) / "home")
            self.assertFalse(result["verified"])
            self.assertEqual(result["status"], "missing_source")

    def test_selected_profile_batch_supports_three_five_and_seven(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profiles = ["orchestrator", "builder", "quality-guardian"]
            for profile in profiles:
                self.make_repo(root, profile)
            results = provision_selected_profiles(root, profiles, root / "homes")
            self.assertEqual(len(results), 3)
            self.assertTrue(all(item["verified"] for item in results))


if __name__ == "__main__":
    unittest.main()
