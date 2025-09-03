from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime

class Health(BaseModel):
    status: str
    service: str
    version: str
    now: datetime
