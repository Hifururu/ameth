from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.db import get_db
from app.schemas import StudyLogCreate, StudyLogOut, StudySummary
from app.services.haru import log_session, summary
from app.agents.haru import KANJIS_N5

router = APIRouter()

@router.get("/kanjis_n5")
def kanjis_n5():
    return {"count": len(KANJIS_N5), "kanjis": KANJIS_N5}

@router.post("/study/log", response_model=StudyLogOut)
def study_log(payload: StudyLogCreate, db: Session = Depends(get_db)):
    s = log_session(db, fecha=payload.fecha, minutos=payload.minutos, tema=payload.tema, kanjis=payload.kanjis)
    return s

@router.get("/study/summary", response_model=StudySummary)
def study_summary(desde: date, hasta: date, db: Session = Depends(get_db)):
    if desde > hasta:
        raise HTTPException(status_code=400, detail="desde no puede ser mayor que hasta")
    sesiones, total_min, k_uni, ult = summary(db, desde, hasta)
    return StudySummary(
        desde=desde,
        hasta=hasta,
        sesiones=sesiones,
        total_minutos=total_min,
        kanjis_unicos=k_uni,
        ultimos_kanjis=ult
    )
