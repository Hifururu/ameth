import os, tempfile
from pathlib import Path
from fastapi import APIRouter

router = APIRouter()

DATA_DIR = Path(os.getenv("AMETH_DATA_DIR", "/data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/diag")
def diag():
    info = {
        "data_dir": str(DATA_DIR),
        "writable": False,
        "error": "",
        "uid": None,
        "gid": None,
    }
    try:
        info["uid"] = os.getuid() if hasattr(os, "getuid") else "n/a"
        info["gid"] = os.getgid() if hasattr(os, "getgid") else "n/a"
    except Exception:
        info["uid"] = "n/a"
        info["gid"] = "n/a"

    try:
        with tempfile.NamedTemporaryFile(dir=str(DATA_DIR), delete=True) as f:
            f.write(b"ok")
            f.flush()
        info["writable"] = True
    except Exception as e:
        info["error"] = str(e)
    return info
