#!/usr/bin/env python3
"""
UserFeed router package

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
from fastapi import APIRouter, Body, Depends
from fastapi.responses import ORJSONResponse

# Internal
from ..dependencies.query_builder import QueryBuilder, Query
from ..internals.user_feed import store_user_feed, extract_user_info, extract_statistics
from ..models.user_feed.user import UserFeedInternal
from ..models.track import RequestType

# --------------------------------------------------------------------------------------------

# Instantiate
router = APIRouter(prefix="/ipt_anonymizer/api/v1/user", tags=["User"])
query_builder = QueryBuilder()


@router.post(
    "/store",
    response_class=ORJSONResponse,
    summary="Store User data",
    response_description="Resource Stored",
)
async def store(user_feed: UserFeedInternal = Body(...)):
    """
    This endpoint anonymize user information and store them in the database
    """
    return await store_user_feed(user_feed)


@router.post(
    "/extract",
    response_class=ORJSONResponse,
    summary="Extract User data",
    response_description="Data requested",
)
async def extract(extraction: Query = Depends(query_builder)):
    """
    This endpoints extracts user info
    """
    if extraction.request in (
        RequestType.inter_modality_space,
        RequestType.inter_modality_time,
    ):
        return await extract_statistics(extraction.request, extraction.query)

    return await extract_user_info(extraction.request, extraction.query)
