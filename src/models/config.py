#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class ScanConfig:
    """Configuration object for FwF - Fast Web Fuzzer."""
    # HTTP Options
    url: Optional[str] = None
    method: str = "GET"
    timeout: int = 10
    follow_redirects: bool = False
    cookie: Optional[str] = None
    
    # General Options
    concurrency: int = 10
    retry: int = 0
    crawl: bool = False
    crawl_depth: int = 2
    
    # Input Options
    wordlist: str = "wordlists/default.txt"
    user_agent: str = "wordlists/user-agents.txt"
    
    # Output Options
    color: bool = False
    verbose: bool = False
    output: Optional[str] = None
    
    # Filter Options
    match_codes: List[int] = field(default_factory=lambda: [
        200, 201, 202, 203, 204, 301, 302, 307, 308, 401, 403
    ])
