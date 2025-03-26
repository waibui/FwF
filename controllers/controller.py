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

import requests
import time
import random
import sys

from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from models.option import Option
from views.logging import Logging
from controllers.scan import scan

class Controller:
    """
    A multi-threaded controller for performing web path scanning.

    This class manages the scanning process using a queue-based approach and 
    thread pooling to optimize scanning speed. It handles wordlists, 
    user-agent selection, cookies, proxies, and result aggregation.

    Attributes:
        option (Option): The configuration options for the scan.
        wordlist_queue (Queue): A queue to manage wordlist paths for scanning.
        user_agents (list): A list of user-agent strings for random selection.
        results (list): A list to store scan results.
        session (requests.Session): A persistent session object for efficient HTTP requests.
        prefix_width (int): The width for formatting printed scan options.
    """

    def __init__(self, option: Option):
        """
        Initializes the Controller with the provided scan options.

        Args:
            option (Option): The configuration settings for the scan.
        """
        self.option = option
        self.wordlist_queue = Queue()
        self.user_agents = []
        self.results = []
        self.session = requests.Session()
        self.prefix_width = 24

    def run(self):
        """
        Starts the scanning process using multiple threads.

        This method loads user agents, reads the wordlist, handles cookies and proxies, 
        and then starts scanning using a ThreadPoolExecutor.
        """
        self.fetch_user_agent()
        self.fetch_wordlist()
        self.handle_cookie()
        self.handle_proxy()
        self.print_options()

        start_t = time.time()

        try:
            executor = ThreadPoolExecutor(max_workers=self.option.thread_count)
            while not self.wordlist_queue.empty():
                executor.submit(self.worker, self.wordlist_queue.get())

            executor.shutdown(wait=True) 
            
            if self.option.output_file is not None:
                Logging.logging_to_file(self.option.output_file, self.results)
                
        except KeyboardInterrupt:
            print("\n[!] Keyboard Interrupt detected! Stopping all threads...")
            if executor:
                executor.shutdown(wait=False, cancel_futures=True) 
            sys.exit(0)  
        except Exception:
            sys.exit(0)
        finally:
            end_t = time.time()
            self.statistical(end_t - start_t)

    def worker(self, path):
        """
        Processes a single path from the queue and performs a scan.

        Args:
            path (str): The URL path to be scanned.
        """
        result = scan(
            session=self.session,
            path=path,
            option=self.option,
            user_agent=self.random_user_agent(),
            cookie=self.cookie,
            proxy=self.proxies,
            wordlist_queue=self.wordlist_queue
        )
        if result:
            Logging.result(result['status'], result['url'])
            self.results.append(result)
        self.wordlist_queue.task_done()

    def print_options(self):
        """
        Prints the configured scan options before starting the scan.
        """
        print("-------------------------------------------------------")
        print(f"{':: Method'.ljust(self.prefix_width)}: {self.option.http_method}") 
        print(f"{':: URL'.ljust(self.prefix_width)}: {self.option.url}")
        print(f"{':: Wordlist'.ljust(self.prefix_width)}: {self.option.wordlists}")
        print(f"{':: User-Agent'.ljust(self.prefix_width)}: {self.option.user_agent}")
        print(f"{':: Threads'.ljust(self.prefix_width)}: {self.option.thread_count}")
        print(f"{':: Timeout'.ljust(self.prefix_width)}: {self.option.timeout}")
        print(f"{':: Matcher'.ljust(self.prefix_width)}: {self.option.match_code}")
        print("-------------------------------------------------------")

    def statistical(self, total_t):
        """
        Generates and prints statistical data based on HTTP status codes found.

        Args:
            total_t (float): The total time taken for the scan.
        """
        if not self.results:
            print("No results found.")
            return

        stats = defaultdict(int)
        for result in self.results:
            stats[result['status']] += 1

        print("-------------------------------------------------------")
        print(f"{':: Total time'.ljust(self.prefix_width)}: {total_t:.2f}(s)")
        for status, count in sorted(stats.items()):
            print(f"{f':: HTTP {status}'.ljust(self.prefix_width)}: {count} path(s)") 
        print("-------------------------------------------------------")

    def fetch_user_agent(self):
        """
        Reads user-agent strings from a file and stores them in a list.

        Raises:
            FileNotFoundError: If the user-agent file does not exist.
        """
        try:
            with open(self.option.user_agent, "r") as f:
                self.user_agents = f.read().splitlines()
        except FileNotFoundError:
            Logging.error(f"Invalid user-agent path '{self.option.user_agent}'")
            sys.exit(1)

    def fetch_wordlist(self):
        """
        Reads the wordlist from a file and stores paths in the queue.

        Raises:
            FileNotFoundError: If the wordlist file does not exist.
        """
        try:
            with open(self.option.wordlists, "r") as f:
                words = [line.strip() for line in f if line.strip()]
                for word in words:
                    self.wordlist_queue.put(word)
        except FileNotFoundError:
            Logging.error(f"Invalid wordlist path '{self.option.wordlists}'")
            sys.exit(1)

    def parse_key_value_string(self, input_string):
        """
        Parses a key-value string into a dictionary.

        The input format should be "key:value,key2:value2".

        Args:
            input_string (str): A comma-separated string of key-value pairs.

        Returns:
            dict or None: A dictionary containing parsed key-value pairs, or None if input is empty or invalid.
        """
        if not input_string:
            return None

        try:
            return {
                key.strip(): value.strip()
                for pair in input_string.split(',')
                if (key := pair.split(":", 1)[0]) and (value := pair.split(":", 1)[1])
            }
        except Exception:
            return None

    def handle_cookie(self):
        """
        Processes and stores cookies as a dictionary.
        """
        self.cookie = self.parse_key_value_string(self.option.cookie)

    def handle_proxy(self):
        """
        Processes and stores proxies as a dictionary.
        """
        self.proxies = self.parse_key_value_string(self.option.proxies)

    def random_user_agent(self):
        """
        Returns a random User-Agent string from the list.

        Returns:
            str: A randomly selected User-Agent string, or a default one if none are loaded.
        """
        return random.choice(self.user_agents) if self.user_agents else "Mozilla/5.0"