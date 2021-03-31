#!/usr/bin/env python3
"""
Test app

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

# Test
from fastapi.testclient import TestClient

# Third Party
from fastapi import status

# Internal
from app.main import app
from .constants import IoT_INPUT_DATA
from .logger import disable_logger

# ---------------------------------------------------------------------------------------------


def clear_test():
    """Clear tests"""
    disable_logger()


class TestIoT:
    """Test IoT router"""

    def test_store(self):
        """Test the behaviour of store IoT data"""

        clear_test()

        with TestClient(app) as client:
            # Store data
            response = client.post(
                "http://localhost/ipt_anonymizer/api/v1/iot/store",
                json=IoT_INPUT_DATA
            )
            assert response.status_code == status.HTTP_200_OK

            # try to store again the same data
            response = client.post(
                "http://localhost/ipt_anonymizer/api/v1/iot/store",
                json=IoT_INPUT_DATA
            )
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_extract(self):
        """Test the behaviour of store IoT data"""
        clear_test()

        with TestClient(app) as client:
            # Extract data
            response = client.post(
                "http://localhost/ipt_anonymizer/api/v1/iot/extract",
                json={
                    "observationGEPid": IoT_INPUT_DATA["observationGEPid"]
                }
            )
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == {
                                        "result_time": IoT_INPUT_DATA["resultTime"],
                                        "datastream": IoT_INPUT_DATA["Datastream"]["@iot.id"],
                                        "feature_of_interest": IoT_INPUT_DATA["FeatureOfInterest"]["@iot.id"],
                                        "phenomenon_time": IoT_INPUT_DATA["phenomenonTime"],
                                        "observation_gep_id": IoT_INPUT_DATA["observationGEPid"],
                                        "result_auth": IoT_INPUT_DATA["result"]["authenticity"],
                                        "value_type": IoT_INPUT_DATA["result"]["valueType"],
                                        "position_type": IoT_INPUT_DATA["result"]["Position"]["type"],
                                        "position_lat": IoT_INPUT_DATA["result"]["Position"]["coordinate"][0],
                                        "position_lon": IoT_INPUT_DATA["result"]["Position"]["coordinate"][1],
                                        "response_value": IoT_INPUT_DATA["result"]["response"]["value"]
                                    }

            # try to store again the same data
            response = client.post(
                "http://localhost/ipt_anonymizer/api/v1/iot/extract",
                json={
                    "observationGEPid": "FAKE_NOT_FOUND"
                }
            )
            assert response.status_code == status.HTTP_404_NOT_FOUND
