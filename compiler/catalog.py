from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .errors import CatalogResolutionError

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "catalog" / "index.json"


class Catalog:
    def __init__(self, index_path: Path = INDEX_PATH) -> None:
        self.index_path = index_path
        try:
            payload = json.loads(index_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CatalogResolutionError(f"cannot load catalog index: {exc}") from exc
        self._entries: dict[str, str] = payload.get("primitives", {})

    def resolve(self, reference: str) -> dict[str, Any]:
        relative_path = self._entries.get(reference)
        if not relative_path:
            raise CatalogResolutionError(f"unknown primitive: {reference}")
        path = self.index_path.parent / relative_path
        if not path.is_file():
            raise CatalogResolutionError(f"catalog file missing for {reference}: {relative_path}")
        name, version = reference.rsplit("@", 1)
        return {"reference": reference, "id": name, "version": version, "path": relative_path}

    def resolve_many(self, references: list[str]) -> list[dict[str, Any]]:
        return [self.resolve(reference) for reference in sorted(set(references))]
