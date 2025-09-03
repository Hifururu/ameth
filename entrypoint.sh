#!/usr/bin/env sh
set -eu

# Asegura ruta de datos y prueba de escritura
: "${AMETH_DATA_DIR:=/data}"
mkdir -p "$AMETH_DATA_DIR" || true

if ! touch "$AMETH_DATA_DIR/__w" 2>/dev/null; then
  echo "ERROR: $AMETH_DATA_DIR no es escribible" >&2
  ls -ld "$AMETH_DATA_DIR" || true
  id || true
  exit 1
fi
rm -f "$AMETH_DATA_DIR/__w" || true

# Lanza la API (módulo y objeto FastAPI: app.main:app)
exec uvicorn app.main:app --host "${HOST:-0.0.0.0}" --port "${PORT:-8080}" --proxy-headers
