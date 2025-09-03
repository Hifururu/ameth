from __future__ import annotations
from pydantic import BaseModel
from typing import Literal

Modo = Literal["work", "offwork", "sleep"]

class CambioModo(BaseModel):
    modo: Modo
