from fastapi import FastAPI
from app.core.config import settings
from app.routers import health, finance, haru_course
from app.db import init_db

app = FastAPI(title="Ameth", version="0.1.0")

app.include_router(health.router, prefix="")
app.include_router(finance.router, prefix="/finance", tags=["finance"])

@app.on_event("startup")
def on_startup():
    init_db()
# (verifica que ya esté; si no, se agrega)

# (verifica que ya esté; si no, se agrega)

from app.routers import health, finance, haru_course
app.include_router(haru_course.router, prefix="/haru", tags=["haru-course"])
app.include_router(haru_course.router, prefix="/haru", tags=["haru-course"])
