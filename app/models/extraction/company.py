#!/usr/bin/env python3
"""
Company model

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
from typing import Optional

# Internal
from ..model import OrjsonModel
from ..track import TypeOfTrack

# --------------------------------------------------------------------------------------------


class CompanyExtraction(OrjsonModel):
    company_code: str = ""
    """Permit the extraction of company related data"""

    company_trip_type: Optional[TypeOfTrack] = None

    _query_company_extraction: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        if self.company_trip_type:
            self._query_company_extraction = f"company_code = '{self.company_code}' AND company_trip_type = '{self.company_trip_type}'"
        else:
            self._query_company_extraction = f"company_code = '{self.company_code}'"
