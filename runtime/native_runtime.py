"""Explicit adapter for Hermes-native runtime operations."""
from __future__ import annotations
from dataclasses import dataclass
import subprocess
from typing import Callable, Sequence

Runner = Callable[..., subprocess.CompletedProcess]


@dataclass(frozen=True)
class RuntimeResult:
    ok: bool
    command: tuple[str, ...]
    stdout: str = ""
    stderr: str = ""
    returncode: int = 0


def activate_yolo(runner: Runner = subprocess.run, hermes: str = "hermes") -> RuntimeResult:
    command = (hermes, "chat", "--command", "/yolo")
    result = runner(list(command), capture_output=True, text=True, check=False)
    return RuntimeResult(result.returncode == 0, command, result.stdout or "", result.stderr or "", result.returncode)


def terminal_command(command: Sequence[str], hermes: str = "hermes") -> tuple[str, ...]:
    return (hermes, "terminal", "exec", "--", *command)


def run_terminal(command: Sequence[str], runner: Runner = subprocess.run, hermes: str = "hermes") -> RuntimeResult:
    full_command = terminal_command(command, hermes)
    result = runner(list(full_command), capture_output=True, text=True, check=False)
    return RuntimeResult(result.returncode == 0, full_command, result.stdout or "", result.stderr or "", result.returncode)
