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

from dataclasses import dataclass

@dataclass
class Result:
    """
    Represents the result of an HTTP request.

    Attributes:
        status_code (int): The HTTP status code.
        url (str): The requested URL.
        elapsed_time (float): The time taken for the request in seconds.
    """
    status_code: int
    url: str
    elapsed_time: float
    links: list[str]
