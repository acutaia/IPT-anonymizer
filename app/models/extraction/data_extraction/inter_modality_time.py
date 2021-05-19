#!/usr/bin/env python3
"""
Inter_Modality_Time model

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
from ..time import StartTimeExtraction, EndTimeExtraction

# --------------------------------------------------------------------------------------------


class InterModalityTime(
    StartTimeExtraction,
    EndTimeExtraction,
    StartCoordinatesExtraction,
    EndCoordinatesExtraction,
    CompanyExtraction,
):
    _query_start_time_extraction: Optional[str] = PrivateAttr(None)
    _query_end_time_extraction: Optional[str] = PrivateAttr(None)
    _query_start_coordinate_extraction: Optional[str] = PrivateAttr(None)
    _query_end_coordinate_extraction: Optional[str] = PrivateAttr(None)
    _query_company_extraction: str = PrivateAttr("")
    _query_select: str = PrivateAttr("")

    def __init__(self, **data):
        super().__init__(**data)
        self._query_select = self._query_company_extraction

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
