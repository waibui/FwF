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

import os

class Setting:
    
    # General settings
    APP_NAME = "psdir"
    VERSION = "1.0.0"
    USAGE = "psdir.py [-u|--url] target [options]."
    CHOOSE = "Choose -h/--help option for more detail."
    EPILOG = "See 'core/setting.py' for the example configuration file"
    FILETYPE =[".txt", ".log", ".json", ".csv", ".xlsx", ".yaml", ".yml", ".md", ".html", ".xml"]
    
    # Scan settings
    DEFAULT_TIMEOUT = 10
    DEFAULT_THREAD = 50
    DEFAULT_STATUS = [200, 204, 301, 302, 307, 401, 403, 429]
    DEFAULT_METHOD = ["GET", "POST", "HEAD", "PUT", "DELETE"]
    ALLOW_REDIRECT = True
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

    
    
    

    
    