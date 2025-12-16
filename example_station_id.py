#!/usr/bin/env python3
"""
Beispielskript für die Tankerkoenig API - Konkrete Tankstellen-ID
Zeigt Detailinformationen und Preise für eine spezifische Tankstelle an
"""

import os
from tankerkoenig import Tankerkoenig
from tankerkoenig.models.gas_prices import GasType

# API-Key
# Bitte deinen API-Key hier eintragen oder als Umgebungsvariable TANKERKOENIG_API_KEY setzen
API_KEY = os.getenv('TANKERKOENIG_API_KEY', 'YOUR_API_KEY_HERE')

# Tankstellen-ID
STATION_ID = "00041450-0002-4444-8888-acdc00000002"

def main():
    # API-Instanz erstellen
    print("Initialisiere Tankerkoenig API...")
    api = Tankerkoenig.ApiBuilder().with_api_key(API_KEY).build()
    
    # 1. Detailinformationen für die Tankstelle abrufen
    print(f"\nLade Detailinformationen für Tankstelle: {STATION_ID}...")
    detail_result = api.detail(STATION_ID).execute()
    
    if not detail_result.is_ok():
        print(f"Fehler beim Abrufen der Tankstellendetails: {detail_result.get_message()}")
        return
    
    station = detail_result.get_station()
    if not station:
        print("Tankstelle nicht gefunden.")
        return
    
    # Tankstellendetails anzeigen (station ist ein Dictionary)
    print("\n" + "=" * 80)
    print("TANKSTELLENDETAILS:")
    print("=" * 80)
    
    name = station.get("name") or "Unbekannt"
    brand = station.get("brand") or "Unbekannt"
    is_open = "✓ Offen" if station.get("isOpen", False) else "✗ Geschlossen"
    station_id = station.get("id", "Unbekannt")
    
    print(f"\nName: {name}")
    print(f"Marke: {brand}")
    print(f"Status: {is_open}")
    print(f"ID: {station_id}")
    
    # Adresse anzeigen
    if "lat" in station or "lng" in station:
        print(f"\nAdresse:")
        if station.get("street"):
            address = station.get("street", "")
            if station.get("houseNumber"):
                address += f" {station.get('houseNumber')}"
            print(f"  {address}")
        if station.get("postCode"):
            print(f"  {station.get('postCode')} {station.get('place', '')}")
        if station.get("state"):
            print(f"  {station.get('state')}")
        if station.get("lat") and station.get("lng"):
            print(f"  Koordinaten: {station.get('lat')}, {station.get('lng')}")
    
    # Öffnungszeiten anzeigen
    if "openingTimes" in station and station["openingTimes"]:
        print(f"\nÖffnungszeiten:")
        for opening_time in station["openingTimes"]:
            if isinstance(opening_time, dict):
                print(f"  {opening_time.get('text', '')}")
                if opening_time.get("start") and opening_time.get("end"):
                    print(f"    {opening_time.get('start')} - {opening_time.get('end')}")
    
    # Gaspreise aus Detail-Ergebnis anzeigen
    if any(key in station for key in ["e5", "e10", "diesel"]):
        print("\n" + "=" * 80)
        print("PREISE (aus Detail-Request):")
        print("=" * 80)
        status = station.get("status", "not found")
        print(f"Status: {status}")
        
        if status == "open":
            for gas_type in ["e5", "e10", "diesel"]:
                price = station.get(gas_type)
                if price:
                    try:
                        price_float = float(price)
                        print(f"{gas_type.upper()}: {price_float:.3f} €/L")
                    except (ValueError, TypeError):
                        print(f"{gas_type.upper()}: {price}")
                else:
                    print(f"{gas_type.upper()}: nicht verfügbar")
        else:
            print(f"Tankstelle ist {status}")
    
    # 2. Aktuelle Preise für die Tankstelle abrufen
    print("\n" + "=" * 80)
    print("AKTUELLE PREISE (aus Prices-Request):")
    print("=" * 80)
    
    prices_result = api.prices().add_id(STATION_ID).execute()
    
    if not prices_result.is_ok():
        print(f"Fehler beim Abrufen der Preise: {prices_result.get_message()}")
        return
    
    prices = prices_result.get_gas_prices()
    gas_prices = prices.get(STATION_ID)
    
    if gas_prices:
        print(f"Status: {gas_prices.get_status().value}")
        
        if gas_prices.get_status().value == "open":
            for gas_type in [GasType.E5, GasType.E10, GasType.DIESEL]:
                price = gas_prices.get_price(gas_type)
                if price:
                    print(f"{gas_type.value.upper()}: {price:.3f} €/L")
                else:
                    print(f"{gas_type.value.upper()}: nicht verfügbar")
        else:
            print("Tankstelle ist geschlossen oder nicht verfügbar")
    else:
        print("Keine Preisinformationen verfügbar")

if __name__ == "__main__":
    main()
