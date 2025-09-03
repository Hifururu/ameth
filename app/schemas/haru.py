from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional

class PlanHaru(BaseModel):
    minutos_diarios: int = Field(..., gt=0)
    kanjis: List[str] = []

class LogEstudio(BaseModel):
    fecha: str      # YYYY-MM-DD
    actividad: str
    minutos: int = Field(..., gt=0)
    notas: Optional[str] = None
