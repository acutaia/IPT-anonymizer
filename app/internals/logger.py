"""
Logger package

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
from functools import lru_cache

# Third Party
from aiologger.loggers.json import JsonLogger, LogLevel

# Internal
from ..config import LoggerSettings


@lru_cache(maxsize=1)
def get_logger() -> JsonLogger:
    """Instantiate app logger"""

    return JsonLogger.with_default_handlers(
        name="IPT-anonymizer",
        serializer_kwargs={"indent": 4},
        level=getattr(LogLevel, LoggerSettings().loglevel, "DEBUG"),
    )
