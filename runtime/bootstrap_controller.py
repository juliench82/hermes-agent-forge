from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable


BOOTSTRAP_CONTROLLER_PROFILE_NAMES = frozenset({"default", "main"})


class BootstrapContractError(ValueError):
    """Raised when a customer team violates the bootstrap boundary."""


@dataclass(frozen=True)
class BootstrapControllerContract:
    """Deterministic, side-effect-free contract for the fixed Hermes controller."""

    controller_profile_names: frozenset[str] = BOOTSTRAP_CONTROLLER_PROFILE_NAMES
    live_provisioning: bool = False
    max_repair_attempts: int = 3

    def __post_init__(self) -> None:
        if not self.controller_profile_names:
            raise BootstrapContractError("at least one controller profile name is required")
        if self.max_repair_attempts < 0:
            raise BootstrapContractError("max_repair_attempts cannot be negative")
        if self.live_provisioning:
            raise BootstrapContractError("live provisioning is not enabled by this contract")

    def validate_customer_profile_names(self, names: Iterable[str]) -> tuple[str, ...]:
        """Validate dynamic customer names without selecting or creating profiles."""

        normalized = tuple(name.strip() for name in names)
        if any(not name for name in normalized):
            raise BootstrapContractError("customer profile names must be non-empty")
        if any(name in self.controller_profile_names for name in normalized):
            raise BootstrapContractError("customer teams cannot claim the bootstrap controller")
        if len(set(normalized)) != len(normalized):
            raise BootstrapContractError("customer profile names must be unique")
        return normalized


def canonical_plan_hash(plan: Any) -> str:
    """Return a stable SHA-256 hash for an approval-bound plan."""

    encoded = json.dumps(plan, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def approval_matches(plan: Any, approved_plan_hash: str) -> bool:
    """Check that approval is bound to this exact canonical plan."""

    return canonical_plan_hash(plan) == approved_plan_hash
