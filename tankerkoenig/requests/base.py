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

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, TypeVar, Generic, Type

from tankerkoenig.exceptions import RequesterException
from tankerkoenig.models.results import BaseResult

R = TypeVar('R', bound=BaseResult)


class Method(Enum):
    """HTTP method for requests"""
    GET = "GET"
    POST = "POST"


class RequestParam(ABC):
    """Interface for request parameters that can be converted to query parameters"""
    
    @abstractmethod
    def to_query_param(self) -> str:
        """Converts the parameter to a query parameter string"""
        pass


class BaseRequest(ABC, Generic[R]):
    """Base class for all request types"""
    
    def __init__(self, api_key: str, base_url: str, requester: 'Requester'):
        self._api_key = api_key
        self._base_url = base_url
        self._requester = requester
    
    def execute(self) -> R:
        """Executes the request using the underlying Requester,
        which will return the requested result object
        
        Raises:
            RequesterException: Checked exceptions that might be thrown during request execution
        """
        return self._requester.execute(self, self.get_result_class())
    
    @abstractmethod
    def get_endpoint(self) -> str:
        """Returns the API endpoint for this request"""
        pass
    
    @abstractmethod
    def get_request_parameters(self) -> Dict[str, Any]:
        """Returns the request parameters as a dictionary"""
        pass
    
    @abstractmethod
    def validate(self) -> None:
        """Validates the request parameters.
        Raises RequestParamException if validation fails"""
        pass
    
    @abstractmethod
    def get_method(self) -> Method:
        """Returns the HTTP method for this request"""
        pass
    
    @abstractmethod
    def get_result_class(self) -> Type[R]:
        """Returns the result class for this request"""
        pass
    
    def get_api_key(self) -> str:
        """Returns the API key"""
        return self._api_key
    
    def get_base_url(self) -> str:
        """Returns the base URL"""
        return self._base_url
