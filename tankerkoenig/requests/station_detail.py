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

from typing import Dict, Any, Type, TYPE_CHECKING

from tankerkoenig.requests.base import BaseRequest, Method
from tankerkoenig.requests.validator import RequestParamValidator
from tankerkoenig.models.results import StationDetailResult
from tankerkoenig.utils import RequestParamBuilder

if TYPE_CHECKING:
    from tankerkoenig.client import Requester


class StationDetailRequest(BaseRequest[StationDetailResult]):
    """Request to obtain detail information for a station, specified by the stations unique ID
    which is obtainable using the StationListRequest"""
    
    ENDPOINT = "detail.php"
    
    def __init__(self, api_key: str, base_url: str, requester: 'Requester', station_id: str):
        super().__init__(api_key, base_url, requester)
        self._station_id = station_id
    
    def get_endpoint(self) -> str:
        return self.ENDPOINT
    
    def get_method(self) -> Method:
        return Method.GET
    
    def get_result_class(self) -> Type[StationDetailResult]:
        return StationDetailResult
    
    def validate(self) -> None:
        RequestParamValidator.not_empty(self._station_id, "ID")
    
    def get_request_parameters(self) -> Dict[str, Any]:
        return RequestParamBuilder.create().add_value("id", self._station_id).build()
