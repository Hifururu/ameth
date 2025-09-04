import os
import json
from pathlib import Path
from fastapi import HTTPException

# Directorio de datos (puedes sobreescribir con la env var AMETH_DATA_DIR)
DATA_DIR = Path(os.getenv("AMETH_DATA_DIR", "/data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

FINANCE_FILE = DATA_DIR / "finance.json"

def _ensure_file() -> None:
    """Crea el archivo si no existe, con una lista vacía."""
    if not FINANCE_FILE.exists():
        FINANCE_FILE.write_text("[]", encoding="utf-8")

def load_finance():
    """Lee y devuelve la lista de movimientos desde JSON."""
    try:
        _ensure_file()
        raw = FINANCE_FILE.read_text(encoding="utf-8")
        return json.loads(raw or "[]")
    except Exception as e:
        # Log visible en runtime
        print(f"[FINANCE][READ][ERROR] {e}", flush=True)
        raise HTTPException(status_code=503, detail=f"storage_unavailable: {e}")

def save_finance(data) -> bool:
    """Guarda la lista de movimientos en JSON (serializa objetos raros con str)."""
    try:
        FINANCE_FILE.write_text(
            json.dumps(data, ensure_ascii=False, default=str),
            encoding="utf-8"
        )
        return True
    except Exception as e:
        print(f"[FINANCE][WRITE][ERROR] {e}", flush=True)
        raise HTTPException(status_code=503, detail=f"storage_unavailable: {e}")
