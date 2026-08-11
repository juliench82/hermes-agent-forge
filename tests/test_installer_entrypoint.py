"""Tests for the real installer entrypoint's lifecycle boundary."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from runtime.onboarding_lifecycle import OnboardingAnswers
from scripts import hermes_forge_install as installer


class InstallerEntrypointTests(unittest.TestCase):
    def setUp(self):
        self.answers = OnboardingAnswers("Accomplish an arbitrary objective", "Project owner", ["Deliver an outcome"])
        self.plan = {
            "answers": self.answers,
            "team": {"team_size": 3, "profiles": [
                {"name": "lead", "description": "Coordinate the work.", "skills": ["coordination"]},
                {"name": "maker", "description": "Produce the deliverable.", "skills": ["production"]},
                {"name": "reviewer", "description": "Validate the result.", "skills": ["validation"]},
            ]},
            "resolved_skills": {
                "lead": [type("Candidate", (), {"identifier": "official/coordination"})()],
                "maker": [type("Candidate", (), {"identifier": "official/production"})()],
                "reviewer": [type("Candidate", (), {"identifier": "official/validation"})()],
            },
        }

    def test_rejection_does_not_execute(self):
        calls = []
        with patch.object(installer, "collect_onboarding_answers", return_value=self.answers), patch.object(installer, "prepare_onboarding_plan", return_value=self.plan), patch.object(installer, "execute_onboarding_plan", side_effect=lambda *args, **kwargs: calls.append(args)):
            result = installer.main(lambda prompt: "no")
        self.assertEqual(result, 2)
        self.assertEqual(calls, [])

    def test_plan_contains_resolved_identifiers_and_assets(self):
        rendered = installer.render_plan(self.plan)
        self.assertIn("official/coordination", rendered)
        self.assertIn("config.yaml", rendered)
        self.assertIn("SOUL.md", rendered)

    def test_failure_state_is_truthful(self):
        with tempfile.TemporaryDirectory() as directory:
            state_file = Path(directory) / "installation_state.json"
            with patch.object(installer, "STATE_FILE", state_file), patch.object(installer, "FORGE_HOME", Path(directory)), patch.object(installer, "collect_onboarding_answers", return_value=self.answers), patch.object(installer, "prepare_onboarding_plan", return_value=self.plan), patch.object(installer, "execute_onboarding_plan", side_effect=RuntimeError("skill installation failed")):
                result = installer.main(lambda prompt: "yes")
            self.assertEqual(result, 1)
            state = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "failed")
            self.assertIn("skill installation failed", state["error"])


if __name__ == "__main__":
    unittest.main()
