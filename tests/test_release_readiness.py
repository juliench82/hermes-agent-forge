from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]


class ReleaseReadinessDocumentationTests(unittest.TestCase):
    def test_checklist_documents_live_boundaries_and_evidence(self):
        content = (ROOT / "RELEASE_READINESS.md").read_text(encoding="utf-8")
        for marker in (
            "HERMES_LIVE_TESTS=1",
            "HERMES_LIVE_HOME",
            "installed Hermes version",
            "exact approved plan hash",
            "admin_action_required",
            "NIP-42",
            "buzz-acp",
            "No Buzz mode is considered live-validated",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)

    def test_readme_does_not_claim_live_completion(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Live Hermes and Buzz validation remain opt-in", content)
        self.assertNotIn("live validation is complete", content.lower())


if __name__ == "__main__":
    unittest.main()
