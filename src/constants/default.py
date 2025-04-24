#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""
from pathlib import Path

# Project info
NAME = "FwF"
DESCRIPTION = "Fast Web Fuzzer - Fast Web Fuzzer: A web path discovery tool"
AUTHOR = "WaiBui"
VERSION = "1.0.0"
LICENSE = "MIT"
URL = "https://github.com/waibui/FwF"        
COPYRIGHT = f"© 2025 {AUTHOR}"
USAGE = "python fwf.py [-u|--url] target [options]"
EPILOG = "Example: python -u example.com -r -mc 200,301"

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WORDLIST = Path.joinpath(PROJECT_ROOT, 'data', 'common.txt')
DEFAULT_USERAGENT = Path.joinpath(PROJECT_ROOT, 'data', 'user_agent.txt')
REQUIREMENTS = Path.joinpath(PROJECT_ROOT, 'requirements.txt')

# Default values
DEFAULT_CONCURRENCY = 100
DEFAULT_TIMEOUT = 10
DEFAULT_RETRY = 0
DEFAULT_CRAWL = 2
DEFAULT_STATUS_CODES = [
    200, 201, 202, 203, 204,             # Success codes
    301, 302, 307, 308,                  # Redirects
    401, 403                             # Auth-related 
]
DEFAULT_FOLLOW_REDIRECTS = False
DEFAULT_METHOD = 'GET'

# Default output
DEFAULT_COLOR = False
DEFAULT_VERBOSE = True

# Default allow
ALLOW_METHOD = ["GET", "POST", "HEAD", "PUT", "DELETE"]
ALLOW_OUTPUT_FORMAT = ["txt", "log", "json", "csv", "xlsx", "yaml", "yml", "md", "html", "xml"]