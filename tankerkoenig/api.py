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

from typing import Optional

from tankerkoenig.client import ClientExecutor, ClientExecutorFactory, Requester
from tankerkoenig.models.mapper import get_instance as get_json_mapper
from tankerkoenig.requests.station_list import StationListRequest
from tankerkoenig.requests.station_detail import StationDetailRequest
from tankerkoenig.requests.prices import PricesRequest
from tankerkoenig.requests.correction import CorrectionRequest, CorrectionType


BASE_URL = "https://creativecommons.tankerkoenig.de/json/"
DEMO_API_KEY = "00000000-0000-0000-0000-000000000002"


class Tankerkoenig:
    """Entry point for creation of the Tankerkoenig API instance.
    
    For technical information: https://creativecommons.tankerkoenig.de/#techInfo
    For usage details: https://creativecommons.tankerkoenig.de/#usage
    For information regarding api key registration: https://creativecommons.tankerkoenig.de/#register
    """
    
    class ApiBuilder:
        """Builder for an API instance"""
        
        def __init__(self, base_url: str = None, client_executor_factory: ClientExecutorFactory = None):
            """Creates a new API builder instance"""
            self._base_url = base_url or BASE_URL
            self._client_executor_factory = client_executor_factory or ClientExecutorFactory()
            self._api_key: Optional[str] = None
            self._client_executor: Optional[ClientExecutor] = None
        
        def with_demo_api_key(self) -> 'Tankerkoenig.ApiBuilder':
            """Sets the API Key to the default key as defined on the official website"""
            self._api_key = DEMO_API_KEY
            return self
        
        def with_api_key(self, api_key: str) -> 'Tankerkoenig.ApiBuilder':
            """Sets the personal API key"""
            self._api_key = api_key
            return self
        
        def with_default_client_executor(self) -> 'Tankerkoenig.ApiBuilder':
            """Uses the default client executor"""
            self._client_executor = self._client_executor_factory.build_default_client_executor()
            return self
        
        def with_client_executor(self, client_executor: ClientExecutor) -> 'Tankerkoenig.ApiBuilder':
            """Uses the specified client executor"""
            self._client_executor = client_executor
            return self
        
        def build(self) -> 'Tankerkoenig.Api':
            """Builds the final API instance. If apiKey is None or empty, will raise an IllegalStateException.
            If no client executor is explicitly specified, will build the default client executor."""
            if not self._api_key:
                raise IllegalStateException("The API key has to be neither empty nor null")
            
            if self._client_executor is None:
                self._client_executor = self._client_executor_factory.build_default_client_executor()
            
            requester = Requester(self._client_executor, get_json_mapper())
            return Tankerkoenig.Api(self._api_key, self._base_url, requester)
    
    class Api:
        """The Tankerkoenig API, which will build the requests"""
        
        def __init__(self, api_key: str, base_url: str, requester: Requester):
            self._api_key = api_key
            self._base_url = base_url
            self._requester = requester
        
        def list(self, lat: float, lng: float) -> StationListRequest:
            """Builds a station list request. The supplied coordinates define the search center
            
            Args:
                lat: Must be between -90 and 90
                lng: Must be between -180 and 180
            """
            return StationListRequest(self._api_key, self._base_url, self._requester).set_coordinates(lat, lng)
        
        def detail(self, station_id: str) -> StationDetailRequest:
            """Builds a station detail request.
            
            Args:
                station_id: The station ID which is obtainable using the list() request
            """
            return StationDetailRequest(self._api_key, self._base_url, self._requester, station_id)
        
        def prices(self) -> PricesRequest:
            """Builds a prices search request"""
            return PricesRequest(self._api_key, self._base_url, self._requester)
        
        def correction(self, station_id: str, correction_type: CorrectionType) -> CorrectionRequest:
            """Builds a station correction request
            
            Args:
                station_id: The station ID which is obtainable using the list() request
                correction_type: The correction request type
            """
            return CorrectionRequest(self._api_key, self._base_url, self._requester, correction_type).set_station_id(station_id)


class IllegalStateException(Exception):
    """Exception for illegal state"""
    pass
