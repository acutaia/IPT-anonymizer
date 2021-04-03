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
from ..aggregation import AggregationType
from ..company import CompanyExtraction
from ..coordinates import StartCoordinatesExtraction, EndCoordinatesExtraction
from ..detection import TypeDetectionExtraction
from ..time import StartTimeExtraction, EndTimeExtraction
from ...track import MobilityType

# --------------------------------------------------------------------------------------------


class StatsNumTracks(
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
    _query_select: str = PrivateAttr("")
    _query_select_main_type_time = PrivateAttr(
        """
        SELECT Distinct(main_type_time),
        count(*) 
        FROM "user_data" WHERE
        """
    )
    _query_select_main_type_space = PrivateAttr(
        """
        SELECT Distinct(main_type_space),
        count(*) 
        FROM "user_data" WHERE
        """
    )
    _query_external: str = PrivateAttr("")
    _query_external_main_type_time: str = PrivateAttr("GROUP BY main_type_time")
    _query_external_main_type_space: str = PrivateAttr("GROUP BY main_type_space")

    type_aggregation: AggregationType = ...
    type_mobility: Optional[MobilityType] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.type_aggregation == AggregationType.time:
            self._query_select = (
                f"{self._query_select_main_type_time} {self._query_company_extraction}"
            )
            self._query_external = self._query_external_main_type_time
        else:
            self._query_select = (
                f"{self._query_select_main_type_space} {self._query_company_extraction}"
            )
            self._query_external = self._query_external_main_type_space

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
            self._query_external = f""" AND '{self.type_mobility}' = "main_type_{self.type_aggregation}" AND {self._query_type_detection_extraction} {self._query_external}"""

        elif self.type_mobility:
            self._query_external = f""" AND '{self.type_mobility}' = "main_type_{self.type_aggregation}" {self._query_external}"""

        elif self._query_type_detection_extraction:
            self._query_external = f" AND {self._query_type_detection_extraction} AND {self._query_external}"

        self._query_select = f"{self._query_select} {self._query_external};"
