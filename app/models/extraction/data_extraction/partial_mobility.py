#!/usr/bin/env python3
"""
Partial_Mobility models

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
from pydantic import validator, PrivateAttr

# Internal
from ..company import CompanyExtraction
from ..coordinates import StartCoordinatesExtraction, EndCoordinatesExtraction
from ..detection import TypeDetectionExtraction
from ..time import StartTimeExtraction, EndTimeExtraction
from ...model import OrjsonModel
from ...track import MobilityType, AggregationType

# --------------------------------------------------------------------------------------------


class PartialMobilityTypeExtraction(OrjsonModel):
    type_mobility: Optional[MobilityType] = None
    type_aggregation: Optional[AggregationType] = None

    _query_type_mobility_extract: Optional[str] = None

    @validator("type_aggregation", always=True)
    def both_mobility_aggregation_must_be_set_or_none(cls, v, values):
        if values["type_mobility"] and v or values["type_mobility"] == v:
            return v
        raise ValueError("both type_mobility and type_aggregation must be set or None")

    def __init__(self, **data):
        super().__init__(**data)
        if self.type_mobility:
            self._query_type_mobility_extract = f""" '{self.type_mobility}' = "type" """


# --------------------------------------------------------------------------------------------


class PartialMobility(
    StartTimeExtraction,
    EndTimeExtraction,
    StartCoordinatesExtraction,
    EndCoordinatesExtraction,
    CompanyExtraction,
    TypeDetectionExtraction,
    PartialMobilityTypeExtraction,
):
    _query_start_time_extraction: Optional[str] = PrivateAttr(None)
    _query_end_time_extraction: Optional[str] = PrivateAttr(None)
    _query_start_coordinate_extraction: Optional[str] = PrivateAttr(None)
    _query_end_coordinate_extraction: Optional[str] = PrivateAttr(None)
    _query_company_extraction: str = PrivateAttr("")
    _query_type_detection_extraction: Optional[str] = PrivateAttr(None)
    _query_type_mobility_extract: Optional[str] = PrivateAttr(None)
    _query_select: str = PrivateAttr(
        """
        SELECT journey_id,
        type,
        mode,
        nested.w1 AS start_time,
        nested.w2 AS end_time,
        nested.y1 AS start_lat,
        nested.y2 AS start_lon,
        nested.y3 AS end_lat,
        nested.y4 AS end_lon,
        nested.z AS meters
        FROM "user_behaviours",
        (
        SELECT journey_id AS x,
        start_lat AS y1,
        start_lon AS y2,
        end_lat AS y3,
        end_lon AS y4,
        distance AS z,
        start_date AS w1,
        end_date AS w2
        FROM "user_data" WHERE"""
    )
    _query_external: str = PrivateAttr(") AS nested WHERE nested.x = journey_id")
    # request: Literal[RequestType.partial_mobility] = ...

    def __init__(self, **data):
        super().__init__(**data)
        self._query_select = (
            f"{self._query_select} {self._query_company_extraction}"
        )
        if self._query_start_time_extraction:
            self._query_select = (
                f"{self._query_select} AND {self._query_start_time_extraction}"
            )

        if self._query_end_time_extraction:
            self._query_select = (
                f"{self._query_select} AND {self._query_end_time_extraction}"
            )

        if self._query_start_coordinate_extraction:
            self._query_select = (
                f"{self._query_select} AND {self._query_start_coordinate_extraction}"
            )

        if self._query_end_coordinate_extraction:
            self._query_select = (
                f"{self._query_select} AND {self._query_end_coordinate_extraction}"
            )

        if self._query_type_mobility_extract and self._query_type_detection_extraction:
            self._query_external = f"{self._query_external} AND {self._query_type_mobility_extract} AND {self._query_type_detection_extraction}"

        elif self._query_type_mobility_extract:
            self._query_external = (
                f"{self._query_external} AND {self._query_type_mobility_extract}"
            )

        elif self._query_type_detection_extraction:
            self._query_external = (
                f"{self._query_external} AND {self._query_type_detection_extraction}"
            )

        self._query_select = f"{self._query_select} {self._query_external};"
