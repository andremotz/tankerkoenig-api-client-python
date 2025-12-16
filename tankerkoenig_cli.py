#!/usr/bin/env python3
"""
Tankerkoenig API CLI Tool
Abfrage von Tankstellenpreisen über die Tankerkoenig API

Verwendung:
    python tankerkoenig_cli.py --station-id "STATION_ID" [OPTIONEN]

Beispiele:
    # Standard-Ausgabe mit allen Preisen
    python tankerkoenig_cli.py --station-id "00041450-0002-4444-8888-acdc00000002"

    # Nur Dieselpreis als Zahl
    python tankerkoenig_cli.py --station-id "..." --fuel-type diesel --output price-only

    # JSON-Output für Skript-Integration
    python tankerkoenig_cli.py --station-id "..." --output json

    # Mit API-Key als Argument
    python tankerkoenig_cli.py --station-id "..." --api-key "your-api-key"
"""

import argparse
import os
import sys
import json
from typing import Optional, Dict, Any, Tuple
from tankerkoenig import Tankerkoenig
from tankerkoenig.models.gas_prices import GasType


def get_api_key(args: argparse.Namespace) -> str:
    """API-Key aus Argument oder Umgebungsvariable holen
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        API-Key string
        
    Raises:
        SystemExit: Wenn kein API-Key gefunden wird
    """
    api_key = args.api_key or os.getenv('TANKERKOENIG_API_KEY')
    
    if not api_key:
        print("Fehler: API-Key fehlt. Bitte --api-key angeben oder TANKERKOENIG_API_KEY Umgebungsvariable setzen.", 
              file=sys.stderr)
        sys.exit(4)
    
    return api_key


def get_price(api: Tankerkoenig.Api, station_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[Any]]:
    """Preise für Tankstelle abrufen
    
    Args:
        api: Tankerkoenig API Instanz
        station_id: Tankstellen-ID
        
    Returns:
        Tuple von (station_data, gas_prices)
        station_data: Dictionary mit Station-Informationen oder None
        gas_prices: GasPrices Objekt oder None
    """
    # Preise abrufen
    prices_result = api.prices().add_id(station_id).execute()
    
    if not prices_result.is_ok():
        print(f"Fehler beim Abrufen der Preise: {prices_result.get_message()}", file=sys.stderr)
        return None, None
    
    prices = prices_result.get_gas_prices()
    gas_prices = prices.get(station_id)
    
    if not gas_prices:
        return None, None
    
    # Station-Details optional abrufen (für Name, etc.)
    station_data = None
    try:
        detail_result = api.detail(station_id).execute()
        if detail_result.is_ok():
            station = detail_result.get_station()
            if station and isinstance(station, dict):
                station_data = station
    except Exception:
        # Station-Details sind optional, Fehler ignorieren
        pass
    
    return station_data, gas_prices


def format_output_human(station_data: Optional[Dict[str, Any]], gas_prices: Any, fuel_type: str) -> str:
    """Human-readable Ausgabe formatieren
    
    Args:
        station_data: Station-Daten Dictionary oder None
        gas_prices: GasPrices Objekt
        fuel_type: Gewünschter Kraftstofftyp (e5, e10, diesel, all)
        
    Returns:
        Formatierter String
    """
    output_lines = []
    
    # Station-Info
    if station_data:
        name = station_data.get("name") or "Unbekannt"
        brand = station_data.get("brand") or "Unbekannt"
        output_lines.append(f"Tankstelle: {name}")
        if brand != "Unbekannt":
            output_lines.append(f"Marke: {brand}")
    
    # Status
    status = gas_prices.get_status().value
    status_symbol = "✓ Offen" if status == "open" else "✗ Geschlossen"
    output_lines.append(f"Status: {status_symbol}")
    
    # Preise
    if status == "open":
        output_lines.append("Preise:")
        
        fuel_types_to_show = [fuel_type] if fuel_type != "all" else ["e5", "e10", "diesel"]
        
        for ft in fuel_types_to_show:
            try:
                gas_type_enum = GasType[ft.upper()] if ft.upper() in ["E5", "E10"] else GasType.DIESEL
                price = gas_prices.get_price(gas_type_enum)
                if price:
                    output_lines.append(f"  {ft.upper()}: {price:.3f} €/L")
                else:
                    output_lines.append(f"  {ft.upper()}: nicht verfügbar")
            except (KeyError, AttributeError):
                output_lines.append(f"  {ft.upper()}: nicht verfügbar")
    else:
        output_lines.append(f"Tankstelle ist {status}")
    
    return "\n".join(output_lines)


def format_output_json(station_data: Optional[Dict[str, Any]], gas_prices: Any, fuel_type: str, station_id: str) -> str:
    """JSON-Ausgabe formatieren
    
    Args:
        station_data: Station-Daten Dictionary oder None
        gas_prices: GasPrices Objekt
        fuel_type: Gewünschter Kraftstofftyp (e5, e10, diesel, all)
        station_id: Tankstellen-ID
        
    Returns:
        JSON-String
    """
    result = {
        "station_id": station_id,
        "status": gas_prices.get_status().value
    }
    
    if station_data:
        result["station_name"] = station_data.get("name")
        result["brand"] = station_data.get("brand")
    
    if gas_prices.get_status().value == "open":
        prices_dict = {}
        fuel_types_to_show = [fuel_type] if fuel_type != "all" else ["e5", "e10", "diesel"]
        
        for ft in fuel_types_to_show:
            try:
                gas_type_enum = GasType[ft.upper()] if ft.upper() in ["E5", "E10"] else GasType.DIESEL
                price = gas_prices.get_price(gas_type_enum)
                if price:
                    prices_dict[ft] = price
            except (KeyError, AttributeError):
                pass
        
        result["prices"] = prices_dict
    else:
        result["prices"] = {}
    
    return json.dumps(result, indent=2, ensure_ascii=False)


def format_output_price_only(gas_prices: Any, fuel_type: str) -> Optional[str]:
    """Nur Preiswert ausgeben
    
    Args:
        gas_prices: GasPrices Objekt
        fuel_type: Gewünschter Kraftstofftyp (e5, e10, diesel)
        
    Returns:
        Preis als String oder None
    """
    if gas_prices.get_status().value != "open":
        return None
    
    if fuel_type == "all":
        # Bei "all" den ersten verfügbaren Preis zurückgeben
        for ft in ["diesel", "e10", "e5"]:
            try:
                gas_type_enum = GasType[ft.upper()] if ft.upper() in ["E5", "E10"] else GasType.DIESEL
                price = gas_prices.get_price(gas_type_enum)
                if price:
                    return f"{price:.3f}"
            except (KeyError, AttributeError):
                continue
        return None
    
    try:
        gas_type_enum = GasType[fuel_type.upper()] if fuel_type.upper() in ["E5", "E10"] else GasType.DIESEL
        price = gas_prices.get_price(gas_type_enum)
        if price:
            return f"{price:.3f}"
    except (KeyError, AttributeError):
        pass
    
    return None


def main() -> int:
    """Hauptfunktion
    
    Returns:
        Exit-Code (0 = Erfolg, >0 = Fehler)
    """
    # Argumente parsen
    parser = argparse.ArgumentParser(
        description='Tankerkoenig API CLI - Abfrage von Tankstellenpreisen',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--station-id', required=True, 
                       help='Tankstellen-ID (erforderlich)')
    parser.add_argument('--api-key', 
                       help='API-Key (optional, sonst TANKERKOENIG_API_KEY Umgebungsvariable)')
    parser.add_argument('--fuel-type', choices=['e5', 'e10', 'diesel', 'all'], 
                       default='all',
                       help='Kraftstofftyp (Standard: all)')
    parser.add_argument('--output', choices=['human', 'json', 'price-only'], 
                       default='human',
                       help='Ausgabeformat (Standard: human)')
    parser.add_argument('--quiet', action='store_true',
                       help='Nur Preis ausgeben (keine Details, nur bei --output price-only)')
    
    args = parser.parse_args()
    
    # API-Key holen
    try:
        api_key = get_api_key(args)
    except SystemExit as e:
        return e.code
    
    # API-Instanz erstellen
    try:
        api = Tankerkoenig.ApiBuilder().with_api_key(api_key).build()
    except Exception as e:
        print(f"Fehler beim Initialisieren der API: {e}", file=sys.stderr)
        return 1
    
    # Preise abrufen
    station_data, gas_prices = get_price(api, args.station_id)
    
    if not gas_prices:
        print(f"Fehler: Tankstelle {args.station_id} nicht gefunden oder keine Preisinformationen verfügbar", 
              file=sys.stderr)
        return 2
    
    # Bei price-only und spezifischem fuel-type prüfen, ob Preis verfügbar
    if args.output == "price-only" and args.fuel_type != "all":
        price_str = format_output_price_only(gas_prices, args.fuel_type)
        if not price_str:
            print(f"Fehler: Preis für {args.fuel_type.upper()} nicht verfügbar", file=sys.stderr)
            return 3
        print(price_str)
        return 0
    
    # Ausgabe formatieren
    if args.output == "human":
        output = format_output_human(station_data, gas_prices, args.fuel_type)
        print(output)
    elif args.output == "json":
        output = format_output_json(station_data, gas_prices, args.fuel_type, args.station_id)
        print(output)
    elif args.output == "price-only":
        price_str = format_output_price_only(gas_prices, args.fuel_type)
        if price_str:
            print(price_str)
        else:
            print("Fehler: Kein Preis verfügbar", file=sys.stderr)
            return 3
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

