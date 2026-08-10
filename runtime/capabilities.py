from dataclasses import asdict, dataclass
from typing import Protocol, Sequence

REQUIRED_CAPABILITIES = frozenset({"profile.create", "profile.start", "profile.status", "runtime.configure", "runtime.isolation", "runtime.audit", "runtime.confirmation", "runtime.secrets"})

@dataclass(frozen=True)
class Capability:
    name: str
    available: bool
    surface: str | None = None
    remediation: str | None = None

@dataclass(frozen=True)
class CapabilityReport:
    status: str
    runtime: str
    runtime_version: str | None
    capabilities: tuple[Capability, ...]
    blockers: tuple[str, ...]
    def to_dict(self):
        return {"status": self.status, "runtime": self.runtime, "runtime_version": self.runtime_version, "capabilities": [asdict(c) for c in self.capabilities], "blockers": list(self.blockers)}

class HermesRuntimeProbe(Protocol):
    def runtime_identity(self) -> tuple[str, str | None]: ...
    def capabilities(self) -> Sequence[Capability]: ...

class UnavailableRuntimeProbe:
    def runtime_identity(self): return "Hermes", None
    def capabilities(self):
        return [Capability(name, False, remediation="Install a supported Hermes runtime and configure its documented capability introspector.") for name in sorted(REQUIRED_CAPABILITIES)]

def inspect_runtime(probe: HermesRuntimeProbe | None = None) -> CapabilityReport:
    probe = probe or UnavailableRuntimeProbe()
    runtime, version = probe.runtime_identity()
    reported = {c.name: c for c in probe.capabilities()}
    capabilities = tuple(reported.get(name, Capability(name, False, remediation="The runtime did not prove this required capability.")) for name in sorted(REQUIRED_CAPABILITIES))
    blockers = tuple(c.name for c in capabilities if not c.available)
    return CapabilityReport("supported" if not blockers else "blocked", runtime, version, capabilities, blockers)
