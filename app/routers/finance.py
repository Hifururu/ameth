from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.db import get_db
from app.schemas import MovimientoCreate, MovimientoOut, SummaryResponse, SummaryItem
from app.services.finance import add_movimiento, resumen, balance_total

router = APIRouter()

@router.post("/add", response_model=MovimientoOut)
def add(mov: MovimientoCreate, db: Session = Depends(get_db)):
    new = add_movimiento(db, fecha=mov.fecha, concepto=mov.concepto, categoria=mov.categoria, monto_clp=mov.monto_clp, tipo=mov.tipo)
    return new

@router.get("/summary", response_model=SummaryResponse)
def summary(desde: date, hasta: date, db: Session = Depends(get_db)):
    if desde > hasta:
        raise HTTPException(status_code=400, detail="desde no puede ser mayor que hasta")
    ingresos, gastos, por_cat = resumen(db, desde, hasta)
    return SummaryResponse(
        desde=desde,
        hasta=hasta,
        ingresos=ingresos,
        gastos=gastos,
        saldo=ingresos - gastos,
        por_categoria=[SummaryItem(categoria=c, total=t) for c, t in por_cat],
    )

@router.get("/balance")
def balance(db: Session = Depends(get_db)):
    return {"balance": balance_total(db)}
