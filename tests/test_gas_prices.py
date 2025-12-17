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
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pytest
from tankerkoenig.models.gas_prices import GasPrices, GasType, Status


class TestGasType:
    """Tests for GasType enum"""
    
    def test_gas_type_values(self):
        """Test that GasType enum has correct values"""
        assert GasType.DIESEL.value == "diesel"
        assert GasType.E5.value == "e5"
        assert GasType.E10.value == "e10"
    
    def test_gas_type_enumeration(self):
        """Test that all expected gas types exist"""
        expected_types = {GasType.DIESEL, GasType.E5, GasType.E10}
        assert set(GasType) == expected_types


class TestStatus:
    """Tests for Status enum"""
    
    def test_status_values(self):
        """Test that Status enum has correct values"""
        assert Status.NOT_FOUND.value == "not found"
        assert Status.CLOSED.value == "closed"
        assert Status.OPEN.value == "open"
    
    def test_status_enumeration(self):
        """Test that all expected statuses exist"""
        expected_statuses = {Status.NOT_FOUND, Status.CLOSED, Status.OPEN}
        assert set(Status) == expected_statuses


class TestGasPrices:
    """Tests for GasPrices dataclass"""
    
    def test_gas_prices_creation(self):
        """Test creating GasPrices with prices"""
        prices = {GasType.E5: 1.234, GasType.DIESEL: 1.456}
        gas_prices = GasPrices(prices=prices, status=Status.OPEN)
        
        assert gas_prices.prices == prices
        assert gas_prices.status == Status.OPEN
    
    def test_get_price_existing(self):
        """Test getting an existing price"""
        prices = {GasType.E5: 1.234, GasType.DIESEL: 1.456}
        gas_prices = GasPrices(prices=prices, status=Status.OPEN)
        
        assert gas_prices.get_price(GasType.E5) == 1.234
        assert gas_prices.get_price(GasType.DIESEL) == 1.456
    
    def test_get_price_not_existing(self):
        """Test getting a non-existing price"""
        prices = {GasType.E5: 1.234}
        gas_prices = GasPrices(prices=prices, status=Status.OPEN)
        
        assert gas_prices.get_price(GasType.DIESEL) is None
        assert gas_prices.get_price(GasType.E10) is None
    
    def test_has_price_existing(self):
        """Test has_price with existing price"""
        prices = {GasType.E5: 1.234, GasType.DIESEL: 1.456}
        gas_prices = GasPrices(prices=prices, status=Status.OPEN)
        
        assert gas_prices.has_price(GasType.E5) is True
        assert gas_prices.has_price(GasType.DIESEL) is True
    
    def test_has_price_not_existing(self):
        """Test has_price with non-existing price"""
        prices = {GasType.E5: 1.234}
        gas_prices = GasPrices(prices=prices, status=Status.OPEN)
        
        assert gas_prices.has_price(GasType.DIESEL) is False
        assert gas_prices.has_price(GasType.E10) is False
    
    def test_has_price_with_none(self):
        """Test has_price when price is None"""
        prices = {GasType.E5: None}
        gas_prices = GasPrices(prices=prices, status=Status.OPEN)
        
        assert gas_prices.has_price(GasType.E5) is False
    
    def test_has_prices_with_prices(self):
        """Test has_prices when prices exist"""
        prices = {GasType.E5: 1.234, GasType.DIESEL: 1.456}
        gas_prices = GasPrices(prices=prices, status=Status.OPEN)
        
        assert gas_prices.has_prices() is True
    
    def test_has_prices_empty(self):
        """Test has_prices when no prices exist"""
        gas_prices = GasPrices(prices={}, status=Status.OPEN)
        
        assert gas_prices.has_prices() is False
    
    def test_has_prices_all_none(self):
        """Test has_prices when all prices are None"""
        prices = {GasType.E5: None, GasType.DIESEL: None}
        gas_prices = GasPrices(prices=prices, status=Status.OPEN)
        
        assert gas_prices.has_prices() is False
    
    def test_get_status(self):
        """Test getting status"""
        prices = {GasType.E5: 1.234}
        
        gas_prices_open = GasPrices(prices=prices, status=Status.OPEN)
        assert gas_prices_open.get_status() == Status.OPEN
        
        gas_prices_closed = GasPrices(prices=prices, status=Status.CLOSED)
        assert gas_prices_closed.get_status() == Status.CLOSED
        
        gas_prices_not_found = GasPrices(prices=prices, status=Status.NOT_FOUND)
        assert gas_prices_not_found.get_status() == Status.NOT_FOUND

