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
from parse.parse_cmd import parse_args
from models.option import Option
from controllers.controller import Controller
from views.logging import Logging
from core.setting import DEFAULT_METHOD, USAGE

sys.dont_write_bytecode = True

def main():
    try:
        parser = parse_args()
        options = Option(parser)
        
        if not options.url:
            Logging.error(f"No URL provided. Please specify a valid URL. \n{USAGE}")
            exit(1)
            
        if options.http_method not in DEFAULT_METHOD:
            Logging.error(f"Invalid HTTP method '{options.http_method}'. Allowed methods: {DEFAULT_METHOD}")
            exit(1)
        
        controller = Controller(option=options)
        controller.run()
    
    except Exception as e:
        Logging.error(f"Unexpected error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
