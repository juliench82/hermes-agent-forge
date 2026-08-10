import json
import unittest
from pathlib import Path
from compiler.onboarding import propose_team
from compiler.team_compiler import BASELINE_PROFILES, TeamCompilerError, compile_team_plan

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "onboarding/fixtures/solo-founder-saas.json"

class TeamCompilerTests(unittest.TestCase):
    def setUp(self):
        fixture = json.loads(FIXTURE.read_text())
        self.proposal = propose_team(fixture["answers"]).team_manifest

    def test_requires_explicit_approval(self):
        with self.assertRaisesRegex(TeamCompilerError, "explicit approval"):
            compile_team_plan(self.proposal)

    def test_compiles_expected_profile_instances(self):
        plan = compile_team_plan(self.proposal, approved=True).manifest
        self.assertEqual(plan["status"], "compiled")
        self.assertEqual([item["profile"] for item in plan["profiles"]], BASELINE_PROFILES)
        self.assertEqual([item["id"] for item in plan["profiles"]], [f"{p}-1" for p in BASELINE_PROFILES])

    def test_reuses_runtime_enforcement_contracts(self):
        plan = compile_team_plan(self.proposal, approved=True).manifest
        self.assertIn("runtime.policy_proxy.PolicyProxy", plan["enforcement"]["policyProxy"])
        self.assertIn("runtime.confirmation.ApprovalGateway", plan["approval"]["gateway"])
        self.assertIn("runtime.audit_log.FileAuditLog", plan["enforcement"]["auditLog"])

    def test_orchestrator_led_topology(self):
        communication = compile_team_plan(self.proposal, approved=True).manifest["communication"]
        self.assertEqual(communication["orchestrator"], "orchestrator-1")
        self.assertFalse(communication["directSpecialistMessaging"])
        self.assertEqual(len(communication["specialists"]), 4)

    def test_plan_is_not_provisioned(self):
        plan = compile_team_plan(self.proposal, approved=True).manifest
        self.assertEqual(plan["bootstrapRepository"], {"active": True, "readOnly": True})
        self.assertFalse(plan["userProjectRepository"]["connected"])
        self.assertEqual(plan["provisioning"], {"workspacesCreated": False, "profilesStarted": False, "connectorsConnected": False})

    def test_rejects_non_proposed_input(self):
        proposal = dict(self.proposal)
        proposal["status"] = "active"
        with self.assertRaisesRegex(TeamCompilerError, "only proposed"):
            compile_team_plan(proposal, approved=True)

if __name__ == "__main__":
    unittest.main()
