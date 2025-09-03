from __future__ import annotations
from fastapi import APIRouter, HTTPException, Request
from typing import List
from datetime import date
from dateutil.parser import isoparse

from app.services.json_store import JsonStore
from app.schemas.haru import PlanHaru, LogEstudio

router = APIRouter(prefix="/haru", tags=["haru"])

F_PLAN = "haru.plan.json"
F_LOGS = "haru.logs.json"

def ensure_init(store: JsonStore):
    if store.read(F_LOGS, None) is None:
        store.write(F_LOGS, [])

@router.post("/plan")
def set_plan(plan: PlanHaru, request: Request):
    store: JsonStore = request.app.state.store
    store.write(F_PLAN, plan.model_dump())
    return {"ok": True, "plan": plan.model_dump()}

@router.get("/plan", response_model=PlanHaru)
def get_plan(request: Request):
    store: JsonStore = request.app.state.store
    plan = store.read(F_PLAN, None)
    if not plan:
        raise HTTPException(404, "No hay plan configurado.")
    return plan

@router.post("/log")
def log_estudio(log: LogEstudio, request: Request):
    store: JsonStore = request.app.state.store
    ensure_init(store)
    logs: List[dict] = store.read(F_LOGS, [])
    logs.append(log.model_dump())
    store.write(F_LOGS, logs)
    return {"ok": True, "log": log.model_dump()}

@router.get("/today")
def today(request: Request):
    store: JsonStore = request.app.state.store
    plan = store.read(F_PLAN, None)
    logs: List[dict] = store.read(F_LOGS, [])
    hoy = date.today()
    minutos_hoy = sum(int(l["minutos"]) for l in logs if isoparse(str(l["fecha"])).date() == hoy)
    faltan = max(plan["minutos_diarios"] - minutos_hoy, 0) if plan else None
    sugerencias = []
    if plan and faltan and faltan > 0:
        for kj in plan.get("kanjis", []):
            if kj and len(sugerencias) < 10:
                sugerencias.append(f"Repasar kanji: {kj}")
    checklist = []
    if faltan and faltan > 0:
        checklist.append(f"Estudiar japonés {faltan} min.")
    return {
        "hoy": str(hoy),
        "plan": plan,
        "minutos_realizados_hoy": minutos_hoy,
        "faltan_minutos_hoy": faltan,
        "sugerencias": sugerencias,
        "checklist": checklist
    }
