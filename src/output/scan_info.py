#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

from src.models.config import ScanConfig
from src.output.logger import Logger
logger = Logger.get_instance()

def print_scan_info(config: ScanConfig):
    """Prints the configuration settings before starting the scan."""
    logger.info("-" * 60)

    def print_field(name: str, value):
        if value is not None:
            logger.info(f":: {name}: {value}")

    print_field("Method", config.method)
    print_field("Target", config.url)
    print_field("Wordlist", config.wordlist)
    print_field("User-Agent", config.user_agent)
    print_field("Concurrency", config.concurrency)
    print_field("Timeout", config.timeout)
    print_field("Retries", config.retry)
    print_field("Follow Redirects", config.follow_redirects if config.follow_redirects else None)
    print_field("Cookies", config.cookie)
    
    if config.match_codes:
        print_field("Match Code", ", ".join(map(str, config.match_codes)))

    print_field("Output File", config.output)
    print_field("Params", config.params)
    print_field("Data", config.data)

    logger.info("-" * 60)
