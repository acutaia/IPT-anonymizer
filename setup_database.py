#!/usr/bin/env python3
"""
Gunicorn App main entry point

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
import asyncio

# Third Party
from asyncpg import Connection, connect
from asyncpg.exceptions import InvalidCatalogNameError
import uvloop

# Internal
from app.config import get_database_settings

# -------------------------------------------------------------------------------

uvloop.install()


class DataBase:
    """Class Used to Instantiate and setup the Database"""

    @classmethod
    async def setup(cls) -> None:
        """Create Database"""
        settings = get_database_settings()
        sys_conn = None
        try:
            sys_conn = await connect(
                user=settings.postgres_user,
                password=settings.postgres_pwd,
                database=settings.postgres_db,
                host=settings.postgres_host,
                port=settings.postgres_port,
            )
        except InvalidCatalogNameError:
            sys_conn = await connect(
                host=settings.postgres_host,
                user=settings.postgres_user,
                port=settings.postgres_port,
                password=settings.postgres_pwd,
                database="template1",
            )
            # Create Database
            await sys_conn.execute(
                f'CREATE DATABASE "{settings.postgres_db}" OWNER "{settings.postgres_user}";'
            )
            await sys_conn.close()

            sys_conn = await connect(
                host=settings.postgres_host,
                user=settings.postgres_user,
                port=settings.postgres_port,
                password=settings.postgres_pwd,
                database=settings.postgres_db,
            )
            # Create tables
            await cls.create_table_user_data(sys_conn)
            await cls.create_table_user_positions(sys_conn)
            await cls.create_table_user_sensors(sys_conn)
            await cls.create_table_user_behaviours(sys_conn)
            await cls.create_table_iot_data(sys_conn)
        finally:
            if sys_conn:
                await sys_conn.close()
            return

    @classmethod
    async def create_table_user_data(cls, sys_conn: Connection):
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

    @classmethod
    async def create_table_user_positions(cls, sys_conn: Connection):
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

    @classmethod
    async def create_table_user_sensors(cls, sys_conn: Connection):
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

    @classmethod
    async def create_table_user_behaviours(cls, sys_conn: Connection):
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

    @classmethod
    async def create_table_iot_data(cls, sys_conn: Connection):
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


# -------------------------------------------------------------------------------


if __name__ == "__main__":
    asyncio.run(DataBase.setup())
