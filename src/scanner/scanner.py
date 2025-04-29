#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

import time
import aiohttp
import asyncio
import random

from src.output.logger import Logger
from src.models.config import ScanConfig
from src.output.writer import FileWriter
from src.scanner.request import process_request
from src.input.file_getter import load_wordlist, load_user_agents
from src.output.scan_info import print_scan_info
from src.output.summary import print_summary

logger = Logger.get_instance()

class FwFScanner:
    """Responsible for performing web path discovery scans."""
    def __init__(self, config: ScanConfig):
        self.config = config
        self.paths = []
        self.user_agents = []
        self.scan_results = []

        self.failed_tasks = 0
                
    async def run(self):
        """Run the scan engine"""
        self.paths = load_wordlist(self.config.wordlist)
        self.user_agents = load_user_agents(self.config.user_agent)
        
        print_scan_info(self.config)
        
        connector, session_timeout = self._config_session_setting()
        start_time = time.time()
        
        await self._execute_tasks(connector, session_timeout)
       
        print_summary(start_time, self.scan_results, self.failed_tasks)
        
        if self.config.output:
            [FileWriter.write_results(results=self.scan_results, output_file=output, config=self.config) for output in self.config.output.split(',')]
    
    async def _execute_tasks(self, connector: aiohttp.TCPConnector, session_timeout: aiohttp.ClientTimeout):
        """Execute all path checking tasks and handle results"""
        try:
            self.semaphore = asyncio.Semaphore(self.config.concurrency)
            
            async with aiohttp.ClientSession(
                timeout=session_timeout,
                connector=connector
            ) as session:
                tasks = [self.create_task(session, path, random.choice(self.user_agents)) for path in self.paths]
                for future in asyncio.as_completed(tasks):
                    try:
                        result = await future
                        if result:
                            self.scan_results.append(result)
                    except Exception as e:
                        logger.error("[Error completing tasks]", str(e))
        except Exception as e:
            logger.error("[Error executing tasks]", str(e))
        
    async def create_task(self, session: aiohttp.ClientSession, path: str, user_agent: str):
        """Create a task that checks a path with retry logic and semaphore control"""
        retries = self.config.retry
        while retries >= 0:
            try:
                async with self.semaphore:
                    result = await process_request(session, self.config, path, user_agent)
                    return result
            except (asyncio.TimeoutError, aiohttp.ClientError) as e:
                retries -= 1
                if retries >= 0:
                    await asyncio.sleep(0.1)
            except Exception as e:
                logger.error("[Unexpected error]", path, str(e))
                break
        self.failed_tasks += 1

    def _config_session_setting(self) -> tuple[aiohttp.TCPConnector, aiohttp.ClientTimeout]:
        """Configure HTTP session settings"""
        connector = aiohttp.TCPConnector(
            limit=self.config.concurrency,
            ttl_dns_cache=300,
            ssl=False
        )
       
        session_timeout = aiohttp.ClientTimeout(
            total=None,
            connect=self.config.timeout,
            sock_connect=self.config.timeout,
            sock_read=self.config.timeout
        )
       
        return connector, session_timeout
