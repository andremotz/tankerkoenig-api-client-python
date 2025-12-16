FROM python:3.11-slim

WORKDIR /app

# System-Abhängigkeiten installieren (falls benötigt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Python Dependencies installieren
COPY logger_requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Tankerkoenig API Client installieren
# Option 1: Von GitHub (empfohlen für Production)
RUN pip install --no-cache-dir git+https://github.com/andremotz/tankerkoenig-api-client-python.git

# Option 2: Von lokalem Verzeichnis (für Development)
# Hinweis: Docker-Build muss vom tankerkoenig-api-client-python Verzeichnis ausgeführt werden:
# docker build -f kubernetes/docker/Dockerfile -t diesel-price-logger:latest .
# COPY . /tmp/tankerkoenig-api-client-python
# RUN pip install --no-cache-dir /tmp/tankerkoenig-api-client-python

# Logging-Skript kopieren
COPY diesel_price_logger.py .

# Entrypoint
ENTRYPOINT ["python", "diesel_price_logger.py"]

