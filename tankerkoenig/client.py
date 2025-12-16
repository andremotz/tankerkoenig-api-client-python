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
from typing import Dict, Any, Type, TypeVar, Generic
import requests
from urllib.parse import urlencode

from tankerkoenig.exceptions import ClientExecutorException, RequesterException, RequestParamException
from tankerkoenig.requests.base import BaseRequest, Method
from tankerkoenig.models.results import BaseResult
from tankerkoenig.models.mapper import JsonMapper

R = TypeVar('R', bound=BaseResult)


class ClientExecutor(ABC):
    """Interface for executing HTTP requests"""
    
    @abstractmethod
    def get(self, url: str, query_parameters: Dict[str, Any]) -> str:
        """Executes a GET request
        
        Args:
            url: The request URL
            query_parameters: The query parameters
            
        Returns:
            The response body
            
        Raises:
            ClientExecutorException: Should be thrown if any parameter or client-side error occurs
        """
        pass
    
    @abstractmethod
    def post(self, url: str, form_params: Dict[str, Any]) -> str:
        """Executes a POST request. Request Parameters should be sent as forms (not multipart)
        
        Args:
            url: The request URL
            form_params: The form parameters
            
        Returns:
            The response body
            
        Raises:
            ClientExecutorException: Should be thrown if any parameter or client-side error occurs
        """
        pass


class RequestsClientExecutor(ClientExecutor):
    """Client Executor which wraps around requests library"""
    
    def __init__(self, session: requests.Session = None):
        """Creates a new RequestsClientExecutor
        
        Args:
            session: Optional requests Session. If None, a new one will be created.
        """
        self._session = session or requests.Session()
    
    def get(self, url: str, query_parameters: Dict[str, Any]) -> str:
        """Executes a GET request"""
        try:
            # Filter out None and empty values
            params = {k: str(v) for k, v in query_parameters.items() if v is not None and str(v)}
            
            response = self._session.get(url, params=params)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise ClientExecutorException(url, f"An exception was thrown while request execution: {str(e)}", e)
    
    def post(self, url: str, form_params: Dict[str, Any]) -> str:
        """Executes a POST request with form data"""
        try:
            # Filter out None and empty values
            data = {k: str(v) for k, v in form_params.items() if v is not None and str(v)}
            
            response = self._session.post(url, data=data)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise ClientExecutorException(url, f"An exception was thrown while request execution: {str(e)}", e)


class ClientExecutorFactory:
    """Factory for ClientExecutors"""
    
    @staticmethod
    def build_default_client_executor() -> ClientExecutor:
        """Builds the default ClientExecutor, which currently wraps requests library"""
        return RequestsClientExecutor()


class Requester:
    """The requester is responsible for the execution of the request
    and mapping the result to the specified result class.
    Recoverable failures will be wrapped by a RequesterException"""
    
    def __init__(self, client_executor: ClientExecutor, json_mapper: JsonMapper):
        """Creates a new Requester
        
        Args:
            client_executor: The client executor to use for HTTP requests
            json_mapper: The JSON mapper to use for deserialization
        """
        self._client_executor = client_executor
        self._json_mapper = json_mapper
    
    def execute(self, request: BaseRequest[R], result_class: Type[R]) -> R:
        """Executes a request and returns the result
        
        Args:
            request: The request to execute
            result_class: The expected result class
            
        Returns:
            The mapped result object
            
        Raises:
            RequesterException: If the request execution fails
        """
        try:
            request.validate()
        except RequestParamException as e:
            raise RequesterException("An exception was thrown during request validation", e)
        
        request_parameters = request.get_request_parameters()
        request_parameters["apikey"] = request.get_api_key()
        
        # Add timestamp if not present
        if "ts" not in request_parameters:
            import time
            request_parameters["ts"] = int(time.time())
        
        try:
            request_url = request.get_base_url() + request.get_endpoint()
            
            if request.get_method() == Method.GET:
                result = self._client_executor.get(request_url, request_parameters)
            elif request.get_method() == Method.POST:
                result = self._client_executor.post(request_url, request_parameters)
            else:
                raise UnsupportedOperationException(f"The request method {request.get_method()} is not supported")
            
            return self._json_mapper.from_json(result, result_class)
        except ClientExecutorException as e:
            raise RequesterException("An exception was thrown while request execution", e)
        except Exception as e:
            raise RequesterException("An unhandled exception was thrown", e)


class UnsupportedOperationException(Exception):
    """Exception for unsupported operations"""
    pass
