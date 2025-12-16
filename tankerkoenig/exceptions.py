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


class TankerkoenigException(Exception):
    """Base exception for all Tankerkoenig API exceptions"""
    pass


class ClientExecutorException(TankerkoenigException):
    """Exceptions thrown if an error at a ClientExecutor occurs"""
    
    def __init__(self, url: str, message: str, cause: Exception = None):
        super().__init__(message)
        self.url = url
        self.cause = cause
    
    def get_url(self) -> str:
        """Returns the URL of the call where the exception occurred"""
        return self.url


class RequesterException(TankerkoenigException):
    """Exceptions thrown by a Requester when the request execution of the underlying
    ClientExecutor failed"""
    
    def __init__(self, message: str, cause: Exception = None):
        super().__init__(message)
        self.cause = cause


class RequestParamException(TankerkoenigException):
    """Exceptions thrown if any request parameter fails validation"""
    
    def __init__(self, message: str, *args):
        super().__init__(message.format(*args) if args else message)


class ResponseParsingException(TankerkoenigException):
    """Exception thrown by a JSON Mapper if the supplied response body could
    not be parsed"""
    
    def __init__(self, original_value: str, type_of_value: str):
        message = f"{type_of_value} could not be parsed (original: {original_value})"
        super().__init__(message)
        self.original_value = original_value
        self.type_of_value = type_of_value
