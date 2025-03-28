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

from queue import Queue
from models.scan_config import ScannerConfig
from views.logger import Logger

class Controller:
    def __init__(self, configs: ScannerConfig):
        self.configs = configs
        self.wordlist = Queue()
        self.user_agent = []

    def run(self):
        self.fetch_wordlist()  
        self.fetch_user_agent() 
            
    def fetch_wordlist(self):
        try:
            with open(self.configs.wordlists, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip()
                    if word:
                        self.wordlist.put(word)
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
            
    