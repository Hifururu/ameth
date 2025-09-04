#!/usr/bin/env sh
set -eu

: "${AMETH_DATA_DIR:=/data}"
: "${HOST:=0.0.0.0}"
: "${PORT:=8080}"
: "${APP_MODULE:=app.main:app}"  # <- puedes sobreescribirlo en Northflank si tu app es distinta

mkdir -p "$AMETH_DATA_DIR" || true

# Test de escritura (para fallar r??pido si no hay permisos)
if ! touch "$AMETH_DATA_DIR/__w" 2>/dev/null; then
  echo "ERROR: $AMETH_DATA_DIR no es escribible" >&2
  ls -ld "$AMETH_DATA_DIR" || true
  id || true
  exit 1
fi
rm -f "$AMETH_DATA_DIR/__w" || true

# Lanza Uvicorn con el m??dulo que corresponda
exec uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT" --proxy-headers