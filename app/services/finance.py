from sqlalchemy.orm import Session
from sqlalchemy import select, func, case
from datetime import date
from app import models
from app.agents.lawrence import auto_categoria
from app.core.textutil import normalize

def add_movimiento(db: Session, *, fecha: date, concepto: str, categoria: str, monto_clp: int, tipo: str):
    if tipo not in ("ingreso","gasto","futuro"):
        raise ValueError("tipo invalido: debe ser ingreso/gasto/futuro")

    cat = (categoria or "").strip()
    if not cat or normalize(cat) == "auto":
        cat = auto_categoria(concepto)

    mov = models.Movimiento(
        fecha=fecha,
        concepto=concepto,
        categoria=cat,
        monto_clp=monto_clp,
        tipo=tipo
    )
    db.add(mov)
    db.commit()
    db.refresh(mov)
    return mov

def resumen(db: Session, desde: date, hasta: date):
    ingresos_expr = func.sum(case((models.Movimiento.tipo == "ingreso", models.Movimiento.monto_clp), else_=0))
    gastos_expr   = func.sum(case((models.Movimiento.tipo == "gasto",   models.Movimiento.monto_clp), else_=0))
    row = db.execute(select(ingresos_expr.label("ingresos"), gastos_expr.label("gastos")).where(models.Movimiento.fecha.between(desde,hasta))).one_or_none()
    ingresos, gastos = (row if row else (0,0))
    ingresos, gastos = int(ingresos or 0), int(gastos or 0)

    por_cat = [
        (c, int(t))
        for c, t in db.execute(
            select(models.Movimiento.categoria, func.sum(models.Movimiento.monto_clp))
            .where(models.Movimiento.fecha.between(desde, hasta), models.Movimiento.tipo == "gasto")
            .group_by(models.Movimiento.categoria)
        ).all()
    ]
    return ingresos, gastos, por_cat

def balance_total(db: Session):
    ingresos_expr = func.sum(case((models.Movimiento.tipo == "ingreso", models.Movimiento.monto_clp), else_=0))
    gastos_expr   = func.sum(case((models.Movimiento.tipo == "gasto",   models.Movimiento.monto_clp), else_=0))
    row = db.execute(select(ingresos_expr, gastos_expr)).one_or_none()
    ingresos, gastos = (row if row else (0,0))
    return int(ingresos or 0) - int(gastos or 0)
