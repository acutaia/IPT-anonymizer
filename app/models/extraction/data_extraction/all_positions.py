#!/usr/bin/env python3
"""
All_Positions model

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
from pydantic import PrivateAttr

# Internal
from ..company import CompanyExtraction
from ..coordinates import StartCoordinatesExtraction, EndCoordinatesExtraction
from ..detection import TypeDetectionExtraction
from ..time import StartTimeExtraction, EndTimeExtraction
from ...track import MobilityType

# --------------------------------------------------------------------------------------------


class AllPositions(
    StartTimeExtraction,
    EndTimeExtraction,
    StartCoordinatesExtraction,
    EndCoordinatesExtraction,
    CompanyExtraction,
    TypeDetectionExtraction,
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
        SELECT nested_pos.y as journey_id,
        nested_behaviour.type,
        nested_behaviour.mode,
        nested_pos.lat,
        nested_pos.lon,
        nested_pos.time,
        nested_pos.partial_distance
        FROM
        (
        SELECT type, mode, journey_id, start_time, end_time
        FROM "user_behaviours"
        ) AS nested_behaviour,
        (
        SELECT journey_id AS y, lat, lon, time, partial_distance
        FROM "user_positions"
        ) AS nested_pos,
        (
        SELECT journey_id AS x
        FROM "user_data" WHERE"""
    )
    _query_external: str = PrivateAttr(
        """) AS nested WHERE nested.x = nested_pos.y 
                                   AND nested_pos.y = nested_behaviour.journey_id
                                   AND nested_behaviour.start_time <= nested_pos.time
                                   AND nested_behaviour.end_time >= nested_pos.time"""
    )
    type_mobility: Optional[MobilityType] = None

    def __init__(self, **data):
        super().__init__(**data)
        self._query_select = f"{self._query_select} {self._query_company_extraction}"
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

        if self.type_mobility and self._query_type_detection_extraction:
            self._query_external = f"""{self._query_external} AND '{self.type_mobility}' = "type" AND {self._query_type_detection_extraction}"""

        elif self.type_mobility:
            self._query_external = (
                f"""{self._query_external} AND '{self.type_mobility}' = "type" """
            )

        elif self._query_type_detection_extraction:
            self._query_external = (
                f"""{self._query_external} AND '{self.type_mobility}' = "type" """
            )

        self._query_select = f"{self._query_select} {self._query_external};"
