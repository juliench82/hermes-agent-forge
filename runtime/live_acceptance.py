from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


class LiveAcceptanceError(ValueError):
    """Raised when live acceptance is not explicitly and safely configured."""


@dataclass(frozen=True)
class LiveAcceptanceConfig:
    enabled: bool
    hermes_home: Path
    timeout_seconds: float = 30.0

    @classmethod
    def from_environment(cls, environ: dict[str, str] | None = None) -> "LiveAcceptanceConfig":
        values = os.environ if environ is None else environ
        enabled = values.get("HERMES_LIVE_TESTS") == "1"
        raw_home = values.get("HERMES_LIVE_HOME", "")
        if not enabled:
            return cls(False, Path(raw_home) if raw_home else Path("."))
        if not raw_home:
            raise LiveAcceptanceError("HERMES_LIVE_HOME is required when live tests are enabled")
        home = Path(raw_home).expanduser()
        if not home.is_absolute():
            raise LiveAcceptanceError("HERMES_LIVE_HOME must be absolute")
        try:
            timeout = float(values.get("HERMES_LIVE_TIMEOUT", "30"))
        except ValueError as exc:
            raise LiveAcceptanceError("HERMES_LIVE_TIMEOUT must be numeric") from exc
        if timeout <= 0 or timeout > 300:
            raise LiveAcceptanceError("HERMES_LIVE_TIMEOUT must be between 0 and 300 seconds")
        return cls(True, home, timeout)

    def require_enabled(self) -> None:
        if not self.enabled:
            raise LiveAcceptanceError("live Hermes acceptance is opt-in")

    def command(self, *arguments: str) -> tuple[str, ...]:
        self.require_enabled()
        if any(not isinstance(argument, str) or not argument for argument in arguments):
            raise LiveAcceptanceError("command arguments must be non-empty strings")
        return ("hermes", *arguments)
