FROM python:3.11-slim

# Config Python y pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Utilidades mínimas (tini para señales, curl para healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tini curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código
COPY app ./app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Asegura el directorio de datos y permisos (compatible con volumen)
RUN mkdir -p /data && chmod 777 /data

# Vars por defecto (puedes sobreescribir en Northflank)
ENV AMETH_DATA_DIR=/data \
    HOST=0.0.0.0 \
    PORT=8080 \
    AMETH_VERSION=v1.2

ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["/entrypoint.sh"]

# Healthcheck interno (consulta /health dentro del contenedor)
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -fsS "http://127.0.0.1:${PORT}/health" || exit 1
