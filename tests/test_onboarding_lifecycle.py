"""Tests for generic onboarding planning and approval-gated execution."""
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from runtime.onboarding_lifecycle import collect_onboarding_answers, execute_onboarding_plan
from runtime.skill_resolution import SkillCandidate


class LifecycleTests(unittest.TestCase):
    def test_collects_generic_answers(self):
        values = iter(["Accomplish a complex objective", "Project owner", "Understand the work", "Deliver outcomes", "", "recommend"])
        answers = collect_onboarding_answers(lambda prompt: next(values))
        self.assertEqual(answers.use_case, "Accomplish a complex objective")
        self.assertEqual(answers.goals, ["Understand the work", "Deliver outcomes"])
        self.assertIsNone(answers.team_size_preference)

    def test_unapproved_plan_has_no_side_effects(self):
        calls = []
        plan = {"team": {"team_size": 3, "profiles": [{"name": "a", "description": "A", "skills": ["x"]}, {"name": "b", "description": "B", "skills": ["y"]}, {"name": "c", "description": "C", "skills": ["z"]}]}, "resolved_skills": {"a": [SkillCandidate("official/a/x")], "b": [SkillCandidate("official/b/y")], "c": [SkillCandidate("official/c/z")]}}
        with self.assertRaises(PermissionError):
            execute_onboarding_plan(plan, approved=False, runner=lambda command, **kwargs: calls.append(command))
        self.assertEqual(calls, [])

    def test_approved_plan_creates_profiles_and_installs_resolved_ids(self):
        calls = []
        def runner(command, **kwargs):
            calls.append(command)
            return subprocess.CompletedProcess(command, 0, "", "")
        team = {"team_size": 3, "profiles": [{"name": "a", "description": "A", "skills": ["x"]}, {"name": "b", "description": "B", "skills": ["y"]}, {"name": "c", "description": "C", "skills": ["z"]}]}
        plan = {"team": team, "resolved_skills": {"a": [SkillCandidate("official/a/x")], "b": [SkillCandidate("official/b/y")], "c": [SkillCandidate("official/c/z")]}}
        with tempfile.TemporaryDirectory() as directory:
            result = execute_onboarding_plan(plan, approved=True, profile_root=Path(directory), runner=runner)
        self.assertEqual(len(result), 3)
        self.assertIn(["hermes", "profile", "create", "a", "--description", "A"], calls)
        self.assertIn(["hermes", "-p", "a", "skills", "install", "official/a/x"], calls)


if __name__ == "__main__":
    unittest.main()
