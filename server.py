
"""
Gunicorn App main entry point

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
import os

# Third Party
from gunicorn.app.base import BaseApplication
from pydantic import BaseSettings

# Internal
from app.main import app

# -------------------------------------------------------------------------------


class GunicornSettings(BaseSettings):
    loglevel: str
    cores_number: int
    keep_alive: int
    server_port: int
    database_max_connection_number: int
    max_workers_number: int
    timeout: int

    class Config:
        env_file = ".env"


# -------------------------------------------------------------------------------


class StandaloneApplication(BaseApplication):
    """Our Gunicorn application."""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


# -------------------------------------------------------------------------------


if __name__ == "__main__":
    settings = GunicornSettings()
    options = {
        "bind": f"0.0.0.0:{settings.server_port}",
        "workers": (settings.cores_number * 2) + 1,
        "keepalive": settings.keep_alive,
        "loglevel": settings.loglevel,
        "accesslog": "-",
        "errorlog": "-",
        "timeout": settings.timeout,
        "worker_class": "uvicorn.workers.UvicornWorker",
    }
    # Regulate workers
    if options["workers"] > settings.max_workers_number:
        options["workers"] = settings.max_workers_number

    # Ensure connections to the database are set to the max value possible
    os.environ["CONNECTION_NUMBER"] = f'{int(settings.database_max_connection_number / options["workers"])}'

    StandaloneApplication(app, options).run()
