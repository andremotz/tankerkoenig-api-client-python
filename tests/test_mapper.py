"""
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
IMPLIED, INCLUDING WITHOUT LIMITATION THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import os
import pytest
from tankerkoenig.models.mapper import JsonMapper
from tankerkoenig.models.gas_prices import GasPrices, GasType, Status
from tankerkoenig.models.station import Station


def get_resource_path(filename):
    """Get path to test resource file"""
    return os.path.join(os.path.dirname(__file__), "resources", filename)


class TestJsonMapper:
    """Tests for JsonMapper JSON parsing"""
    
    def test_parse_prices_json(self):
        """Test parsing prices JSON response"""
        with open(get_resource_path("prices.json"), "r") as f:
            json_str = f.read()
        
        mapper = JsonMapper()
        result = mapper.from_json(json_str, dict)
        
        assert result is not None
        assert "ok" in result
        assert result["ok"] is True
        assert "prices" in result
        
        prices = result["prices"]
        assert "1723edea-8e01-4de3-8c5e-ca227a49e2c3" in prices
        
        station_prices = prices["1723edea-8e01-4de3-8c5e-ca227a49e2c3"]
        assert station_prices["status"] == "open"
        assert station_prices["e5"] == 1.234
        assert station_prices["e10"] == 1.234
        assert station_prices["diesel"] == 1.234
    
    def test_deserialize_gas_prices(self):
        """Test deserializing GasPrices from JSON"""
        price_data = {
            "status": "open",
            "e5": 1.234,
            "e10": 1.189,
            "diesel": 1.456
        }
        
        mapper = JsonMapper()
        gas_prices = mapper._deserialize_gas_prices(price_data)
        
        assert gas_prices.status == Status.OPEN
        assert gas_prices.get_price(GasType.E5) == 1.234
        assert gas_prices.get_price(GasType.E10) == 1.189
        assert gas_prices.get_price(GasType.DIESEL) == 1.456
    
    def test_deserialize_station(self):
        """Test deserializing Station from JSON"""
        with open(get_resource_path("detail.json"), "r") as f:
            json_data = json.load(f)
        
        station_data = json_data["station"]
        mapper = JsonMapper()
        station = mapper._deserialize_station(station_data)
        
        assert station.id == "51d4b660-a095-1aa0-e100-80009459e03a"
        assert station.name == "JET BERLIN HERZBERGSTR. 27"
        assert station.brand == "JET"
        assert station.is_open is True
        assert station.whole_day is True
        
        assert station.location is not None
        assert station.location.lat == 52.5262
        assert station.location.lng == 13.4886
        assert station.location.city == "BERLIN"
        assert station.location.zip_code == 10365
        
        assert station.gas_prices is not None
        assert station.gas_prices.get_price(GasType.E5) == 1.009
        assert station.gas_prices.get_price(GasType.E10) == 1.009
        assert station.gas_prices.get_price(GasType.DIESEL) == 1.009
        
        assert station.opening_times is not None
        assert len(station.opening_times) == 4
        
        assert station.overriding_opening_times is not None
        assert len(station.overriding_opening_times) == 2

