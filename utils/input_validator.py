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

import os

def is_valid_file(file_path: str) -> bool:
    """Check if a file exists and is readable."""
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)

def is_valid_url(url: str) -> bool:
    """Basic URL validation."""
    return isinstance(url, str) and url.startswith(("http://", "https://"))
