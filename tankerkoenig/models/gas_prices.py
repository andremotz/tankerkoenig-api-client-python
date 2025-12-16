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

from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum


class GasType(Enum):
    """A set of requestable gas types"""
    DIESEL = "diesel"
    E5 = "e5"
    E10 = "e10"


class Status(Enum):
    """A set of possible status flags of the station"""
    NOT_FOUND = "not found"
    CLOSED = "closed"
    OPEN = "open"


@dataclass
class GasPrices:
    """Represents gas prices for a station"""
    prices: Dict[GasType, float]
    status: Status
    
    def get_price(self, gas_type: GasType) -> Optional[float]:
        """Returns the gas price, if available"""
        return self.prices.get(gas_type)
    
    def has_price(self, gas_type: GasType) -> bool:
        """Determines if a gas price of a certain type is available"""
        return gas_type in self.prices and self.prices[gas_type] is not None
    
    def has_prices(self) -> bool:
        """Determines if any price is available"""
        return len(self.prices) > 0 and any(
            price is not None for price in self.prices.values()
        )
    
    def get_status(self) -> Status:
        """Returns the stations status / availability.
        If it returns NOT_FOUND, the supplied ID at the request was wrong or the station
        is temporarily unavailable"""
        return self.status
