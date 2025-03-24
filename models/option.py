# -*- coding: utf-8 -*-
#  psdir - Web Path Scanner
#  Copyright (C) 2025 waibui
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  Author: waibui

from typing import Any

option: dict[str, Any] = {
    "urls": [],
    "wordlists": "",
    "user-agent": "",
    "extensions": "",
    "remove_extensions": False,
    "thread_count": 40,
    "timeout": 10.0,
    "http_method": "GET",
    "match_code": "",
    "output_file": "",
    "quiet": False,
}