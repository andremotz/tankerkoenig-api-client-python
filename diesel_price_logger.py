#!/usr/bin/env python3
"""
Dieselpreis Logger
Ruft Dieselpreise einer Tankstelle ab und speichert sie in InfluxDB.

Kann sowohl standalone als auch in Kubernetes/Docker verwendet werden.

Standalone-Verwendung:
    python diesel_price_logger.py

Umgebungsvariablen:
    STATION_ID - Tankstellen-ID (erforderlich)
    TANKERKOENIG_API_KEY - API-Key (erforderlich)
    INFLUXDB_URL - InfluxDB URL (erforderlich)
    INFLUXDB_ORG - InfluxDB Organisation (erforderlich)
    INFLUXDB_BUCKET - InfluxDB Bucket (Standard: gas_prices)
    INFLUXDB_TOKEN - InfluxDB Token (optional)
"""

import os
import sys
import json
import logging
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from tankerkoenig import Tankerkoenig
from tankerkoenig.models.gas_prices import GasType

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_diesel_price(station_id: str, api_key: str) -> dict:
    """Ruft Dieselpreis für eine Tankstelle ab
    
    Args:
        station_id: Tankstellen-ID
        api_key: Tankerkoenig API-Key
        
    Returns:
        Dictionary mit Preis-Daten oder None bei Fehler
    """
    try:
        # API-Instanz erstellen
        api = Tankerkoenig.ApiBuilder().with_api_key(api_key).build()
        
        # Preise abrufen
        prices_result = api.prices().add_id(station_id).execute()
        
        if not prices_result.is_ok():
            logger.error(f"Fehler beim Abrufen der Preise: {prices_result.get_message()}")
            return None
        
        prices = prices_result.get_gas_prices()
        gas_prices = prices.get(station_id)
        
        if not gas_prices:
            logger.error(f"Keine Preisinformationen für Station {station_id} verfügbar")
            return None
        
        # Station-Details optional abrufen (für Name)
        station_name = None
        try:
            detail_result = api.detail(station_id).execute()
            if detail_result.is_ok():
                station = detail_result.get_station()
                if station and isinstance(station, dict):
                    station_name = station.get("name")
        except Exception as e:
            logger.warning(f"Konnte Station-Details nicht abrufen: {e}")
        
        # Dieselpreis extrahieren
        diesel_price = gas_prices.get_price(GasType.DIESEL)
        status = gas_prices.get_status().value
        
        if diesel_price is None:
            logger.warning(f"Dieselpreis für Station {station_id} nicht verfügbar (Status: {status})")
            return None
        
        return {
            "price": diesel_price,
            "status": status,
            "station_id": station_id,
            "station_name": station_name or "Unbekannt"
        }
        
    except Exception as e:
        logger.error(f"Fehler beim Abrufen des Dieselpreises: {e}", exc_info=True)
        return None


def write_to_influxdb(data: dict, influxdb_config: dict) -> bool:
    """Schreibt Preis-Daten in InfluxDB
    
    Args:
        data: Dictionary mit Preis-Daten
        influxdb_config: InfluxDB Konfiguration
        
    Returns:
        True bei Erfolg, False bei Fehler
    """
    try:
        # InfluxDB Client erstellen
        client = InfluxDBClient(
            url=influxdb_config["url"],
            token=influxdb_config.get("token", ""),
            org=influxdb_config["org"]
        )
        
        write_api = client.write_api(write_options=SYNCHRONOUS)
        
        # Point erstellen
        point = Point("gas_prices") \
            .tag("station_id", data["station_id"]) \
            .tag("fuel_type", "diesel") \
            .tag("station_name", data["station_name"]) \
            .field("price", data["price"]) \
            .field("status", data["status"])
        
        # In InfluxDB schreiben
        write_api.write(
            bucket=influxdb_config["bucket"],
            org=influxdb_config["org"],
            record=point
        )
        
        logger.info(f"Preis erfolgreich in InfluxDB geschrieben: {data['price']:.3f} €/L für Station {data['station_id']}")
        
        # Client schließen
        client.close()
        
        return True
        
    except Exception as e:
        logger.error(f"Fehler beim Schreiben in InfluxDB: {e}", exc_info=True)
        return False


def main() -> int:
    """Hauptfunktion
    
    Returns:
        Exit-Code (0 = Erfolg, >0 = Fehler)
    """
    # Umgebungsvariablen lesen
    station_id = os.getenv("STATION_ID")
    api_key = os.getenv("TANKERKOENIG_API_KEY")
    
    influxdb_url = os.getenv("INFLUXDB_URL")
    influxdb_token = os.getenv("INFLUXDB_TOKEN", "")
    influxdb_org = os.getenv("INFLUXDB_ORG")
    influxdb_bucket = os.getenv("INFLUXDB_BUCKET", "gas_prices")
    
    # Validierung
    if not station_id:
        logger.error("STATION_ID Umgebungsvariable fehlt")
        return 1
    
    if not api_key:
        logger.error("TANKERKOENIG_API_KEY Umgebungsvariable fehlt")
        return 1
    
    if not influxdb_url:
        logger.error("INFLUXDB_URL Umgebungsvariable fehlt")
        return 1
    
    if not influxdb_org:
        logger.error("INFLUXDB_ORG Umgebungsvariable fehlt")
        return 1
    
    # InfluxDB Konfiguration
    influxdb_config = {
        "url": influxdb_url,
        "token": influxdb_token,
        "org": influxdb_org,
        "bucket": influxdb_bucket
    }
    
    logger.info(f"Starte Dieselpreis-Abfrage für Station: {station_id}")
    
    # Dieselpreis abrufen
    price_data = get_diesel_price(station_id, api_key)
    
    if not price_data:
        logger.error("Konnte Dieselpreis nicht abrufen")
        return 2
    
    # In InfluxDB schreiben
    success = write_to_influxdb(price_data, influxdb_config)
    
    if not success:
        logger.error("Konnte Daten nicht in InfluxDB schreiben")
        return 3
    
    logger.info("Dieselpreis erfolgreich geloggt")
    return 0


if __name__ == "__main__":
    sys.exit(main())

