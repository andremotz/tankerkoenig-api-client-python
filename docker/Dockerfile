FROM python:3.11-slim

WORKDIR /app

# System-Abhängigkeiten installieren (falls benötigt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Tankerkoenig Package kopieren und installieren
COPY tankerkoenig/ /app/tankerkoenig/
COPY setup.py /app/
COPY README.md /app/

# Lokales Package installieren
RUN pip install --no-cache-dir .

# FastAPI-Abhängigkeiten installieren
COPY docker/requirements.txt /app/docker/requirements.txt
RUN pip install --no-cache-dir -r docker/requirements.txt

# FastAPI-App kopieren
COPY docker/app.py /app/app.py

# Port freigeben
EXPOSE 8000

# Server starten
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
