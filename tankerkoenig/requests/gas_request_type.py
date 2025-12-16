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

from tankerkoenig.requests.base import RequestParam


class GasRequestType(RequestParam):
    """Defines which price data should be requested, which is either
    specific (DIESEL, E5, E10) or ALL"""
    
    DIESEL = "diesel"
    E5 = "e5"
    E10 = "e10"
    ALL = "all"
    
    def __init__(self, value: str):
        self._value = value
    
    def to_query_param(self) -> str:
        """Converts the gas request type to a query parameter"""
        return self._value
    
    def __eq__(self, other):
        if not isinstance(other, GasRequestType):
            return False
        return self._value == other._value
    
    def __hash__(self):
        return hash(self._value)


# Create singleton instances
GasRequestType.DIESEL = GasRequestType("diesel")
GasRequestType.E5 = GasRequestType("e5")
GasRequestType.E10 = GasRequestType("e10")
GasRequestType.ALL = GasRequestType("all")
