from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Protocol

from runtime.bootstrap_controller import canonical_plan_hash


class LedgerError(ValueError):
    """Raised when installation state would become untruthful or invalid."""


class InstallationState(str, Enum):
    PLANNED = "planned"
    APPROVED = "approved"
    PROVISIONING = "provisioning"
    VERIFYING = "verifying"
    REPAIRING = "repairing"
    COMPLETED = "completed"
    PARTIAL = "partial"
    ADMIN_ACTION_REQUIRED = "admin_action_required"
    FAILED = "failed"


@dataclass(frozen=True)
class OperationResult:
    kind: str
    target: str
    required: bool
    status: str
    evidence: str = ""

    @property
    def verified(self) -> bool:
        return self.status == "verified" and bool(self.evidence.strip())


class AdministratorNotifier(Protocol):
    def notify(self, ledger: "InstallationLedger") -> None: ...


@dataclass
class InstallationLedger:
    plan: Any
    max_repair_attempts: int = 3
    state: InstallationState = InstallationState.PLANNED
    approved_plan_hash: str | None = None
    repair_attempts: int = 0
    operations: list[OperationResult] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.max_repair_attempts < 0:
            raise LedgerError("max_repair_attempts cannot be negative")

    @property
    def plan_hash(self) -> str:
        return canonical_plan_hash(self.plan)

    def approve(self, approved_plan_hash: str) -> None:
        self._require_state(InstallationState.PLANNED)
        if approved_plan_hash != self.plan_hash:
            raise LedgerError("approval does not match the exact plan")
        self.approved_plan_hash = approved_plan_hash
        self.state = InstallationState.APPROVED

    def begin_provisioning(self) -> None:
        self._require_state(InstallationState.APPROVED)
        self.state = InstallationState.PROVISIONING

    def record(self, result: OperationResult) -> None:
        if self.state not in {InstallationState.PROVISIONING, InstallationState.REPAIRING}:
            raise LedgerError("operations can only be recorded while provisioning or repairing")
        if result.kind not in {"profile", "skill", "asset"}:
            raise LedgerError("operation kind must be profile, skill, or asset")
        if not result.target.strip():
            raise LedgerError("operation target is required")
        self.operations = [
            operation
            for operation in self.operations
            if (operation.kind, operation.target) != (result.kind, result.target)
        ]
        self.operations.append(result)

    def begin_verification(self) -> None:
        self._require_state(InstallationState.PROVISIONING)
        self.state = InstallationState.VERIFYING

    def complete(self) -> None:
        self._require_state(InstallationState.VERIFYING)
        if any(operation.required and not operation.verified for operation in self.operations):
            raise LedgerError("all required operations must be verified before completion")
        self.state = InstallationState.COMPLETED

    def mark_partial(self) -> None:
        self._require_state(InstallationState.VERIFYING)
        self.state = InstallationState.PARTIAL

    def begin_repair(self, notifier: AdministratorNotifier | None = None) -> None:
        if self.state not in {InstallationState.VERIFYING, InstallationState.PARTIAL}:
            raise LedgerError("repair can only follow verification or partial state")
        if self.repair_attempts >= self.max_repair_attempts:
            self.state = InstallationState.ADMIN_ACTION_REQUIRED
            if notifier is not None:
                notifier.notify(self)
            return
        self.repair_attempts += 1
        self.state = InstallationState.REPAIRING

    def finish_repair(self) -> None:
        self._require_state(InstallationState.REPAIRING)
        self.state = InstallationState.VERIFYING

    def persist(self, path: Path) -> None:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "plan": self.plan,
            "plan_hash": self.plan_hash,
            "approved_plan_hash": self.approved_plan_hash,
            "max_repair_attempts": self.max_repair_attempts,
            "repair_attempts": self.repair_attempts,
            "state": self.state.value,
            "operations": [asdict(operation) for operation in self.operations],
        }
        descriptor, temporary = tempfile.mkstemp(prefix=".ledger.", dir=destination.parent)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, sort_keys=True)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, destination)
        except Exception:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            raise

    @classmethod
    def load(cls, path: Path) -> "InstallationLedger":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        ledger = cls(
            plan=payload["plan"],
            max_repair_attempts=payload["max_repair_attempts"],
            state=InstallationState(payload["state"]),
            approved_plan_hash=payload.get("approved_plan_hash"),
            repair_attempts=payload["repair_attempts"],
            operations=[OperationResult(**operation) for operation in payload["operations"]],
        )
        if payload["plan_hash"] != ledger.plan_hash:
            raise LedgerError("persisted plan hash does not match the plan")
        if ledger.approved_plan_hash not in {None, ledger.plan_hash}:
            raise LedgerError("persisted approval does not match the plan")
        return ledger

    def _require_state(self, state: InstallationState) -> None:
        if self.state != state:
            raise LedgerError(f"expected {state.value}, got {self.state.value}")
