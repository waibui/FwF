#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

import aiohttp

from src.models.result import ScanResult

async def process_presponse(url: str, response: aiohttp.ClientResponse) -> ScanResult:
    """Process a successful HTTP response"""
    return 