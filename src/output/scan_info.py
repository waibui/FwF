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
    logger.info("-"*60)
    logger.info("::", "Method:", config.method)
    logger.info("::", "Target:", config.url)
    logger.info("::", "Wordlist:", config.wordlist)
    logger.info("::", "User-Agent:", config.user_agent)
    logger.info("::", "Concurrency:", config.concurrency)
    logger.info("::", "Timeout:", config.timeout)
    logger.info("::", "Retries:", config.retry)
    logger.info("::", "Follow Redirects:", config.follow_redirects)
    logger.info("::", "Cookies:", config.cookie or "None")
    logger.info("::", "Match Code:", ", ".join(map(str, config.match_codes)))
    logger.info("::", "Crawl:", config.crawl)
    logger.info("::", "Crawl Depth:", config.crawl_depth if config.crawl else "N/A")
    logger.info("::", "Output File:", getattr(config, 'output', None) or "None")
    logger.info("-"*60)