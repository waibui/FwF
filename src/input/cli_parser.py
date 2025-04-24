#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

import argparse
from src.constants import default
from src.validators.parse_validator import Validator
from src.output.logger import Logger

logger = Logger.get_instance()

def parse_arguments():
    """
    Parse command-line arguments and update the provided Config object.
    """    
    parser = argparse.ArgumentParser(
        description=default.DESCRIPTION,
        usage=default.USAGE,
        epilog=default.EPILOG,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )    
    parser.add_argument(
        "-V", "--version",
        action="store_true",
        help="Show version"
    )
    
    # HTTP options
    http = parser.add_argument_group("http option")
    http.add_argument(
        "-u", "--url",
        type=Validator.is_valid_url,
        help="Target URL"
    )
    http.add_argument(
        "-X", "--method",
        type=Validator.valid_http_method,
        default=default.DEFAULT_METHOD,
        help="HTTP method to use (e.g., GET, POST)"
    )
    http.add_argument(
        "-r", "--follow-redirects",
        action="store_true",
        default=default.DEFAULT_FOLLOW_REDIRECTS,
        help="Follow HTTP redirects"
    )
    http.add_argument(
        "-t", "--timeout",
        type=Validator.positive_timeout,
        default=default.DEFAULT_TIMEOUT,
        help="Request timeout in seconds"
    )
    http.add_argument(
        "-x", "--proxy",
        type=Validator.valid_proxy,
        default=None,
        help="Proxy to use (e.g., 'http://user:pass@proxy.com:8080')"
    )
    http.add_argument(
        "-ck", "--cookie",
        type=Validator.valid_cookie,
        default=None,
        help="Cookies for requests (e.g., 'key=value,key2=value2')"
    )
    
    # General options
    general = parser.add_argument_group("general option")
    general.add_argument(
        "-c", "--concurrency",
        type=Validator.positive_threads,
        default=default.DEFAULT_CONCURRENCY,
        help="Number of concurrent threads"
    )
    general.add_argument(
        "-rt", "--retry",
        type=Validator.non_negative_int,
        default=default.DEFAULT_RETRY,
        help="Number of times to retry failed requests"
    )
    general.add_argument(
        "--crawl",
        action="store_true",
        help="Crawl the web"
    )
    general.add_argument(
        "--crawl-depth", 
        type=Validator.non_negative_int, 
        default=2, 
        help="Maximum crawl depth"
    )
    # Input options
    input = parser.add_argument_group("input option")
    input.add_argument(
        "-w", "--wordlist",
        default=default.DEFAULT_WORDLIST,
        help="Path to wordlist file"
    )
    input.add_argument(
        "-ua", "--user-agent",
        default=default.DEFAULT_USERAGENT,
        help="Path to User-Agent file or static string"
    )
    
    # Output options
    output = parser.add_argument_group("output option")
    output.add_argument(
        "--color",
        action="store_true",
        default=default.DEFAULT_COLOR,
        help="Disable colored output"
    )
    output.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=default.DEFAULT_VERBOSE,
        help="Suppress all non-essential output"
    )
    output.add_argument(
        "-o", "--output",
        type=Validator.valid_output,
        default=None,
        help="Save output to file (.txt, .log, .json, etc.)"
    )
    
     # Filter options
    filters = parser.add_argument_group("filter option")

    filters.add_argument(
        "-mc", "--match-codes",
        type=Validator.valid_match_code,
        default=default.DEFAULT_STATUS_CODES,
        help=f"Filter status codes (comma-separated). Default: {default.DEFAULT_STATUS_CODES}"
    )

    args = parser.parse_args()
    
    if args.version:
        logger.info("version", default.VERSION)
        exit(0)
        
    if not args.url:
        logger.error("-u option required")
        logger.error("use", default.USAGE)
        exit(0)
    
    return args

def parse_cookies(cookie_string: str) -> dict:
    """
    Parse cookies from a string format like 'key=value,key2=value2' into a dictionary.
    
    Args:
        cookie_string: String containing cookies in 'key=value,key2=value2' format
        
    Returns:
        Dictionary of cookies with key-value pairs
    """
    if not cookie_string:
        return None
        
    cookies = {}
    for cookie_item in cookie_string.split(','):
        if '=' in cookie_item:
            key, value = cookie_item.strip().split('=', 1)
            cookies[key] = value
    
    return cookies if cookies else None