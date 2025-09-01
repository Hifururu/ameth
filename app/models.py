from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql import func
from app.db import Base
import enum

# Validamos con Enum de Python, pero guardamos como texto en la DB (más robusto en SQLite)
class TipoMovimiento(str, enum.Enum):
    ingreso = "ingreso"
    gasto = "gasto"
    futuro = "futuro"

class Movimiento(Base):
    __tablename__ = "movimientos"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False, server_default=func.current_date())
    concepto = Column(String(200), nullable=False)
    categoria = Column(String(100), nullable=False)
    monto_clp = Column(Integer, nullable=False)  # entero, sin decimales
    tipo = Column(String(20), nullable=False)    # guardamos como texto (ingreso/gasto/futuro)
# --- HARU (estudio) ---
from sqlalchemy import Text, DateTime
from datetime import datetime, date

class StudySession(Base):
    __tablename__ = "study_sessions"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False, server_default=func.current_date())
    minutos = Column(Integer, nullable=False, default=0)
    tema = Column(String(200), nullable=True)
    kanjis = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
