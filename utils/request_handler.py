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

import aiohttp
import time

from view.logger import logger
from model.result import Result
from utils.scrape import extract_links

async def request(args, session, path, user_agent):
    url = f"{args.url.rstrip('/')}/{path.lstrip('/')}"
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
            
            result = None
            if response.status in args.match_code:
                logger.info(f"[+] {response.status} - {elapsed_time:.3f}s - {url}")
                result = Result(response.status, url, elapsed_time, None)
                
                if args.scrape and response.status == 200:
                    content = await response.text()
                    links = extract_links(url, content)
                    result.links = links
                return result
    except aiohttp.ClientError:
        pass
    except Exception as e:
        pass
    return None