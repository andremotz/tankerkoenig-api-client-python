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

from typing import Dict, Any, Type, Collection, TYPE_CHECKING

from tankerkoenig.requests.base import BaseRequest, Method
from tankerkoenig.requests.validator import RequestParamValidator
from tankerkoenig.models.results import PricesResult
from tankerkoenig.utils import RequestParamBuilder, join

if TYPE_CHECKING:
    from tankerkoenig.client import Requester


class PricesRequest(BaseRequest[PricesResult]):
    """Request for gas prices.
    Between 1 and 10 station IDs can and must be supplied, or the request will fail."""
    
    ENDPOINT = "prices.php"
    
    def __init__(self, api_key: str, base_url: str, requester: 'Requester'):
        super().__init__(api_key, base_url, requester)
        self._station_ids: set = set()
    
    def add_id(self, station_id: str) -> 'PricesRequest':
        """Adds a station id. Will only be added if not None nor empty.
        A maximum of 10 IDs is allowed and IDs are getting added uniquely"""
        if station_id:
            self._station_ids.add(station_id)
        return self
    
    def add_ids(self, *station_ids: str) -> 'PricesRequest':
        """Adds multiple station ids. Will only be added if not None nor empty.
        A maximum of 10 IDs is allowed and IDs are getting added uniquely"""
        return self.add_ids_collection(station_ids)
    
    def add_ids_collection(self, station_ids: Collection[str]) -> 'PricesRequest':
        """Adds multiple station ids from a collection. Will only be added if not None nor empty.
        A maximum of 10 IDs is allowed and IDs are getting added uniquely"""
        filtered_ids = {id for id in station_ids if id}
        self._station_ids.update(filtered_ids)
        return self
    
    def get_endpoint(self) -> str:
        return self.ENDPOINT
    
    def get_method(self) -> Method:
        return Method.GET
    
    def get_result_class(self) -> Type[PricesResult]:
        return PricesResult
    
    def validate(self) -> None:
        RequestParamValidator.not_empty_collection(self._station_ids, "IDs")
        RequestParamValidator.max_count(self._station_ids, 10, "IDs")
    
    def get_request_parameters(self) -> Dict[str, Any]:
        return RequestParamBuilder.create().add_value("ids", join(self._station_ids, ",")).build()
