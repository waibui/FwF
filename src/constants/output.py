#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

from enum import Enum, auto

class OutputFormat(Enum):
    """Output enum"""
    TEXT = "text"
    JSON = "json"
    CSV = "csv"
    HTML = "html"