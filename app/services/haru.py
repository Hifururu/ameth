from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import date
from app import models

def log_session(db: Session, *, fecha: date, minutos: int, tema: str | None, kanjis: list[str] | None):
    ks = ",".join(kanjis) if kanjis else None
    s = models.StudySession(fecha=fecha, minutos=minutos, tema=tema, kanjis=ks)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

def summary(db: Session, desde: date, hasta: date):
    q = select(func.count(models.StudySession.id), func.sum(models.StudySession.minutos))\
        .where(models.StudySession.fecha.between(desde, hasta))
    sesiones, total_min = db.execute(q).one_or_none() or (0, 0)
    sesiones = int(sesiones or 0)
    total_min = int(total_min or 0)

    q2 = select(models.StudySession.kanjis)\
        .where(models.StudySession.fecha.between(desde, hasta))\
        .order_by(models.StudySession.fecha.desc(), models.StudySession.id.desc())
    rows = db.execute(q2).all()
    seen = []
    unique = set()
    for (csv,) in rows:
        if not csv:
            continue
        for k in csv.split(","):
            k = k.strip()
            if not k:
                continue
            seen.append(k)
            unique.add(k)
    ultimos = []
    for k in seen:
        if k not in ultimos:
            ultimos.append(k)
        if len(ultimos) >= 10:
            break
    return sesiones, total_min, len(unique), ultimos
