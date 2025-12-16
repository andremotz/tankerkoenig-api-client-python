#!/usr/bin/env python3
"""
Beispielskript für die Tankerkoenig API - Radius-Suche
Zeigt Tankstellen in einem bestimmten Radius um gegebene Koordinaten und deren Preise an
"""

import os
from tankerkoenig import Tankerkoenig
from tankerkoenig.models.gas_prices import GasType

# API-Key
# Bitte deinen API-Key hier eintragen oder als Umgebungsvariable TANKERKOENIG_API_KEY setzen
API_KEY = os.getenv('TANKERKOENIG_API_KEY', 'YOUR_API_KEY_HERE')

# Koordinaten (München Klinikum Großhadern)
LATITUDE = 48.1100
LONGITUDE = 11.4700
SEARCH_RADIUS = 5  # Kilometer

def main():
    # API-Instanz erstellen
    print("Initialisiere Tankerkoenig API...")
    api = Tankerkoenig.ApiBuilder().with_api_key(API_KEY).build()
    
    # 1. Liste von Tankstellen in der Nähe abrufen
    print(f"\nSuche Tankstellen in {SEARCH_RADIUS} km Umkreis um {LATITUDE}, {LONGITUDE}...")
    list_result = api.list(LATITUDE, LONGITUDE).set_search_radius(SEARCH_RADIUS).execute()
    
    if not list_result.is_ok():
        print(f"Fehler beim Abrufen der Tankstellenliste: {list_result.get_message()}")
        return
    
    stations = list_result.get_stations()
    print(f"Gefunden: {len(stations)} Tankstellen\n")
    
    if len(stations) == 0:
        print("Keine Tankstellen gefunden.")
        return
    
    # Erste 5 Tankstellen anzeigen
    print("=" * 80)
    print("TANKSTELLEN IN DER NÄHE:")
    print("=" * 80)
    
    station_ids = []
    for i, station in enumerate(stations[:5], 1):
        station_ids.append(station.id)
        name = station.get_name() or "Unbekannt"
        brand = station.get_brand() or "Unbekannt"
        distance = station.location.get_distance() if station.location else None
        is_open = "✓ Offen" if station.is_open else "✗ Geschlossen"
        
        print(f"\n{i}. {name} ({brand})")
        print(f"   Status: {is_open}")
        if distance:
            print(f"   Entfernung: {distance:.2f} km")
        if station.location:
            loc = station.location
            address = f"{loc.street_name}"
            if loc.house_number:
                address += f" {loc.house_number}"
            if loc.zip_code:
                address += f", {loc.zip_code} {loc.city}"
            print(f"   Adresse: {address}")
        print(f"   ID: {station.id}")
    
    # 2. Preise für die gefundenen Tankstellen abrufen
    if station_ids:
        print("\n" + "=" * 80)
        print("AKTUELLE PREISE:")
        print("=" * 80)
        
        prices_result = api.prices().add_ids_collection(station_ids).execute()
        
        if not prices_result.is_ok():
            print(f"Fehler beim Abrufen der Preise: {prices_result.get_message()}")
            return
        
        prices = prices_result.get_gas_prices()
        
        for station_id, gas_prices in prices.items():
            # Station-Info finden
            station = next((s for s in stations if s.id == station_id), None)
            station_name = station.get_name() if station else "Unbekannt"
            
            print(f"\n{station_name}:")
            print(f"  Status: {gas_prices.get_status().value}")
            
            if gas_prices.get_status().value == "open":
                # Preise anzeigen
                for gas_type in [GasType.E5, GasType.E10, GasType.DIESEL]:
                    price = gas_prices.get_price(gas_type)
                    if price:
                        print(f"  {gas_type.value.upper()}: {price:.3f} €/L")
                    else:
                        print(f"  {gas_type.value.upper()}: nicht verfügbar")
            else:
                print(f"  Tankstelle ist geschlossen oder nicht verfügbar")

if __name__ == "__main__":
    main()
