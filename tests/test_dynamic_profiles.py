"""Tests for Hermes-native dynamic profile discovery and provisioning."""
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from runtime.dynamic_profiles import HermesCommandError, create_profiles_from_team, discover_profiles_via_hermes


TEAM_JSON = '{"team_size": 3, "profiles": [{"name": "lead", "description": "Coordinate the team.", "skills": ["planning"]}, {"name": "builder", "description": "Build the work.", "skills": ["delivery"]}, {"name": "reviewer", "description": "Review results.", "skills": ["quality"]}]}'
TEAM = {"team_size": 3, "profiles": [{"name": "lead", "description": "Coordinate the team.", "skills": ["planning"]}, {"name": "builder", "description": "Build the work.", "skills": ["delivery"]}, {"name": "reviewer", "description": "Review results.", "skills": ["quality"]}], "validation_errors": []}


def completed(stdout: str = "", stderr: str = "", returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr=stderr)


class DiscoveryTests(unittest.TestCase):
    def test_discovery_uses_noninteractive_cli(self):
        calls = []

        def runner(command, **kwargs):
            calls.append((command, kwargs))
            return completed(TEAM_JSON)

        result = discover_profiles_via_hermes("Test use case", "Founder", ["Ship product"], runner=runner)
        self.assertEqual(result["validation_errors"], [])
        self.assertEqual(calls[0][0][:3], ["hermes", "chat", "-q"])
        self.assertIn("-Q", calls[0][0])
        self.assertEqual(calls[0][1]["check"], False)

    def test_discovery_retries_invalid_response(self):
        responses = iter([completed("not json"), completed(TEAM_JSON)])
        calls = []

        def runner(command, **kwargs):
            calls.append(command)
            return next(responses)

        result = discover_profiles_via_hermes("Use case", "Role", ["Goal"], runner=runner)
        self.assertEqual(result["team_size"], 3)
        self.assertEqual(len(calls), 2)
        self.assertIn("invalid", calls[1][-2].lower())

    def test_discovery_stops_after_max_attempts(self):
        def runner(command, **kwargs):
            return completed("not json")

        with self.assertRaises(HermesCommandError):
            discover_profiles_via_hermes("Use case", "Role", ["Goal"], runner=runner, max_attempts=2)


class ProvisioningTests(unittest.TestCase):
    def test_invalid_team_is_rejected_before_subprocess(self):
        calls = []

        def runner(command, **kwargs):
            calls.append(command)
            return completed()

        with self.assertRaises(ValueError):
            create_profiles_from_team({"team_size": 3, "profiles": [], "validation_errors": ["invalid team"]}, runner=runner)
        self.assertEqual(calls, [])

    def test_profiles_skills_and_soul_are_created(self):
        calls = []

        def runner(command, **kwargs):
            calls.append(command)
            return completed()

        with tempfile.TemporaryDirectory() as directory:
            results = create_profiles_from_team(TEAM, runner=runner, profile_root=Path(directory), skills_by_profile={"lead": ["official/project/planning"]})
            soul = Path(directory, "lead", "SOUL.md").read_text(encoding="utf-8")

        self.assertEqual(len(results), 3)
        self.assertEqual(calls[0], ["hermes", "profile", "create", "lead", "--description", "Coordinate the team."])
        self.assertEqual(calls[1], ["hermes", "-p", "lead", "skills", "install", "official/project/planning"])
        self.assertIn("# lead", soul)
        self.assertIn("Coordinate the team.", soul)
        self.assertIn("- planning", soul)

    def test_profile_creation_failure_is_reported(self):
        def runner(command, **kwargs):
            return completed(stderr="permission denied", returncode=1)

        with self.assertRaises(HermesCommandError):
            create_profiles_from_team(TEAM, runner=runner)


if __name__ == "__main__":
    unittest.main()
