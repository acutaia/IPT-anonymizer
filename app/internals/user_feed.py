#!/usr/bin/env python3
"""
UserFeed utilities package

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
import asyncio
import time

# Internal
from .lbs import get_lbs_route, post_lbs_route
from ..models.track import RequestType
from ..models.security import Authenticity
from ..models.user_feed.user import UserFeedInternal, PositionObject
from ..db.postgresql import get_database

# --------------------------------------------------------------------------------------------


def anonymize(user_feed: UserFeedInternal) -> UserFeedInternal:
    """
    Add cryptography to anonymize data and nodes

    :param user_feed: Data to anonymize
    :return: Anonymized user_feed
    """
    fake_position = PositionObject.construct(
        **{
            "authenticity": Authenticity.unknown,
            "lat": 0.0,
            "lon": 0.0,
            "partialDistance": 0,
            "time": int(time.time() * 1000),
        }
    )
    # TODO: Add algorithm to generate fake positions coherent with the real positions
    #  and add them at the beginning and end fo de trace_information list
    #  after that we'll anonymize the first user defined behaviour start position and
    #  the last user_ defined end position with fake position
    user_feed.trace_information.insert(0, fake_position)
    user_feed.trace_information.append(fake_position)
    user_feed.behaviour.user_defined[0].start = fake_position
    user_feed.behaviour.user_defined[-1].end = fake_position

    return user_feed


async def store_user_feed(user_feed: UserFeedInternal) -> dict:
    """
    Store UserFeed data in the anonymizer

    :param user_feed: data to store
    """
    database = get_database()
    return await database.store_user(user_feed)


async def extract_user_info(request: RequestType, query: str) -> list:
    """
    Extract user info from the database

    :param request: requested info
    :param query: database query
    """
    database = get_database()
    return await database.extract_user(request, query)


async def extract_statistics(request: RequestType, conditions: str) -> list:
    """
    Extract statistics from the database

    :param request: requested statistics
    :param conditions: requested conditions
    """
    database = get_database()
    return await database.extract_mobility_statistics(request, conditions)


async def journey_analysis(user_feed: UserFeedInternal) -> None:
    # TODO:  Update entry in the db using user_feed.journey_id
    try:
        journey_id = await post_lbs_route(user_feed.dict())
        # Wait some time before asking the result
        await asyncio.sleep(10)
        behaviour = await get_lbs_route(journey_id)
        database = get_database()
        await database.update_user(behaviour)
    finally:
        return
