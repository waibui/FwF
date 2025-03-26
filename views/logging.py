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

from views.file_logging import FileLogging

class Logging:
    """
    A logging utility class for handling console and file-based logging.
    
    Methods:
        _base_logging_console(prefix, message):
            A private method to print log messages with a specified prefix.
        
        info(message):
            Logs an informational message.
        
        debug(message):
            Logs a debug message.
        
        warning(message):
            Logs a warning message.
        
        error(message):
            Logs an error message.
        
        critical(message):
            Logs a critical message.
        
        result(statuscode, message):
            Logs a result message with a custom status code.
        
        logging_to_file(file_path, data):
            Logs data to a specified file using FileLogging.
    """
    
    @staticmethod
    def _base_logging_console(prefix, message):
        """Prints a log message with a given prefix."""
        print(f"{prefix}: {message}")
    
    @classmethod
    def info(cls, message):
        """Logs an informational message."""
        cls._base_logging_console('Info', message)

    @classmethod
    def debug(cls, message):
        """Logs a debug message."""
        cls._base_logging_console('Debug', message)

    @classmethod
    def warning(cls, message):
        """Logs a warning message."""
        cls._base_logging_console('Warning', message)

    @classmethod
    def error(cls, message):
        """Logs an error message."""
        cls._base_logging_console('Error', message)

    @classmethod
    def critical(cls, message):
        """Logs a critical message."""
        cls._base_logging_console('Critical', message)
        
    @classmethod
    def result(cls, statuscode, message):
        """Logs a result message with a custom status code."""
        cls._base_logging_console(statuscode, message)
    
    @classmethod    
    def logging_to_file(cls, file_path: str, data: list):
        """Logs data to a file using the FileLogging module."""
        FileLogging.log(file_path, data)