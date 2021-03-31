#!/usr/bin/env python3
"""
Time Extraction models

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
from abc import ABC

# Standard Library
from typing import Optional, Literal

# Third Party
from pydantic import Field, validator, confloat, PrivateAttr

# Internal
from ..track import (
    RequestType,
    DetectionType,
    MobilityType,
    AggregationType,
    TypeDay,
    TypeOfTrack,
)
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class TimeWindowExtraction(OrjsonModel):
    time_window_low: Optional[str] = None
    """Left time boundary"""
    time_window_high: Optional[str] = None
    """Right time boundary"""

    _query_time_window_extraction: Optional[str] = None
    """Query_related_to_time_window"""

    @validator("time_window_high", always=True)
    def both_time_window_must_be_set_or_none(cls, v, values):
        if values["time_window_low"] and v or values["time_window_low"] == v:
            return v
        raise ValueError("both time_window must be set or None")

    def __init__(self, **data):
        super().__init__(**data)


# --------------------------------------------------------------------------------------------------


class StartTimeExtraction(OrjsonModel):
    start_time: Optional[int] = None
    """Starting time in ms example=1611819579051"""
    start_time_high_threshold: Optional[int] = None
    """Right boundary of the starting time example=3600_000"""

    _query_start_time_extraction: Optional[str] = None

    @validator("start_time_high_threshold", always=True)
    def both_start_time_must_be_set_or_none(cls, v, values):
        if values["start_time"] and v or values["start_time"] == v:
            return v
        raise ValueError(
            "both start_time and start_time_high_threshold must be set or None"
        )

    def __init__(self, **data):
        super().__init__(**data)
        # check only one arguments cause if one is set, every other is also set
        if self.start_time:
            self._query_start_time_extraction = f"start_date BETWEEN {self.start_time} AND {self.start_time + self.start_time_high_threshold}"


# --------------------------------------------------------------------------------------------------


class EndTimeExtraction(OrjsonModel):
    end_time: Optional[int] = None
    """Ending time in ms example=1611819579051"""
    end_time_high_threshold: Optional[int] = None
    """Right boundary of the ending time example=3600_000"""

    _query_end_time_extraction: Optional[str] = None

    @validator("end_time_high_threshold", always=True)
    def both_end_time_must_be_set_or_none(cls, v, values):
        if values["end_time"] and v or values["end_time"] == v:
            return v
        raise ValueError(
            "both end_time and end_time_high_threshold must be set or None"
        )

    def __init__(self, **data):
        super().__init__(**data)
        # check only one arguments cause if one is set, every other is also set
        if self.end_time:
            self._query_end_time_extraction = f"end_date BETWEEN {self.end_time} AND {self.end_time + self.end_time_high_threshold}"
