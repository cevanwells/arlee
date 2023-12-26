#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2023 Chris Wells <chris@arlee.org>
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Arlee - Base application/event-loop
"""

import asyncio
import pathlib
import secrets
import os
import logging

import quart

import __main__

LOGGER = logging.getLogger(__name__)

loop = asyncio.get_event_loop()


class ArleeApp(quart.Quart):
    """Subclass of quart.Quart to include our bits and bobs"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_dir = pathlib.Path(__main__.__file__).parent
        self.app_id = 'arlee'

        _token_filename = self.app_dir / "apptoken.txt"
        if os.path.isfile(_token_filename):
            self.secret_key = open(_token_filename).read()
        else:
            self.secret_key = secrets.token_hex()

            try:
                with open(_token_filename, "w") as f:
                    f.write(self.secret_key)
            except PermissionError:
                LOGGER.error(f"Could not open {_token_filename} for writing. Session permanence cannot be guaranteed!")


def construct(name, *args, **kwargs):

    global APP
    APP = ArleeApp(name, *args, **kwargs)

    import app
    app.APP = APP
    return APP
