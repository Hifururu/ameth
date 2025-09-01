from datetime import date
from typing import Optional, List, Literal
from pydantic import BaseModel, Field

# =========================
# Finanzas (Lawrence)
# =========================

class MovimientoCreate(BaseModel):
    fecha: date
    concepto: str = Field(min_length=1, max_length=200)
    # categoria ahora es OPCIONAL; si no viene, Lawrence la deduce
    categoria: Optional[str] = None
    monto_clp: int
    tipo: Literal["ingreso", "gasto", "futuro"]

class MovimientoOut(MovimientoCreate):
    id: int
    class Config:
        from_attributes = True

class SummaryItem(BaseModel):
    categoria: str
    total: int

class SummaryResponse(BaseModel):
    desde: date
    hasta: date
    ingresos: int
    gastos: int
    saldo: int
    por_categoria: List[SummaryItem]

# =========================
# Haru (estudio japonés)
# =========================

class StudyLogCreate(BaseModel):
    fecha: date
    minutos: int
    tema: Optional[str] = None
    kanjis: Optional[List[str]] = None

class StudyLogOut(StudyLogCreate):
    id: int
    class Config:
        from_attributes = True

class StudySummary(BaseModel):
    desde: date
    hasta: date
    sesiones: int
    total_minutos: int
    kanjis_unicos: int
    ultimos_kanjis: List[str]

