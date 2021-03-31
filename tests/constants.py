#!/usr/bin/env python3
"""
Constants for testing the app

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
import uuid

# ---------------------------------------------------------------------------------------------


IoT_INPUT_DATA = {

    "resultTime": "2021-01-28T07:40:19.151000+00:00",
    "Datastream": {
        "@iot.id": 5
    },
    "FeatureOfInterest": {
        "@iot.id": 1
    },
    "phenomenonTime": "2021-01-28T07:40:19.151000+00:00",
    "result": {
        "authenticity": 1,
        "valueType": "NO2",
        "Position": {
          "type": "Point",
          "coordinate": [
            59.338747,
            18.067612
          ]
        },
        "response": {
          "value": 6.8
        }
    },
    "observationGEPid": str(uuid.uuid4())
}