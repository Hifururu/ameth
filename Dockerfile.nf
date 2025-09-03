# ---- Base ----
FROM python:3.11-slim

# Evita .pyc y asegura logs en stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# ---- Dependencias ----
# Solo requirements para cachear mejor cuando el código cambie
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Código de la app ----
COPY . .

# ⚠️ Sanea conflictos de versiones antiguas y valida que sean paquetes
# (con WORKDIR=/app, tu código queda en /app/app/…)
RUN rm -f app/schemas.py && \
    test -f app/__init__.py && \
    test -f app/schemas/__init__.py && \
    test -f app/routers/__init__.py && \
    test -f app/services/__init__.py

# Puerto expuesto
EXPOSE 8080

# Arranque
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
