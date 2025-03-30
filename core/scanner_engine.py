import asyncio
import aiohttp
from collections import defaultdict
from core.requests import request

class ScannerEngine:
    def __init__(self, configs, wordlist, user_agent):
        self.configs = configs
        self.wordlist = wordlist
        self.user_agent = user_agent
        self.results = []
        self.status_count = defaultdict(int)
        self.semaphore = asyncio.Semaphore(200)  

    async def scan(self):
        connector = aiohttp.TCPConnector(limit=100, enable_cleanup_closed=True)
        async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
            tasks = [self.worker(session, path) for path in self.wordlist]
            results = await asyncio.gather(*tasks) 
            
            self.results = [res for res in results if res]
        
        return self.results

    async def worker(self, session, path):
        async with self.semaphore:
            try:
                result = await request(session, path, self.configs, self.user_agent)
                return result if result else None
            except Exception:
                return None  
