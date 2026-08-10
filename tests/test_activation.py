import json
import unittest
from pathlib import Path
from compiler.activation import activate_bootstrap
from compiler.team_compiler import TeamCompilerError

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "onboarding/fixtures/solo-founder-saas.json"

class ActivationPathTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads(FIXTURE.read_text())

    def test_requires_explicit_approval(self):
        with self.assertRaisesRegex(TeamCompilerError, "explicit approval"):
            activate_bootstrap(ROOT, self.fixture["answers"])

    def test_repository_to_team_summary(self):
        result = activate_bootstrap(ROOT, self.fixture["answers"], approved=True)
        self.assertTrue(result.discovery.is_bootstrap_source)
        self.assertEqual(result.onboarding.use_case, "solo-founder-saas")
        self.assertEqual(result.summary, {
            "team": "solo-founder-saas",
            "profiles": ["orchestrator", "product-strategist", "architect", "builder", "quality-guardian"],
            "status": "active",
            "approvalMode": "human-in-the-loop",
            "bootstrapRepository": {"active": True, "readOnly": True},
            "userProjectRepository": {"connected": False},
            "runtimeReady": True,
            "provisioned": False,
        })

    def test_activation_does_not_start_runtime(self):
        result = activate_bootstrap(ROOT, self.fixture["answers"], approved=True)
        provisioning = result.team_plan.manifest["provisioning"]
        self.assertFalse(provisioning["workspacesCreated"])
        self.assertFalse(provisioning["profilesStarted"])
        self.assertFalse(provisioning["connectorsConnected"])
        self.assertFalse(result.team_plan.manifest["userProjectRepository"]["connected"])

if __name__ == "__main__":
    unittest.main()
