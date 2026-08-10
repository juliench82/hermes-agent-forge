from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Mapping
import shutil

class RoleAssetError(RuntimeError):
    pass

@dataclass(frozen=True)
class InstalledAsset:
    source: str
    destination: str
    sha256: str

def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()

class RoleAssetInstaller:
    """Copies only destinations explicitly supplied by the approved team manifest."""

    def install(self, source_root: Path, profile_root: Path, mapping: Mapping[str, str]) -> tuple[InstalledAsset, ...]:
        if not mapping:
            raise RoleAssetError("approved role-asset destination mapping is required")
        installed: list[InstalledAsset] = []
        source_root = source_root.resolve()
        profile_root = profile_root.resolve()
        for source_name, destination_name in sorted(mapping.items()):
            source = (source_root / source_name).resolve()
            destination = (profile_root / destination_name).resolve()
            if source_root not in source.parents or not source.is_file():
                raise RoleAssetError(f"role asset is missing or outside source root: {source_name}")
            if profile_root not in destination.parents:
                raise RoleAssetError(f"role asset destination escapes profile root: {destination_name}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists() and _digest(destination) == _digest(source):
                installed.append(InstalledAsset(source_name, destination_name, _digest(source)))
                continue
            shutil.copyfile(source, destination)
            installed.append(InstalledAsset(source_name, destination_name, _digest(destination)))
        return tuple(installed)
