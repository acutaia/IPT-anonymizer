#!/usr/bin/env python3
"""
Database Constants module

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

# ---------------------------------------------------------------------------------------------------------


INSERT_USER_DATA_QUERY = """
                INSERT INTO "user_data"(
                journey_id,
                source_app,
                company_code,
                company_trip_type,
                distance,
                elapsed_time,
                end_date,
                id,
                main_type_space,
                main_type_time,
                start_date,
                start_lat,
                start_lon,
                end_lat,
                end_lon
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15);"""
"""Query to store User_Data in the database"""

# ---------------------------------------------------------------------------------------------------------


INSERT_USER_POSITIONS_QUERY = """
                INSERT INTO "user_positions"(
                journey_id,
                time,
                authenticity,
                lat,
                lon,
                partial_distance
                ) VALUES ($1, $2, $3, $4, $5, $6);"""
"""Query to store User_Positions in the database"""

# ---------------------------------------------------------------------------------------------------------


INSERT_USER_BEHAVIOURS_QUERY = """
                INSERT INTO "user_behaviours"(
                journey_id,
                source_app,
                mode,
                pos,
                type,
                meters,
                accuracy,
                start_auth,
                start_lat,
                start_lon,
                start_partial_distance,
                start_time,
                end_auth,
                end_lat,
                end_lon,
                end_partial_distance,
                end_time 
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17);"""
"""Query to store User_Behaviours in the database"""

# ---------------------------------------------------------------------------------------------------------


INSERT_USER_SENSORS_QUERY = """
                INSERT INTO "user_sensors"(
                journey_id,
                time,
                name,
                data
                ) VALUES ($1, $2, $3, $4) ON CONFLICT(journey_id, time, name) DO NOTHING;"""
"""Query to store User_Sensors in the database"""

# ---------------------------------------------------------------------------------------------------------

INSERT_IOT_DATA_QUERY = """
                INSERT INTO "iot_data"(
                result_time,
                datastream,
                feature_of_interest,
                phenomenon_time,
                observation_gep_id,
                result_auth,
                value_type,
                position_type,
                position_lat,
                position_lon,
                response_value
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11);"""
"""Query to store IoT_Data in the database"""

# ---------------------------------------------------------------------------------------------------------
