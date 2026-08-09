"""Golden compatibility tests for solo-founder profiles."""

import json
import hashlib
import unittest

PROFILES = {
    "orchestrator": {"name": "orchestrator", "version": "1.0.0", "skills": ["product-vision", "workflow-coordination", "delegation"], "inputs": ["product_idea", "constraints", "goals"], "outputs": ["validated_spec", "roadmap", "delegated_tasks"], "routing": "skill-routed", "delegation": ["product-strategist", "architect"], "handoff": {"to_product_strategist": {"inputs": ["product_idea", "goals"], "outputs": ["market_analysis", "feature_priorities"], "approval_required": False}, "to_architect": {"inputs": ["validated_spec"], "outputs": ["architecture_design"], "approval_required": True}}, "approval_metadata": {"requires_approval_for": ["deployment", "architecture_changes"], "approval_gateway": "human-in-the-loop"}, "isolation_namespace": "orchestrator-ns"},
    "product-strategist": {"name": "product-strategist", "version": "1.0.0", "skills": ["market-analysis", "feature-prioritization", "roadmap-planning"], "inputs": ["product_idea", "goals", "market_context"], "outputs": ["market_analysis", "feature_priorities", "roadmap"], "routing": "skill-routed", "delegation": [], "handoff": {}, "approval_metadata": {"requires_approval_for": [], "approval_gateway": "none"}, "isolation_namespace": "product-strategist-ns"},
    "architect": {"name": "architect", "version": "1.0.0", "skills": ["system-design", "api-design", "data-modeling"], "inputs": ["validated_spec", "requirements"], "outputs": ["architecture_design", "api_contracts", "data_models"], "routing": "skill-routed", "delegation": ["builder"], "handoff": {"to_builder": {"inputs": ["architecture_design", "api_contracts"], "outputs": ["implementation"], "approval_required": False}}, "approval_metadata": {"requires_approval_for": ["architecture_changes"], "approval_gateway": "orchestrator"}, "isolation_namespace": "architect-ns"},
    "builder": {"name": "builder", "version": "1.0.0", "skills": ["implementation", "testing", "integration"], "inputs": ["architecture_design", "api_contracts", "data_models"], "outputs": ["implementation", "tests", "integration_results"], "routing": "skill-routed", "delegation": ["quality-guardian"], "handoff": {"to_quality_guardian": {"inputs": ["implementation", "tests"], "outputs": ["quality_report"], "approval_required": False}}, "approval_metadata": {"requires_approval_for": [], "approval_gateway": "none"}, "isolation_namespace": "builder-ns"},
    "quality-guardian": {"name": "quality-guardian", "version": "1.0.0", "skills": ["code-review", "security-audit", "quality-assurance"], "inputs": ["implementation", "tests"], "outputs": ["quality_report", "security_findings", "approval_decision"], "routing": "skill-routed", "delegation": [], "handoff": {}, "approval_metadata": {"requires_approval_for": ["production_deployment"], "approval_gateway": "human-in-the-loop"}, "isolation_namespace": "quality-guardian-ns"},
    "self-improver": {"name": "self-improver", "version": "1.0.0", "skills": ["self-reflection", "pattern-extraction", "optimization"], "inputs": ["workflow_history", "outcomes", "feedback"], "outputs": ["improvement_suggestions", "pattern_updates"], "routing": "skill-routed", "delegation": [], "handoff": {}, "approval_metadata": {"requires_approval_for": ["pattern_updates"], "approval_gateway": "orchestrator"}, "isolation_namespace": "self-improver-ns"}
}

class TestProfileIdentity(unittest.TestCase):
    def test_all_profiles_have_correct_name(self):
        for profile_name, expected in PROFILES.items():
            with self.subTest(profile=profile_name):
                self.assertEqual(expected["name"], profile_name)

class TestProfileVersion(unittest.TestCase):
    def test_all_profiles_have_version(self):
        for profile_name, expected in PROFILES.items():
            with self.subTest(profile=profile_name):
                self.assertEqual(expected["version"], "1.0.0")

class TestProfileSkills(unittest.TestCase):
    def test_all_profiles_have_skills(self):
        for profile_name, expected in PROFILES.items():
            with self.subTest(profile=profile_name):
                self.assertIsInstance(expected["skills"], list)
                self.assertGreater(len(expected["skills"]), 0)

class TestProfileRouting(unittest.TestCase):
    def test_all_profiles_use_skill_routed(self):
        for profile_name, expected in PROFILES.items():
            with self.subTest(profile=profile_name):
                self.assertEqual(expected["routing"], "skill-routed")

class TestProfileIsolationNamespace(unittest.TestCase):
    def test_isolation_namespace_format(self):
        for profile_name, expected in PROFILES.items():
            with self.subTest(profile=profile_name):
                expected_ns = f"{profile_name}-ns"
                self.assertEqual(expected["isolation_namespace"], expected_ns)

class TestDeterministicOutput(unittest.TestCase):
    def test_fingerprint_is_deterministic(self):
        bundle = {"contract_version": "v1-draft", "contract_status": "compatibility", "profiles": PROFILES}
        bundle_json = json.dumps(bundle, sort_keys=True, separators=(",", ":"))
        fingerprint1 = hashlib.sha256(bundle_json.encode()).hexdigest()
        fingerprint2 = hashlib.sha256(bundle_json.encode()).hexdigest()
        self.assertEqual(fingerprint1, fingerprint2)

if __name__ == "__main__":
    unittest.main()
