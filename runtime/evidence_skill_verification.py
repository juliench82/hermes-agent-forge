from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping


class SkillVerificationError(ValueError):
    """Raised when a skill cannot be tied to observed evidence."""


class ResolutionSource(str, Enum):
    CATALOG = "catalog"
    BOOTSTRAP = "bootstrap"
    LOCAL = "local"
    HERMES_GENERATED = "hermes-generated"


@dataclass(frozen=True)
class SkillResolution:
    requested_capability: str
    selected_identity: str
    resolution_source: ResolutionSource
    search_evidence: str
    installation_evidence: str = ""
    verification_evidence: str = ""
    status: str = "proposed"


class EvidenceBasedSkillVerifier:
    def validate_capabilities(self, capabilities: Iterable[str]) -> tuple[str, ...]:
        values = tuple(value.strip() for value in capabilities)
        if not 1 <= len(values) <= 10:
            raise SkillVerificationError("profiles must have between one and ten capabilities")
        if any(not value for value in values):
            raise SkillVerificationError("capabilities must be non-empty")
        if len(set(values)) != len(values):
            raise SkillVerificationError("capabilities must be unique")
        return values

    def resolve(
        self,
        requested_capability: str,
        *,
        observed_candidates: Mapping[str, ResolutionSource],
        search_evidence: str,
    ) -> SkillResolution:
        capability = requested_capability.strip()
        if not capability:
            raise SkillVerificationError("requested capability must be non-empty")
        if not search_evidence.strip():
            raise SkillVerificationError("observed search evidence is required")
        if not observed_candidates:
            raise SkillVerificationError("no observed skill identity matches the capability")
        if len(observed_candidates) != 1:
            raise SkillVerificationError("skill identity is ambiguous")
        identity, source = next(iter(observed_candidates.items()))
        if not identity.strip():
            raise SkillVerificationError("selected skill identity must be non-empty")
        return SkillResolution(
            requested_capability=capability,
            selected_identity=identity,
            resolution_source=source,
            search_evidence=search_evidence,
        )

    def verify_installed(
        self,
        resolution: SkillResolution,
        installed_identities: Iterable[str],
        verification_evidence: str,
    ) -> SkillResolution:
        installed = {identity.strip() for identity in installed_identities}
        if not verification_evidence.strip():
            raise SkillVerificationError("post-install evidence is required")
        if resolution.selected_identity not in installed:
            raise SkillVerificationError("selected skill identity was not observed after installation")
        return SkillResolution(
            **{
                **resolution.__dict__,
                "verification_evidence": verification_evidence,
                "status": "verified",
            }
        )
