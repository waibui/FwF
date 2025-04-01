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
import time
from collections import defaultdict
from fake_useragent import UserAgent

from utils.file import get_file_content
from view.banner import print_banner
from view.config import print_config
from view.result import print_results
from model.scanner import Scanner

class Controller:
    def __init__(self, args):
        self.args = args
        self.wordlist = get_file_content(self.args.wordlist)
        self.user_agent = UserAgent()
        self.results = []
        self.status_count = defaultdict(int)

    def run(self):
        print_banner()
        print_config(self.args, self.wordlist)
        
        start_time = time.time()
        self.results = asyncio.run(
            Scanner(self.args, self.wordlist, self.user_agent).scan()
        )
        total_time = time.time() - start_time
        self.process_results()
        print_results(total_time, self.results, self.status_count)

    def process_results(self):
        for result in self.results:
            if result: 
                self.status_count[result.status_code] += 1



