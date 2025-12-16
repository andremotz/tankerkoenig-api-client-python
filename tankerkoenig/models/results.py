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
from typing import Optional, List, Dict
from enum import Enum

from tankerkoenig.models.station import Station
from tankerkoenig.models.gas_prices import GasPrices


class ResponseStatus(Enum):
    """Response status from API"""
    OK = "ok"
    ERROR = "error"


@dataclass
class BaseResult:
    """Base class for all result types"""
    status: Optional[ResponseStatus] = None
    message: Optional[str] = None
    license: Optional[str] = None
    data: Optional[str] = None
    ok: Optional[bool] = None
    
    def get_status(self) -> Optional[ResponseStatus]:
        """Returns the response status.
        Won't be filled for requests by CorrectionRequest"""
        return self.status
    
    def get_message(self) -> Optional[str]:
        """In case of an error, will return the error message"""
        return self.message
    
    def get_license(self) -> Optional[str]:
        """Will return the APIs license information.
        Won't be filled for requests by CorrectionRequest"""
        return self.license
    
    def get_data(self) -> Optional[str]:
        """Returns the original data supplier for gas prices.
        Won't be filled for requests by CorrectionRequest"""
        return self.data
    
    def is_ok(self) -> Optional[bool]:
        """Returns whether the request was successful"""
        return self.ok


@dataclass
class StationListResult(BaseResult):
    """Result of StationListRequest. In case of success, is_ok() will return True.
    Else, the error information are supplied as described in BaseResult"""
    stations: List[Station] = field(default_factory=list)
    
    def get_stations(self) -> List[Station]:
        """Returns an unmodifiable list of stations, which might be empty"""
        return self.stations


@dataclass
class StationDetailResult(BaseResult):
    """Result of StationDetailRequest. In case of success, is_ok() will return True.
    Else, the error information are supplied as described in BaseResult"""
    station: Optional[Station] = None
    
    def get_station(self) -> Optional[Station]:
        """Returns the station, which is None in case of an error"""
        return self.station


@dataclass
class PricesResult(BaseResult):
    """Result of PricesRequest. In case of success, is_ok() will return True.
    Else, the error information are supplied as described in BaseResult"""
    prices: Dict[str, GasPrices] = field(default_factory=dict)
    
    def get_gas_prices(self) -> Dict[str, GasPrices]:
        """Will return an unmodifiable map of gas prices, which uses the
        Station ID as key"""
        return self.prices
    
    def get_gas_price(self, station_id: str) -> Optional[GasPrices]:
        """Will return the gas prices for a station, defined by the Station ID"""
        return self.prices.get(station_id)


@dataclass
class CorrectionResult(BaseResult):
    """Result of CorrectionRequest. In case of success, is_ok() will return True.
    Else, the error information are supplied as described in BaseResult"""
    pass
