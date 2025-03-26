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
    """
    A class to store configuration options for a web request.
    
    Attributes:
        url (str): The target URL.
        wordlists (str): The path to the wordlist file.
        user_agent (str): The User-Agent string to use in requests.
        thread_count (int): The number of concurrent threads.
        timeout (float): The request timeout duration in seconds.
        http_method (str): The HTTP method to use (e.g., GET, POST).
        match_code (str): The response status codes to match.
        output_file (str): The file to save output results.
        cookie (str): The cookie string for authentication.
        proxies (str): The proxy settings for requests.
        allow_redirect (bool): Whether to allow HTTP redirects.
    """
    
    def __init__(self, value: Values = None):
        """Initializes the Option class with provided values."""
        self.url: str = value.url
        self.wordlists: str = value.wordlists
        self.user_agent: str = value.user_agent
        self.thread_count: int = value.thread_count
        self.timeout: float = value.timeout
        self.http_method: str = value.http_method
        self.match_code: str = value.match_code
        self.output_file: str = value.output_file
        self.cookie: str = value.cookie
        self.proxies: str = value.proxies
        self.allow_redirect: bool = value.allow_redirect

