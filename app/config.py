#!/usr/bin/env python3
"""
App Settings

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

# Standard Library
from functools import lru_cache

# Third Party
from pydantic import BaseSettings

# -------------------------------------------------------------------


class LbsSettings(BaseSettings):
    get_route_url: str
    post_route_url: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_lbs_settings() -> LbsSettings:
    return LbsSettings()


# -------------------------------------------------------------------


class DatabaseSettings(BaseSettings):
    postgres_user: str
    postgres_pwd: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    connection_number: int

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


# -------------------------------------------------------------------
