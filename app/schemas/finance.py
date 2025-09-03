from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal

TipoMovimiento = Literal["gasto", "ingreso"]

class Movimiento(BaseModel):
    fecha: str  # YYYY-MM-DD
    concepto: str
    categoria: str
    monto_clp: int = Field(..., ge=0)
    tipo: TipoMovimiento

class ResumenMensual(BaseModel):
    mes: str  # YYYY-MM
    total_gastos: int
    total_ingresos: int
    neto: int
    gastos_por_categoria: dict[str, int]
    ingresos_por_categoria: dict[str, int]
    movimientos: int
