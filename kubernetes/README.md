# Dieselpreis Logger - Kubernetes Deployment

Dieses Verzeichnis enthält die Kubernetes-Konfiguration für den Dieselpreis Logger.

Der Logger selbst (`diesel_price_logger.py`) befindet sich im Hauptverzeichnis 
und kann auch standalone ohne Kubernetes/Docker verwendet werden.

## Architektur

```
Kubernetes CronJob (stündlich)
    ↓
Docker Container (Python-Skript)
    ↓
tankerkoenig_cli.py (Dieselpreis abrufen)
    ↓
InfluxDB (Time-Series Datenbank)
```

## Komponenten

### 1. Python-Logging-Skript (`diesel_price_logger.py`)
- Nutzt die Tankerkoenig API direkt
- Ruft Dieselpreis für konfigurierte Station-ID ab
- Schreibt Daten in InfluxDB mit Timestamp
- Fehlerbehandlung und Logging

### 2. Docker-Image
- Basis: Python 3.11-slim
- Installiert: tankerkoenig-api-client, influxdb-client
- Enthält: Logging-Skript

### 3. Kubernetes CronJob
- Schedule: `0 * * * *` (jede Stunde)
- Nutzt: Docker-Image
- ConfigMap: Station-ID, InfluxDB-Config
- Secret: API-Key

## Datenstruktur in InfluxDB

**Measurement:** `gas_prices`

**Tags:**
- `station_id`: Tankstellen-ID
- `fuel_type`: "diesel"
- `station_name`: Name der Tankstelle

**Fields:**
- `price`: Dieselpreis (float)
- `status`: Station-Status ("open"/"closed")

**Timestamp:** Automatisch (Zeitpunkt der Abfrage)

## Setup

### 1. Docker-Image bauen

**Option A: Mit Build-Skript (empfohlen)**
```bash
cd tankerkoenig-api-client-python
kubernetes/docker/build.sh
# Oder mit Custom-Image-Name:
IMAGE_NAME=your-registry/diesel-price-logger kubernetes/docker/build.sh
```

**Option B: Manuell**
```bash
cd tankerkoenig-api-client-python
docker build -f kubernetes/docker/Dockerfile -t your-registry/diesel-price-logger:latest .
docker push your-registry/diesel-price-logger:latest
```

### 2. Kubernetes Secrets erstellen

```bash
# Secret-Template kopieren und anpassen
cp kubernetes/secret.yaml.example kubernetes/secret.yaml
# Bearbeite secret.yaml und füge deine API-Keys ein

# Secret erstellen
kubectl apply -f kubernetes/secret.yaml
```

### 3. ConfigMap anpassen und erstellen

```bash
# Bearbeite kubernetes/configmap.yaml
# Setze deine Station-ID, InfluxDB URL, Org und Bucket

# ConfigMap erstellen
kubectl apply -f kubernetes/configmap.yaml
```

### 4. InfluxDB deployen (falls nicht vorhanden)

```bash
# Optional: Falls InfluxDB noch nicht im Cluster existiert
kubectl apply -f kubernetes/influxdb-deployment.yaml
```

### 5. CronJob deployen

```bash
# Bearbeite kubernetes/cronjob.yaml
# Setze dein Docker-Image

# CronJob erstellen
kubectl apply -f kubernetes/cronjob.yaml
```

## Überprüfung

### CronJob Status prüfen

```bash
kubectl get cronjob diesel-price-logger
kubectl get jobs
```

### Logs ansehen

```bash
# Letzten Job finden
kubectl get pods -l app=diesel-price-logger

# Logs anzeigen
kubectl logs <pod-name>
```

### InfluxDB Daten prüfen

```bash
# In InfluxDB Container einloggen
kubectl exec -it deployment/influxdb -- /bin/bash

# Oder über InfluxDB CLI
influx query 'from(bucket:"gas_prices") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "gas_prices")'
```

## Konfiguration

### Umgebungsvariablen

- `STATION_ID`: Tankstellen-ID (aus ConfigMap)
- `TANKERKOENIG_API_KEY`: API-Key (aus Secret)
- `INFLUXDB_URL`: InfluxDB URL (aus ConfigMap)
- `INFLUXDB_ORG`: InfluxDB Organisation (aus ConfigMap)
- `INFLUXDB_BUCKET`: InfluxDB Bucket (aus ConfigMap)
- `INFLUXDB_TOKEN`: InfluxDB Token (aus Secret, optional)

### Cron-Schedule anpassen

In `kubernetes/cronjob.yaml` kann der Schedule angepasst werden:

- `0 * * * *` - Jede Stunde
- `0 */6 * * *` - Alle 6 Stunden
- `0 0 * * *` - Täglich um Mitternacht
- `*/15 * * * *` - Alle 15 Minuten

## Troubleshooting

### Job schlägt fehl

1. Logs prüfen: `kubectl logs <pod-name>`
2. ConfigMap/Secret prüfen: `kubectl describe configmap logger-config`
3. InfluxDB-Verbindung testen
4. API-Key validieren

### Keine Daten in InfluxDB

1. InfluxDB-Bucket existiert?
2. InfluxDB-Token hat Schreibrechte?
3. Netzwerk-Verbindung zum InfluxDB-Service?

## Monitoring

Optional können Prometheus Metrics und Grafana Dashboards hinzugefügt werden, um:
- Erfolgreiche/fehlgeschlagene Jobs zu tracken
- Preisverlauf zu visualisieren
- Alerts bei fehlgeschlagenen Jobs zu erhalten

