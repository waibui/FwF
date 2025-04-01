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
from utils.logger import Logger
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
        self.rate_limiter = asyncio.Semaphore(self.rate_limit) if self.rate_limit else None

    async def scan(self):
        try:
            connector = aiohttp.TCPConnector(limit=self.args.concurrency, enable_cleanup_closed=True)
            async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
                tasks = [self.worker(session, path) for path in self.wordlist]
                results = await asyncio.gather(*tasks, return_exceptions=True)  

                results = [res for res in results if res and not isinstance(res, Exception)]

                if self.extracted_links:
                    Logger.info(f"[+] Checking status codes for {len(self.extracted_links)} extracted links...")
                    link_tasks = [check_link_status(session, link, self.user_agent, self.args) for link in self.extracted_links]
                    link_results = await asyncio.gather(*link_tasks, return_exceptions=True)
                    results.extend([res for res in link_results if res and not isinstance(res, Exception)])

            return results

        except asyncio.CancelledError:
            Logger.info("[!] Scan was cancelled. Cleaning up...")
            return []

        except KeyboardInterrupt:
            Logger.info("[!] User interrupted. Exiting gracefully.")
            return []

    async def worker(self, session, path):
        async with self.semaphore:
            if self.rate_limiter:
                async with self.rate_limiter:
                    await asyncio.sleep(1 / self.rate_limit)  
            
            try:
                result, links = await request(session, path, self.user_agent, self.args)

                if links:
                    self.extracted_links.extend(links)

                return result
            except Exception as e:
                Logger.debug(f"Error in worker: {str(e)}")
                return None
