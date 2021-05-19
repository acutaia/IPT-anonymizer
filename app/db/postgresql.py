#!/usr/bin/env python3
"""
Database utility functions

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

# Standard library
from functools import lru_cache
from typing import List

# Third party
from asyncpg import create_pool, connect, Connection
from asyncpg.exceptions import (
    PostgresError,
    DuplicateDatabaseError,
    InvalidCatalogNameError,
)
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
        RequestType.stats_avg_time,
    }
    """No methods for format needed"""

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

        try:
            # Try to create a connection pool to the Database
            cls.pool = await create_pool(
                user=settings.postgres_user,
                password=settings.postgres_pwd,
                database=settings.postgres_db,
                host=settings.postgres_host,
                port=settings.postgres_port,
                max_size=settings.connection_number,
            )

        except InvalidCatalogNameError:
            # Flag that indicates if the tables must be created
            create_tables = True
            # Connect to Database template
            sys_conn = await connect(
                host=settings.postgres_host,
                user=settings.postgres_user,
                port=settings.postgres_port,
                password=settings.postgres_pwd,
                database="template1",
            )
            try:
                # Create Database
                await sys_conn.execute(
                    f'CREATE DATABASE "{settings.postgres_db}" OWNER "{settings.postgres_user}";'
                )
            except DuplicateDatabaseError:
                # Another process created the database so set create_tables to False
                create_tables = False

            finally:
                # Disconnect from database template
                await sys_conn.close()

            # Create a connection pool to the Database
            cls.pool = await create_pool(
                user=settings.postgres_user,
                password=settings.postgres_pwd,
                database=settings.postgres_db,
                host=settings.postgres_host,
                port=settings.postgres_port,
                max_size=settings.connection_number,
            )

            # Check if the tables must be created
            if create_tables:
                async with cls.pool.acquire() as connection:
                    # Create tables
                    await cls.__create_table_user_data(connection)
                    await cls.__create_table_user_positions(connection)
                    await cls.__create_table_user_sensors(connection)
                    await cls.__create_table_user_behaviours(connection)
                    await cls.__create_table_iot_data(connection)

    @staticmethod
    async def __create_table_user_data(sys_conn: Connection):
        """
        Create a table to store user data

        :param sys_conn: connection to the database
        """
        await sys_conn.execute(
            """
               CREATE TABLE IF NOT EXISTS "user_data" (
               journey_id text,
               source_app text,
               company_code text,
               PRIMARY KEY (journey_id),
               company_trip_type text,
               distance integer,
               elapsed_time text,
               end_date bigint,
               id text,
               main_type_space text,
               main_type_time text,
               start_date bigint,
               start_lat float,
               start_lon float,
               end_lat float,
               end_lon float
               );
                """
        )

        await sys_conn.execute(
            """CREATE INDEX user_data_index_b_tree on "user_data" (
            distance,
            elapsed_time,
            start_lat,
            start_lon,
            end_lat,
            end_lon,
            start_date,
            end_date);"""
        )
        for hash_key in (
            "source_app",
            "company_code",
            "company_trip_type",
            "main_type_space",
            "main_type_time",
        ):
            await sys_conn.execute(
                f"""CREATE INDEX user_data_{hash_key} on "user_data" USING hash ({hash_key});"""
            )

    @staticmethod
    async def __create_table_user_positions(sys_conn: Connection):
        """
        Create a table to store user positions

        :param sys_conn: connection to the database
        """
        await sys_conn.execute(
            """CREATE TABLE IF NOT EXISTS "user_positions" (
               journey_id text,
               time bigint,
               PRIMARY KEY (journey_id, time),
               authenticity integer,
               lat float,
               lon float,
               partial_distance integer
               );
                """
        )

        await sys_conn.execute(
            """CREATE INDEX user_positions_index_b_tree on "user_positions" (
            time,
            lat,
            lon,
            partial_distance);"""
        )

    @staticmethod
    async def __create_table_user_sensors(sys_conn: Connection):
        """
        Create a table to store user sensors

        :param sys_conn: connection to the database
        """
        await sys_conn.execute(
            """
               CREATE TABLE IF NOT EXISTS "user_sensors" (
               journey_id text,
               time bigint,
               name text,
               data jsonb,
               PRIMARY KEY (journey_id, time, name)
               );
                """
        )

    @staticmethod
    async def __create_table_user_behaviours(sys_conn: Connection):
        """
        Create a table to store user behaviours

        :param sys_conn: connection to the database
        """
        await sys_conn.execute(
            """
               CREATE TABLE IF NOT EXISTS "user_behaviours" (
               journey_id text,
               source_app text,
               mode text,
               pos integer,
               type text,
               PRIMARY KEY (journey_id, mode, pos),
               meters integer,
               accuracy float,
               start_auth integer,
               start_lat float,
               start_lon float,
               start_partial_distance integer,
               start_time bigint,
               end_auth float,
               end_lat float,
               end_lon float,
               end_partial_distance integer,
               end_time bigint 
               );
                """
        )

        await sys_conn.execute(
            """CREATE INDEX user_behaviours_index_b_tree on "user_behaviours" (
            meters,
            start_lat,
            start_lon,
            end_lat,
            end_lon,
            start_time,
            end_time);"""
        )

        for hash_key in ("source_app", "mode", "type"):
            await sys_conn.execute(
                f"""CREATE INDEX user_behaviours_{hash_key} on "user_behaviours" USING hash ({hash_key});"""
            )

    @staticmethod
    async def __create_table_iot_data(sys_conn: Connection):
        """
        Create a table to store iot data

        :param sys_conn: connection to the database
        """
        await sys_conn.execute(
            """
               CREATE TABLE IF NOT EXISTS "iot_data" (
               result_time timestamp with time zone,
               datastream int,
               feature_of_interest int,
               phenomenon_time timestamp with time zone,
               observation_gep_id text,
               result_auth integer,
               value_type text,
               position_type text,
               position_lat float,
               position_lon float,
               response_value float,
               PRIMARY KEY (observation_gep_id)
               );
                """
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
                await logger.warning(msg={"query": query, "error": error.as_dict()})
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={
                        "resource": "USER",
                        "request": request,
                        "status": "Something went wrong extracting data",
                    },
                )

    @classmethod
    async def extract_mobility_statistics(
        cls, request: RequestType, conditions: str
    ) -> list:
        """
        Extract mobility statistics from the database

        :param request: type of statistics
        :param conditions: requested conditions
        :return: list of data
        """
        if request == RequestType.inter_modality_space:
            return await cls.extract_space_statistics(conditions)
        else:
            return await cls.extract_time_statistics(conditions)

    @classmethod
    async def extract_space_statistics(cls, conditions: str) -> list:
        """
        Extract space statistics from the database

        :param conditions: requested conditions
        :return: list of data
        """
        logger = get_logger()
        async with cls.pool.acquire() as conn:
            try:
                # generate first part of the first row
                result_1 = await conn.fetch(
                    f"""Select avg(aggregated.n_mobility_type),sum(aggregated.n_mobility_type)
                    from (Select count(journey_id) as n_mobility_type
                    from user_behaviours,
                    (select journey_id as x
                    from user_data
                    where distance < 5000 and {conditions} ) as nested
                    where journey_id = nested.x group by journey_id) as aggregated;"""
                )
                # The list of data will always have length 1
                result_1 = dict(result_1[0])

                # Check if there is at least one mobility
                if result_1["sum"] is None:
                    result_1["avg"] = 0
                    result_1_2 = []

                else:
                    # generate second part of the first row
                    result_1_2 = await conn.fetch(
                        f"""Select distinct(aggregated.type),((sum(aggregated.n_mobility_type)/{int(result_1["sum"])})*100) as perc
                        from
                        (
                        Select count(journey_id) as n_mobility_type, type
                        from user_behaviours,
                        (
                        select journey_id as x
                        from user_data
                        where distance < 5000 and {conditions} ) as nested
                        where journey_id = nested.x group by type) as aggregated
                        group by aggregated.type;"""
                    )

                # first row complete
                first_row = {
                    "distance": "< 5 Km",
                    "mob_type_per_journey": result_1["avg"],
                    "mob_type": result_1_2,
                }

                # generate first part of the second row
                result_2 = await conn.fetch(
                    f"""Select avg(aggregated.n_mobility_type),sum(aggregated.n_mobility_type)
                    from (Select count(journey_id) as n_mobility_type
                    from user_behaviours,
                    (select journey_id as x
                    from user_data
                    where distance BETWEEN 10000 AND 5000 and {conditions} ) as nested
                    where journey_id = nested.x group by journey_id) as aggregated;"""
                )
                # The list of data will always have length 1
                result_2 = dict(result_2[0])

                # Check if there is at least one mobility
                if result_2["sum"] is None:
                    result_2["avg"] = 0
                    result_2_2 = []

                else:
                    # generate second part of the second row
                    result_2_2 = await conn.fetch(
                        f"""Select distinct(aggregated.type),((sum(aggregated.n_mobility_type)/{int(result_2["sum"])})*100) as perc
                        from
                        (
                        Select count(journey_id) as n_mobility_type, type
                        from user_behaviours,
                        (
                        select journey_id as x
                        from user_data
                        where distance BETWEEN 10000 AND 5000 and {conditions} ) as nested
                        where journey_id = nested.x group by type) as aggregated
                        group by aggregated.type;"""
                    )

                # second row complete
                second_row = {
                    "distance": "5 Km - 10 Km",
                    "mob_type_per_journey": result_2["avg"],
                    "mob_type": result_2_2,
                }

                # generate first part of the third row
                result_3 = await conn.fetch(
                    f"""Select avg(aggregated.n_mobility_type),sum(aggregated.n_mobility_type)
                    from (Select count(journey_id) as n_mobility_type
                    from user_behaviours,
                    (select journey_id as x
                    from user_data
                    where distance > 10000 and {conditions} ) as nested
                    where journey_id = nested.x group by journey_id) as aggregated;"""
                )
                # The list of data will always have length 1
                result_3 = dict(result_3[0])

                # Check if there is at least one mobility
                if result_3["sum"] is None:
                    result_3["avg"] = 0
                    result_3_2 = []

                else:
                    # generate second part of the third row
                    result_3_2 = await conn.fetch(
                        f"""Select distinct(aggregated.type),
                        ((sum(aggregated.n_mobility_type)/{int(result_3["sum"])})*100) as perc
                        from
                        (
                        Select count(journey_id) as n_mobility_type, type
                        from user_behaviours,
                        (
                        select journey_id as x
                        from user_data
                        where distance > 10000 and {conditions} ) as nested
                        where journey_id = nested.x group by type) as aggregated
                        group by aggregated.type;"""
                    )

                # third row complete
                third_row = {
                    "distance": "> 10 Km",
                    "mob_type_per_journey": result_3["avg"],
                    "mob_type": result_3_2,
                }

                return [first_row, second_row, third_row]

            except PostgresError as error:
                await logger.warning(msg=error.as_dict())
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={
                        "resource": "USER",
                        "request": RequestType.inter_modality_space,
                        "status": "Something went wrong extracting data",
                    },
                )

    @classmethod
    async def extract_time_statistics(cls, conditions: str) -> list:
        """
        Extract time statistics from the database

        :param conditions: requested conditions
        :return: list of data
        """
        logger = get_logger()
        async with cls.pool.acquire() as conn:
            try:
                # generate first part of the first row
                result_1 = await conn.fetch(
                    f"""Select avg(aggregated.n_mobility_type),sum(aggregated.n_mobility_type)
                    from (Select count(journey_id) as n_mobility_type
                    from user_behaviours,
                    (select journey_id as x from user_data
                    where elapsed_time::interval < '15 minutes'::interval and {conditions} ) as nested
                    where journey_id = nested.x group by journey_id) as aggregated;"""
                )
                # The list of data will always have length 1
                result_1 = dict(result_1[0])

                # Check if there is at least one mobility
                if result_1["sum"] is None:
                    result_1["avg"] = 0
                    result_1_2 = []

                else:
                    # generate second part of the first row
                    result_1_2 = await conn.fetch(
                        f"""Select distinct(aggregated.type),((sum(aggregated.n_mobility_type)/{result_1["sum"]})*100) as perc
                        from (Select count(journey_id) as n_mobility_type, type 
                        from user_behaviours,
                        ( select journey_id as x from user_data where elapsed_time::interval < '15 minutes'::interval 
                        and {conditions} ) as nested
                        where journey_id = nested.x group by type) as aggregated
                        group by aggregated.type;"""
                    )

                # first row complete
                first_row = {
                    "time": "< 15 min",
                    "mob_type_per_journey": result_1["avg"],
                    "mob_type": result_1_2,
                }

                # generate first part of the second row
                result_2 = await conn.fetch(
                    f"""Select avg(aggregated.n_mobility_type),sum(aggregated.n_mobility_type)
                    from
                    (Select count(journey_id) as n_mobility_type
                    from user_behaviours,
                    (select journey_id as x
                    from user_data
                    where elapsed_time::interval <= '30 minutes'::interval and elapsed_time::interval >= '15 minutes'::interval
                    and {conditions} ) as nested
                    where journey_id = nested.x group by journey_id) as aggregated;"""
                )
                # The list of data will always have length 1
                result_2 = dict(result_2[0])

                # Check if there is at least one mobility
                if result_2["sum"] is None:
                    result_2["avg"] = 0
                    result_2_2 = []

                else:
                    # generate second part of the second row
                    result_2_2 = await conn.fetch(
                        f"""Select distinct(aggregated.type),((sum(aggregated.n_mobility_type)/{int(result_2["sum"])})*100) as perc
                            from
                            (
                            Select count(journey_id) as n_mobility_type, type
                            from user_behaviours,
                            (
                            select journey_id as x
                            from user_data
                            where elapsed_time::interval <= '30 minutes'::interval and elapsed_time::interval >= '15 minutes'::interval
                            and {conditions} ) as nested
                            where journey_id = nested.x group by type) as aggregated group by aggregated.type;"""
                    )

                # second row complete
                second_row = {
                    "time": "15 - 30 min",
                    "mob_type_per_journey": result_2["avg"],
                    "mob_type": result_2_2,
                }

                # generate first part of the third row
                result_3 = await conn.fetch(
                    f"""Select avg(aggregated.n_mobility_type),sum(aggregated.n_mobility_type)
                    from (Select count(journey_id) as n_mobility_type
                    from user_behaviours,
                    (select journey_id as x from user_data
                    where elapsed_time::interval > '30 minutes'::interval and {conditions} ) as nested
                    where journey_id = nested.x group by journey_id) as aggregated;"""
                )
                # The list of data will always have length 1
                result_3 = dict(result_3[0])

                # Check if there is at least one mobility
                if result_3["sum"] is None:
                    result_3["avg"] = 0
                    result_3_2 = []

                else:
                    # generate second part of the third row
                    result_3_2 = await conn.fetch(
                        f"""Select distinct(aggregated.type),((sum(aggregated.n_mobility_type)/{result_1["sum"]})*100) as perc
                        from 
                        (Select count(journey_id) as n_mobility_type, type
                        from user_behaviours,
                        (select journey_id as x
                        from user_data
                        where elapsed_time::interval > '30 minutes'::interval and {conditions}
                        ) as nested
                        where journey_id = nested.x group by type) as aggregated
                        group by aggregated.type;"""
                    )

                # third row complete
                third_row = {
                    "time": "> 30 min",
                    "mob_type_per_journey": result_3["avg"],
                    "mob_type": result_3_2,
                }

                return [first_row, second_row, third_row]

            except PostgresError as error:
                await logger.warning(msg=error.as_dict())
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={
                        "resource": "USER",
                        "request": RequestType.inter_modality_time,
                        "status": "Something went wrong extracting data",
                    },
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
                if result is None:
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
                    },
                )


# ---------------------------------------------------------------------------------------


@lru_cache(maxsize=1)
def get_database() -> DataBase:
    """Obtain as a singleton an instance of the database"""
    return DataBase()


# ---------------------------------------------------------------------------------------
