from __future__ import annotations
from fastapi import APIRouter, HTTPException, Request
from app.schemas.mode import CambioModo
from app.services.json_store import JsonStore
from app.routers.mode import switch  # reutilizamos lógica de cambio de modo

router = APIRouter(tags=["phrase"])

@router.post("/phrase")
def phrase_router(payload: dict, request: Request):
    frase: str = str(payload.get("frase","")).strip().lower()
    if not frase:
        raise HTTPException(400, "Envia 'frase'")

    store: JsonStore = request.app.state.store

    if "me voy a dormir" in frase:
        return switch(CambioModo(modo="sleep"), request)
    if "me voy al trabajo" in frase:
        return switch(CambioModo(modo="work"), request)
    if "salí de mi hora de trabajo" in frase or "sali de mi hora de trabajo" in frase:
        return switch(CambioModo(modo="offwork"), request)
    return {"ok": True, "mensaje": "Frase recibida, sin acción predefinida."}
