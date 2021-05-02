#!python
#cython: language_level=3

"""
Simplified Reversed Haversine function

:author: Angelo Cutaia
:copyright: Copyright 2021, Angelo Cutaia
:version: 1.0.0
..
    Copyright 2021 Angelo Cutaia
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
# Standard c++ library
from libc.math cimport cos, sqrt, pi
from typing import Tuple


# -------------------------------------------------------------------------------------------

# CONSTANTS
cdef int R

R = 6378137

# -------------------------------------------------------------------------------------------


def reversed_haversine(double lat, double lon, int start_radius) -> Tuple[float, float, float, float]:
    cdef double dn, de, dLat, dLon, lat_input, lon_input

    lat_input = lat
    lon_input = lon
    dn = start_radius / sqrt(2)
    de = dn
    dLat = dn / R
    dLon = de / (R * cos(pi * lat_input / 180))

    return lat_input - dLat * 180 / pi, lat_input + dLat * 180 / pi, lon_input - dLon * 180 / pi, lon_input + dLon * 180 / pi

# -------------------------------------------------------------------------------------------