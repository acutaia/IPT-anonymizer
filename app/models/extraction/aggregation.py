#!/usr/bin/env python3
"""
Aggregation model

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
from pydantic import validator

# Internal
from ..model import OrjsonModel
from ..track import AggregationType

# --------------------------------------------------------------------------------------------


class AggregationExtract(OrjsonModel):

    type_aggregation: Optional[AggregationType] = None
    space_aggregation: Optional[int] = None
    time_aggregation: Optional[int] = None

    @validator("space_aggregation", always=True)
    def type_aggregation_must_be_space_or_none(cls, v, values):
        if values["type_aggregation"] == v or (
            values["type_aggregation"] == AggregationType.space and v is None
        ):
            return v
        raise ValueError(
            f"type_aggregation must be {AggregationType.space} if space_aggregation is set"
        )

    @validator("time_aggregation", always=True)
    def type_aggregation_must_be_time_or_none(cls, v, values):
        if values["type_aggregation"] == v or (
            values["type_aggregation"] == AggregationType.time and v is None
        ):
            return v
        raise ValueError(
            f"type_aggregation must be {AggregationType.time} if time_aggregation is set"
        )
