#!/usr/bin/env python3
"""
Database internals package

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
from typing import List

# Third Party
from fastuuid import uuid4

# Internal
from ..models.iot_feed.iot import IotInput
from ..models.user_feed.user import (
    UserFeedInternal,
    Behaviour,
    SensorInformation,
    PositionObject,
)

# --------------------------------------------------------------------------------------


def partial_mobility_format(record_list: List[dict]) -> list:
    """
    Convert data extracted from the database  in partial_mobility_format

    :param record_list: data to convert
    :return: converted data
    """
    journey_id = record_list[0]["journey_id"]
    del record_list[0]["journey_id"]

    temp_obj = {journey_id: record_list[0]}
    temp_obj[journey_id]["type"] = [temp_obj[journey_id]["type"]]

    for pos in range(1, len(record_list)):

        if record_list[pos]["journey_id"] in temp_obj.keys():
            temp_obj[record_list[pos]["journey_id"]]["type"].append(
                record_list[pos]["type"]
            )
        else:
            journey_id = record_list[pos]["journey_id"]
            object_to_add = record_list[pos]
            del object_to_add["journey_id"]

            temp_obj[journey_id] = object_to_add
            temp_obj[journey_id]["type"] = [temp_obj[journey_id]["type"]]

    return [temp_obj[key] for key in temp_obj.keys()]


# --------------------------------------------------------------------------------------


def all_positions_and_complete_mobility_format(record_list: List[dict]) -> list:
    """
    Convert data extracted from the database  in a format compatible with
    all positions and complete_mobility

    :param record_list: data to convert
    :return: converted data
    """
    journey_id = record_list[0]["journey_id"]
    record_list[0]["journey_id"] = uuid4()
    temp_obj = {journey_id: record_list[0]}

    for pos in range(1, len(record_list)):

        if record_list[pos]["journey_id"] in temp_obj.keys():
            journey_id = record_list[pos]["journey_id"]
            record_list[pos]["journey_id"] = temp_obj[journey_id]["journey_id"]
            temp_obj[str(uuid4())] = record_list[pos]
        else:
            journey_id = record_list[pos]["journey_id"]
            record_list[pos]["journey_id"] = uuid4()
            temp_obj[journey_id] = record_list[pos]

    return [temp_obj[key] for key in temp_obj.keys()]


# --------------------------------------------------------------------------------------


def user_data_generation(user_feed: UserFeedInternal) -> tuple:
    """
    Convert user_feed in a tuple of user_data
    """
    return (
        user_feed.journey_id,
        user_feed.source_app,
        user_feed.company_code,
        user_feed.company_trip_type,
        user_feed.distance,
        user_feed.elapsedTime,
        user_feed.endDate,
        user_feed.id,
        user_feed.mainTypeSpace,
        user_feed.mainTypeTime,
        user_feed.startDate,
        user_feed.trace_information[0].lat,
        user_feed.trace_information[0].lon,
        user_feed.trace_information[-1].lat,
        user_feed.trace_information[-1].lon,
    )


# --------------------------------------------------------------------------------------


def user_positions_generation(
    trace_information: List[PositionObject], journey_id: str
) -> List[tuple]:
    """
    Convert trace_information in a list of user_positions data
    """
    return [
        (
            journey_id,
            position.time,
            position.authenticity,
            position.lat,
            position.lon,
            position.partialDistance,
        )
        for position in trace_information
    ]


# --------------------------------------------------------------------------------------


def user_sensors_generation(
    sensors_information: List[SensorInformation], journey_id: str
) -> List[tuple]:
    """
    Convert sensors_information data in a list of user_sensors data
    """
    return [
        (journey_id, sensor.time, sensor.name, sensor.data.json())
        for sensor in sensors_information
    ]


# --------------------------------------------------------------------------------------


def user_behaviours_generation(
    behaviour_defined: Behaviour, journey_id: str, source_app: str
) -> List[tuple]:
    """
    Convert behaviour_defined in a list of user_behaviours data
    """

    def __analyze_behaviour() -> List[tuple]:
        for behaviour_and_mode in (
            (behaviour_defined.user_defined, "user_defined"),
            (behaviour_defined.tpv_defined, "tpv_defined"),
            (behaviour_defined.app_defined, "app_defined"),
        ):
            behaviour = behaviour_and_mode[0]
            mode = behaviour_and_mode[1]
            for pos in range(len(behaviour)):
                yield (
                    journey_id,
                    source_app,
                    mode,
                    pos,
                    behaviour[pos].type,
                    behaviour[pos].meters,
                    behaviour[pos].accuracy,
                    behaviour[pos].start.authenticity,
                    behaviour[pos].start.lat,
                    behaviour[pos].start.lon,
                    behaviour[pos].start.partialDistance,
                    behaviour[pos].start.time,
                    behaviour[pos].end.authenticity,
                    behaviour[pos].end.lat,
                    behaviour[pos].end.lon,
                    behaviour[pos].end.partialDistance,
                    behaviour[pos].end.time,
                )

    return [element for element in __analyze_behaviour()]


# --------------------------------------------------------------------------------------


def iot_data_generation(iot_feed: IotInput) -> tuple:
    """
    Convert IoTInput in iot_data

    :param iot_feed: data to convert
    """
    return (
        iot_feed.resultTime,
        iot_feed.Datastream["@iot.id"],
        iot_feed.FeatureOfInterest["@iot.id"],
        iot_feed.phenomenonTime,
        iot_feed.observationGEPid,
        iot_feed.result.authenticity,
        iot_feed.result.valueType,
        iot_feed.result.Position.type,
        iot_feed.result.Position.coordinate[0],
        iot_feed.result.Position.coordinate[1],
        iot_feed.result.response.value,
    )
