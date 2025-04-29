#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

import time
from src.models.result import ScanResult
from src.output.logger import Logger

logger = Logger.get_instance()

def print_summary(start_time: float, scan_results: list[ScanResult], failed_tasks: int = 0):
    """Print summary statistics of the scan"""
    if not scan_results and failed_tasks == 0:
        logger.warning("No paths discovered.")
        return

    logger.info('-'*60)
    elapsed = time.time() - start_time

    logger.info("[*]", f"Scan completed in {elapsed:.2f} seconds")

    total = len(scan_results)
    found_2xx = sum(1 for r in scan_results if 200 <= r.status < 300)
    found_3xx = sum(1 for r in scan_results if 300 <= r.status < 400)
    found_4xx = sum(1 for r in scan_results if 400 <= r.status < 500)
    found_5xx = sum(1 for r in scan_results if 500 <= r.status < 600)

    logger.info("::", "Total paths discovered:".ljust(25), total)
    logger.info("::", "2xx Success responses:".ljust(25), found_2xx)
    logger.info("::", "3xx Redirection:".ljust(25), found_3xx)
    logger.info("::", "4xx Client errors:".ljust(25), found_4xx)
    logger.info("::", "5xx Server errors:".ljust(25), found_5xx)
    logger.info("::", "Failed tasks:".ljust(25), failed_tasks)
    logger.info('-'*60)
