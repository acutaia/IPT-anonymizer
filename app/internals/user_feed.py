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
from ..models.track import RequestType
from ..models.security import Authenticity
from ..models.user_feed.user import UserFeedInternal, PositionObject
from ..db.postgresql import get_database

# --------------------------------------------------------------------------------------------


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
