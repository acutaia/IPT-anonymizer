#!/usr/bin/env python3
"""
Query builder dependence

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
from fastapi import status, Body, HTTPException
from pydantic import ValidationError

# Internal
from ..models.model import OrjsonModel
from ..models.extraction.data_extraction.all_positions import AllPositions
from ..models.extraction.data_extraction.complete_mobility import CompleteMobility
from ..models.extraction.data_extraction.input import InputJSONExtraction
from ..models.extraction.data_extraction.inter_modality_space import InterModalitySpace
from ..models.extraction.data_extraction.inter_modality_time import InterModalityTime
from ..models.extraction.data_extraction.partial_mobility import PartialMobility
from ..models.extraction.data_extraction.stats_num_tracks import StatsNumTracks
from ..models.extraction.data_extraction.stats_avg_space import StatsAvgSpace
from ..models.extraction.data_extraction.stats_avg_time import StatsAvgTime
from ..models.track import RequestType


# ---------------------------------------------------------------------------------------------


class Query(OrjsonModel):
    """Query Model"""

    request: RequestType
    query: str


# noinspection PyProtectedMember
class QueryBuilder:

    query_select = {
        RequestType.partial_mobility: PartialMobility,
        RequestType.complete_mobility: CompleteMobility,
        RequestType.all_positions: AllPositions,
        RequestType.stats_num_tracks: StatsNumTracks,
        RequestType.stats_avg_space: StatsAvgSpace,
        RequestType.stats_avg_time: StatsAvgTime,
        RequestType.inter_modality_space: InterModalitySpace,
        RequestType.inter_modality_time: InterModalityTime,
    }
    """Request associated to a Model"""

    def __call__(self, extraction: InputJSONExtraction = Body(...)) -> Query:
        """Called by the Depends class from FastApi to inspect InputJSONExtraction Body"""
        try:
            query = Query.construct(
                **{
                    "request": extraction.request,
                    "query": self.query_select[extraction.request]
                    .parse_obj(extraction.dict())
                    ._query_select,
                }
            )
        except ValidationError as err:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=err.errors()
            )
        return query
