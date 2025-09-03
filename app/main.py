from __future__ import annotations
import os
from datetime import datetime
from fastapi import FastAPI
from app.services.json_store import JsonStore
from app.schemas.health import Health

SERVICE = "ameth"
VERSION = "v1.1"

DATA_DIR = os.getenv("DATA_DIR", "./data")
store = JsonStore(DATA_DIR)

app = FastAPI(title="Ameth API", version=VERSION)

# guardar store en app.state para acceder desde routers (evita import circular)
app.state.store = store

# Routers
from app.routers.finance import router as finance_router
from app.routers.haru import router as haru_router
from app.routers.mode import router as mode_router
from app.routers.phrase import router as phrase_router

app.include_router(finance_router)
app.include_router(haru_router)
app.include_router(mode_router)
app.include_router(phrase_router)

@app.get("/health", response_model=Health)
def health():
    return Health(status="ok", service=SERVICE, version=VERSION, now=datetime.now())

@app.get("/version")
def version():
    return {"service": SERVICE, "version": VERSION}
