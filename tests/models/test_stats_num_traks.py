#!/usr/bin/env python3
"""
Test All Positions Model

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

# Test
import pytest

# Third Party
from pydantic import ValidationError

# Internal
from app.models.extraction.data_extraction.stats_num_tracks import StatsNumTracks
from .constants import *

# ----------------------------------------------------------------------------------------


class TestStatsNumTracks:
    def test_no_extra_request(self):
        data = StatsNumTracks(source_app="travis", type_aggregation="space")
        assert data._query_select is not None
        data = StatsNumTracks(source_app="travis", type_aggregation="time")
        assert data._query_select is not None

    def test_start_time_extraction(self):
        for type_aggregation in ("space", "time"):
            data = StatsNumTracks(
                source_app="travis",
                type_aggregation=type_aggregation,
                start_time=START_TIME,
                start_time_high_threshold=START_TIME_HIGH_THRESHOLD,
            )

            assert (
                data._query_start_time_extraction
                == f"start_date BETWEEN {START_TIME} AND {START_TIME + START_TIME_HIGH_THRESHOLD}"
            )
            # Both value must be set or unset
            with pytest.raises(ValidationError):
                StatsNumTracks(
                    source_app="travis",
                    type_aggregation=type_aggregation,
                    start_time=START_TIME,
                )

            with pytest.raises(ValidationError):
                StatsNumTracks(
                    source_app="travis",
                    type_aggregation=type_aggregation,
                    start_time_high_threshold=START_TIME_HIGH_THRESHOLD,
                )

    def test_end_time_extraction(self):
        for type_aggregation in ("space", "time"):
            data = StatsNumTracks(
                source_app="travis",
                type_aggregation=type_aggregation,
                end_time=END_TIME,
                end_time_high_threshold=END_TIME_HIGH_THRESHOLD,
            )

            assert (
                data._query_end_time_extraction
                == f"end_date BETWEEN {END_TIME} AND {END_TIME + END_TIME_HIGH_THRESHOLD}"
            )
            # Both value must be set or unset
            with pytest.raises(ValidationError):
                StatsNumTracks(
                    source_app="travis",
                    type_aggregation=type_aggregation,
                    end_time=END_TIME,
                )

            with pytest.raises(ValidationError):
                StatsNumTracks(
                    source_app="travis",
                    type_aggregation=type_aggregation,
                    end_time_high_threshold=END_TIME_HIGH_THRESHOLD,
                )

    def test_start_coordinates_extraction(self):
        for type_aggregation in ("space", "time"):
            data = StatsNumTracks(
                source_app="travis",
                type_aggregation=type_aggregation,
                start_lat=START_LAT,
                start_lon=START_LON,
                start_radius=START_RADIUS,
            )

            assert data._query_start_coordinate_extraction
            # Both value must be set or unset
            with pytest.raises(ValidationError):
                StatsNumTracks(
                    source_app="travis",
                    type_aggregation=type_aggregation,
                    start_lat=START_LAT,
                )

            with pytest.raises(ValidationError):
                StatsNumTracks(
                    source_app="travis",
                    type_aggregation=type_aggregation,
                    start_lon=START_LON,
                )

            with pytest.raises(ValidationError):
                StatsNumTracks(
                    source_app="travis",
                    type_aggregation=type_aggregation,
                    start_lat=START_LAT,
                    start_lon=START_LON,
                )

            with pytest.raises(ValidationError):
                StatsNumTracks(
                    source_app="travis",
                    type_aggregation=type_aggregation,
                    start_lon=START_LON,
                    start_radius=START_RADIUS,
                )

    def test_end_coordinates_extraction(self):
        for type_aggregation in ("space", "time"):
            data = StatsNumTracks(
                source_app="travis",
                type_aggregation=type_aggregation,
                end_lat=END_LAT,
                end_lon=END_LON,
                end_radius=END_RADIUS,
            )
            assert data._query_end_coordinate_extraction
            # Both value must be set or unset
            with pytest.raises(ValidationError):
                StatsNumTracks(
                    source_app="travis",
                    type_aggregation=type_aggregation,
                    end_lat=END_LAT,
                )

            with pytest.raises(ValidationError):
                StatsNumTracks(
                    source_app="travis",
                    type_aggregation=type_aggregation,
                    end_lon=END_LON,
                )

            with pytest.raises(ValidationError):
                StatsNumTracks(
                    source_app="travis",
                    type_aggregation=type_aggregation,
                    end_lat=END_LAT,
                    end_lon=END_LON,
                )

            with pytest.raises(ValidationError):
                StatsNumTracks(
                    source_app="travis",
                    type_aggregation=type_aggregation,
                    end_lon=END_LON,
                    end_radius=END_RADIUS,
                )

    def test_company_extraction(self):
        for type_aggregation in ("space", "time"):
            data = StatsNumTracks(
                source_app="travis",
                type_aggregation=type_aggregation,
                company_code=COMPANY_CODE,
                company_trip_type=COMPANY_TRIP_TYPE,
            )
            assert (
                data._query_company_extraction
                == f"source_app = 'travis' AND company_code = '{COMPANY_CODE}' AND company_trip_type = '{COMPANY_TRIP_TYPE}'"
            )

    def test_type_detection_extraction(self):
        for type_aggregation in ("space", "time"):
            data = StatsNumTracks(
                source_app="travis",
                type_aggregation=type_aggregation,
                type_mobility=TYPE_MOBILITY,
                type_detection=TYPE_DETECTION,
            )
            assert (
                f"""'{TYPE_MOBILITY}' = "main_type_{type_aggregation}" AND """
                in data._query_external
            )
            assert data._query_type_detection_extraction

            data = StatsNumTracks(
                source_app="travis",
                type_aggregation=type_aggregation,
                type_mobility=TYPE_MOBILITY,
            )
            assert (
                f"""'{TYPE_MOBILITY}' = "main_type_{type_aggregation}" """
                in data._query_external
            )
            assert data._query_type_detection_extraction is None

            data = StatsNumTracks(
                source_app="travis",
                type_aggregation=type_aggregation,
                type_detection=TYPE_DETECTION,
            )
            assert data._query_type_detection_extraction
