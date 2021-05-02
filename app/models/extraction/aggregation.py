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
from pydantic import validator

# Internal
from ..model import OrjsonModel
from ..track import AggregationType

# --------------------------------------------------------------------------------------------


class AggregationExtract(OrjsonModel):
    space_aggregation: Optional[int] = None
    time_aggregation: Optional[int] = None
    type_aggregation: Optional[AggregationType] = None

    @validator("type_aggregation", always=True)
    def type_aggregation_must_be_coherent(cls, v, values):
        if v == AggregationType.time:
            if values["time_aggregation"] and values["space_aggregation"] is None:
                return v
            else:
                ValueError(
                    "type_aggregation is time so time_aggregation must be set and space_aggregation unset"
                )
        elif v == AggregationType.space:
            if values["space_aggregation"] and values["time_aggregation"] is None:
                return v
            else:
                ValueError(
                    "type_aggregation is space so space_aggregation must be set and time_aggregation unset"
                )
        else:
            if values["space_aggregation"] == values["time_aggregation"] and v is None:
                return v
            else:
                ValueError("type_aggregation is not set")

    def __init__(self, **data):
        super().__init__(**data)
