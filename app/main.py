from datetime import datetime, timezone
from fastapi import FastAPI
from app.schemas.health import Health

# Routers (estos routers ya tienen prefix interno)
from app.routers.finance import router as finance_router
from app.routers.haru import router as haru_router
from app.routers.mode import router as mode_router
from app.routers.phrase import router as phrase_router

APP_VERSION = "v1.1"

app = FastAPI(title="Ameth API", version=APP_VERSION)

@app.get("/health", response_model=Health, tags=["meta"])
def health():
    return {
        "status": "ok",
        "service": "ameth",
        "version": APP_VERSION,
        "now": datetime.now(timezone.utc),
    }

@app.get("/version", tags=["meta"])
def version():
    return {"service": "ameth", "version": APP_VERSION}

# 👇 OJO: montamos sin prefix aquí, porque cada router ya tiene su propio prefix
app.include_router(finance_router)
app.include_router(haru_router)
app.include_router(mode_router)
app.include_router(phrase_router)
