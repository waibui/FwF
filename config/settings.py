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
#
#  Author: waibui
#  Email: waibui@example.com
#  Website: https://github.com/waibui

import os

class Setting:
    
    # General settings
    APP_NAME = "psdir"
    VERSION = "1.0.0"
    USAGE = "psdir.py [-u|--url] target [options]."
    CHOOSE = "Choose -h/--help option for more detail."
    EPILOG = "See 'config/settings.py' for the example configuration file"
    FILETYPE =[".txt", ".log", ".json", ".csv", ".xlsx", ".yaml", ".yml", ".md", ".html", ".xml"]
    
    # Scan settings
    DEFAULT_TIMEOUT = 10
    DEFAULT_THREAD = 50
    DEFAULT_STATUS = [200, 204, 301, 302, 307, 401, 403, 429]
    DEFAULT_METHOD = ["GET", "POST", "HEAD", "PUT", "DELETE"]
    ALLOW_REDIRECT = False
    ALLOW_SCRAPE = False
    
    # Application directory
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    
    # Wordlist & User-Agent configuration
    DEFAULT_WORDLIST = os.path.join(BASE_DIR, "data", "wordlist.txt")
    DEFAULT_USER_AGENT = os.path.join(BASE_DIR, "data", "user-agent.txt")
    
    # Requirement file
    REQUIREMENTS = os.path.join(BASE_DIR, "requirements.txt")
    
    # Banner
    BANNER = '''
    ██████╗ ███████╗██████╗ ██╗██████╗   %s
    ██╔══██╗██╔════╝██╔══██╗██║██╔══██╗  %s
    ██████╔╝███████╗██║  ██║██║██████╔╝  %s
    ██╔═══╝ ╚════██║██║  ██║██║██╔══██╗  %s
    ██║     ███████║██████╔╝██║██║  ██║  %s
    ╚═╝     ╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝  %s                                                                         
    '''
    
    # Separator
    SEPARATOR = "-" * 60

    
    
    

    
    