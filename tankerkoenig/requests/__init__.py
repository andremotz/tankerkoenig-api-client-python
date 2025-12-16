"""Request classes for Tankerkoenig API"""

from tankerkoenig.requests.base import BaseRequest, RequestParam, Method
from tankerkoenig.requests.station_list import StationListRequest, SortingRequestType
from tankerkoenig.requests.station_detail import StationDetailRequest
from tankerkoenig.requests.prices import PricesRequest
from tankerkoenig.requests.correction import CorrectionRequest
from tankerkoenig.requests.gas_request_type import GasRequestType

__all__ = [
    "BaseRequest",
    "RequestParam",
    "Method",
    "StationListRequest",
    "SortingRequestType",
    "StationDetailRequest",
    "PricesRequest",
    "CorrectionRequest",
    "GasRequestType",
]
