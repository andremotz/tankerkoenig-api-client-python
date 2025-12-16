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

from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from tankerkoenig.models.gas_prices import GasPrices


class State(Enum):
    """German state codes"""
    # Brandenburg
    deBB = "deBB"
    # Berlin
    deBE = "deBE"
    # Baden-Württemberg
    deBW = "deBW"
    # Bavaria
    deBY = "deBY"
    # Bremen
    deHB = "deHB"
    # Hesse
    deHE = "deHE"
    # Hamburg
    deHH = "deHH"
    # Mecklenburg-Vorpommern
    deMV = "deMV"
    # Lower Saxony
    deNI = "deNI"
    # North Rhine-Westphalia
    deNW = "deNW"
    # Rhineland-Palatinate
    deRP = "deRP"
    # Schleswig-Holstein
    deSH = "deSH"
    # Saarland
    deSL = "deSL"
    # Saxony
    deSN = "deSN"
    # Saxony-Anhalt
    deST = "deST"
    # Thuringia
    deTH = "deTH"


@dataclass
class Location:
    """Represents the location of a Station"""
    lat: float
    lng: float
    street_name: str = ""
    house_number: Optional[str] = None
    zip_code: Optional[int] = None
    city: str = ""
    state: Optional[State] = None
    distance: Optional[float] = None  # Only available in StationListResult
    
    def get_distance(self) -> Optional[float]:
        """Returns the distance to the position which is passed to the StationListRequest.
        Unavailable for StationDetailResult"""
        return self.distance
    
    def get_house_number(self) -> Optional[str]:
        """Returns the house number of the Station.
        Sometimes the station owners will put the house number inside the street name,
        so this information is not always available."""
        return self.house_number if self.house_number else None
    
    def get_state(self) -> Optional[State]:
        """Returns the state of the Station.
        This information is not available most of the time, therefore it is marked as optional."""
        return self.state


@dataclass
class OpeningTime:
    """Represents the opening times of a Station"""
    text: str
    days: Optional[List[int]] = None  # List of day numbers (1=Monday, 7=Sunday)
    start: Optional[str] = None  # Format: HH:MM:ss
    end: Optional[str] = None  # Format: HH:MM:ss
    includes_holidays: bool = False
    
    def get_days(self) -> Optional[List[int]]:
        """Returns the list of days of the week for that the times are valid"""
        return self.days if self.days else None


@dataclass
class Station:
    """Represents a gas station"""
    id: str
    name: Optional[str] = None
    location: Optional[Location] = None
    brand: Optional[str] = None
    is_open: bool = False
    price: Optional[float] = None
    gas_prices: Optional['GasPrices'] = None  # type: ignore  # Forward reference
    opening_times: Optional[List[OpeningTime]] = None
    overriding_opening_times: Optional[List[str]] = None
    whole_day: Optional[bool] = None
    
    def get_name(self) -> Optional[str]:
        """Returns the stations name"""
        return self.name if self.name else None
    
    def get_brand(self) -> Optional[str]:
        """Returns the stations brand.
        Sometimes this information is not available, which is mostly the case for
        gas stations in private ownership."""
        return self.brand
    
    def get_gas_prices(self) -> Optional['GasPrices']:
        """Returns the stations gas prices.
        Will only be available with StationListRequest if GasRequestType is set to ALL,
        or StationDetailRequest"""
        return self.gas_prices
    
    def get_opening_times(self) -> Optional[List[OpeningTime]]:
        """Returns an unmodifiable list of opening times for the station.
        Will only be available with StationDetailResult"""
        return self.opening_times if self.opening_times else None
    
    def get_overriding_opening_times(self) -> Optional[List[str]]:
        """Returns an unmodifiable list of overriding opening times for the station.
        Those are arbitrary strings without any specific structure which define
        temporary changes of opening times.
        Will only be available with StationDetailResult"""
        return self.overriding_opening_times if self.overriding_opening_times else None
    
    def is_whole_day(self) -> Optional[bool]:
        """Defines if the station is opened the whole day.
        Not Present is equivalent to False"""
        return self.whole_day
    
    def get_price(self) -> Optional[float]:
        """Returns the gas price for the requested GasRequestType.
        Will only be available with StationListRequest if GasRequestType is set to E5, E10 or DIESEL"""
        return self.price
    
    def __eq__(self, other):
        if not isinstance(other, Station):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
