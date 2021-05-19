#!/usr/bin/env python3
"""
Test Inter Modality Space Model

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

# Test
import pytest

# Third Party
from pydantic import ValidationError

# Internal
from app.models.extraction.data_extraction.inter_modality_space import (
    InterModalitySpace,
)
from .constants import *

# ----------------------------------------------------------------------------------------


class TestInterModalitySpace:
    def test_no_extra_request(self):
        data = InterModalitySpace(source_app="travis")
        assert data._query_select is not None

    def test_start_time_extraction(self):
        data = InterModalitySpace(
            source_app="travis",
            start_time=START_TIME,
            start_time_high_threshold=START_TIME_HIGH_THRESHOLD,
        )

        assert (
            data._query_start_time_extraction
            == f"start_date BETWEEN {START_TIME} AND {START_TIME + START_TIME_HIGH_THRESHOLD}"
        )
        # Both value must be set or unset
        with pytest.raises(ValidationError):
            InterModalitySpace(source_app="travis", start_time=START_TIME)

        with pytest.raises(ValidationError):
            InterModalitySpace(
                source_app="travis", start_time_high_threshold=START_TIME_HIGH_THRESHOLD
            )

    def test_end_time_extraction(self):
        data = InterModalitySpace(
            source_app="travis",
            end_time=END_TIME,
            end_time_high_threshold=END_TIME_HIGH_THRESHOLD,
        )

        assert (
            data._query_end_time_extraction
            == f"end_date BETWEEN {END_TIME} AND {END_TIME + END_TIME_HIGH_THRESHOLD}"
        )
        # Both value must be set or unset
        with pytest.raises(ValidationError):
            InterModalitySpace(end_time=END_TIME)

        with pytest.raises(ValidationError):
            InterModalitySpace(end_time_high_threshold=END_TIME_HIGH_THRESHOLD)

    def test_start_coordinates_extraction(self):
        data = InterModalitySpace(
            source_app="travis",
            start_lat=START_LAT,
            start_lon=START_LON,
            start_radius=START_RADIUS,
        )

        assert data._query_start_coordinate_extraction
        # Both value must be set or unset
        with pytest.raises(ValidationError):
            InterModalitySpace(source_app="travis", start_lat=START_LAT)

        with pytest.raises(ValidationError):
            InterModalitySpace(source_app="travis", start_lon=START_LON)

        with pytest.raises(ValidationError):
            InterModalitySpace(
                source_app="travis", start_lat=START_LAT, start_lon=START_LON
            )

        with pytest.raises(ValidationError):
            InterModalitySpace(
                source_app="travis", start_lon=START_LON, start_radius=START_RADIUS
            )

    def test_end_coordinates_extraction(self):

        data = InterModalitySpace(
            source_app="travis", end_lat=END_LAT, end_lon=END_LON, end_radius=END_RADIUS
        )
        assert data._query_end_coordinate_extraction
        # Both value must be set or unset
        with pytest.raises(ValidationError):
            InterModalitySpace(source_app="travis", end_lat=END_LAT)

        with pytest.raises(ValidationError):
            InterModalitySpace(source_app="travis", end_lon=END_LON)

        with pytest.raises(ValidationError):
            InterModalitySpace(source_app="travis", end_lat=END_LAT, end_lon=END_LON)

        with pytest.raises(ValidationError):
            InterModalitySpace(
                source_app="travis", end_lon=END_LON, end_radius=END_RADIUS
            )

    def test_company_extraction(self):
        data = InterModalitySpace(
            source_app="travis",
            company_code=COMPANY_CODE,
            company_trip_type=COMPANY_TRIP_TYPE,
        )
        assert (
            data._query_company_extraction
            == f"source_app = 'travis' AND company_code = '{COMPANY_CODE}' AND company_trip_type = '{COMPANY_TRIP_TYPE}'"
        )
