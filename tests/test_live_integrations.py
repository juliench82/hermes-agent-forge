from pathlib import Path
from subprocess import CompletedProcess

import pytest

from runtime.buzz_setup import BuzzSetup, BuzzSetupError, BuzzSetupRequired
from runtime.obsidian_setup import ObsidianSetupError, resolve_vault

def test_buzz_requires_separate_approval():
    with pytest.raises(BuzzSetupRequired):
        BuzzSetup().configure("orchestrator", False)

def test_buzz_uses_injected_runner_and_never_exposes_output():
    calls = []
    def runner(argv):
        calls.append(argv)
        return CompletedProcess(argv, 0, "private key omitted", "")
    result = BuzzSetup(runner=runner).configure("builder", True)
    assert result.configured
    assert calls == [["hermes", "-p", "builder", "gateway", "setup"]]
    assert "private" not in repr(result)

def test_buzz_failure_is_explicit():
    def runner(argv):
        return CompletedProcess(argv, 1, "", "relay unavailable")
    with pytest.raises(BuzzSetupError, match="relay unavailable"):
        BuzzSetup(runner=runner).configure("architect", True)

def test_obsidian_skip_is_explicit():
    assert resolve_vault("SKIP") == {"status": "skipped", "path": None}

def test_obsidian_path_must_be_a_writable_directory(tmp_path):
    assert resolve_vault("PATH", str(tmp_path))["status"] == "ready"
    with pytest.raises(ObsidianSetupError):
        resolve_vault("PATH", str(tmp_path / "missing"))
