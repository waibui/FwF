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
import time
from lxml import html
from urllib.parse import urljoin, urlparse
from view.logger import logger
from model.result import Result

async def request(session, url, path, user_agent, args):
    full_url = f"{args.url.rstrip('/')}/{path.lstrip('/')}"
    headers = {"User-Agent": user_agent.random}
    kwargs = {
        "headers": headers,
        "timeout": aiohttp.ClientTimeout(total=args.timeout),
        "allow_redirects": args.allow_redirect
    }

    if args.cookie:
        kwargs["cookies"] = args.cookie
    if args.proxies:
        kwargs["proxy"] = args.proxies

    start_time = time.time()
    try:
        async with session.get(full_url, **kwargs) as response:
            elapsed_time = time.time() - start_time  

            result = None
            if response.status in args.match_code:
                logger.info(f"[+] {response.status} - {elapsed_time:.3f}s - {full_url}")
                result = Result(response.status, full_url, elapsed_time)
                
                if args.scrape and response.status == 200:
                    content = await response.text()
                    links = extract_links(full_url, content, args)
                    return result, links
            return result, []
    except aiohttp.ClientError:
        pass
    except Exception as e:
        pass
    return None, []

def extract_links(base_url, html_content, args):
    crawled_links = set()
    extracted_links = []
    try:
        if not html_content.strip():
            return []

        if isinstance(html_content, str):
            html_content = html_content.encode('utf-8')

        tree = html.fromstring(html_content)
        links = []

        for link in tree.xpath('//a[@href]'):
            href = link.get('href')
            if href:
                absolute_url = urljoin(base_url, href)
                if (absolute_url not in crawled_links and 
                    not href.startswith('#') and 
                    not href.startswith('javascript:') and
                    not href.startswith('mailto:') and
                    not href.startswith('tel:')):

                    base_domain = urlparse(args.url).netloc
                    link_domain = urlparse(absolute_url).netloc

                    if base_domain == link_domain:
                        links.append(absolute_url)
                        crawled_links.add(absolute_url)
                        extracted_links.append(absolute_url)

        return links
    except Exception as e:
        return []

async def check_link_status(session, url, user_agent, args):
    headers = {"User-Agent": user_agent.random}
    kwargs = {
        "headers": headers,
        "timeout": aiohttp.ClientTimeout(total=args.timeout),
        "allow_redirects": args.allow_redirect
    }

    if args.cookie:
        kwargs["cookies"] = args.cookie
    if args.proxies:
        kwargs["proxy"] = args.proxies

    start_time = time.time()
    try:
        async with session.get(url, **kwargs) as response:
            elapsed_time = time.time() - start_time
            if response.status in args.match_code:
                logger.info(f"[+] {response.status} - {elapsed_time:.3f}s - {url} (extracted link)")

                result = Result(response.status, url, elapsed_time)
                return result
    except aiohttp.ClientError as e:
        pass
    except Exception as e:
        pass

    return None

class Scanner:
    def __init__(self, args, wordlist, user_agent):
        self.args = args
        self.wordlist = wordlist
        self.user_agent = user_agent
        self.semaphore = asyncio.Semaphore(args.threads)
        self.crawled_links = set()
        self.extracted_links = []
        self.link_results = []

    async def scan(self):
        connector = aiohttp.TCPConnector(limit=self.args.threads, enable_cleanup_closed=True)
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
                return result
            except Exception as e:
                logger.debug(f"Error in worker: {str(e)}")
                return None
