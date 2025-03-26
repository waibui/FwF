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

from optparse import Values

class Option:
    def __init__(self, value: Values = None):
        self.url: str = value.url
        self.wordlists: str = value.wordlists
        self.user_agent: str = value.user_agent
        self.thread_count: int = value.thread_count
        self.timeout: float = value.timeout
        self.http_method: str = value.http_method
        self.match_code: str = value.match_code
        self.output_file: str = value.output_file
        self.quiet: bool = value.quiet
        self.cookie: str = value.cookie
        self.proxies: str = value.proxies
        self.auth: str = value.auth
        self.allow_redirect: bool = value.allow_redirect
