#!/usr/bin/env python3
"""
IoTFeed router package

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
from fastapi import APIRouter, Body
from fastapi.responses import ORJSONResponse

# Internal
from ..internals.iot_feed import store_iot_feed, extract_iot_info
from ..models.extraction.data_extraction.iot import ExtractIoT
from ..models.iot_feed.iot import IotInput

# --------------------------------------------------------------------------------------------

# Instantiate router
router = APIRouter(prefix="/ipt_anonymizer/api/v1/iot", tags=["IoT"])


@router.post(
    "/store",
    response_class=ORJSONResponse,
    summary="Store IoT data",
    response_description="Resource Stored",
)
async def store(iot_feed: IotInput = Body(...)):
    """
    This endpoint collects iot information and store them in the database
    """
    return await store_iot_feed(iot_feed)


@router.post(
    "/extract",
    response_class=ORJSONResponse,
    summary="Extract IoT data",
    response_description="Data requested",
)
async def extract(extraction: ExtractIoT = Body(...)):
    """
    This endpoints extracts user info
    """
    return await extract_iot_info(extraction.observationGEPid)
