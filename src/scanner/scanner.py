#!/usr/bin/env python3

import time
import aiohttp
import asyncio
import random
from typing import Set, List
from src.output.logger import Logger
from src.models.config import ScanConfig
from src.models.result import ScanResult
from src.scanner.crawler import WebCrawler
from src.output.writer import FileWriter
from src.input.file_loader import load_wordlist, load_user_agent
from src.input.cli_parser import parse_cookies

logger = Logger.get_instance()

class FwFScanner:
    def __init__(self, config: ScanConfig):
        self.config = config
        self.wordlist: Set[str] = set()
        self.user_agents: List[str] = list()
        self.found_paths: Set[ScanResult] = set()
        self.start_time = 0
        self.crawler = WebCrawler(config) if config.crawl else None

    def display_input_info(self):
        logger.info("Starting scan", f"Target: {self.config.url}")
        logger.info("Method", self.config.method)
        logger.info("Concurrency", self.config.concurrency)
        logger.info("Timeout", self.config.timeout)
        logger.info("Retries", self.config.retry)
        logger.info("Follow Redirects", self.config.follow_redirects)
        logger.info("Proxy", self.config.proxy or "None")
        logger.info("Cookies", self.config.cookie or "None")
        logger.info("Custom Headers", self.config.headers or "None")
        logger.info("Status Code Match", self.config.match_codes)
        logger.info("Crawling Enabled", self.config.crawl)
        logger.info("Crawl Depth", self.config.crawl_depth if self.config.crawl else "N/A")
        logger.info("Output File", getattr(self.config, 'output', None) or "None")
        logger.info("Wordlist Loaded", f"{len(self.wordlist)} entries")
        logger.info("User-Agents Loaded", f"{len(self.user_agents)} entries")
        print("-"*60)
        
    async def scan(self):
        self.start_time = time.time()

        self.wordlist, self.user_agents = await asyncio.gather(
            load_wordlist(self.config.wordlist),
            load_user_agent(self.config.user_agent)
        )
        self.display_input_info()

        if self.config.crawl:
            crawled_urls = await self.crawler.crawl(self.config.url, self.config.crawl_depth)

            base_url = self.config.url.rstrip("/")
            for url in crawled_urls:
                if url.startswith(base_url):
                    path = url[len(base_url):].strip("/")
                    if path:
                        self.wordlist.add(path)

            logger.info("Crawling", f"Found {len(crawled_urls)} URLs, added {len(self.wordlist)} unique paths")

        await self._perform_scan()

        if self.config.output:
            [FileWriter.write_results(self.found_paths, file) for file in self.config.output.split(',')]
            
        elapsed = time.time() - self.start_time
        print('-'*60)
        logger.info("Scan completed", f"{elapsed:.2f}s elapsed, {len(self.found_paths)} paths found")

    async def _perform_scan(self):
        connector = aiohttp.TCPConnector(
            limit=self.config.concurrency,
            limit_per_host=self.config.concurrency,
            ttl_dns_cache=300,
            enable_cleanup_closed=True,
            force_close=False,
            ssl=False
        )
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)

        cookies = parse_cookies(self.config.cookie)

        session_kwargs = {
            'connector': connector,
            'timeout': timeout,
        }

        if cookies:
            session_kwargs['cookies'] = cookies

        if self.config.proxy:
            session_kwargs['proxy'] = self.config.proxy

        async with aiohttp.ClientSession(**session_kwargs) as session:
            tasks = []
            base_url = self.config.url.rstrip("/")

            for path in self.wordlist:
                if not path.strip() or path.startswith("#"):
                    continue
                url = f"{base_url}/{path.strip()}"
                path_clean = path.strip()
                tasks.append(asyncio.create_task(self._scan_path(session, url, path_clean)))

            await asyncio.gather(*tasks, return_exceptions=True)

    async def _scan_path(self, session: aiohttp.ClientSession, url: str, path: str):
        retries_left = self.config.retry

        while retries_left >= 0:
            try:
                start_time = time.time()
                headers = {
                    "User-Agent": random.choice(self.user_agents) if self.user_agents else "FwFScanner/1.0"
                }

                if self.config.headers:
                    headers.update(self.config.headers)

                method = self.config.method.upper()

                request_kwargs = {
                    'headers': headers,
                    'allow_redirects': self.config.follow_redirects
                }

                async with getattr(session, method.lower())(url, **request_kwargs) as response:
                    response_time = time.time() - start_time
                    content_length = len(await response.read())
                    content_type = response.headers.get('Content-Type')

                    if (response.status in self.config.match_codes):
                        result = ScanResult(
                            url=url,
                            path=path,
                            status=response.status,
                            content_length=content_length,
                            response_time=response_time,
                            content_type=content_type,
                        )
                        self.found_paths.add(result)
                        logger.http(response.status, f"[{method}] {url}", f"{response_time:.3f}s")
                    return
            except asyncio.TimeoutError:
                retries_left -= 1
                if retries_left >= 0:
                    await asyncio.sleep(0.5)
            except Exception as e:
                break

    def get_results(self) -> Set[ScanResult]:
        return self.found_paths
