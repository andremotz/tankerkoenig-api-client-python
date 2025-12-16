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

from typing import Dict, Any, Type, Optional, TYPE_CHECKING
from enum import Enum, EnumMeta
from abc import ABCMeta

from tankerkoenig.requests.base import BaseRequest, Method, RequestParam
from tankerkoenig.requests.validator import RequestParamValidator
from tankerkoenig.models.results import CorrectionResult
from tankerkoenig.utils import RequestParamBuilder

if TYPE_CHECKING:
    from tankerkoenig.client import Requester


class RequestParamEnumMeta(EnumMeta, ABCMeta):
    """Metaclass that combines EnumMeta and ABCMeta to allow Enum classes to inherit from ABC"""
    pass


class CorrectionType(RequestParam, Enum, metaclass=RequestParamEnumMeta):
    """The type of the correction request"""
    
    # Correction of the stations name - Requires a correction value of String
    WRONG_PETROL_STATION_NAME = "wrongPetrolStationName"
    # Correction of the current opening status of the gas station if open - Requires no correction value
    WRONG_STATUS_OPEN = "wrongStatusOpen"
    # Correction of the current opening status of the gas station if closed - Requires no correction value
    WRONG_STATUS_CLOSED = "wrongStatusClosed"
    # Correction of the price for E5 gasoline - Requires a correction value of Float (#.##)
    WRONG_PRICE_E5 = "wrongPriceE5"
    # Correction of the price for E10 gasoline - Requires a correction value of Float (#.##)
    WRONG_PRICE_E10 = "wrongPriceE10"
    # Correction of the price for Diesel - Requires a correction value of Float (#.##)
    WRONG_PRICE_DIESEL = "wrongPriceDiesel"
    # Correction for the stations brand - Requires a correction value of String
    WRONG_PETROL_STATION_BRAND = "wrongPetrolStationBrand"
    # Correction for the stations street - Requires a correction value of String
    WRONG_PETROL_STATION_STREET = "wrongPetrolStationStreet"
    # Correction for the stations house number - Requires a correction value of String
    WRONG_PETROL_STATION_HOUSE_NUMBER = "wrongPetrolStationHouseNumber"
    # Correction for the stations post code - Requires a correction value of Numeric (5 digits)
    WRONG_PETROL_STATION_POSTCODE = "wrongPetrolStationPostcode"
    # Correction of the stations city - Requires a correction value of String
    WRONG_PETROL_STATION_PLACE = "wrongPetrolStationPlace"
    # Correction of the stations location data - Requires a correction value of String
    WRONG_PETROL_STATION_LOCATION = "wrongPetrolStationLocation"
    
    def to_query_param(self) -> str:
        """Converts the correction type to a query parameter"""
        return self.value
    
    def requires_correction_value(self) -> bool:
        """Determines if the correction type requires a correction value"""
        return self not in (CorrectionType.WRONG_STATUS_OPEN, CorrectionType.WRONG_STATUS_CLOSED)


class CorrectionRequest(BaseRequest[CorrectionResult]):
    """Request for station data corrections.
    Most CorrectionTypes will require correction data except for WRONG_STATUS_OPEN AND WRONG_STATUS_CLOSED.
    The type of the correction values depend on the CorrectionType.
    The station ID is always required"""
    
    ENDPOINT = "complaint.php"
    
    def __init__(self, api_key: str, base_url: str, requester: 'Requester', correction_type: CorrectionType):
        super().__init__(api_key, base_url, requester)
        self._type = correction_type
        self._station_id: Optional[str] = None
        self._correction_value: Optional[str] = None
    
    def set_station_id(self, station_id: str) -> 'CorrectionRequest':
        """Sets the station ID for the correction request. This information is required
        
        Args:
            station_id: The unique station ID, which is provided with StationListResult or StationDetailResult
        """
        self._station_id = station_id
        return self
    
    def set_correction_value(self, correction_value: str) -> 'CorrectionRequest':
        """Sets the corrected value for the correction request. This information is required.
        
        The type of the data is determined by the correction type:
        - Float (#.##): WRONG_PRICE_E5, WRONG_PRICE_E10, WRONG_PRICE_DIESEL
        - Post Code (e.g. 12345): WRONG_PETROL_STATION_POSTCODE
        - Location Data (e.g. 53.0, 13.0): WRONG_PETROL_STATION_LOCATION
        - Any String: Everything else
        
        Args:
            correction_value: The correction value
        """
        self._correction_value = correction_value
        return self
    
    def get_endpoint(self) -> str:
        return self.ENDPOINT
    
    def get_method(self) -> Method:
        return Method.POST
    
    def get_result_class(self) -> Type[CorrectionResult]:
        return CorrectionResult
    
    def validate(self) -> None:
        RequestParamValidator.not_null(self._type, "Type")
        RequestParamValidator.not_empty(self._station_id, "Station ID")
        
        if self._type.requires_correction_value():
            RequestParamValidator.not_empty(self._correction_value, "Correction Value")
            
            if self._type in (CorrectionType.WRONG_PRICE_E5, CorrectionType.WRONG_PRICE_E10, CorrectionType.WRONG_PRICE_DIESEL):
                RequestParamValidator.is_float(self._correction_value, "Correction Value")
            elif self._type == CorrectionType.WRONG_PETROL_STATION_POSTCODE:
                RequestParamValidator.is_post_code(self._correction_value)
            elif self._type == CorrectionType.WRONG_PETROL_STATION_LOCATION:
                RequestParamValidator.is_location_data(self._correction_value)
    
    def get_request_parameters(self) -> Dict[str, Any]:
        builder = RequestParamBuilder.create()
        builder.add_value("id", self._station_id)
        builder.add_value("type", self._type)
        
        if self._type.requires_correction_value():
            builder.add_value("correction", self._correction_value)
        
        return builder.build()
