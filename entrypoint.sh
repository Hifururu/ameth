#!/usr/bin/env sh
set -eu

# Variables con valores por defecto (puedes sobreescribirlas en Northflank)
: "${AMETH_DATA_DIR:=/data}"
: "${HOST:=0.0.0.0}"
: "${PORT:=8080}"
: "${APP_MODULE:=app.main:app}"  # Si tu app est?? en app/main.py con 'app = FastAPI()'

# Asegura el directorio de datos
mkdir -p "$AMETH_DATA_DIR" || true

# Test de escritura (fallar r??pido si no hay permiso)
if ! touch "$AMETH_DATA_DIR/__w" 2>/dev/null; then
  echo "ERROR: $AMETH_DATA_DIR no es escribible" >&2
  ls -ld "$AMETH_DATA_DIR" || true
  id || true
  exit 1
fi
rm -f "$AMETH_DATA_DIR/__w" || true

# Lanza Uvicorn con el m??dulo correcto
exec uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT" --proxy-headers