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

from views.file_logger import FileLogger

def _base_logging_console(prefix, message):
        """Prints a log message with a given prefix."""
        print(f"{prefix}: {message}")
    
class Logger:    
    @classmethod
    def info(cls, message):
        """Logs an informational message."""
        _base_logging_console('Info', message)

    @classmethod
    def debug(cls, message):
        """Logs a debug message."""
        _base_logging_console('Debug', message)

    @classmethod
    def warning(cls, message):
        """Logs a warning message."""
        _base_logging_console('Warning', message)

    @classmethod
    def error(cls, message):
        """Logs an error message."""
        _base_logging_console('Error', message)

    @classmethod
    def critical(cls, message):
        """Logs a critical message."""
        _base_logging_console('Critical', message)
        
    @classmethod
    def result_scan(cls, statuscode, message):
        """Logs a result message with a custom status code."""
        _base_logging_console(statuscode, message)
        
    @classmethod    
    def logging_to_file(cls, file_path: str, data: list):
        """Logs data to a file using the FileLogging module."""
        FileLogger.log(file_path, data)