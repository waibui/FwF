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

import argparse
from config.settings import Setting
from utils.validators import (
    is_valid_url, positive_timeout, positive_threads, positive_rate_limit, valid_http_method, 
    valid_cookie, valid_proxy, valid_output, str2bool, valid_match_code
)

def parse_args() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        usage=Setting.USAGE,
        epilog=Setting.EPILOG,
        description="psdir - Web Path Scanner",
    )

    # General settings
    parser.add_argument("-u", "--url", required=True, type=is_valid_url, help="Target URL")
    parser.add_argument("-w", "--wordlist", default=Setting.DEFAULT_WORDLIST, help="Path to wordlist file(s)")
    parser.add_argument("-ua", "--user-agent", help="User-Agent string")
    parser.add_argument("-c", "--concurrency", type=positive_threads, default=Setting.DEFAULT_THREAD, help="Number of threads")
    parser.add_argument("-t", "--timeout", type=positive_timeout, default=Setting.DEFAULT_TIMEOUT, help="Connection timeout in seconds")
    parser.add_argument("-m", "--http-method", type=valid_http_method, default="GET", help="HTTP method")
    parser.add_argument("-mc", "--match-code", type=valid_match_code, default=Setting.DEFAULT_STATUS, help="Match HTTP status codes")

    # Optional HTTP configurations
    http_group = parser.add_argument_group("HTTP Settings")
    http_group.add_argument("--cookie", type=valid_cookie, help="Cookies for requests (e.g., 'key=value; key2=value2')")
    http_group.add_argument("--proxies", type=valid_proxy, help="Proxy for requests (e.g., 'http://user:pass@proxy.com:8080')")
    http_group.add_argument("-ar", "--allow-redirect", action="store_true", default=Setting.ALLOW_REDIRECT, help="Allow HTTP redirects (true/false)")
    http_group.add_argument("-s", "--scrape", action="store_true", default=Setting.ALLOW_SCRAPE, help="Scrape <a> tags and request their URLs")
    http_group.add_argument("-rl","--rate-limit", type=positive_rate_limit, help="Limit requests per second (default: unlimited)")

    # Output options
    output_group = parser.add_argument_group("Output Settings")
    output_group.add_argument("-o", "--output", type=valid_output, help="Save output to a file (.txt, .log, .json)")

    return parser.parse_args()