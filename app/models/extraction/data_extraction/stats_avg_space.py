#!/usr/bin/env python3
"""
Stats_num_tracks model

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


class StatsAvgSpace(
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
        SELECT Distinct(type), avg(meters), count(journey_id)
        FROM user_behaviours,
        (SELECT journey_id as x FROM "user_data" WHERE"""
    )
    _query_external: str = PrivateAttr(") AS nested WHERE journey_id=nested.x")
    _query_external_extra: str = PrivateAttr("GROUP BY type")

    type_mobility: Optional[MobilityType] = None

    def __init__(self, **data):
        super().__init__(**data)

        if self._query_start_time_extraction:
            self._query_select = (
                f"{self._query_select} {self._query_start_time_extraction} AND"
            )

        if self._query_end_time_extraction:
            self._query_select = (
                f"{self._query_select} {self._query_end_time_extraction} AND"
            )

        if self._query_start_coordinate_extraction:
            self._query_select = (
                f"{self._query_select} {self._query_start_coordinate_extraction} AND"
            )

        if self._query_end_coordinate_extraction:
            self._query_select = (
                f"{self._query_select} {self._query_end_coordinate_extraction} AND"
            )

        if self.type_mobility and self._query_type_detection_extraction:
            self._query_external = f"""{self._query_external} AND '{self.type_mobility}' = "type" AND {self._query_type_detection_extraction}"""

        elif self.type_mobility:
            self._query_external = (
                f"""{self._query_external} AND '{self.type_mobility}' = "type" """
            )

        elif self._query_type_detection_extraction:
            self._query_external = (
                f"{self._query_external} AND {self._query_type_detection_extraction}"
            )

        self._query_select = f"{self._query_select[:-4]} {self._query_external} {self._query_external_extra};"
