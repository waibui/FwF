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

import sys
import requests
import time

from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from models.scan_config import ScannerConfig
from views.logger import Logger

from core.requests import request

class ScannerEngine:
    def __init__(self, configs: ScannerConfig, wordlist: Queue, user_agent: list):
        self.configs = configs
        self.wordlist = wordlist
        self.user_agent = user_agent
        self.session = requests.Session()
    
    def scan(self):
        try:
            start_t = time.time()
            executor = ThreadPoolExecutor(max_workers=self.configs.threads)
            while not self.wordlist.empty():
                executor.submit(self.worker, self.wordlist.get())
            
            executor.shutdown(wait=True)
            
            if self.option.output_file is not None:
                Logger.logging_to_file(self.option.output_file, self.results)
                
        except KeyboardInterrupt:
            Logger.info("\n[!] Keyboard Interrupt detected! Stopping all threads...")
            if executor:
                executor.shutdown(wait=False, cancel_futures=True) 
            sys.exit(0)  
        except Exception:
            sys.exit(0)
        finally:
            end_t = time.time()
            self.statistical(end_t - start_t)
            
    def worker(self, path):
        pass