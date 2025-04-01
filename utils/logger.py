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
import sys
from utils.file_logger import FileLogger

class Logger:
    _instance = None 

    class CustomFormatter(logging.Formatter):
        def format(self, record):
            if record.levelno == logging.INFO:
                return f"{record.getMessage()}"
            elif record.levelno == logging.WARNING:
                return f"Warning: {record.getMessage()}"
            elif record.levelno == logging.ERROR:
                return f"Error: {record.getMessage()}"
            elif record.levelno == logging.DEBUG:
                return f"Debug: {record.getMessage()}"
            return f"{record.levelname} - {record.getMessage()}"

    def __new__(cls, log_file=None):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(log_file)
        return cls._instance

    def _initialize(self, log_file):
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.DEBUG)  

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.CustomFormatter())
        self.logger.addHandler(console_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(self.CustomFormatter())
            self.logger.addHandler(file_handler)

    @classmethod
    def log(cls, level, message):
        instance = cls._instance or cls()
        instance.logger.log(level, message)

    @classmethod
    def info(cls, message):
        cls.log(logging.INFO, message)

    @classmethod
    def warning(cls, message):
        cls.log(logging.WARNING, message)

    @classmethod
    def error(cls, message):
        cls.log(logging.ERROR, message)

    @classmethod
    def debug(cls, message):
        cls.log(logging.DEBUG, message)
    
    @classmethod
    def log_to_file(cls, file_path,message):
        FileLogger.log(file_path, message)
