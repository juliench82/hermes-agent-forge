import json
import unittest
from pathlib import Path
from compiler.activation import activate_bootstrap
from compiler.first_interaction import FirstInteractionError, produce_first_interaction

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples/solo-founder-saas.acceptance.json"

class SoloFounderAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads(FIXTURE.read_text())
        self.activation = activate_bootstrap(ROOT, self.fixture["onboardingAnswers"], approved=True)

    def test_first_interaction_has_expected_sections(self):
        result = produce_first_interaction(self.activation.summary, self.fixture["firstRequest"])
        for section in self.fixture["expectedSections"]:
            self.assertIn(section, result)
        self.assertTrue(result["productBrief"])
        self.assertGreaterEqual(len(result["acceptanceCriteria"]), 3)

    def test_no_user_project_repository_or_side_effects(self):
        result = produce_first_interaction(self.activation.summary, self.fixture["firstRequest"])
        self.assertEqual(result["userProjectRepository"], {"connected": False})
        self.assertEqual(result["sideEffects"], {"implementationStarted": False, "connectorsConnected": False, "externalWrites": False})

    def test_rejects_connected_project_repository(self):
        summary = dict(self.activation.summary)
        summary["userProjectRepository"] = {"connected": True}
        with self.assertRaisesRegex(FirstInteractionError, "remain disconnected"):
            produce_first_interaction(summary, self.fixture["firstRequest"])

if __name__ == "__main__":
    unittest.main()
