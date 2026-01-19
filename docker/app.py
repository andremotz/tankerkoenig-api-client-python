#!/usr/bin/env python3
"""
FastAPI Server für Dieselpreis-Abfrage
Ruft Dieselpreise einer Tankstelle über die Tankerkoenig API ab.

Endpoints:
    POST /diesel-price - Gibt Dieselpreis für eine Tankstelle zurück
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from tankerkoenig import Tankerkoenig
from tankerkoenig.models.gas_prices import GasType

app = FastAPI(
    title="Tankerkoenig Dieselpreis API",
    description="API für Abfrage von Dieselpreisen über die Tankerkoenig API",
    version="1.0.0"
)


class DieselPriceRequest(BaseModel):
    """Request-Modell für Dieselpreis-Abfrage"""
    station_id: str
    api_key: str


class DieselPriceResponse(BaseModel):
    """Response-Modell für Dieselpreis-Abfrage"""
    price: float
    status: str
    station_id: str
    station_name: str


def get_diesel_price(station_id: str, api_key: str) -> Optional[dict]:
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
            raise ValueError(f"Fehler beim Abrufen der Preise: {prices_result.get_message()}")
        
        prices = prices_result.get_gas_prices()
        gas_prices = prices.get(station_id)
        
        if not gas_prices:
            raise ValueError(f"Keine Preisinformationen für Station {station_id} verfügbar")
        
        # Station-Details optional abrufen (für Name)
        station_name = None
        try:
            detail_result = api.detail(station_id).execute()
            if detail_result.is_ok():
                station = detail_result.get_station()
                if station and isinstance(station, dict):
                    station_name = station.get("name")
        except Exception:
            # Station-Details sind optional, Fehler ignorieren
            pass
        
        # Dieselpreis extrahieren
        diesel_price = gas_prices.get_price(GasType.DIESEL)
        status = gas_prices.get_status().value
        
        if diesel_price is None:
            raise ValueError(f"Dieselpreis für Station {station_id} nicht verfügbar (Status: {status})")
        
        return {
            "price": diesel_price,
            "status": status,
            "station_id": station_id,
            "station_name": station_name or "Unbekannt"
        }
        
    except ValueError as e:
        # ValueError weiterwerfen für bessere Fehlerbehandlung
        raise
    except Exception as e:
        raise ValueError(f"Fehler beim Abrufen des Dieselpreises: {str(e)}")


@app.post("/diesel-price", response_model=DieselPriceResponse)
async def diesel_price(request: DieselPriceRequest):
    """Gibt den aktuellen Dieselpreis für eine Tankstelle zurück
    
    Args:
        request: Request mit station_id und api_key
        
    Returns:
        DieselPriceResponse mit Preis-Daten
        
    Raises:
        HTTPException: Bei Fehlern (400 für ungültige Parameter, 500 für Server-Fehler)
    """
    try:
        price_data = get_diesel_price(request.station_id, request.api_key)
        
        if not price_data:
            raise HTTPException(
                status_code=500,
                detail="Konnte Dieselpreis nicht abrufen"
            )
        
        return DieselPriceResponse(**price_data)
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Interner Serverfehler: {str(e)}"
        )


@app.get("/")
async def root():
    """Health-Check Endpoint"""
    return {"status": "ok", "service": "Tankerkoenig Dieselpreis API"}
