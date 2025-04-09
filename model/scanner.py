# -*- coding: utf-8 -*-
#  psdir - Web Path Scanner
#  Copyright (c) 2025 waibui
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import asyncio
import aiohttp
from core.logger import Logger
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
