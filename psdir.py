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

#=================================#
#      dont create pycache        #   
#=================================#
import sys
sys.dont_write_bytecode = True

#=================================#
#       check dependencies        #   
#=================================#
from core.dependencies import install_dependencies
install_dependencies()

from parses.command_parser import parse_args
from models.option import Option
from controllers.scan_controller import Controller
from views.logger import Logging
from core.setting import DEFAULT_METHOD, USAGE

def main():
    """Main function to run the Web Path Scanner."""
    try:
        parser = parse_args()
        options = Option(parser)

        if not options.url:
            Logging.error(f"No URL provided. Please specify a valid URL.\n{USAGE}")
            sys.exit(1)

        options.http_method = options.http_method.upper()
        if options.http_method not in DEFAULT_METHOD:
            Logging.error(f"Invalid HTTP method '{options.http_method}'. Allowed methods: {DEFAULT_METHOD}")
            sys.exit(1)

        Controller(option=options).run()

    except KeyboardInterrupt:
        sys.exit(0)

    except Exception as e:
        Logging.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
