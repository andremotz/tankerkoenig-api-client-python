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

from typing import Dict, Any, Optional, Type, TYPE_CHECKING

from tankerkoenig.requests.base import BaseRequest, Method, RequestParam
from tankerkoenig.requests.validator import RequestParamValidator
from tankerkoenig.requests.gas_request_type import GasRequestType
from tankerkoenig.models.results import StationListResult
from tankerkoenig.utils import RequestParamBuilder

if TYPE_CHECKING:
    from tankerkoenig.client import Requester


class SortingRequestType(RequestParam):
    """Sorting type for station list requests"""
    
    PRICE = "price"
    DISTANCE = "dist"
    
    def __init__(self, value: str):
        self._value = value
    
    def to_query_param(self) -> str:
        """Converts the sorting type to a query parameter"""
        return self._value
    
    def __eq__(self, other):
        if not isinstance(other, SortingRequestType):
            return False
        return self._value == other._value
    
    def __hash__(self):
        return hash(self._value)


# Create singleton instances
SortingRequestType.PRICE = SortingRequestType("price")
SortingRequestType.DISTANCE = SortingRequestType("dist")


class StationListRequest(BaseRequest[StationListResult]):
    """Request to obtain a list of stations. The search is based around the coordinates,
    which are mandatory and must be in the specified boundaries."""
    
    ENDPOINT = "list.php"
    
    def __init__(self, api_key: str, base_url: str, requester: 'Requester'):
        super().__init__(api_key, base_url, requester)
        self._lat: Optional[float] = None
        self._lng: Optional[float] = None
        self._search_radius: float = 5.0
        self._gas_request_type: GasRequestType = GasRequestType.ALL
        self._sorting: SortingRequestType = SortingRequestType.DISTANCE
    
    def set_coordinates(self, lat: float, lng: float) -> 'StationListRequest':
        """Sets the center of the search
        
        Args:
            lat: Must be between -90 and 90
            lng: Must be between -180 and 180
        """
        self._lat = lat
        self._lng = lng
        return self
    
    def set_gas_request_type(self, gas_request_type: GasRequestType) -> 'StationListRequest':
        """Sets which gas prices should be requested, which can either be a specific
        one or ALL. Default is: ALL"""
        self._gas_request_type = gas_request_type
        return self
    
    def set_search_radius(self, radius: float) -> 'StationListRequest':
        """Sets the search radius in Kilometers. Default is: 5
        
        Args:
            radius: Must be between 1.0 and 25.0 km
        """
        self._search_radius = radius
        return self
    
    def set_sorting(self, sorting: SortingRequestType) -> 'StationListRequest':
        """Sets the sorting for the results. Default is: DISTANCE"""
        self._sorting = sorting
        return self
    
    def get_endpoint(self) -> str:
        return self.ENDPOINT
    
    def get_method(self) -> Method:
        return Method.GET
    
    def get_result_class(self) -> Type[StationListResult]:
        return StationListResult
    
    def validate(self) -> None:
        RequestParamValidator.not_null(self._lat, "Latitude")
        RequestParamValidator.not_null(self._lng, "Longitude")
        RequestParamValidator.min_max(self._lat, -90, 90, "Latitude")
        RequestParamValidator.min_max(self._lng, -180, 180, "Longitude")
        RequestParamValidator.min_max(self._search_radius, 1, 25, "Radius")
        RequestParamValidator.not_null(self._gas_request_type, "Gas Request Type")
        RequestParamValidator.not_null(self._sorting, "Sorting")
    
    def get_request_parameters(self) -> Dict[str, Any]:
        builder = RequestParamBuilder.create()
        builder.add_value("lat", self._lat)
        builder.add_value("lng", self._lng)
        builder.add_value("rad", self._search_radius)
        builder.add_value("type", self._gas_request_type)
        
        # If gas_request_type is ALL, always use DISTANCE sorting
        sort_value = SortingRequestType.DISTANCE if self._gas_request_type == GasRequestType.ALL else self._sorting
        builder.add_value("sort", sort_value)
        
        return builder.build()
