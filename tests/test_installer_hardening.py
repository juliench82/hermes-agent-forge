import json
import tempfile
import unittest
from pathlib import Path

from runtime.adaptive_installer import PROFILES, config_yaml
from runtime.hardening import managed_config, verify_profile, write_truthful_state


class InstallerHardeningTests(unittest.TestCase):
    def test_team_sizes_are_bounded_and_complete(self):
        self.assertEqual([len(PROFILES[n]) for n in (3, 5, 7)], [3, 5, 7])
        self.assertEqual(PROFILES[3], ["orchestrator", "builder", "quality-guardian"])
        self.assertIn("devops-security", PROFILES[7])

    def test_managed_config_preserves_user_content_and_is_idempotent(self):
        generated = config_yaml("nous", "default", "builder")
        first, action1 = managed_config("user_setting: keep\n", generated)
        second, action2 = managed_config(first, generated)
        self.assertEqual(action1, "appended")
        self.assertEqual(action2, "updated")
        self.assertEqual(first, second)
        self.assertIn("user_setting: keep", second)
        self.assertEqual(second.count("_config_version: 34"), 1)

    def test_profile_verification_is_evidence_based(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            self.assertFalse(verify_profile(home)["verified"])
            (home / "config.yaml").write_text("x: 1\n")
            (home / "SOUL.md").write_text("# profile\n")
            self.assertTrue(verify_profile(home)["verified"])

    def test_state_reports_partial_and_completed_truthfully(self):
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "installation_state.json"
            config = {"provider": "nous", "model": "default", "team_size": 3}
            self.assertEqual(write_truthful_state(state_path, config, [], [{"profile": "builder", "error": "failed"}]), "partial")
            self.assertEqual(write_truthful_state(state_path, config, [{"name": "builder", "verified": True}], []), "completed")
            self.assertEqual(json.loads(state_path.read_text())["status"], "completed")


if __name__ == "__main__":
    unittest.main()
