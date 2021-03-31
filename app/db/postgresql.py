#!/usr/bin/env python3
"""
Database utility functions
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

# Standard library
from functools import lru_cache
from typing import List

# Third party
from asyncpg import create_pool, Connection
from asyncpg.exceptions import PostgresError
from asyncpg.pool import Pool
from fastapi import status, HTTPException

# Internal
from .constants import (
    INSERT_USER_DATA_QUERY,
    INSERT_USER_SENSORS_QUERY,
    INSERT_USER_POSITIONS_QUERY,
    INSERT_USER_BEHAVIOURS_QUERY,
    INSERT_IOT_DATA_QUERY,
)

from ..config import get_database_settings
from ..internals.database import (
    partial_mobility_format,
    all_positions_and_complete_mobility_format,
    user_data_generation,
    user_positions_generation,
    user_sensors_generation,
    user_behaviours_generation,
    iot_data_generation,
)

from ..internals.logger import get_logger
from ..models.user_feed.behaviour import Behaviour
from ..models.track import RequestType
from ..models.iot_feed.iot import IotInput
from ..models.user_feed.user import UserFeedInternal

# ---------------------------------------------------------------------------------------


class DataBase:
    pool: Pool = None
    """Connection pool to the database"""

    format_user_extraction = {
        RequestType.partial_mobility: partial_mobility_format,
        RequestType.all_positions: all_positions_and_complete_mobility_format,
        RequestType.complete_mobility: all_positions_and_complete_mobility_format,
    }
    """Format methods for user extraction"""

    no_format_user_extraction_needed = {
        RequestType.stats_num_tracks,
        RequestType.stats_avg_space,
    }
    """No methods methods needed"""

    _store_single_row = {
        "user_data": INSERT_USER_DATA_QUERY,
        "iot_data": INSERT_IOT_DATA_QUERY,
    }
    """Query to insert a single row to a specific table"""

    _store_multiple_rows = {
        "user_positions": INSERT_USER_POSITIONS_QUERY,
        "user_behaviours": INSERT_USER_BEHAVIOURS_QUERY,
        "user_sensors": INSERT_USER_SENSORS_QUERY,
    }
    """Query to insert multiple rows to a specific table"""

    @classmethod
    async def connect(cls) -> None:
        """
        Create a connection pool to the database
        """
        settings = get_database_settings()

        cls.pool = await create_pool(
            user=settings.postgres_user,
            password=settings.postgres_pwd,
            database=settings.postgres_db,
            host=settings.postgres_host,
            port=settings.postgres_port,
            min_size=settings.connection_number,
            max_size=settings.connection_number
        )

    @classmethod
    async def disconnect(cls):
        """
        Disconnect from the database
        """
        await cls.pool.close()

    @classmethod
    async def store_user(cls, user_feed: UserFeedInternal) -> dict:
        """
        Store user info in the database
        :param user_feed: data to store
        """
        try:
            async with cls.pool.acquire() as conn:

                # Store User Data
                await cls.insert_single_row(
                    user_data_generation(user_feed), conn, "user_data"
                )

                # Store User Positions
                await cls.insert_multiple_rows(
                    user_positions_generation(
                        user_feed.trace_information, user_feed.journey_id
                    ),
                    conn,
                    "user_positions",
                )

                # Store User Sensors
                await cls.insert_multiple_rows(
                    user_sensors_generation(
                        user_feed.sensors_information, user_feed.journey_id
                    ),
                    conn,
                    "user_sensors",
                )

                # Store User Behaviours
                await cls.insert_multiple_rows(
                    user_behaviours_generation(
                        user_feed.behaviour, user_feed.journey_id, user_feed.source_app
                    ),
                    conn,
                    "user_behaviours",
                )

        except PostgresError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "resource": "USER",
                    "status": "Something went wrong storing the data",
                },
            )
        return {"resource": "USER", "status": "Stored"}

    @classmethod
    async def insert_single_row(
        cls, data_to_store: tuple, conn: Connection, table_name: str
    ):
        """
        Insert a single row in a specific table

        :param data_to_store: data of interests
        :param conn: a connection taken from the connection pool of the db
        :param table_name: table that will contain the data
        """
        logger = get_logger()
        try:
            await conn.execute(cls._store_single_row[table_name], *data_to_store)
        except PostgresError as error:
            await logger.warning(msg=error.as_dict())
            raise error

    @classmethod
    async def insert_multiple_rows(
        cls, data_to_store: List[tuple], conn: Connection, table_name: str
    ):
        """
        Insert a multiple rows in a specific table

        :param data_to_store: data of interests
        :param conn: a connection taken from the connection pool of the db
        :param table_name: table that will contain the data
        """
        logger = get_logger()
        try:
            await conn.executemany(cls._store_multiple_rows[table_name], data_to_store)
        except PostgresError as error:
            await logger.warning(msg=error.as_dict())
            raise error

    @classmethod
    async def update_user(cls, behaviours: Behaviour):
        """
        Update info about user behaviours

        :param behaviours: data to update
        """
        pass

    @classmethod
    async def extract_user(cls, request: RequestType, query: str) -> list:
        """
        Extract user data from the database

        :param request: type of request
        :param query: query for the extraction
        :return: list of data
        """
        logger = get_logger()
        async with cls.pool.acquire() as conn:
            try:
                result = await conn.fetch(query)
                if len(result) == 0:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={
                            "resource": "USER",
                            "status": "Info requested not found",
                        },
                    )

                if request in cls.no_format_user_extraction_needed:
                    return result

                return cls.format_user_extraction[request](
                    [dict(res) for res in result]
                )
            except PostgresError as error:
                await logger.warning(
                    msg={
                        "query": query,
                        "error": error.as_dict()
                    }
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={
                        "resource": "USER",
                        "request": request,
                        "status": "Something went wrong extracting data",
                    }
                )

    @classmethod
    async def store_iot(cls, iot_feed: IotInput):
        """
        Store iot info in the database
        :param iot_feed: data to store
        """
        try:
            async with cls.pool.acquire() as conn:
                # Store IoT Data
                await cls.insert_single_row(
                    iot_data_generation(iot_feed), conn, "iot_data"
                )

        except PostgresError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "resource": "IOT",
                    "status": "Something went wrong storing the data",
                },
            )
        return {"resource": "IOT", "status": "Stored"}

    @classmethod
    async def extract_iot(cls, observation_gep_id: str) -> dict:
        """
        Extract iot data elated to a specific identifier from the database

        :param observation_gep_id: identifier
        :return: info requested
        """

        logger = get_logger()
        async with cls.pool.acquire() as conn:
            try:
                result = await conn.fetchrow(
                    f"""SELECT * from "iot_data" WHERE observation_gep_id = '{observation_gep_id}';"""
                )
                if len(result) == 0:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={
                            "resource": "IOT",
                            "status": "Info requested not found",
                        },
                    )
                return result

            except PostgresError as error:
                # Log the error
                await logger.warning(error.as_dict())
                # Raise exception
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={
                            "resource": "IOT",
                            "request": "extract observation_gep_id associated data",
                            "status": "Something went wrong extracting data",
                    }
                )


# ---------------------------------------------------------------------------------------


@lru_cache(maxsize=1)
def get_database() -> DataBase:
    """Obtain as a singleton an instance of the database"""
    return DataBase()


# ---------------------------------------------------------------------------------------
