#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

import re
import argparse
from typing import List
from src.constants import default

class Validator:
    # ========== URL & REQUEST VALIDATORS ==========
    def is_valid_url(value: str) -> str:
        """Validate and return a properly formatted URL."""
        url_pattern = re.compile(r"^(https?://)?([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,6})(:[0-9]{1,5})?(/.*)?$")
        if not url_pattern.match(value):
            raise argparse.ArgumentTypeError(f"Invalid URL: '{value}'. Must start with 'http://' or 'https://'.")
        return value if value.startswith(("http://", "https://")) else "https://" + value

    def valid_http_method(value: str) -> str:
        """Validate the HTTP method."""
        method = value.upper()
        if method not in default.ALLOW_METHOD:
            raise argparse.ArgumentTypeError(f"Invalid HTTP method '{method}'. Allowed: {default.DEFAULT_METHOD}.")
        return method

    # ========== NUMERIC VALIDATORS ==========
    def positive_timeout(value: str) -> float:
        """Ensure timeout is at least 1.0 seconds."""
        timeout = float(value)
        if timeout < 1.0:
            raise argparse.ArgumentTypeError("Timeout must be at least 1.0 seconds.")
        return timeout

    def positive_threads(value: str) -> int:
        """Ensure thread count is at least 1."""
        threads = int(value)
        if threads < 1:
            raise argparse.ArgumentTypeError("Thread count must be at least 1.")
        return threads

    def positive_rate_limit(value: str) -> int:
        """Ensure rate limit is at least 1."""
        rate_limit = int(value)
        if rate_limit < 1:
            raise argparse.ArgumentTypeError("Rate limit must be at least 1.")
        return rate_limit
    
    def non_negative_int(value):
        ivalue = int(value)
        if ivalue < 0:
            raise argparse.ArgumentTypeError("Value must be a non-negative integer")
        return ivalue

    # ========== FORMAT VALIDATORS ==========
    def valid_cookie(value: str) -> str:
        """Validate the cookie format (key=value; key2=value2)."""
        cookie_pattern = re.compile(r"^([\w-]+=[^;]+)(;[\w-]+=[^;]+)*$")
        if not cookie_pattern.match(value):
            raise argparse.ArgumentTypeError("Invalid cookie format. Use 'key=value; key2=value2'.")
        return value

    def valid_proxy(value: str) -> str:
        """
        Validate proxy format:
        - http[s]://host:port
        - http[s]://user:pass@host:port
        """
        proxy_pattern = re.compile(
            r"^(https?://)"                  
            r"(?:(\S+):(\S+)@)?"             
            r"((?:[\w.-]+)|(?:\d{1,3}(?:\.\d{1,3}){3}))"  
            r":(\d{2,5})$"                  
        )
        if not proxy_pattern.match(value):
            raise argparse.ArgumentTypeError(
                "Invalid proxy format. Use 'http://user:pass@host:port' or 'https://host:port'."
            )
        return value

    def valid_output(value: str) -> str:
        """Validate the output file path format."""
        if value.split('.')[-1] not in default.ALLOW_OUTPUT_FORMAT:
            raise argparse.ArgumentTypeError(f"Output file must have a valid extension ({', '.join(default.ALLOW_OUTPUT_FORMAT)}).")
        return value

    # ========== BOOLEAN & MATCH CODE VALIDATORS ==========
    def str2bool(value: str) -> bool:
        """Convert a string to boolean."""
        true_values = {"yes", "true", "t", "1"}
        false_values = {"no", "false", "f", "0"}
        
        value_lower = value.lower()
        if value_lower in true_values:
            return True
        elif value_lower in false_values:
            return False
        else:
            raise argparse.ArgumentTypeError("Boolean value expected: 'true' or 'false'.")

    def valid_match_code(value: str) -> List[int]:
        """Validate match HTTP status codes based on Config.DEFAULT_STATUS."""
        try:
            codes = [int(code.strip()) for code in value.split(",")]
        except ValueError:
            raise argparse.ArgumentTypeError("Match codes must be integers (comma-separated).")

        invalid_codes = [code for code in codes if code not in default.DEFAULT_STATUS_CODES]
        if invalid_codes:
            raise argparse.ArgumentTypeError(
                f"Invalid match codes: {invalid_codes}. Allowed values: {default.DEFAULT_STATUS_CODES}."
            )
        return codes
