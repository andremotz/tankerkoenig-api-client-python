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

import pytest


@pytest.fixture
def sample_gas_prices():
    """Fixture providing sample GasPrices"""
    from tankerkoenig.models.gas_prices import GasPrices, GasType, Status
    return GasPrices(
        prices={GasType.E5: 1.234, GasType.E10: 1.189, GasType.DIESEL: 1.456},
        status=Status.OPEN
    )


@pytest.fixture
def sample_location():
    """Fixture providing sample Location"""
    from tankerkoenig.models.station import Location, State
    return Location(
        lat=52.5200,
        lng=13.4050,
        street_name="Test Street",
        house_number="123",
        zip_code=10115,
        city="Berlin",
        state=State.deBE,
        distance=5.5
    )


@pytest.fixture
def sample_station(sample_location, sample_gas_prices):
    """Fixture providing sample Station"""
    from tankerkoenig.models.station import Station, OpeningTime
    return Station(
        id="test-station-id",
        name="Test Station",
        location=sample_location,
        brand="Test Brand",
        is_open=True,
        price=1.234,
        gas_prices=sample_gas_prices,
        opening_times=[
            OpeningTime(text="Mo-Fr", start="08:00:00", end="18:00:00")
        ]
    )

