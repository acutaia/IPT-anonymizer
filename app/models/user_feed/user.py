"""
User models package

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

# Standard Library
from typing import List

# Third Party
from fastuuid import uuid4
from pydantic import Field

# Internal
from .behaviour import Behaviour
from .position import PositionObject
from .sensor import SensorInformation
from ..track import TypeOfTrack
from ..model import OrjsonModel

# ------------------------------------------------------------------------------------------------------


class UserFeedBase(OrjsonModel):
    """Base Model for UserFeed"""

    source_app: str = Field(..., description="Source of the data")
    journey_id: str = Field(..., description="identifier of the journey")

    behaviour: Behaviour = Field(..., description="Behaviour of the user")
    company_code: str = Field(
        ...,
        title="Company Code",
        description="ID of the Company",
        example="GP0000000004",
    )
    company_trip_type: TypeOfTrack = Field(
        ..., title="Type of track", example="private"
    )
    distance: int = Field(..., description="Overall distance covered", example=1939)
    elapsedTime: str = Field(
        ...,
        title="Elapsed Time",
        description="Overall amount of time elapsed",
        example="0:16:15",
    )
    endDate: int = Field(
        ...,
        title="Ending Date",
        description="UTC timestamp expressed in ms",
        example=1611820537461,
    )
    id: str = Field(
        ...,
        title="Device ID",
        description="Anonymous UUID_V4 assigned to the device",
        example=str(uuid4()),
    )

    mainTypeSpace: str = Field(
        ...,
        title="Main Type Space",
        description="Main type of mobility with respect to the space covered",
        example="bicycle",
    )
    mainTypeTime: str = Field(
        ...,
        title="Main Type Time",
        description="Main type of mobility with respect to time elapsed",
        example="bicycle",
    )
    startDate: int = Field(
        ...,
        title="Starting Date",
        description="UTC timestamp expressed in ms",
        example=1611820537452,
    )


class UserFeedInternal(UserFeedBase):
    """UserFeed Input model"""

    sensors_information: List[SensorInformation] = Field(
        ..., description="List of sensors information"
    )
    trace_information: List[PositionObject] = Field(
        ...,
        title="Trace Information",
        description="list of position objects, collected through the Galileo navigation system",
    )


# ------------------------------------------------------------------------------------------------------
