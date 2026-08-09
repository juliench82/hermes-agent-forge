import tempfile
import unittest
from pathlib import Path

from runtime.hermes_kernel import (
    ContractError, PermissionDenied, Profile, ProfileResolver, SessionContext,
    SkillLoader, TaskStore, Tool, ToolRegistry, validate_handoff,
)


class KernelTests(unittest.TestCase):
    def test_task_lifecycle_and_invalid_transition(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = TaskStore(Path(tmp) / "state.db")
            store.create_task("T-1", "build", "orchestrator", acceptance_criteria=["works"])
            store.transition("T-1", "claimed", "builder", owner="builder")
            store.transition("T-1", "in_progress", "builder")
            store.transition("T-1", "review", "builder")
            store.transition("T-1", "done", "quality-guardian")
            with self.assertRaises(ContractError):
                store.transition("T-1", "todo", "builder")
            store.close()

    def test_tool_permissions_and_normalized_failure(self):
        profile = Profile("builder", "build", frozenset({"read", "write"}), frozenset({"write"}))
        registry = ToolRegistry()
        registry.register(Tool("read", lambda: "ok"))
        registry.register(Tool("write", lambda: "changed", "external-write"))
        self.assertEqual(registry.dispatch("read", profile)["result"], "ok")
        with self.assertRaises(PermissionDenied):
            registry.dispatch("write", profile)
        self.assertEqual(registry.dispatch("write", profile, approved=True)["result"], "changed")
        registry.register(Tool("broken", lambda: 1 / 0))
        profile = Profile("builder", "build", frozenset({"broken"}))
        result = registry.dispatch("broken", profile)
        self.assertFalse(result["ok"])
        self.assertEqual(result["error_type"], "ZeroDivisionError")

    def test_profile_and_progressive_skill_loading(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile_dir = root / "profiles" / "builder"
            profile_dir.mkdir(parents=True)
            (profile_dir / "profile.yaml").write_text("name: builder\npurpose: build\nallowed_tools:\n  - read\nrequires_approval_for:\n  - write\nskills:\n  - build\n")
            profile = ProfileResolver(root).load("builder")
            self.assertEqual(profile.name, "builder")
            skill_dir = root / "skills"; skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text("---\nname: build\nversion: 1\ntriggers:\n  - approved task\nrisk_level: local-write\n---\n# Procedure\n")
            skills = SkillLoader(skill_dir).index()
            self.assertEqual(skills["build"].triggers, ("approved task",))

    def test_session_budget_and_handoff(self):
        session = SessionContext("builder", {"policy": "stable"}, {"task": "T-1"}, max_turns=2, max_tool_calls=3)
        self.assertEqual(session.prompt_snapshot()["stable"]["policy"], "stable")
        with self.assertRaises(ContractError):
            session.check_budget(3, 0)
        validate_handoff({"task_id": "T-1", "profile": "builder", "status": "completed", "summary": "done", "acceptance_criteria": [], "tests": [{"result": "passed"}], "next_action": "review"})
        with self.assertRaises(ContractError):
            validate_handoff({"task_id": "T-1", "profile": "builder", "status": "completed", "summary": "done", "acceptance_criteria": [], "tests": [], "next_action": "review"})


if __name__ == "__main__":
    unittest.main()
