"""Isolation helpers: namespace, network, filesystem, memory boundaries."""
from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict


class NetworkPolicy(str, Enum):
    DEFAULT_DENY = "default-deny"
    RESTRICTED = "restricted"
    OPEN = "open"


class FilesystemPolicy(str, Enum):
    ISOLATED = "isolated"
    SHARED_READ = "shared-read"
    SHARED_WRITE = "shared-write"


class MemoryPolicy(str, Enum):
    PRIVATE = "private"
    SHARED_READ = "shared-read"
    SHARED_WRITE = "shared-write"


@dataclass
class IsolationConfig:
    network: NetworkPolicy
    filesystem: FilesystemPolicy
    memory: MemoryPolicy
    data_namespace: str


def apply_isolation(cfg: IsolationConfig, workdir: Path) -> Dict[str, Any]:
    """Return environment and context overrides to enforce isolation."""
    env: Dict[str, Any] = {}

    # Network: default-deny by disabling outbound network in subprocesses
    if cfg.network == NetworkPolicy.DEFAULT_DENY:
        env["HERMES_NETWORK_POLICY"] = "deny"

    # Filesystem: isolate by setting WORKDIR to agent-specific subdir
    if cfg.filesystem == FilesystemPolicy.ISOLATED:
        agent_root = workdir / cfg.data_namespace.replace(".", "_")
        agent_root.mkdir(parents=True, exist_ok=True)
        env["HERMES_WORKDIR"] = str(agent_root)
        env["HERMES_FILESYSTEM_POLICY"] = "isolated"

    # Memory: private (no shared state) is default; enforced by process isolation
    env["HERMES_MEMORY_POLICY"] = cfg.memory.value

    return env
