#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from src.constants import default

@dataclass
class ScanConfig:
    """
    Data class to hold configuration for a web path scanning session.
    Includes target info, request options, input settings, and output filters.
    """
    url: str = ""
    method: str = default.DEFAULT_METHOD
    timeout: float = default.DEFAULT_TIMEOUT
    follow_redirects: bool = default.DEFAULT_FOLLOW_REDIRECTS
    proxy: Optional[str] = None
    cookie: Optional[str] = None
    user_agent: str = default.DEFAULT_USERAGENT
    headers: Dict[str, str] = field(default_factory=dict)
    wordlist: str = default.DEFAULT_WORDLIST
    crawl: bool = False
    concurrency: int = 100
    retry: int = 0
    crawl: bool = False,
    crawl_depth: int = 2,
    match_codes: List[int] = field(default_factory=lambda: default.DEFAULT_STATUS_CODES)
    color: bool = default.DEFAULT_COLOR
    output: Optional[str] = None
    verbose: bool = default.DEFAULT_VERBOSE
