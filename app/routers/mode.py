from __future__ import annotations
from fastapi import APIRouter, Request
from datetime import datetime
from app.services.json_store import JsonStore
from app.schemas.mode import CambioModo

router = APIRouter(prefix="/mode", tags=["mode"])

F_MODE = "mode.estado.json"

CHECKLISTS = {
    "sleep": [
        "✔ Registrar gastos del día (Lawrence).",
        "✔ Marcar fin de jornada.",
        "✔ Anotar pendientes para mañana."
    ],
    "work": [
        "✔ Revisar calendario y prioridades.",
        "✔ Abrir lista de tareas críticas.",
        "✔ Modo foco 25–50 min."
    ],
    "offwork": [
        "✔ ¿Necesitas locomoción / ruta?",
        "✔ ¿Comprar algo camino a casa?",
        "✔ Tiempo personal: japonés/dibujo/patines."
    ]
}

def ensure_init(store: JsonStore):
    if store.read(F_MODE, None) is None:
        store.write(F_MODE, {"modo":"offwork","cambio": datetime.now().isoformat()})

@router.post("/switch")
def switch(req: CambioModo, request: Request):
    store: JsonStore = request.app.state.store
    ensure_init(store)
    state = {"modo": req.modo, "cambio": datetime.now().isoformat()}
    store.write(F_MODE, state)
    return {"ok": True, "estado": state, "checklist": CHECKLISTS.get(req.modo, [])}

@router.get("/status")
def status(request: Request):
    store: JsonStore = request.app.state.store
    ensure_init(store)
    return store.read(F_MODE, {})
