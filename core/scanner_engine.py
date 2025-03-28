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
import threading
import signal
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed

from models.scan_config import ScannerConfig
from views.logger import Logger
from core.utilities import Utilities
from core.requests import request

class ScannerEngine:
   
    def __init__(self, configs: ScannerConfig, wordlist: Queue, user_agent: list):
   
        self.configs = configs
        self.wordlist = wordlist
        self.user_agent = user_agent
        self.session = requests.Session()
        self.results = []
        self.stop_event = threading.Event()
        signal.signal(signal.SIGINT, self.handle_exit)

    def handle_exit(self, signum, frame):
        Logger.info("[!] Keyboard Interrupt detected! Stopping all threads immediately...")
        self.stop_event.set()
        sys.exit(1)

    def scan(self):
      
        try:
            with ThreadPoolExecutor(max_workers=self.configs.threads) as executor:
                futures = {executor.submit(self.worker, path): path for path in list(self.wordlist.queue)}
                
                for future in as_completed(futures):
                    if self.stop_event.is_set():
                        break
                    try:
                        result = future.result()
                        if result:
                            self.results.append(result)
                    except Exception as e:
                        Logger.error(f"[!] Worker error: {e}")

            if self.configs.output and not self.stop_event.is_set():
                Logger.logging_to_file(self.configs.output, self.results)
        
        except (KeyboardInterrupt, SystemExit):
            self.stop_event.set()
            Logger.info("[!] Stopping all workers...")
            sys.exit(1)
        except Exception as e:
            Logger.error(f"[!] Unexpected error: {e}")
            sys.exit(1)
        
        return self.results

    def worker(self, path):
        if self.stop_event.is_set():
            return None
        try:
            result = request(
                session=self.session,
                path=path,
                configs=self.configs,
                user_agent=Utilities.random_user_agent(self.user_agent)
            )
            if result and not self.stop_event.is_set():
                Logger.result_scan(result[0],result[1])
                return result
        except Exception as e:
            if not self.stop_event.is_set():
                Logger.error(f"[!] Error scanning {path}: {e}")
        return None