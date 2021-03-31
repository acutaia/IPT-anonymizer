#!/usr/bin/env python3
"""
Coordinates models

:author: Angelo Cutaia
:copyright: Copyright 2021, Angelo Cutaia
:version: 1.0.0

..

    Copyright 2021 Angelo Cutaia

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Standard Library
from typing import Optional

# Third Party
from pydantic import validator, confloat

# Internal
from .position_alteration_detection import reversed_haversine
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class StartCoordinatesExtraction(OrjsonModel):
    start_lat: Optional[float] = None
    """Starting latitude example=5.74235"""
    start_lon: Optional[float] = None
    """Starting longitude example=14.45236"""
    start_radius: Optional[confloat(ge=100)] = None
    """Starting radius with specified center in meters example=123.35161"""

    _query_start_coordinate_extraction: Optional[str] = None

    @validator("start_radius", always=True)
    def both_start_radius_lat_lon_must_be_set_or_none(cls, v, values):
        if (
            values["start_lat"]
            and values["start_lon"]
            and v
            or (values["start_lat"] == v and values["start_lon"] == v)
        ):
            return v
        raise ValueError(
            "both start_lat, start_lon and start_radius must be set or None"
        )

    def __init__(self, **data):
        super().__init__(**data)
        # check only one arguments cause if one is set, every other is also set
        if self.start_lat:
            lat0, lat1, lon0, lon1 = reversed_haversine(
                self.start_lat, self.start_lon, self.start_radius
            )
            self._query_start_coordinate_extraction = f"start_lat BETWEEN {lat0} AND {lat1} AND start_lon BETWEEN {lon0} AND {lon1}"


# --------------------------------------------------------------------------------------------


class EndCoordinatesExtraction(OrjsonModel):
    end_lat: Optional[float] = None
    """Ending latitude example=5.74235"""
    end_lon: Optional[float] = None
    """Ending longitude example=14.45236"""
    end_radius: Optional[confloat(ge=100)] = None
    """Ending radius with specified center in meters example=123.35161"""

    _query_end_coordinate_extraction: Optional[str] = None

    @validator("end_radius", always=True)
    def both_end_radius_lat_lon_must_be_set_or_none(cls, v, values):
        if (
            values["end_lat"]
            and values["end_lon"]
            and v
            or (values["end_lat"] == v and values["end_lon"] == v)
        ):
            return v
        raise ValueError("both end_lat, end_lon and end_radius must be set or None")

    def __init__(self, **data):
        super().__init__(**data)
        # check only one arguments cause if one is set, every other is also set
        if self.end_lat:
            lat0, lat1, lon0, lon1 = reversed_haversine(
                self.end_lat, self.end_lon, self.end_radius
            )
            self._query_end_coordinate_extraction = f"end_lat BETWEEN {lat0} AND {lat1} AND end_lon BETWEEN {lon0} AND {lon1}"
