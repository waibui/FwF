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

try:
    import sys
    sys.dont_write_bytecode = True
    
    from core.dependencies import install_dependencies
    from parses.command_parser import parse_args
    install_dependencies()
    
    from controllers.scan_controller1 import Controller
    from views.logger import Logger
    
except KeyboardInterrupt:
    errMsg = "[!] Keyboard Interrupt detected!"
    sys.exit(errMsg)
    
def main():
    args = parse_args()
    print(args)
    controller = Controller(args)   
    controller.run()
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass