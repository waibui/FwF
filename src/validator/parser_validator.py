#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

import argparse
import re
from pathlib import Path

from src.constants import default as df 
from src.constants import regex 

class ParserValidator:
    """Collection of static methods for validating and formatting command-line parser."""
    @staticmethod
    def is_valid_url(value: str) -> str:
        """Check if is valid Url, return a properly formatted URL."""
        if not re.match(regex.URL_PATTERN, value):
            raise argparse.ArgumentTypeError(f"Invalid URL: '{value}'")
        return value if value.startswith(("http://", "https://")) else "https://" + value
    
    @staticmethod
    def is_valid_method(value: str) -> str:
        """Check if is valid HTTP method, return a properly formatted HTTP method."""
        method = value.upper()
        if method not in df.ALLOW_METHOD:
            raise argparse.ArgumentTypeError(f"Invalid HTTP method '{value}'. Allowed: {", ".join(df.ALLOW_METHOD)}.")
        return method
    
    @staticmethod
    def is_positive_number(value: str) -> int:
        "Validate that the input is a positive integer (>= 1)."
        number = int(value)
        if number < 1:
            raise argparse.ArgumentTypeError("Value must be at least 1.")
        return number
    
    @staticmethod
    def is_non_negative(value: str) -> int:
        """Check if a number is greater than or equal to 0."""
        number = int(value)
        if number < 0:
            raise argparse.ArgumentTypeError("Value must be at least 0.")
        return number
    
    @staticmethod
    def is_valid_proxy(value: str) -> str:
        """
        Validate proxy format:
        - http[s]://host:port
        - http[s]://user:pass@host:port
        """
        if not re.match(regex.PROXY_PATTERN, value):
            raise argparse.ArgumentTypeError("Invalid proxy format. Use 'http://user:pass@host:port' or 'https://host:port'.")
        return value
    
    @staticmethod
    def is_valid_cookie(value: str) -> str:
        """Validate and convert cookie from 'key=value,key2=value2' to 'key=value; key2=value2'."""
        if not re.match(regex.COOKIE_PATTERN, value):
            raise argparse.ArgumentTypeError("Invalid cookie format. Use 'key=value,key2=value2'.")
        
        parts = [item.strip() for item in value.split(',')]
        return '; '.join(parts)

    @staticmethod
    def is_valid_path(value: str) -> str:
        """Validate the file path."""
        if not Path(value).exists():
            raise argparse.ArgumentTypeError("File not found")
        return value
    
    @staticmethod
    def is_valid_output(value: str) -> str:
        """Validate the output file path format."""
        if value.split('.')[-1] not in df.ALLOW_OUTPUT_FORMAT:
            raise argparse.ArgumentTypeError(f"Output file must have a valid extension: {', '.join(df.ALLOW_OUTPUT_FORMAT)}.")
        return value
    
    @staticmethod
    def is_match_code(value: str) -> str:
        """Validate match HTTP status codes."""
        codes = [int(code.strip()) for code in value.split(",")]
        if not set(codes).issubset(set(df.DEFAULT_STATUS_CODES)):
            raise argparse.ArgumentTypeError(f"Invalid match codes: {codes}. Allowed values: {df.DEFAULT_STATUS_CODES}.")
        return codes