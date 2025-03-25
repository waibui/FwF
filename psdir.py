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

sys.dont_write_bytecode = True

def main():
    parser = parse_args()
    option = Option(parser)
    controller = Controller(option=option)
    
    controller.run()

if __name__ == "__main__":
    main()