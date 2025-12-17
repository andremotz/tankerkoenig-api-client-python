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
IMPLIED, INCLUDING WITHOUT LIMITATION THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pytest
from tankerkoenig.requests.validator import RequestParamValidator
from tankerkoenig.exceptions import RequestParamException


class TestRequestParamValidator:
    """Tests for RequestParamValidator"""
    
    def test_min_max_valid(self):
        """Test min_max validation with valid value"""
        RequestParamValidator.min_max(5.0, 1, 10, "Test Value")
        RequestParamValidator.min_max(1.0, 1, 10, "Test Value")
        RequestParamValidator.min_max(10.0, 1, 10, "Test Value")
    
    def test_min_max_too_low(self):
        """Test min_max validation with value too low"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.min_max(0.0, 1, 10, "Test Value")
        assert "has to be between 1 and 10" in str(exc_info.value)
    
    def test_min_max_too_high(self):
        """Test min_max validation with value too high"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.min_max(11.0, 1, 10, "Test Value")
        assert "has to be between 1 and 10" in str(exc_info.value)
    
    def test_not_null_valid(self):
        """Test not_null validation with valid value"""
        RequestParamValidator.not_null("test", "Test Value")
        RequestParamValidator.not_null(123, "Test Value")
        RequestParamValidator.not_null(0, "Test Value")
        RequestParamValidator.not_null(False, "Test Value")
    
    def test_not_null_invalid(self):
        """Test not_null validation with None"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.not_null(None, "Test Value")
        assert "must not be null" in str(exc_info.value)
    
    def test_not_empty_valid(self):
        """Test not_empty validation with valid string"""
        RequestParamValidator.not_empty("test", "Test Value")
        RequestParamValidator.not_empty("a", "Test Value")
    
    def test_not_empty_empty_string(self):
        """Test not_empty validation with empty string"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.not_empty("", "Test Value")
        assert "must not be empty" in str(exc_info.value)
    
    def test_not_empty_none(self):
        """Test not_empty validation with None"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.not_empty(None, "Test Value")
        assert "must not be null" in str(exc_info.value)
    
    def test_not_empty_collection_valid(self):
        """Test not_empty_collection validation with valid collection"""
        RequestParamValidator.not_empty_collection([1, 2, 3], "Test Collection")
        RequestParamValidator.not_empty_collection((1, 2), "Test Collection")
        RequestParamValidator.not_empty_collection({1, 2, 3}, "Test Collection")
    
    def test_not_empty_collection_empty(self):
        """Test not_empty_collection validation with empty collection"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.not_empty_collection([], "Test Collection")
        assert "must not be empty" in str(exc_info.value)
    
    def test_not_empty_collection_none(self):
        """Test not_empty_collection validation with None"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.not_empty_collection(None, "Test Collection")
        assert "must not be null" in str(exc_info.value)
    
    def test_max_count_valid(self):
        """Test max_count validation with valid count"""
        RequestParamValidator.max_count([1, 2, 3], 5, "Test Items")
        RequestParamValidator.max_count([1, 2, 3], 3, "Test Items")
        RequestParamValidator.max_count([], 5, "Test Items")
    
    def test_max_count_too_many(self):
        """Test max_count validation with too many items"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.max_count([1, 2, 3, 4, 5, 6], 5, "Test Items")
        assert "A maximum of 5 Test Items is allowed per request" in str(exc_info.value)
    
    def test_max_count_negative_max(self):
        """Test max_count validation with negative max"""
        with pytest.raises(RuntimeError) as exc_info:
            RequestParamValidator.max_count([1, 2, 3], -1, "Test Items")
        assert "Max must not be below 0" in str(exc_info.value)
    
    def test_is_float_valid(self):
        """Test is_float validation with valid float strings"""
        RequestParamValidator.is_float("1.234", "Test Float")
        RequestParamValidator.is_float("-1.234", "Test Float")
        RequestParamValidator.is_float("0.0", "Test Float")
        RequestParamValidator.is_float("123.456", "Test Float")
    
    def test_is_float_invalid(self):
        """Test is_float validation with invalid strings"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.is_float("abc", "Test Float")
        assert "is not a valid floating point value" in str(exc_info.value)
        
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.is_float("123", "Test Float")  # No decimal point
        assert "is not a valid floating point value" in str(exc_info.value)
    
    def test_is_float_none(self):
        """Test is_float validation with None"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.is_float(None, "Test Float")
        assert "must not be null" in str(exc_info.value)
    
    def test_is_post_code_valid(self):
        """Test is_post_code validation with valid post codes"""
        RequestParamValidator.is_post_code("12345")
        RequestParamValidator.is_post_code("00000")
        RequestParamValidator.is_post_code("99999")
    
    def test_is_post_code_invalid(self):
        """Test is_post_code validation with invalid post codes"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.is_post_code("1234")  # Too short
        assert "is not a valid post code" in str(exc_info.value)
        
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.is_post_code("123456")  # Too long
        assert "is not a valid post code" in str(exc_info.value)
        
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.is_post_code("abcde")  # Not numeric
        assert "is not a valid post code" in str(exc_info.value)
    
    def test_is_post_code_none(self):
        """Test is_post_code validation with None"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.is_post_code(None)
        assert "must not be null" in str(exc_info.value)
    
    def test_is_location_data_valid(self):
        """Test is_location_data validation with valid location strings"""
        RequestParamValidator.is_location_data("52.5200,13.4050")
        RequestParamValidator.is_location_data("-52.5200,13.4050")
        RequestParamValidator.is_location_data("52.5200,-13.4050")
        RequestParamValidator.is_location_data("52.5200, 13.4050")  # With space
    
    def test_is_location_data_invalid(self):
        """Test is_location_data validation with invalid location strings"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.is_location_data("52.5200")  # Missing lng
        assert "is not a location data" in str(exc_info.value)
        
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.is_location_data("abc,def")  # Not numeric
        assert "is not a location data" in str(exc_info.value)
        
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.is_location_data("52")  # Too short
        assert "is not a location data" in str(exc_info.value)
    
    def test_is_location_data_none(self):
        """Test is_location_data validation with None"""
        with pytest.raises(RequestParamException) as exc_info:
            RequestParamValidator.is_location_data(None)
        assert "must not be null" in str(exc_info.value)

