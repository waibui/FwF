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

BANNER = '''
██████╗ ███████╗██████╗ ██╗██████╗   %s
██╔══██╗██╔════╝██╔══██╗██║██╔══██╗  %s
██████╔╝███████╗██║  ██║██║██████╔╝  %s
██╔═══╝ ╚════██║██║  ██║██║██╔══██╗  %s
██║     ███████║██████╔╝██║██║  ██║  %s
╚═╝     ╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝  %s                                                                         
'''
USAGE = "Usage: psdir.py [-u|--url] target [options].\nChoose -h/--help option for more detail."
VERSION = "1.0.0"

# OPTION DEFAULT
WORDLIST_PATH = "statics/wordlist.txt"
USER_AGENT_PATH = "statics/user-agent.txt"
DEFAULT_METHOD = "GET,POST,HEAD,PUT,DELETE"
