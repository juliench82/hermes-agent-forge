from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

TASK_STATES = {"todo", "claimed", "in_progress", "review", "blocked", "done"}
TRANSITIONS = {
    "todo": {"claimed", "blocked"},
    "claimed": {"in_progress", "blocked"},
    "in_progress": {"review", "blocked"},
    "review": {"in_progress", "done", "blocked"},
    "blocked": {"todo", "claimed"},
    "done": set(),
}

class ContractError(ValueError):
    pass

class PermissionDenied(PermissionError):
    pass

def _now() -> float:
    return time.time()

def _front_matter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    lines = text.splitlines()[1:]
    try:
        end = lines.index("---")
    except ValueError:
        return {}
    result: dict[str, Any] = {}
    key = None
    for line in lines[:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and key:
            result.setdefault(key, []).append(line[4:].strip().strip("'\""))
        elif ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            key, value = k.strip(), v.strip().strip("'\"")
            result[key] = [] if not value else value
    return result

@dataclass(frozen=True)
class Profile:
    name: str
    purpose: str
    allowed_tools: frozenset[str] = frozenset()
    requires_approval_for: frozenset[str] = frozenset()
    skills: tuple[str, ...] = ()

class ProfileResolver:
    def __init__(self, root: Path):
        self.root = Path(root)

    def load(self, name: str) -> Profile:
        path = self.root / "profiles" / name / "profile.yaml"
        if not path.is_file():
            raise ContractError(f"profile contract missing: {path}")
        text = path.read_text()
        data = _front_matter(text) if text.startswith("---") else _front_matter("---\n" + text + "\n---")
        required = {"name", "purpose", "allowed_tools", "requires_approval_for"}
        missing = required - data.keys()
        if missing:
            raise ContractError(f"profile {name} missing: {', '.join(sorted(missing))}")
        return Profile(str(data["name"]), str(data["purpose"]), frozenset(data["allowed_tools"] or []), frozenset(data["requires_approval_for"] or []), tuple(data.get("skills") or []))

@dataclass(frozen=True)
class Skill:
    name: str
    version: str
    triggers: tuple[str, ...]
    risk_level: str
    body: str

class SkillLoader:
    def __init__(self, root: Path):
        self.root = Path(root)

    def index(self) -> dict[str, Skill]:
        skills: dict[str, Skill] = {}
        for path in self.root.glob("**/SKILL.md"):
            text = path.read_text()
            meta = _front_matter(text)
            if not meta.get("name"):
                raise ContractError(f"skill missing name: {path}")
            name = str(meta["name"])
            if name in skills:
                raise ContractError(f"duplicate skill: {name}")
            skills[name] = Skill(name, str(meta.get("version", "1")), tuple(meta.get("triggers") or []), str(meta.get("risk_level", "read")), text.split("---", 2)[-1].strip())
        return skills

@dataclass(frozen=True)
class Tool:
    name: str
    handler: Callable[..., Any]
    risk_class: str = "read-only"
    check_fn: Callable[[], bool] = lambda: True

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ContractError(f"duplicate tool: {tool.name}")
        self._tools[tool.name] = tool

    def available(self, profile: Profile) -> list[str]:
        return sorted(n for n, t in self._tools.items() if n in profile.allowed_tools and t.check_fn())

    def dispatch(self, name: str, profile: Profile, approved: bool = False, **kwargs: Any) -> Any:
        if name not in self._tools:
            raise ContractError(f"unknown tool: {name}")
        tool = self._tools[name]
        if name not in profile.allowed_tools or not tool.check_fn():
            raise PermissionDenied(f"tool unavailable for profile: {name}")
        if tool.risk_class in {"external-write", "high-impact"} and (name in profile.requires_approval_for or tool.risk_class == "high-impact") and not approved:
            raise PermissionDenied(f"approval required: {name}")
        try:
            return {"ok": True, "result": tool.handler(**kwargs)}
        except Exception as exc:
            return {"ok": False, "error_type": type(exc).__name__, "retryable": False, "message": str(exc)}

class TaskStore:
    def __init__(self, path: Path):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript("CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, data TEXT NOT NULL, status TEXT NOT NULL, owner TEXT, updated REAL NOT NULL); CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT NOT NULL, actor TEXT NOT NULL, event TEXT NOT NULL, data TEXT NOT NULL, created REAL NOT NULL); CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, profile TEXT NOT NULL, snapshot TEXT NOT NULL, created REAL NOT NULL);")
        self.db.commit()

    def create_task(self, task_id: str, objective: str, actor: str, **fields: Any) -> None:
        data = {"id": task_id, "objective": objective, "acceptance_criteria": fields.pop("acceptance_criteria", []), **fields}
        self.db.execute("INSERT INTO tasks VALUES (?, ?, 'todo', NULL, ?)", (task_id, json.dumps(data), _now()))
        self._event(task_id, actor, "created", data)
        self.db.commit()

    def transition(self, task_id: str, state: str, actor: str, reason: str = "", owner: str | None = None) -> None:
        if state not in TASK_STATES:
            raise ContractError(f"invalid task state: {state}")
        row = self.db.execute("SELECT status FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row or state not in TRANSITIONS[row["status"]]:
            raise ContractError(f"invalid transition to {state} for {task_id}")
        self.db.execute("UPDATE tasks SET status=?, owner=COALESCE(?, owner), updated=? WHERE id=?", (state, owner, _now(), task_id))
        self._event(task_id, actor, "transition", {"to": state, "reason": reason, "owner": owner})
        self.db.commit()

    def _event(self, task_id: str, actor: str, event: str, data: Any) -> None:
        self.db.execute("INSERT INTO events(task_id, actor, event, data, created) VALUES (?, ?, ?, ?, ?)", (task_id, actor, event, json.dumps(data), _now()))

    def close(self) -> None:
        self.db.close()

@dataclass(frozen=True)
class SessionContext:
    profile: str
    stable: dict[str, Any]
    context: dict[str, Any]
    volatile: dict[str, Any] = field(default_factory=dict)
    max_turns: int = 25
    max_tool_calls: int = 30

    def prompt_snapshot(self) -> dict[str, Any]:
        return {"stable": self.stable, "context": self.context, "volatile": self.volatile}

    def check_budget(self, turns: int, tool_calls: int) -> None:
        if turns > self.max_turns or tool_calls > self.max_tool_calls:
            raise ContractError("session iteration budget exceeded")

def validate_handoff(handoff: dict[str, Any]) -> None:
    required = {"task_id", "profile", "status", "summary", "acceptance_criteria", "tests", "next_action"}
    missing = required - handoff.keys()
    if missing:
        raise ContractError(f"handoff missing: {', '.join(sorted(missing))}")
    if handoff["status"] == "completed" and not handoff["tests"]:
        raise ContractError("completed handoff requires test evidence")
