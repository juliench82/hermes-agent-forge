"""Domain-agnostic end-to-end tests for Hermes onboarding orchestration."""
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from runtime.dynamic_profiles import HermesCommandError, create_profiles_from_team, discover_profiles_via_hermes


class FakeHermes:
    def __init__(self, responses: list[subprocess.CompletedProcess[str]]):
        self.responses = iter(responses)
        self.calls: list[list[str]] = []

    def __call__(self, command, **kwargs):
        self.calls.append(command)
        return next(self.responses)


def result(stdout: str = "", stderr: str = "", returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess([], returncode, stdout, stderr)


class DomainAgnosticDiscoveryTests(unittest.TestCase):
    def test_arbitrary_customer_context_is_forwarded_without_catalog_lookup(self):
        response = '{"team_size": 3, "profiles": [{"name": "coordination", "description": "Coordinate the customer workflow.", "skills": ["planning"]}, {"name": "research", "description": "Gather and evaluate relevant information.", "skills": ["research"]}, {"name": "delivery", "description": "Turn approved work into completed outcomes.", "skills": ["execution"]}]}'
        hermes = FakeHermes([result(response)])
        team = discover_profiles_via_hermes("Coordinate a complex customer workflow", "Project owner", ["Understand the work", "Deliver repeatable outcomes"], runner=hermes)
        self.assertEqual(team["team_size"], 3)
        self.assertEqual(len(team["profiles"]), 3)
        self.assertEqual(team["validation_errors"], [])
        self.assertIn("Coordinate a complex customer workflow", hermes.calls[0][3])
        self.assertNotIn("music", hermes.calls[0][3].lower())

    def test_another_context_can_return_a_different_valid_team(self):
        response = '{"team_size": 5, "profiles": [{"name": "lead", "description": "Coordinate the initiative.", "skills": ["planning"]}, {"name": "analyst", "description": "Analyze inputs and constraints.", "skills": ["analysis"]}, {"name": "designer", "description": "Shape a usable solution.", "skills": ["design"]}, {"name": "implementer", "description": "Implement approved work.", "skills": ["implementation"]}, {"name": "assurance", "description": "Verify outcomes and quality.", "skills": ["verification"]}]}'
        hermes = FakeHermes([result(response)])
        team = discover_profiles_via_hermes("Improve an internal operational process", "Operations owner", ["Reduce friction", "Measure outcomes"], runner=hermes)
        self.assertEqual(team["team_size"], 5)
        self.assertEqual({profile["name"] for profile in team["profiles"]}, {"lead", "analyst", "designer", "implementer", "assurance"})

    def test_invalid_response_is_bounded_and_reported(self):
        hermes = FakeHermes([result('{"team_size": 4, "profiles": []}'), result('{"team_size": 4, "profiles": []}')])
        with self.assertRaises(HermesCommandError):
            discover_profiles_via_hermes("Any customer objective", "Owner", ["Goal"], runner=hermes, max_attempts=2)
        self.assertEqual(len(hermes.calls), 2)


class DomainAgnosticProvisioningTests(unittest.TestCase):
    def test_invalid_team_has_no_side_effects(self):
        calls = []

        def runner(command, **kwargs):
            calls.append(command)
            return result()

        invalid = {"team_size": 3, "profiles": [{"name": "unsafe name", "description": "x", "skills": ["x"]}], "validation_errors": ["invalid team"]}
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                create_profiles_from_team(invalid, runner=runner, profile_root=Path(directory))
            self.assertEqual(calls, [])
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_valid_team_provisions_without_domain_specific_assets(self):
        calls = []

        def runner(command, **kwargs):
            calls.append(command)
            return result()

        team = {"team_size": 3, "profiles": [{"name": "coordination", "description": "Coordinate the workflow.", "skills": ["planning"]}, {"name": "execution", "description": "Complete approved work.", "skills": ["execution"]}, {"name": "review", "description": "Verify outcomes.", "skills": ["verification"]}], "validation_errors": []}
        with tempfile.TemporaryDirectory() as directory:
            created = create_profiles_from_team(team, runner=runner, profile_root=Path(directory), skills_by_profile={"coordination": ["official/planning/workflow"]})
            self.assertTrue(Path(directory, "coordination", "SOUL.md").exists())
        self.assertEqual(len(created), 3)
        self.assertNotIn("music", " ".join(calls).lower())
        self.assertEqual(calls[1], ["hermes", "-p", "coordination", "skills", "install", "official/planning/workflow"])


if __name__ == "__main__":
    unittest.main()
