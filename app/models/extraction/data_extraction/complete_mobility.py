"""
Complete_Mobility model

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
from pydantic import PrivateAttr

# Internal
from ..company import CompanyExtraction
from ..coordinates import StartCoordinatesExtraction, EndCoordinatesExtraction
from ..detection import TypeDetectionExtraction
from ..time import StartTimeExtraction, EndTimeExtraction
from ...track import MobilityType

# --------------------------------------------------------------------------------------------


class CompleteMobility(
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
        SELECT journey_id,
        type,
        mode,
        start_time,
        end_time,
        start_lat,
        start_lon,
        end_lat,
        end_lon,
        meters
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
