import pytest
from runtime.capabilities import Capability, REQUIRED_CAPABILITIES, inspect_runtime
from runtime.installation_state import InstallationState, InstallationStatus, StateTransitionError

class SupportedProbe:
    def runtime_identity(self): return "Hermes", "test-1.0"
    def capabilities(self): return [Capability(name, True, f"verified:{name}") for name in REQUIRED_CAPABILITIES]

def test_unavailable_runtime_fails_closed():
    report=inspect_runtime()
    assert report.status == "blocked"
    assert set(report.blockers) == REQUIRED_CAPABILITIES
    assert all(capability.remediation for capability in report.capabilities)

def test_supported_probe_reports_only_proven_surfaces():
    report=inspect_runtime(SupportedProbe())
    assert report.status == "supported"
    assert all(capability.surface.startswith("verified:") for capability in report.capabilities)

def test_running_requires_provisioning_and_smoke_tests():
    state=InstallationState.discovered({"repository":"juliench82/hermes-agent-forge"})
    for status in (InstallationStatus.ONBOARDING,InstallationStatus.PROPOSED,InstallationStatus.APPROVED,InstallationStatus.PROVISIONING,InstallationStatus.PROVISIONED,InstallationStatus.SMOKE_TESTED): state.transition(status)
    with pytest.raises(StateTransitionError): state.transition(InstallationStatus.RUNNING)
    state.provisioning={"complete":True}; state.smoke_tests={"passed":True}; state.transition(InstallationStatus.RUNNING)
    assert state.status is InstallationStatus.RUNNING
