#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

import argparse

from src import __version__
from src.constants import default as df 
from src.validator.parser_validator import ParserValidator as pv

def parse_arguments() -> argparse.Namespace: 
    """
    Parse command-line arguments.
    """    
    parser = argparse.ArgumentParser(
        description=df.DESCRIPTION,
        usage=df.USAGE,
        epilog=df.EPILOG,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )    
    
    parser.add_argument(
        '-v', "--version",
        help="Show tool's version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    # ========== HTTP Options ==========
    http = parser.add_argument_group("HTTP Option")
    http.add_argument(
        "-u", "--url",
        required=True,
        type=pv.is_valid_url,
        help="Target URL"
    )
    http.add_argument(
        "-X", "--method",
        type=pv.is_valid_method,
        default=df.DEFAULT_METHOD,
        help="HTTP method to use (e.g., GET, POST)"
    )
    http.add_argument(
        "-t", "--timeout",
        type=pv.is_positive_number,
        default=df.DEFAULT_TIMEOUT,
        help="Request timeout in seconds"
    )
    http.add_argument(
        "-r", "--follow-redirects",
        action="store_true",
        default=df.DEFAULT_FOLLOW_REDIRECTS,
        help="Follow HTTP redirects"
    )
    http.add_argument(
        "-k", "--cookie",
        type=pv.is_valid_cookie,
        default=None,
        help="Cookies for requests (e.g., 'key=value,key2=value2')"
    )
    
    # ========= General Options ==========
    general = parser.add_argument_group("General Option")
    general.add_argument(
        "-c", "--concurrency",
        type=pv.is_positive_number,
        default=df.DEFAULT_CONCURRENCY,
        help="Number of concurrent threads"
    )
    general.add_argument(
        "-y", "--retry",
        type=pv.is_non_negative,
        default=df.DEFAULT_RETRY,
        help="Number of times to retry failed requests"
    )
    
    # ========= Input Options ==========
    input = parser.add_argument_group("Input Options")
    input.add_argument(
        "-w", "--wordlist",
        type=pv.is_valid_path,
        default=df.DEFAULT_WORDLIST,
        help="Path to Wordlist file"
    )
    input.add_argument(
        "-a", "--user-agent",
        type=pv.is_valid_path,
        default=df.DEFAULT_USERAGENT,
        help="Path to User-Agent file"
    )
    
    # ========== Output Options ==========
    output = parser.add_argument_group("output option")
    output.add_argument(
        "--color",
        action="store_true",
        default=df.DEFAULT_COLOR,
        help="Disable colored output"
    )
    output.add_argument(
        "--verbose",
        action="store_true",
        default=df.DEFAULT_VERBOSE,
        help="Suppress all non-essential output"
    )
    output.add_argument(
        "-o", "--output",
        type=pv.is_valid_output,
        default=None,
        help="Save output to file (.txt, .log, .json, etc.)"
    )
    
    # ========== Filter Options ==========
    filters = parser.add_argument_group("filter option")
    filters.add_argument(
        "-m", "--match-codes",
        type=pv.is_match_code,
        default=df.DEFAULT_STATUS_CODES,
        help=f"Filter status codes (comma-separated). Default: {df.DEFAULT_STATUS_CODES}"
    )
    
    args = parser.parse_args()
    
    return args