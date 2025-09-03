from fastapi import FastAPI
from datetime import datetime
import os

from app.diag_routes import router as diag_router
from app.finance_routes import router as finance_router

app = FastAPI(title="Ameth API", version=os.getenv("AMETH_VERSION", "v1"))

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ameth",
        "version": os.getenv("AMETH_VERSION", "v1"),
        "now": datetime.utcnow().isoformat() + "Z",
    }

@app.get("/version")
def version():
    return {
        "version": os.getenv("AMETH_VERSION", "v1"),
        "data_dir": os.getenv("AMETH_DATA_DIR", "/data"),
    }

# Rutas
app.include_router(diag_router)       # /diag
app.include_router(finance_router)    # /finance/*
