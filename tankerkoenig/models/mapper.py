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

import json
from typing import Type, TypeVar, Dict, Any, Optional, List
from dataclasses import dataclass

from tankerkoenig.models.gas_prices import GasPrices, GasType, Status
from tankerkoenig.models.station import Station, Location, OpeningTime, State

T = TypeVar('T')


class JsonMapper:
    """A JSON Mapper which simply converts a string to an object"""
    
    def from_json(self, json_str: str, result_class: Type[T]) -> T:
        """Converts the supplied JSON string to the result class
        
        Args:
            json_str: The json string
            result_class: The expected result class
            
        Returns:
            The mapped result object
        """
        data = json.loads(json_str)
        return self._deserialize(data, result_class)
    
    def _deserialize(self, data: Any, target_class: Type[T]) -> T:
        """Deserializes data into the target class"""
        if target_class == GasPrices:
            return self._deserialize_gas_prices(data)
        elif target_class == Station:
            return self._deserialize_station(data)
        elif target_class == Location:
            return self._deserialize_location(data)
        elif target_class == OpeningTime:
            return self._deserialize_opening_time(data)
        elif hasattr(target_class, '__dataclass_fields__'):
            # It's a dataclass
            return self._deserialize_dataclass(data, target_class)
        else:
            # Try to construct directly
            if isinstance(data, dict):
                return target_class(**data)
            return data
    
    def _deserialize_gas_prices(self, data: Dict[str, Any]) -> GasPrices:
        """Deserializes GasPrices from JSON"""
        prices: Dict[GasType, float] = {}
        
        # Map gas types from JSON keys
        for gas_type in GasType:
            key = gas_type.value
            if key in data and data[key] is not None:
                try:
                    prices[gas_type] = float(data[key])
                except (ValueError, TypeError):
                    pass
        
        # Map status
        status_str = data.get("status", "not found")
        try:
            status = Status(status_str)
        except ValueError:
            status = Status.NOT_FOUND
        
        return GasPrices(prices=prices, status=status)
    
    def _deserialize_station(self, data: Dict[str, Any]) -> Station:
        """Deserializes Station from JSON"""
        station = Station(
            id=data.get("id", ""),
            name=data.get("name"),
            brand=data.get("brand"),
            is_open=data.get("isOpen", False),
            price=self._get_float(data, "price"),
            whole_day=data.get("wholeDay")
        )
        
        # Deserialize location
        if any(key in data for key in ["lat", "lng", "street", "postCode", "place"]):
            station.location = self._deserialize_location(data)
        
        # Deserialize gas prices
        if any(key in data for key in ["e5", "e10", "diesel", "status"]):
            gas_prices = self._deserialize_gas_prices(data)
            if gas_prices.has_prices():
                station.gas_prices = gas_prices
        
        # Deserialize opening times
        if "openingTimes" in data and data["openingTimes"]:
            station.opening_times = [
                self._deserialize_opening_time(ot) for ot in data["openingTimes"]
            ]
        
        # Deserialize overriding opening times
        if "overrides" in data and data["overrides"]:
            station.overriding_opening_times = data["overrides"]
        
        return station
    
    def _deserialize_location(self, data: Dict[str, Any]) -> Location:
        """Deserializes Location from JSON"""
        return Location(
            lat=float(data.get("lat", 0)),
            lng=float(data.get("lng", 0)),
            street_name=data.get("street", ""),
            house_number=data.get("houseNumber"),
            zip_code=data.get("postCode"),
            city=data.get("place", ""),
            state=self._deserialize_state(data.get("state")),
            distance=self._get_float(data, "dist")
        )
    
    def _deserialize_state(self, state_str: Optional[str]) -> Optional[State]:
        """Deserializes State enum from string"""
        if not state_str:
            return None
        try:
            return State[state_str]
        except KeyError:
            return None
    
    def _deserialize_opening_time(self, data: Dict[str, Any]) -> OpeningTime:
        """Deserializes OpeningTime from JSON"""
        text = data.get("text", "")
        start = data.get("start")
        end = data.get("end")
        
        days: Optional[List[int]] = None
        includes_holidays = False
        
        if text:
            if text == "täglich ausser Feiertag":
                days = list(range(1, 8))
            elif text == "täglich":
                days = list(range(1, 8))
                includes_holidays = True
            elif text == "täglich ausser Sonn- und Feiertagen":
                days = list(range(1, 7))  # Monday to Saturday
            else:
                # Try to parse day ranges or individual days
                try:
                    days = self._parse_days(text)
                    if days and 8 in days:  # Holiday
                        includes_holidays = True
                        days = [d for d in days if d != 8]
                except Exception:
                    days = None
        
        return OpeningTime(
            text=text,
            days=days,
            start=start,
            end=end,
            includes_holidays=includes_holidays
        )
    
    def _parse_days(self, text: str) -> List[int]:
        """Parses day strings to day numbers (1=Monday, 7=Sunday, 8=Holiday)"""
        day_map = {
            "Montag": 1, "Mo": 1,
            "Dienstag": 2, "Di": 2,
            "Mittwoch": 3, "Mi": 3,
            "Donnerstag": 4, "Do": 4,
            "Freitag": 5, "Fr": 5,
            "Samstag": 6, "Sa": 6,
            "Sonntag": 7, "So": 7,
            "Feiertag": 8
        }
        
        if "-" in text:
            # Day range
            parts = text.split("-", 1)
            from_day = day_map.get(parts[0].strip(), -1)
            to_day = day_map.get(parts[1].strip(), -1)
            if from_day == -1 or to_day == -1:
                raise ValueError(f"Cannot parse day range: {text}")
            return list(range(from_day, to_day + 1))
        elif "," in text:
            # Comma-separated days
            day_strs = [s.strip() for s in text.split(",")]
            days = [day_map.get(d, -1) for d in day_strs]
            if -1 in days:
                raise ValueError(f"Cannot parse days: {text}")
            return days
        else:
            # Single day
            day = day_map.get(text.strip(), -1)
            if day == -1:
                raise ValueError(f"Cannot parse day: {text}")
            return [day]
    
    def _deserialize_dataclass(self, data: Dict[str, Any], target_class: Type[T]) -> T:
        """Deserializes a dataclass from a dictionary"""
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data)}")
        
        # Get field names from dataclass
        fields = target_class.__dataclass_fields__
        kwargs = {}
        
        for field_name, field_info in fields.items():
            # Try different JSON key names
            json_key = field_name
            if hasattr(field_info, 'metadata') and field_info.metadata:
                json_key = field_info.metadata.get('json_key', field_name)
            
            # Try field name, then json_key, then various alternatives
            value = None
            for key in [field_name, json_key, field_name.replace("_", ""), field_name.title()]:
                if key in data:
                    value = data[key]
                    break
            
            if value is not None:
                # Recursively deserialize if needed
                field_type = field_info.type
                if hasattr(field_type, '__origin__'):
                    # Handle generic types like List, Dict, Optional
                    origin = field_type.__origin__
                    if origin is list or origin is List:
                        args = field_type.__args__
                        if args and args[0] != str:
                            value = [self._deserialize(v, args[0]) for v in value]
                    elif origin is dict or origin is Dict:
                        args = field_type.__args__
                        if len(args) >= 2:
                            value = {k: self._deserialize(v, args[1]) for k, v in value.items()}
                elif isinstance(value, dict):
                    value = self._deserialize(value, field_type)
                elif isinstance(value, list):
                    args = getattr(field_type, '__args__', None)
                    if args:
                        value = [self._deserialize(v, args[0]) for v in value]
            
            kwargs[field_name] = value
        
        return target_class(**kwargs)
    
    def _get_float(self, data: Dict[str, Any], key: str) -> Optional[float]:
        """Safely gets a float value from data"""
        value = data.get(key)
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None


# Singleton instance
_json_mapper = JsonMapper()


def get_instance() -> JsonMapper:
    """Returns the singleton JsonMapper instance"""
    return _json_mapper
