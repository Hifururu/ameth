FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código
COPY . .

# Puerto
EXPOSE 8080

# Arranque
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
