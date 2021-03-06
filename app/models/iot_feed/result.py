"""
Result models

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
from typing import Literal

# Third Party
from pydantic import Field

# Internal
from .point import Point
from ..security import Authenticity
from ..model import OrjsonModel

# --------------------------------------------------------------------------------------------


class Response(OrjsonModel):
    """
    Telemetry
    """

    value: float = Field(..., description="Value sensed", example=6.8)


class Result(OrjsonModel):
    """
    Result of the measurement
    """

    valueType: Literal["NO2"] = Field(
        ..., title="NO2", description="Type of measurement", example="NO2"
    )
    Position: Point = Field(..., description="Position where the measurement occurred")
    response: Response = Field(..., description="Measurement")


class ResultOutput(Result):
    """
    Output of the result measurement
    """

    authenticity: Authenticity = Field(
        ...,
        title="Authenticity of the data",
        description="""Value | Status        | Description
                       ------| --------------|------------------------------------------------------------
                       1     | Authentic     | Input raw data are authentic
                       -1    | Unknown       | Input raw data aren't present or impossible to authenticate 
                       0     | Not Authentic | Input raw data aren't authentic""",
        example=1,
    )
