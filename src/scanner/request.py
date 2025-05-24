#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

import asyncio
import aiohttp
import time

from src.models.config import ScanConfig
from src.models.result import ScanResult
from src.output.logger import Logger

logger = Logger.get_instance()

async def process_request(session: aiohttp.ClientSession, config: ScanConfig, path: str, user_agent: str) -> ScanResult:
    """Check information of the path."""
    url = f"{config.url.rstrip('/')}/{path.lstrip('/')}"
    start_time = time.time()
    
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
    }
    
    if config.cookie:
        headers["Cookie"] = config.cookie

    request_kwargs = {
        'headers': headers,
        'allow_redirects': config.follow_redirects,
        'params': config.params,
        'data': config.data
    }
    
    method_func = {
        "get": session.get,
        "post": session.post,
        "head": session.head,
        "put": session.put,
        "delete": session.delete,
        "patch": session.patch
    }.get(config.method.lower())

    if not method_func:
        logger.error("[INVALID METHOD]", config.method)
        return

    try:
        async with asyncio.timeout(config.timeout):
            async with method_func(url, **request_kwargs) as response:
                elapsed = time.time() - start_time
                logger.http(response.status,config.match_codes, url, f"{elapsed:.2f}s")
                content_type = response.headers.get('Content-Type')
                content_length = int(response.headers.get('Content-Length', 0))
                return ScanResult(
                    url=url,
                    status=response.status,
                    content_length=content_length,
                    response_time=elapsed,
                    content_type=content_type
                )
    except asyncio.TimeoutError:
        logger.error('[TIMEOUT]', url, f'{config.timeout}s')
        raise
    except aiohttp.ClientError as e:
        logger.error('[HTTP ERROR]', url, str(e))
        raise
    except Exception as e:
        logger.error('[UNEXPECTED]', url, str(e))
        raise
