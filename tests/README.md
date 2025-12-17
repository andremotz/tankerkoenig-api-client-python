# Tests

Dieses Verzeichnis enthält die Unit-Tests für den Tankerkoenig API Client.

## Test-Struktur

- `test_gas_prices.py` - Tests für GasPrices, GasType und Status
- `test_station.py` - Tests für Station, Location und OpeningTime
- `test_validator.py` - Tests für RequestParamValidator
- `test_mapper.py` - Tests für JSON-Mapping
- `conftest.py` - Pytest-Fixtures für gemeinsame Test-Daten
- `resources/` - Test-Ressourcen (JSON-Dateien)

## Ausführung

### Installation der Test-Dependencies

```bash
pip install -e ".[dev]"
# oder
pip install pytest
```

### Tests ausführen

```bash
# Alle Tests ausführen
pytest

# Mit ausführlicher Ausgabe
pytest -v

# Spezifische Test-Datei
pytest tests/test_gas_prices.py

# Spezifischer Test
pytest tests/test_gas_prices.py::TestGasPrices::test_get_price_existing

# Mit Coverage
pytest --cov=tankerkoenig --cov-report=html
```

## Test-Abdeckung

Die Tests decken folgende Bereiche ab:

- **GasPrices**: Preis-Abfragen, Status-Checks, Verfügbarkeitsprüfungen
- **Station**: Getter-Methoden, Gleichheit, Hashing
- **Location**: Koordinaten, Adressdaten, Distanz
- **OpeningTime**: Öffnungszeiten-Parsing
- **RequestParamValidator**: Validierung von Parametern (min/max, not_null, not_empty, etc.)
- **JsonMapper**: JSON-Deserialisierung für API-Responses

## Test-Ressourcen

Die Test-Ressourcen in `resources/` enthalten Beispiel-JSON-Responses von der Tankerkoenig API:

- `prices.json` - Beispiel für Prices-API Response
- `detail.json` - Beispiel für Detail-API Response

Diese werden für Integration-Tests verwendet, um die JSON-Parsing-Funktionalität zu testen.

