# -*- coding: utf-8 -*-
#  psdir - Web Path Scanner
#  Copyright (c) 2025 waibui
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import argparse
from core.config import Config
from utils.validators import (
    is_valid_url, positive_timeout, positive_threads, positive_rate_limit, valid_http_method, 
    valid_cookie, valid_proxy, valid_output, str2bool, valid_match_code
)

def parse_args() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        usage=Config.USAGE,
        epilog=Config.EPILOG,
        description="psdir - Web Path Scanner",
    )

    # General Configs
    parser.add_argument("-u", "--url", required=True, type=is_valid_url, help="Target URL")
    parser.add_argument("-w", "--wordlist", default=Config.DEFAULT_WORDLIST, help="Path to wordlist file")
    parser.add_argument("-ua", "--user-agent", help="Path to user-agent file")
    parser.add_argument("-c", "--concurrency", type=positive_threads, default=Config.DEFAULT_THREAD, help="Number of threads")
    parser.add_argument("-t", "--timeout", type=positive_timeout, default=Config.DEFAULT_TIMEOUT, help="Connection timeout in seconds")
    parser.add_argument("-m", "--http-method", type=valid_http_method, default="GET", help="HTTP method")
    parser.add_argument("-mc", "--match-code", type=valid_match_code, default=Config.DEFAULT_STATUS, help="Match HTTP status codes")

    # Optional HTTP configurations
    http_group = parser.add_argument_group("HTTP Configs")
    http_group.add_argument("--cookie", type=valid_cookie, help="Cookies for requests (e.g., 'key=value;key2=value2')")
    http_group.add_argument("--proxies", type=valid_proxy, help="Proxy for requests (e.g., 'http://user:pass@proxy.com:8080')")
    http_group.add_argument("-ar", "--allow-redirect", action="store_true", default=Config.ALLOW_REDIRECT, help="Allow HTTP redirects (true/false)")
    http_group.add_argument("-s", "--scrape", action="store_true", default=Config.ALLOW_SCRAPE, help="Scrape <a> tags and request their URLs")
    http_group.add_argument("-rl","--rate-limit", type=positive_rate_limit, help="Limit requests per second (default: unlimited)")

    # Output options
    output_group = parser.add_argument_group("Output Configs")
    output_group.add_argument("-o", "--output", type=valid_output, help="Save output to a file (.txt, .log, .json,...)")

    return parser.parse_args()