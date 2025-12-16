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

from typing import Collection, Dict, Any


def join(values: Collection[str], separator: str) -> str:
    """Joins a collection of strings with a separator, filtering out None and empty values"""
    if not values:
        return ""
    
    filtered = [v for v in values if v]
    return separator.join(filtered)


class RequestParamBuilder:
    """Builder for request parameters"""
    
    def __init__(self):
        self._map: Dict[str, Any] = {}
    
    @staticmethod
    def create() -> 'RequestParamBuilder':
        """Creates a new RequestParamBuilder instance"""
        return RequestParamBuilder()
    
    def add_value(self, key: str, value: Any) -> 'RequestParamBuilder':
        """Adds a value to the parameter map.
        If value is a RequestParam, it will be converted using to_query_param()"""
        if hasattr(value, 'to_query_param'):
            self._map[key] = value.to_query_param()
        else:
            self._map[key] = value
        return self
    
    def build(self) -> Dict[str, Any]:
        """Builds the final parameter map"""
        return self._map
