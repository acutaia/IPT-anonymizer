"""
Data Extraction models

:author: Angelo Cutaia
:copyright: Copyright 2021, LINKS Foundation
:version: 1.0.0

..

    Copyright 2021 LINKS Foundation

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Standard Library
from typing import Optional

# Third Party
from pydantic import confloat

# Internal
from ...track import (
    RequestType,
    DetectionType,
    MobilityType,
    AggregationType,
    TypeOfTrack,
)
from ...model import OrjsonModel

# --------------------------------------------------------------------------------------------


class InputJSONExtraction(OrjsonModel):
    """Input model for extract data"""

    request: RequestType = ...
    """Typology of request"""

    source_app: str = ...
    "Source app"

    time_window_low: Optional[str] = None
    """Left time boundary"""
    time_window_high: Optional[str] = None
    """Right time boundary"""

    start_time: Optional[int] = None
    """Starting time in ms example=1611819579051"""
    start_time_high_threshold: Optional[int] = None
    """Right boundary of the starting time example=3600_000"""

    start_lat: Optional[float] = None
    """Starting latitude example=5.74235"""
    start_lon: Optional[float] = None
    """Starting longitude example=14.45236"""
    start_radius: Optional[confloat(ge=100)] = None
    """Starting radius with specified center in meters example=123.35161"""

    end_time: Optional[int] = None
    """Ending time in ms example=1611819579051"""
    end_time_high_threshold: Optional[int] = None
    """Right boundary of the ending time example=3600_000"""

    end_lat: Optional[float] = None
    """Starting latitude example=5.74235"""
    end_lon: Optional[float] = None
    """Starting longitude example=14.45236"""
    end_radius: Optional[confloat(ge=100)] = None
    """Starting radius with specified center in meters example=123.35161"""

    type_detection: Optional[DetectionType] = None
    type_mobility: Optional[MobilityType] = None

    company_code: str = ""
    """Permit the extraction of company related data"""
    company_trip_type: Optional[TypeOfTrack] = None

    type_aggregation: Optional[AggregationType] = None
    space_aggregation: Optional[int] = None


# --------------------------------------------------------------------------------------------------
