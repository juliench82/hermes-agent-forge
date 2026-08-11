"""Tests for domain-agnostic capability preflight and skill installation."""
from __future__ import annotations

import unittest

from runtime.dynamic_skill_integration import SkillPipelineError, install_team_skills, resolve_team_capabilities
from runtime.skill_resolution import SkillCandidate


TEAM = {"team_size": 3, "profiles": [{"name": "coordination", "description": "Coordinate the workflow.", "skills": ["planning"]}, {"name": "execution", "description": "Complete approved work.", "skills": ["delivery"]}, {"name": "review", "description": "Verify outcomes.", "skills": ["quality"]}]}


class SkillPreflightTests(unittest.TestCase):
    def test_all_capabilities_are_resolved(self):
        catalog = {"planning": [SkillCandidate("official/process/planning")], "delivery": [SkillCandidate("official/process/delivery")], "quality": [SkillCandidate("official/process/quality")]}
        resolved = resolve_team_capabilities(TEAM, searcher=lambda capability: catalog[capability])
        self.assertEqual(resolved["coordination"][0].identifier, "official/process/planning")
        self.assertEqual(resolved["execution"][0].identifier, "official/process/delivery")

    def test_unresolved_capability_fails_before_side_effects(self):
        with self.assertRaises(SkillPipelineError):
            resolve_team_capabilities(TEAM, searcher=lambda capability: [])

    def test_ambiguous_capability_fails(self):
        with self.assertRaises(SkillPipelineError):
            resolve_team_capabilities(TEAM, searcher=lambda capability: [SkillCandidate("official/a/value"), SkillCandidate("official/b/value")])


class InstallationTests(unittest.TestCase):
    def test_approval_is_required(self):
        with self.assertRaises(PermissionError):
            install_team_skills({"coordination": [SkillCandidate("official/process/planning")]}, approved=False)

    def test_only_resolved_identifiers_are_installed(self):
        calls = []
        def installer(profile, skill, **kwargs):
            calls.append((profile, skill.identifier, kwargs["approved"]))
        install_team_skills({"coordination": [SkillCandidate("official/process/planning")]}, approved=True, installer=installer)
        self.assertEqual(calls, [("coordination", "official/process/planning", True)])


if __name__ == "__main__":
    unittest.main()
