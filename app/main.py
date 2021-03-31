#!/usr/bin/env python3
"""
App main entry point

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

# Third Party
from fastapi import FastAPI

# Internal
from .db.postgresql import get_database
from .internals.logger import get_logger
from .routers import user_feed, iot

# --------------------------------------------------------------------------------------------

# Instantiate
database = get_database()
app = FastAPI(redoc_url=None, openapi_url=None)

# Include routers
app.include_router(user_feed.router)
app.include_router(iot.router)


# Configure logger
@app.on_event("startup")
async def startup_logger_and_sessions():
    get_logger()
    await database.connect()


# Shutdown logger
@app.on_event("shutdown")
async def shutdown_logger_and_sessions():
    logger = get_logger()
    await database.disconnect()
    await logger.shutdown()
