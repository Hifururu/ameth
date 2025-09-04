from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, field_validator
from datetime import date
from typing import Literal, List, Dict, Any
from app.finance_storage import load_finance, save_finance

router = APIRouter(prefix="/finance", tags=["finance"])

TipoMovimiento = Literal["gasto", "ingreso"]

class RecordIn(BaseModel):
    fecha: date
    concepto: str
    categoria: str
    monto_clp: int
    tipo: TipoMovimiento

    @field_validator("monto_clp")
    @classmethod
    def monto_positivo(cls, v: int) -> int:
        if v < 0:
            raise ValueError("monto_clp debe ser >= 0")
        return v

@router.post("/record")
def record_item(item: RecordIn) -> Dict[str, Any]:
    """
    Forzamos serialización segura: fecha -> ISO y monto_clp -> int.
    Evita 'Object of type date is not JSON serializable'.
    """
    # dict plano desde Pydantic
    rec = item.model_dump()
    # normalizaciones explícitas
    rec["fecha"] = item.fecha.isoformat()          # "YYYY-MM-DD"
    rec["monto_clp"] = int(item.monto_clp)         # asegurar int puro

    print(f"[FINANCE][RECORD] {rec}", flush=True)

    data: List[Dict[str, Any]] = load_finance()
    data.append(rec)
    save_finance(data)
    return {"ok": True}

@router.get("/list")
def list_items() -> Dict[str, Any]:
    data = load_finance()
    data_sorted = sorted(data, key=lambda x: x.get("fecha", ""))
    return {"items": data_sorted, "count": len(data_sorted)}

@router.get("/summary")
def summary(month: str = Query(..., description="Formato YYYY-MM")) -> Dict[str, Any]:
    if len(month) != 7 or month[4] != "-":
        raise HTTPException(status_code=400, detail="Formato de mes inválido. Use YYYY-MM")

    data = load_finance()
    gastos = 0
    ingresos = 0
    items_mes = []

    for it in data:
        f = str(it.get("fecha", ""))
        if f.startswith(month):
            items_mes.append(it)
            tipo = it.get("tipo")
            try:
                monto = int(it.get("monto_clp", 0))
            except Exception:
                monto = 0
            if tipo == "gasto":
                gastos += monto
            elif tipo == "ingreso":
                ingresos += monto

    neto = ingresos - gastos
    return {
        "month": month,
        "gastos": gastos,
        "ingresos": ingresos,
        "neto": neto,
        "count": len(items_mes),
    }
