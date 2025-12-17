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

import re
from typing import Collection, Any

from tankerkoenig.exceptions import RequestParamException


class RequestParamValidator:
    """Static validator methods for request parameters"""
    
    _post_code_pattern = re.compile(r'\d{5}')
    _float_pattern = re.compile(r'[-]?[0-9]*\.[0-9]+')
    _location_pattern = re.compile(_float_pattern.pattern + r'\s?,\s?' + _float_pattern.pattern)
    
    @staticmethod
    def min_max(value: float, min_val: int, max_val: int, label: str) -> None:
        """Validates that a value is between min and max"""
        if value < min_val or value > max_val:
            raise RequestParamException(f"{label} has to be between {min_val} and {max_val}")
    
    @staticmethod
    def not_null(value: Any, label: str) -> None:
        """Validates that a value is not None"""
        if value is None:
            raise RequestParamException(f"{label} must not be null")
    
    @staticmethod
    def not_empty(value: str, label: str) -> None:
        """Validates that a string is not empty"""
        RequestParamValidator.not_null(value, label)
        if not value:
            raise RequestParamException(f"{label} must not be empty")
    
    @staticmethod
    def not_empty_collection(collection: Collection, label: str) -> None:
        """Validates that a collection is not empty"""
        RequestParamValidator.not_null(collection, label)
        if len(collection) == 0:
            raise RequestParamException(f"{label} must not be empty")
    
    @staticmethod
    def max_count(collection: Collection, max_val: int, label: str) -> None:
        """Validates that a collection has at most max_val elements"""
        if max_val < 0:
            raise RuntimeError("Max must not be below 0")
        
        RequestParamValidator.not_null(collection, label)
        
        if len(collection) > max_val:
            raise RequestParamException(f"A maximum of {max_val} {label} is allowed per request")
    
    @staticmethod
    def is_float(value: str, label: str) -> None:
        """Validates that a string is a valid floating point number"""
        RequestParamValidator.not_null(value, label)
        if not RequestParamValidator._float_pattern.match(value):
            raise RequestParamException(f"{value} is not a valid floating point value for {label}")
    
    @staticmethod
    def is_post_code(value: str) -> None:
        """Validates that a string is a valid German post code (5 digits)"""
        RequestParamValidator.not_null(value, "Post Code")
        if len(value) != 5 or not RequestParamValidator._post_code_pattern.match(value):
            raise RequestParamException(f"{value} is not a valid post code, it must have a format of 12345")
    
    @staticmethod
    def is_location_data(value: str) -> None:
        """Validates that a string is valid location data (lat, lng format)"""
        RequestParamValidator.not_null(value, "Location")
        if len(value) < 3 or not RequestParamValidator._location_pattern.match(value):
            raise RequestParamException(f'{value} is not a location data, it must be in the format of "58.0,13.0"')
