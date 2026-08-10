from subprocess import CompletedProcess

from runtime.capabilities import REQUIRED_CAPABILITIES
from runtime.hermes_cli_probe import HermesCliProbe


def successful_runner(argv):
    if argv[-1] == "--version" and len(argv) == 2:
        return CompletedProcess(argv, 0, "Hermes 1.2.3", "")
    return CompletedProcess(argv, 0, "help", "")


def test_cli_probe_reports_supported_when_all_help_surfaces_exist():
    probe = HermesCliProbe(runner=successful_runner)
    name, version = probe.runtime_identity()
    assert name == "Hermes"
    assert version == "Hermes 1.2.3"
    capabilities = {capability.name: capability for capability in probe.capabilities()}
    for name in ("profile.create", "profile.status", "profile.start", "runtime.configure", "runtime.isolation"):
        assert capabilities[name].available
        assert capabilities[name].surface.startswith("hermes ")
    for name in ("runtime.audit", "runtime.confirmation", "runtime.secrets"):
        assert not capabilities[name].available


def test_cli_probe_fails_closed_when_executable_is_missing():
    def missing(argv):
        raise FileNotFoundError

    probe = HermesCliProbe(runner=missing)
    capabilities = {capability.name: capability for capability in probe.capabilities()}
    blocked = {name for name, capability in capabilities.items() if not capability.available}
    assert blocked == set(REQUIRED_CAPABILITIES)
