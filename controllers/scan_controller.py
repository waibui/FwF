import sys
import time
import asyncio
from collections import defaultdict
from models.scan_config import ScannerConfig
from views.logger import Logger
from core.scanner_engine import ScannerEngine
from views.banner_display import print_banner
from views.option_display import print_option

class Controller:
    def __init__(self, configs: ScannerConfig):
        self.configs = configs
        self.wordlist = []  # ✅ Dùng list thay vì Queue
        self.user_agent = []
        self.results = []

    def run(self):
        self.fetch_wordlist()  
        self.fetch_user_agent() 
        
        print_banner()
        print_option(self.configs)
        start = time.time()
        
        # ✅ Chạy scan() bằng asyncio
        self.results = asyncio.run(
            ScannerEngine(configs=self.configs, wordlist=self.wordlist, user_agent=self.user_agent).scan()
        )
        
        end = time.time()
        self.statistical(end - start)
        
    def fetch_wordlist(self):
        try:
            with open(self.configs.wordlists, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip()
                    if word:
                        self.wordlist.append(word)  # ✅ Thêm vào list thay vì Queue
        except FileNotFoundError:
            Logger.error(f"Invalid wordlist path: '{self.configs.wordlists}'")
            sys.exit(1)
            
    def fetch_user_agent(self):
        try:
            with open(self.configs.user_agent, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip()
                    if word:
                        self.user_agent.append(word)
        except FileNotFoundError:
            Logger.error(f"Invalid user-agent path '{self.configs.user_agent}'")
            sys.exit(1)
            
    def statistical(self, total):
        """Thống kê kết quả dựa trên mã HTTP"""
        if not self.results:
            print("No results found.")
            return

        stats = defaultdict(int)
        for result in self.results:
            stats[result[0]] += 1
        print("-------------------------------------------------------")
        print(f"{':: Total time'.ljust(24)}: {total:.2f}(s)")
        for status, count in sorted(stats.items()):
            print(f"{f':: HTTP {status}'.ljust(24)}: {count} path(s)") 
        print("-------------------------------------------------------")
