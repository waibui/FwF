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

class Logging:
    @staticmethod
    def _base_logging_console(prefix, message):
        print(f"[{prefix}] {message}")
    
    @classmethod
    def info(cls, message):
        cls._base_logging_console('INFO', message)

    @classmethod
    def debug(cls, message):
        cls._base_logging_console('DEBUG', message)

    @classmethod
    def warning(cls, message):
        cls._base_logging_console('WARNING', message)

    @classmethod
    def error(cls, message):
        cls._base_logging_console('ERROR', message)

    @classmethod
    def critical(cls, message):
        cls._base_logging_console('CRITICAL', message)
        
    @classmethod
    def result(cls, statuscode, message):
        cls._base_logging_console(statuscode, message)