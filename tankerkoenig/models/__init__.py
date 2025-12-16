"""Models for Tankerkoenig API responses"""

from tankerkoenig.models.station import Station, Location, OpeningTime, State
from tankerkoenig.models.gas_prices import GasPrices
from tankerkoenig.models.results import (
    BaseResult,
    StationListResult,
    StationDetailResult,
    PricesResult,
    CorrectionResult,
    ResponseStatus
)

__all__ = [
    "Station",
    "Location",
    "OpeningTime",
    "State",
    "GasPrices",
    "BaseResult",
    "StationListResult",
    "StationDetailResult",
    "PricesResult",
    "CorrectionResult",
    "ResponseStatus",
]
