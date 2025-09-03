from __future__ import annotations
import json
from pathlib import Path
from threading import Lock
from typing import Any

class JsonStore:
    def __init__(self, base_dir: str):
        self.base = Path(base_dir)
        self.base.mkdir(parents=True, exist_ok=True)
        self._locks: dict[str, Lock] = {}

    def _path(self, name: str) -> Path:
        return self.base / name

    def _lock(self, name: str) -> Lock:
        if name not in self._locks:
            self._locks[name] = Lock()
        return self._locks[name]

    def read(self, name: str, default: Any) -> Any:
        p = self._path(name)
        if not p.exists():
            return default
        with self._lock(name):
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                return default

    def write(self, name: str, data: Any) -> None:
        p = self._path(name)
        with self._lock(name):
            tmp = p.with_suffix(".tmp")
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            tmp.replace(p)
