#!/usr/bin/env python3
"""
IoT internals package

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

# Internal
from ..db.postgresql import get_database
from ..models.iot_feed.iot import IotInput

# --------------------------------------------------------------------------------------------


async def store_iot_feed(iot_feed: IotInput) -> dict:
    """
    Store UserFeed data in the anonymizer

    :param iot_feed: data to store
    """
    database = get_database()
    return await database.store_iot(iot_feed)


async def extract_iot_info(observation_gep_id: str) -> dict:
    """
    Extract ser info from the database

    :param observation_gep_id: iot data identifier
    """
    database = get_database()
    return await database.extract_iot(observation_gep_id)
