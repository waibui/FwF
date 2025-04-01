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

class DependencyError(Exception):
    """Custom exception for dependency-related errors."""
    pass

class RequirementsFileNotFoundError(FileNotFoundError):
    """Custom exception raised when the requirements.txt file is missing."""
    pass

class ScannerError(Exception):
    """General errors for scanning."""
    pass

class InvalidURLError(ScannerError):
    """Error when URL is invalid."""
    pass
