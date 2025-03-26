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

import threading
import random
import sys

from queue import Queue
from models.option import Option
from views.logging import Logging
from controllers.scan_controller import scan_path

class Controller:
    def __init__(self, option:Option):
        self.option = option
        self.wordlist_queue = Queue()
        self.user_agents = []
        self.threads = [] 

    def run(self):
        """
        Run the main controller using threading
        """
        self.fetch_user_agent()
        self.fetch_wordlist()
        self.print_options()

        try:
            for _ in range(self.option.thread_count):
                t = threading.Thread(target=self.worker,daemon=True)
                t.start()
                self.threads.append(t)

            for t in self.threads:
                t.join()
        
        except KeyboardInterrupt:
            print("User Interupt")
            self.stop_threads()
            sys.exit(0)  
    
    def worker(self):
        """Get path from queue and scan"""
        while not self.wordlist_queue.empty():
            path = self.wordlist_queue.get()
            scan_path(
                path=path,
                option=self.option,
                user_agent=self.random_user_agent()
            )
    
    def stop_threads(self):
        """Close all threads by emptying the queue"""
        while not self.wordlist_queue.empty():
            self.wordlist_queue.get()
            
    def print_options(self):
        """Print out options before starting scan"""
        prefix_width = 24
        print("-------------------------------------------------------")
        print(f"{':: Method'.ljust(prefix_width)}: {self.option.http_method}") 
        print(f"{':: URL'.ljust(prefix_width)}: {self.option.url}")
        print(f"{':: Wordlist'.ljust(prefix_width)}: {self.option.wordlists}")
        print(f"{':: User-Agent'.ljust(prefix_width)}: {self.option.user_agent}")
        print(f"{':: Threads'.ljust(prefix_width)}: {self.option.thread_count}")
        print(f"{':: Timeout'.ljust(prefix_width)}: {self.option.timeout}")
        print(f"{':: Matcher'.ljust(prefix_width)}: {self.option.match_code}")
        print("-------------------------------------------------------")

    def fetch_user_agent(self):
        """Reads User-Agent strings from a file."""
        try:
            with open(self.option.user_agent, "r") as f:
                self.user_agents.extend(f.read().splitlines())
        except FileNotFoundError:
            Logging.error(f"File not found: {self.option.user_agent}")
            exit(1)
        except Exception as e:
            Logging.error(f"Error loading user agent file: {e}")
            exit(1)

    def fetch_wordlist(self):
        """Reads wordlist and adds to queue."""
        try:
            with open(self.option.wordlists, "r") as f:
                for line in f:
                    self.wordlist_queue.put(line.strip())
        except FileNotFoundError:
            Logging.error(f"File not found: {self.option.wordlists}")
            exit(1)
        except Exception as e:
            Logging.error(f"Error loading wordlist file: {e}")
            exit(1)
                
    def random_user_agent(self):
        """Get random user agent from file."""
        return random.choice(self.user_agents)
    
