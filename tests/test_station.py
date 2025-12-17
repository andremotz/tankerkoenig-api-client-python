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
from tankerkoenig.models.station import Station, Location, OpeningTime, State
from tankerkoenig.models.gas_prices import GasPrices, GasType, Status


class TestLocation:
    """Tests for Location dataclass"""
    
    def test_location_creation(self):
        """Test creating a Location"""
        location = Location(lat=52.5200, lng=13.4050)
        
        assert location.lat == 52.5200
        assert location.lng == 13.4050
    
    def test_location_with_address(self):
        """Test creating a Location with address"""
        location = Location(
            lat=52.5200,
            lng=13.4050,
            street_name="Test Street",
            house_number="123",
            zip_code=10115,
            city="Berlin",
            state=State.deBE
        )
        
        assert location.street_name == "Test Street"
        assert location.house_number == "123"
        assert location.zip_code == 10115
        assert location.city == "Berlin"
        assert location.state == State.deBE
    
    def test_get_distance(self):
        """Test getting distance"""
        location = Location(lat=52.5200, lng=13.4050, distance=5.5)
        assert location.get_distance() == 5.5
        
        location_no_distance = Location(lat=52.5200, lng=13.4050)
        assert location_no_distance.get_distance() is None
    
    def test_get_house_number(self):
        """Test getting house number"""
        location = Location(lat=52.5200, lng=13.4050, house_number="123")
        assert location.get_house_number() == "123"
        
        location_no_house = Location(lat=52.5200, lng=13.4050)
        assert location_no_house.get_house_number() is None
    
    def test_get_state(self):
        """Test getting state"""
        location = Location(lat=52.5200, lng=13.4050, state=State.deBE)
        assert location.get_state() == State.deBE
        
        location_no_state = Location(lat=52.5200, lng=13.4050)
        assert location_no_state.get_state() is None


class TestOpeningTime:
    """Tests for OpeningTime dataclass"""
    
    def test_opening_time_creation(self):
        """Test creating an OpeningTime"""
        opening_time = OpeningTime(
            text="Mo-Fr",
            days=[1, 2, 3, 4, 5],
            start="08:00:00",
            end="18:00:00",
            includes_holidays=False
        )
        
        assert opening_time.text == "Mo-Fr"
        assert opening_time.days == [1, 2, 3, 4, 5]
        assert opening_time.start == "08:00:00"
        assert opening_time.end == "18:00:00"
        assert opening_time.includes_holidays is False
    
    def test_get_days(self):
        """Test getting days"""
        opening_time = OpeningTime(text="Mo-Fr", days=[1, 2, 3, 4, 5])
        assert opening_time.get_days() == [1, 2, 3, 4, 5]
        
        opening_time_no_days = OpeningTime(text="Always open")
        assert opening_time_no_days.get_days() is None


class TestStation:
    """Tests for Station dataclass"""
    
    def test_station_creation_minimal(self):
        """Test creating a Station with minimal data"""
        station = Station(id="test-id")
        
        assert station.id == "test-id"
        assert station.name is None
        assert station.location is None
        assert station.brand is None
        assert station.is_open is False
    
    def test_station_creation_full(self):
        """Test creating a Station with all data"""
        location = Location(lat=52.5200, lng=13.4050)
        gas_prices = GasPrices(prices={GasType.E5: 1.234}, status=Status.OPEN)
        opening_times = [OpeningTime(text="Mo-Fr", start="08:00:00", end="18:00:00")]
        
        station = Station(
            id="test-id",
            name="Test Station",
            location=location,
            brand="Test Brand",
            is_open=True,
            price=1.234,
            gas_prices=gas_prices,
            opening_times=opening_times,
            overriding_opening_times=["Special hours"],
            whole_day=False
        )
        
        assert station.id == "test-id"
        assert station.name == "Test Station"
        assert station.location == location
        assert station.brand == "Test Brand"
        assert station.is_open is True
        assert station.price == 1.234
        assert station.gas_prices == gas_prices
        assert station.opening_times == opening_times
    
    def test_get_name(self):
        """Test getting station name"""
        station = Station(id="test-id", name="Test Station")
        assert station.get_name() == "Test Station"
        
        station_no_name = Station(id="test-id")
        assert station_no_name.get_name() is None
    
    def test_get_brand(self):
        """Test getting station brand"""
        station = Station(id="test-id", brand="Test Brand")
        assert station.get_brand() == "Test Brand"
        
        station_no_brand = Station(id="test-id")
        assert station_no_brand.get_brand() is None
    
    def test_get_gas_prices(self):
        """Test getting gas prices"""
        gas_prices = GasPrices(prices={GasType.E5: 1.234}, status=Status.OPEN)
        station = Station(id="test-id", gas_prices=gas_prices)
        
        assert station.get_gas_prices() == gas_prices
        
        station_no_prices = Station(id="test-id")
        assert station_no_prices.get_gas_prices() is None
    
    def test_get_opening_times(self):
        """Test getting opening times"""
        opening_times = [OpeningTime(text="Mo-Fr", start="08:00:00", end="18:00:00")]
        station = Station(id="test-id", opening_times=opening_times)
        
        assert station.get_opening_times() == opening_times
        
        station_no_times = Station(id="test-id")
        assert station_no_times.get_opening_times() is None
    
    def test_get_overriding_opening_times(self):
        """Test getting overriding opening times"""
        overriding = ["Special hours", "Holiday hours"]
        station = Station(id="test-id", overriding_opening_times=overriding)
        
        assert station.get_overriding_opening_times() == overriding
        
        station_no_overriding = Station(id="test-id")
        assert station_no_overriding.get_overriding_opening_times() is None
    
    def test_is_whole_day(self):
        """Test is_whole_day"""
        station = Station(id="test-id", whole_day=True)
        assert station.is_whole_day() is True
        
        station_not_whole_day = Station(id="test-id", whole_day=False)
        assert station_not_whole_day.is_whole_day() is False
        
        station_no_whole_day = Station(id="test-id")
        assert station_no_whole_day.is_whole_day() is None
    
    def test_get_price(self):
        """Test getting price"""
        station = Station(id="test-id", price=1.234)
        assert station.get_price() == 1.234
        
        station_no_price = Station(id="test-id")
        assert station_no_price.get_price() is None
    
    def test_equality(self):
        """Test station equality"""
        station1 = Station(id="test-id", name="Station 1")
        station2 = Station(id="test-id", name="Station 2")
        station3 = Station(id="other-id", name="Station 1")
        
        assert station1 == station2  # Same ID
        assert station1 != station3  # Different ID
        assert station1 != "not a station"  # Different type
    
    def test_hash(self):
        """Test station hashing"""
        station1 = Station(id="test-id")
        station2 = Station(id="test-id")
        station3 = Station(id="other-id")
        
        assert hash(station1) == hash(station2)  # Same ID
        assert hash(station1) != hash(station3)  # Different ID
        
        # Can be used in sets
        station_set = {station1, station2, station3}
        assert len(station_set) == 2  # station1 and station2 are equal

