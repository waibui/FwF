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
from core.config import Config
from models.scan_config import ScannerConfig
from parses.validators import (
    is_valid_url, positive_timeout, positive_threads, valid_http_method, 
    valid_cookie, valid_proxy, valid_output, str2bool, valid_match_code
)

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        usage=Config.USAGE,
        epilog=Config.EPILOG,
        description="psdir - Web Path Scanner",
    )

    # === Required Arguments ===
    parser.add_argument("-u", "--url", required=True, type=is_valid_url, help="Target URL")

    # === Optional Arguments ===
    parser.add_argument("-w", "--wordlists", default=Config.DEFAULT_WORDLIST, help="Path to wordlist file(s)")
    parser.add_argument("-ua", "--user-agent", default=Config.DEFAULT_USER_AGENT, help="User-Agent string")
    parser.add_argument("-t", "--threads", type=positive_threads, default=Config.DEFAULT_THREAD, help="Number of threads")
    parser.add_argument("-to", "--timeout", type=positive_timeout, default=Config.DEFAULT_TIMEOUT, help="Connection timeout in seconds")

    # === HTTP Settings ===
    parser.add_argument("-m", "--http-method", type=valid_http_method, default="GET", help="HTTP method")
    parser.add_argument("-mc", "--match-code", type=valid_match_code, default=Config.DEFAULT_STATUS, help="Match HTTP status codes")
    parser.add_argument("--cookie", type=valid_cookie, help="Cookies for requests (e.g., 'key=value; key2=value2')")
    parser.add_argument("--proxies", type=valid_proxy, help="Proxy for requests (e.g., 'http://user:pass@proxy.com:8080')")
    parser.add_argument("-ar", "--allow-redirect", type=str2bool, default=Config.ALLOW_REDIRECT, help="Allow HTTP redirects (true/false)")

    # === Output Settings ===
    parser.add_argument("-o", "--output", type=valid_output, help="Save output to a file (.txt, .log, .json)")
    
    # === Scrape Mode  ===
    parser.add_argument("-s", "--scrape", type=str2bool, default=Config.ALLOW_SCRAPE, help="Scrape <a> tags and request their URLs")

    return parser

def parse_args() -> ScannerConfig:
    """Parse command-line arguments and return a ScannerConfig instance."""
    parser = create_parser()
    args = parser.parse_args()

    return ScannerConfig(
        url=args.url,
        wordlists=args.wordlists,
        user_agent=args.user_agent,
        threads=args.threads,
        timeout=args.timeout,
        http_method=args.http_method,
        match_code=args.match_code,
        cookie=args.cookie,
        proxies=args.proxies,
        allow_redirect=args.allow_redirect,
        output=args.output,
        scrape=args.scrape
    )
