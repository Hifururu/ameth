# Ameth — Asistente personal (clon de Sophie) desde cero

Ameth es un clon de Sophie con módulos de finanzas (Lawrence) y estudio de japonés (Haru) listos para extender.
Stack: **Python 3.11 + FastAPI + SQLAlchemy + SQLite + Uvicorn**.

## 🚀 Quickstart (local)

```bash
# 1) Crear entorno
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Variables de entorno (opcional)
cp .env.example .env

# 4) Iniciar
uvicorn app.main:app --reload --port 8000
```

## 🧪 Probar rápido
- Salud: `GET http://localhost:8000/health`
- Agregar movimiento: `POST http://localhost:8000/finance/add`
- Resumen: `GET http://localhost:8000/finance/summary?desde=2025-09-01&hasta=2025-09-30`
- Balance: `GET http://localhost:8000/finance/balance`

## 🐳 Docker
```bash
docker build -t ameth:latest .
# Windows (PowerShell)
docker run --name ameth -p 8000:8000 --env-file .env -v ${PWD}\data:/app/data ameth:latest
# Linux/Mac
docker run --name ameth -p 8000:8000 --env-file .env -v $(pwd)/data:/app/data ameth:latest
```

## 📦 Deploy (Northflank u otros)
- Build desde este repo con el Dockerfile incluido.
- Configurar variable `APP_ENV=prod` y montar volumen persistente en `/app/data` si es posible.

## 🧭 Estructura
```
ameth/
├─ app/
│  ├─ main.py
│  ├─ db.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ core/config.py
│  ├─ routers/
│  │  ├─ health.py
│  │  └─ finance.py
│  ├─ services/finance.py
│  └─ agents/
│     ├─ lawrence.py
│     └─ haru.py
├─ scripts/dev.sh
├─ scripts/dev.ps1
├─ requirements.txt
├─ Dockerfile
├─ .env.example
├─ .gitignore
├─ README.md
└─ tests/test_health.py
```

## 👥 Multi-PC (trabajo y casa)
1. Crea un repo vacío en GitHub llamado `ameth`.
2. En **cada PC**:
   ```bash
   git init
   git branch -M main
   git remote add origin https://github.com/<tu-usuario>/ameth.git
   git add .
   git commit -m "feat: ameth bootstrap"
   git push -u origin main
   ```
3. Para sincronizar cambios entre PCs:
   ```bash
   git pull --rebase
   git push
   ```

## 🧩 Extensiones próximas
- Autenticación (API keys simples).
- Webhooks para registrar gastos desde el teléfono.
- Migrar a Postgres si lo necesitas.
- Panel web minimal (FastAPI + Jinja o Next.js aparte).
