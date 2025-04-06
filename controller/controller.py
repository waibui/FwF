# -*- coding: utf-8 -*-
#  psdir - Web Path Scanner
#  Copyright (c) 2025 waibui
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import asyncio
import time
from collections import defaultdict
from fake_useragent import UserAgent

from utils.file import get_file_content
from view.banner import print_banner
from view.config import print_config
from view.result import print_results
from model.scanner import Scanner
from utils.logger import Logger

class Controller:
    def __init__(self, args):
        self.args = args
        self.wordlist = get_file_content(self.args.wordlist)
        self.user_agent = get_file_content(self.args.user_agent) if self.args.user_agent else UserAgent()
        self.results = []
        self.status_count = defaultdict(int)

    def run(self):
        print_banner()
        print_config(self.args, self.wordlist)

        try:
            start_time = time.time()
            self.results = asyncio.run(
                Scanner(self.args, self.wordlist, self.user_agent).scan()
            )
       
            total_time = time.time() - start_time
            self.process_results()
            print_results(total_time, self.results, self.status_count)
            
            if self.args.output:
                for out in self.args.output.split(','):
                    Logger.log_to_file(out, self.results)

        except KeyboardInterrupt:
            print("[!] User interrupted. Exiting gracefully.")

    def process_results(self):
        for result in self.results:
            if result: 
                self.status_count[result.status_code] += 1



