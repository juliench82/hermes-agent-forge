"""Tests for safe, domain-agnostic Hermes skill resolution."""
from __future__ import annotations

import subprocess
import unittest

from runtime.skill_resolution import SkillCandidate, SkillResolutionError, install_resolved_skill, parse_skill_search_output, resolve_capability, search_skill_catalog


def result(stdout: str = "", stderr: str = "", returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess([], returncode, stdout, stderr)


class ParsingTests(unittest.TestCase):
    def test_parse_json_catalog(self):
        candidates = parse_skill_search_output('{"results": [{"identifier": "official/workflow/planning", "name": "planning"}]}')
        self.assertEqual(candidates, [SkillCandidate("official/workflow/planning", "planning", "")])

    def test_parse_text_catalog(self):
        candidates = parse_skill_search_output("official/workflow/planning\nofficial/research/analysis")
        self.assertEqual([candidate.identifier for candidate in candidates], ["official/workflow/planning", "official/research/analysis"])


class ResolutionTests(unittest.TestCase):
    def test_exact_and_single_candidate_resolution(self):
        exact = SkillCandidate("official/workflow/planning", "planning")
        self.assertEqual(resolve_capability("planning", [exact]), exact)
        self.assertEqual(resolve_capability("any label", [exact]), exact)

    def test_unresolved_and_ambiguous_capabilities_fail(self):
        with self.assertRaises(SkillResolutionError):
            resolve_capability("missing", [])
        with self.assertRaises(SkillResolutionError):
            resolve_capability("planning", [SkillCandidate("official/a/planning"), SkillCandidate("official/b/planning")])

    def test_search_uses_catalog_command_without_shell(self):
        calls = []

        def runner(command, **kwargs):
            calls.append((command, kwargs))
            return result('{"skills": [{"id": "official/workflow/planning"}]}')

        candidates = search_skill_catalog("customer-defined capability", runner=runner)
        self.assertEqual(candidates[0].identifier, "official/workflow/planning")
        self.assertEqual(calls[0][0], ["hermes", "skills", "search", "customer-defined capability"])
        self.assertFalse(calls[0][1].get("shell", False))


class InstallationTests(unittest.TestCase):
    def test_install_requires_approval(self):
        calls = []

        def runner(command, **kwargs):
            calls.append(command)
            return result()

        skill = SkillCandidate("official/workflow/planning")
        with self.assertRaises(PermissionError):
            install_resolved_skill("coordination", skill, approved=False, runner=runner)
        self.assertEqual(calls, [])

    def test_install_uses_resolved_identifier(self):
        calls = []

        def runner(command, **kwargs):
            calls.append(command)
            return result()

        install_resolved_skill("coordination", SkillCandidate("official/workflow/planning"), approved=True, runner=runner)
        self.assertEqual(calls, [["hermes", "-p", "coordination", "skills", "install", "official/workflow/planning"]])

    def test_install_failure_is_reported(self):
        def runner(command, **kwargs):
            return result(stderr="install failed", returncode=1)

        with self.assertRaises(SkillResolutionError):
            install_resolved_skill("coordination", SkillCandidate("official/workflow/planning"), approved=True, runner=runner)


if __name__ == "__main__":
    unittest.main()
