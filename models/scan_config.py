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
from typing import Optional

@dataclass
class ScannerConfig:
    """
    Data class to store configuration settings for the web path scanner.

    Attributes:
        url (str): The target URL to scan.
        wordlists (str): Path to the wordlist file(s) used for scanning.
        user_agent (str): The User-Agent string for HTTP requests.
        threads (int): Number of threads to use for concurrent requests.
        timeout (float): Timeout for HTTP requests in seconds.
        http_method (str): HTTP method to use (e.g., GET, POST).
        match_code (str): HTTP status code(s) to match.
        cookie (Optional[str]): Cookie string for HTTP requests, if any.
        proxies (Optional[str]): Proxy URL for routing requests, if any.
        allow_redirect (bool): Whether to allow HTTP redirects.
        output (Optional[str]): File path to save the scan results, if specified.
    """
    url: str
    wordlists: str
    user_agent: str
    threads: int
    timeout: float
    http_method: str
    match_code: str
    cookie: Optional[str]
    proxies: Optional[str]
    allow_redirect: bool
    output: Optional[str]
    scrape: bool
