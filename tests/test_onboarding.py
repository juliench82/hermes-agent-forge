import json
import unittest
from pathlib import Path
from compiler.onboarding import BASELINE_PROFILES, OnboardingError, classify_use_case, propose_team, validate_answers

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "onboarding/fixtures/solo-founder-saas.json"

class OnboardingTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads(FIXTURE.read_text())

    def test_fixture_selects_solo_founder_saas(self):
        self.assertEqual(classify_use_case(self.fixture["answers"]), "solo-founder-saas")

    def test_proposes_expected_profiles(self):
        profiles = propose_team(self.fixture["answers"]).team_manifest["team"]["profiles"]
        self.assertEqual([profile["id"] for profile in profiles], BASELINE_PROFILES)
        self.assertNotIn("self-improver", [profile["id"] for profile in profiles])

    def test_proposal_is_not_active_or_provisioned(self):
        manifest = propose_team(self.fixture["answers"]).team_manifest
        self.assertEqual(manifest["status"], "proposed")
        self.assertFalse(manifest["sideEffects"]["provisioned"])
        self.assertFalse(manifest["userProjectRepository"]["connected"])
        self.assertEqual(manifest["approval"]["mode"], "human-in-the-loop")

    def test_missing_answer_fails(self):
        answers = dict(self.fixture["answers"])
        del answers["autonomy"]
        with self.assertRaisesRegex(OnboardingError, "missing onboarding answers"):
            validate_answers(answers)

    def test_unsupported_user_type_fails(self):
        answers = dict(self.fixture["answers"])
        answers["userType"] = "agency"
        with self.assertRaisesRegex(OnboardingError, "unsupported userType"):
            classify_use_case(answers)

    def test_non_matching_intent_fails(self):
        answers = dict(self.fixture["answers"])
        answers["objective"] = "Manage restaurant reservations"
        answers["workflowCategory"] = ["reservations"]
        with self.assertRaisesRegex(OnboardingError, "no supported"):
            classify_use_case(answers)

if __name__ == "__main__":
    unittest.main()
