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

### diesel_price_logger.py

A script for logging diesel prices of a specific gas station to InfluxDB. Can be used standalone (e.g., with cron) or in Kubernetes/Docker.

**Standalone Usage:**
```bash
# Install dependencies
pip install -r logger_requirements.txt

# Set environment variables
export TANKERKOENIG_API_KEY="your-api-key"
export STATION_ID="00041450-0002-4444-8888-acdc00000002"
export INFLUXDB_URL="http://localhost:8086"
export INFLUXDB_ORG="my-org"
export INFLUXDB_BUCKET="gas_prices"

# Run the logger
python diesel_price_logger.py
```

**With cron (Linux/macOS):**
```bash
# Add to crontab for hourly execution:
# 0 * * * * cd /path/to/tankerkoenig-api-client-python && /usr/bin/python3 diesel_price_logger.py
```

**Environment Variables:**
- `STATION_ID` (required): Gas station ID
- `TANKERKOENIG_API_KEY` (required): API key
- `INFLUXDB_URL` (required): InfluxDB URL
- `INFLUXDB_ORG` (required): InfluxDB organization
- `INFLUXDB_BUCKET` (optional): InfluxDB bucket name (default: `gas_prices`)
- `INFLUXDB_TOKEN` (optional): InfluxDB authentication token

**Docker Usage:**
```bash
# Build Docker image
cd tankerkoenig-api-client-python
kubernetes/docker/build.sh

# Or manually:
docker build -f kubernetes/docker/Dockerfile -t diesel-price-logger:latest .

# Run container
docker run --rm \
  -e TANKERKOENIG_API_KEY="your-api-key" \
  -e STATION_ID="00041450-0002-4444-8888-acdc00000002" \
  -e INFLUXDB_URL="http://influxdb:8086" \
  -e INFLUXDB_ORG="my-org" \
  -e INFLUXDB_BUCKET="gas_prices" \
  diesel-price-logger:latest
```

**Kubernetes Deployment:**
```bash
# 1. Create ConfigMap (adjust values in configmap.yaml)
kubectl apply -f kubernetes/configmap.yaml

# 2. Create Secret (copy secret.yaml.example and fill in your values)
kubectl apply -f kubernetes/secret.yaml

# 3. Deploy CronJob (runs hourly)
kubectl apply -f kubernetes/cronjob.yaml

# Check status
kubectl get cronjob diesel-price-logger
kubectl get jobs
```

For detailed Kubernetes setup instructions, see `kubernetes/README.md`.

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
