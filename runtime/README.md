# Runtime Kernel

`hermes_kernel.py` is a dependency-free coordination kernel for the bootstrapper. It provides SQLite task persistence, audited state transitions, profile and skill discovery, tool permission checks, session budgets, and handoff validation.

## Usage

```python
from pathlib import Path
from runtime.hermes_kernel import TaskStore, ProfileResolver, ToolRegistry, SessionContext

store = TaskStore(Path(".hermes/state.db"))
store.create_task("TASK-1", "Implement a feature", "orchestrator", acceptance_criteria=["tests pass"])
store.transition("TASK-1", "claimed", "builder", owner="builder")
store.transition("TASK-1", "in_progress", "builder")
```

The kernel is intentionally model- and provider-agnostic. An adapter should own the LLM API call and use `SessionContext.check_budget()` around the agent loop. External and high-impact tools must be registered with a risk class and dispatched with explicit approval.

## Guarantees

- Invalid task transitions fail closed.
- Task events are append-only and timestamped.
- SQLite uses WAL mode for concurrent readers.
- Tool failures are normalized into structured results.
- Completed handoffs require test evidence.
- Profiles and skills are loaded progressively instead of injecting every body into every prompt.

Run the repository smoke test with `python -m unittest discover -s tests -v`.
