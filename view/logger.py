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

import logging

class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            return record.getMessage()  
        return f"{record.levelname} - {record.getMessage()}" 

logger = logging.getLogger("AppLogger")
logger.setLevel(logging.DEBUG) 

console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())

if logger.hasHandlers():
    logger.handlers.clear()

logger.addHandler(console_handler)
