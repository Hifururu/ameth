from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query, Request
from typing import Optional, List
from collections import defaultdict
from dateutil.parser import isoparse

from app.services.json_store import JsonStore
from app.schemas.finance import Movimiento, ResumenMensual

router = APIRouter(prefix="/finance", tags=["finance"])

F_MOVS = "finance.movimientos.json"

def parse_month(s: str) -> tuple[int, int]:
    try:
        y, m = s.split("-")
        return int(y), int(m)
    except Exception:
        raise HTTPException(400, "Parámetro 'month' debe ser 'YYYY-MM'")

def ensure_init(store: JsonStore):
    if store.read(F_MOVS, None) is None:
        store.write(F_MOVS, [])

@router.post("/record")
def record(mov: Movimiento, request: Request):
    store: JsonStore = request.app.state.store
    ensure_init(store)
    movs: List[dict] = store.read(F_MOVS, [])
    movs.append(mov.model_dump())
    store.write(F_MOVS, movs)
    return {"ok": True, "guardado": mov.model_dump()}

@router.get("/list")
def list_(
    request: Request,
    desde: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
    hasta: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
):
    store: JsonStore = request.app.state.store
    ensure_init(store)
    movs: List[dict] = store.read(F_MOVS, [])
    def in_range(m):
        f = isoparse(str(m["fecha"])).date()
        if desde and f < isoparse(desde).date(): return False
        if hasta and f > isoparse(hasta).date(): return False
        return True
    return [m for m in movs if in_range(m)]

@router.get("/summary", response_model=ResumenMensual)
def summary(request: Request, month: str = Query(..., description="YYYY-MM")):
    store: JsonStore = request.app.state.store
    ensure_init(store)
    year, mon = parse_month(month)
    movs: List[dict] = store.read(F_MOVS, [])
    gastos_cat = defaultdict(int)
    ingresos_cat = defaultdict(int)
    tg = ti = 0
    count = 0
    for m in movs:
        f = isoparse(str(m["fecha"])).date()
        if f.year == year and f.month == mon:
            count += 1
            monto = int(m["monto_clp"])
            if m["tipo"] == "gasto":
                gastos_cat[m["categoria"]] += monto
                tg += monto
            else:
                ingresos_cat[m["categoria"]] += monto
                ti += monto
    return ResumenMensual(
        mes=month,
        total_gastos=tg,
        total_ingresos=ti,
        neto=ti - tg,
        gastos_por_categoria=dict(gastos_cat),
        ingresos_por_categoria=dict(ingresos_cat),
        movimientos=count,
    )
