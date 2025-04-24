#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

from src.output.logger import Logger

logger = Logger.get_instance()

def log_scan_start_info(
    target_url: str,
    wordlist_path: str,
    total_paths: int,
    concurrency: int,
    timeout: float
) -> None:
    """Log information about the scan at startup."""
    logger.info(f"Starting scan on {target_url or ''}")
    logger.info(f"Using wordlist: {wordlist_path or ''} ({total_paths or ''} paths)")
    logger.info(f"Concurrency: {concurrency or ''}, Timeout: {timeout or ''}s")
