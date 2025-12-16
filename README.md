Tankerkoenig API Client (Python)
==================================

**Python port** of the [original Java API client](https://github.com/codengine/tankerkoenig-api-client) 
for calling the [Tankerkoenig API](https://creativecommons.tankerkoenig.de) (Official Website: http://www.tankerkoenig.de).

Original Java implementation by [Stefan Hueg (Codengine)](https://github.com/codengine/tankerkoenig-api-client).

Installation
============

Install from source:

```bash
git clone https://github.com/andremotz/tankerkoenig-api-client-python
cd tankerkoenig-api-client-python
pip install .
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/andremotz/tankerkoenig-api-client-python.git
```

Requirements
============

- Python 3.7 or higher
- requests library

Obtaining an API Key
=====================

In order to use the API client, you first have to obtain a personal API key.

Enter the [API Registration Page](https://creativecommons.tankerkoenig.de/#register), fill out the form and confirm the email which is sent to you afterwards.

Be careful not to make your private API key publicly available!

Usage
=====

Basic Example:

```python
from tankerkoenig import Tankerkoenig

# Create API instance
api = Tankerkoenig.ApiBuilder().with_api_key("YOUR_API_KEY").build()

# Get list of stations near coordinates
result = api.list(52.5200, 13.4050).set_search_radius(5).execute()

if result.is_ok():
    for station in result.get_stations():
        print(f"{station.get_name()}: {station.id}")

# Get prices for specific stations
prices_result = api.prices().add_id("STATION_ID").execute()

if prices_result.is_ok():
    gas_prices = prices_result.get_gas_price("STATION_ID")
    if gas_prices:
        e5_price = gas_prices.get_price(GasPrices.GasType.E5)
        if e5_price:
            print(f"E5: {e5_price} €")
```

More Examples
==============

Get station details:

```python
detail_result = api.detail("STATION_ID").execute()
if detail_result.is_ok():
    station = detail_result.get_station()
    if station:
        print(f"Name: {station.get_name()}")
        print(f"Open: {station.is_open}")
```

Submit a correction:

```python
from tankerkoenig.requests.correction import CorrectionType

correction_result = api.correction(
    "STATION_ID",
    CorrectionType.WRONG_STATUS_OPEN
).execute()

if correction_result.is_ok():
    print("Correction submitted successfully")
```

Example Scripts
===============

This repository includes several example scripts to help you get started:

### example_radius_search.py

Searches for gas stations within a specified radius around given coordinates and displays their prices.

**Usage:**
```bash
python example_radius_search.py
```

**Features:**
- Searches stations in a configurable radius (default: 5 km)
- Displays station details (name, brand, address, distance)
- Shows current prices for E5, E10, and Diesel
- Coordinates can be customized in the script

**Configuration:**
Edit the script to change:
- `LATITUDE` and `LONGITUDE`: Search center coordinates
- `SEARCH_RADIUS`: Search radius in kilometers (1-25 km)

### example_station_id.py

Retrieves detailed information and prices for a specific gas station by its ID.

**Usage:**
```bash
python example_station_id.py
```

**Features:**
- Displays complete station information (name, brand, address, opening times)
- Shows current prices from the Prices API
- Demonstrates how to work with a specific station ID

**Configuration:**
Edit the script to change:
- `STATION_ID`: The gas station ID to query
- `API_KEY`: Your Tankerkoenig API key

### tankerkoenig_cli.py

A production-ready command-line tool for querying gas station prices with flexible output formats.

**Usage:**
```bash
# Set API key as environment variable
export TANKERKOENIG_API_KEY="your-api-key"

# Standard output with all prices
python tankerkoenig_cli.py --station-id "00041450-0002-4444-8888-acdc00000002"

# Only diesel price as number (for scripts)
python tankerkoenig_cli.py --station-id "..." --fuel-type diesel --output price-only

# JSON output for script integration
python tankerkoenig_cli.py --station-id "..." --output json

# With API key as argument
python tankerkoenig_cli.py --station-id "..." --api-key "your-api-key"
```

**Options:**
- `--station-id` (required): Gas station ID
- `--api-key` (optional): API key (or use `TANKERKOENIG_API_KEY` environment variable)
- `--fuel-type` (optional): Fuel type filter (`e5`, `e10`, `diesel`, `all`) - default: `all`
- `--output` (optional): Output format (`human`, `json`, `price-only`) - default: `human`
- `--quiet` (optional): Minimal output (only price, works with `--output price-only`)

**Output Formats:**
- `human`: Formatted, readable output with station details
- `json`: JSON output for script integration
- `price-only`: Only the price value (e.g., `1.548`)

**Exit Codes:**
- `0`: Success
- `1`: API error or invalid arguments
- `2`: Station not found
- `3`: Price not available (when using `--fuel-type`)
- `4`: API key missing

**Examples:**
```bash
# Get only E5 price
python tankerkoenig_cli.py --station-id "..." --fuel-type e5

# Get diesel price as number for shell scripts
DIESEL_PRICE=$(python tankerkoenig_cli.py --station-id "..." --fuel-type diesel --output price-only)
echo "Diesel costs $DIESEL_PRICE €/L"

# Get JSON and parse with jq
python tankerkoenig_cli.py --station-id "..." --output json | jq '.prices.diesel'
```

Terms of Usage
==============

The [Terms of Usage](https://creativecommons.tankerkoenig.de/#usage) of the API provider must be read and adhered to as defined on their website. The client does not provide any throttling or control, so be careful about request limits which will result in a 503 Internal Server Error!

License
========

MIT License

Copyright (c) 2017 Stefan Hueg (Codengine)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
