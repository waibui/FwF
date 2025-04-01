# -*- coding: utf-8 -*-
#  psdir - Web Path Scanner
#  Copyright (C) 2025 waibui
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  Author: waibui

import asyncio
import aiohttp
from view.logger import logger

from utils.request_handler import check_link_status, request

class Scanner:
    def __init__(self, args, wordlist, user_agent):
        self.args = args
        self.wordlist = wordlist
        self.user_agent = user_agent
        self.semaphore = asyncio.Semaphore(args.concurrency)
        self.rate_limit = args.rate_limit
        self.crawled_links = set()
        self.extracted_links = []
        self.link_results = []

    async def scan(self):
        connector = aiohttp.TCPConnector(limit=self.args.concurrency, enable_cleanup_closed=True)
        async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
            tasks = [self.worker(session, path) for path in self.wordlist]
            results = await asyncio.gather(*tasks)
            initial_results = [res for res in results if res]

            if self.extracted_links:
                logger.info(f"[+] Checking status codes for {len(self.extracted_links)} extracted links...")
                link_tasks = [check_link_status(session, link, self.user_agent, self.args) for link in self.extracted_links]
                link_results = await asyncio.gather(*link_tasks)
                initial_results.extend(link_results)
            
        return initial_results

    async def worker(self, session, path):
        async with self.semaphore:
            try:
                result, links = await request(session, self.args.url, path, self.user_agent, self.args)
                if links:
                    self.extracted_links.extend(links)
                    
                if self.rate_limit and self.rate_limit > 1:
                    await asyncio.sleep(1 / self.rate_limit)
                    
                return result
            except Exception as e:
                logger.debug(f"Error in worker: {str(e)}")
                return None
