"""
Constants for testing the app

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

# Third Party
from fastuuid import uuid4

# ---------------------------------------------------------------------------------------------


IoT_INPUT_DATA = {
    "resultTime": "2021-01-28T07:40:19.151000+00:00",
    "Datastream": {"@iot.id": 5},
    "FeatureOfInterest": {"@iot.id": 1},
    "phenomenonTime": "2021-01-28T07:40:19.151000+00:00",
    "result": {
        "authenticity": 1,
        "valueType": "NO2",
        "Position": {"type": "Point", "coordinate": [59.338747, 18.067612]},
        "response": {"value": 6.8},
    },
    "observationGEPid": str(uuid4()),
}

# ---------------------------------------------------------------------------------------------

USER_INPUT_DATA = {
    "source_app": "travis",
    "behaviour": {
        "app_defined": [],
        "tpv_defined": [],
        "user_defined": [
            {
                "end": {
                    "authenticity": -1,
                    "lat": 45.0704191,
                    "lon": 7.4716152,
                    "partialDistance": 20,
                    "time": 1611819719151,
                },
                "meters": 1939,
                "start": {
                    "authenticity": -1,
                    "lat": 45.0704091,
                    "lon": 7.4716152,
                    "partialDistance": 10,
                    "time": 1611819619151,
                },
                "type": "bicycle",
            },
            {
                "end": {
                    "authenticity": -1,
                    "lat": 45.0704291,
                    "lon": 7.4716152,
                    "partialDistance": 50,
                    "time": 1611820019151,
                },
                "meters": 1939,
                "start": {
                    "authenticity": -1,
                    "lat": 45.0704291,
                    "lon": 7.4716152,
                    "partialDistance": 30,
                    "time": 1611819819151,
                },
                "type": "walk",
            },
        ],
    },
    "company_code": str(uuid4()),
    "company_trip_type": "",
    "distance": 1939,
    "elapsedTime": "0:16:15",
    "endDate": 1611820019151,
    "id": str(uuid4()),
    "journey_id": str(uuid4()),
    "mainTypeSpace": "bicycle",
    "mainTypeTime": "bicycle",
    "sensors_information": [
        {
            "data": {"x": 0.0, "y": 1.0, "z": 8.0},
            "name": "accellerometer",
            "time": 1611819561195,
        }
    ],
    "startDate": 1611819619151,
    "trace_information": [
        {
            "authenticity": -1,
            "lat": 45.0704091,
            "lon": 7.4716152,
            "partialDistance": 10,
            "time": 1611819619151,
        },
        {
            "authenticity": -1,
            "lat": 45.0704191,
            "lon": 7.4716152,
            "partialDistance": 20,
            "time": 1611819719151,
        },
        {
            "authenticity": -1,
            "lat": 45.0704291,
            "lon": 7.4716152,
            "partialDistance": 30,
            "time": 1611819819151,
        },
        {
            "authenticity": -1,
            "lat": 45.0704291,
            "lon": 7.4716152,
            "partialDistance": 40,
            "time": 1611819919151,
        },
        {
            "authenticity": -1,
            "lat": 45.0704291,
            "lon": 7.4716152,
            "partialDistance": 50,
            "time": 1611820019151,
        },
    ],
}
