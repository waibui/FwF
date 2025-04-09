# -*- coding: utf-8 -*-
#  psdir - Web Path Scanner
#  Copyright (c) 2025 waibui
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import logging
import sys
import json
import csv
import yaml
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
from model.result import Result


class Logger:
    """
    Singleton Logger class for console and file logging in multiple formats.
    """
    _instance = None

    class CustomFormatter(logging.Formatter):
        """
        Custom log formatter to simplify log output depending on log level.
        """
        def format(self, record):
            """Format log message based on its severity level."""
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
        """
        Create a single instance of Logger (singleton pattern).
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(log_file)
        return cls._instance

    def _initialize(self, log_file):
        """
        Set up logger handlers for console and optional file logging.
        """
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
        """
        Log a message with the specified logging level.
        """
        instance = cls._instance or cls()
        instance.logger.log(level, message)

    @classmethod
    def info(cls, message):
        """
        Log an info-level message.
        """
        cls.log(logging.INFO, message)

    @classmethod
    def warning(cls, message):
        """
        Log a warning-level message.
        """
        cls.log(logging.WARNING, message)

    @classmethod
    def error(cls, message):
        """
        Log an error-level message.
        """
        cls.log(logging.ERROR, message)

    @classmethod
    def debug(cls, message):
        """
        Log a debug-level message.
        """
        cls.log(logging.DEBUG, message)

    @classmethod
    def log_to_file(cls, file_path: str, data: list[Result]):
        """
        Log result data to a file, formatted based on the file extension.
        """
        ext = cls._get_file_extension(file_path)
        command = " ".join(sys.argv)
        formatted_data = cls._format_data(data, command)

        if ext == "json":
            cls._log_json(file_path, formatted_data)
        elif ext == "csv":
            cls._log_csv(file_path, formatted_data)
        elif ext == "html":
            cls._log_html(file_path, formatted_data)
        elif ext == "md":
            cls._log_md(file_path, formatted_data)
        elif ext == "xml":
            cls._log_xml(file_path, formatted_data)
        elif ext in ["yaml", "yml"]:
            cls._log_yaml(file_path, formatted_data)
        elif ext == "xlsx":
            cls._log_xlsx(file_path, formatted_data)
        elif ext == "log":
            cls._log_log(file_path, formatted_data)
        else:
            cls._log_txt(file_path, formatted_data)

    @staticmethod
    def _get_file_extension(file_path: str) -> str:
        """
        Extract and return the file extension from a file path.
        """
        return file_path.rsplit(".", 1)[-1].lower() if "." in file_path else ""

    @staticmethod
    def _format_data(data: list, command: str) -> list:
        """
        Format the result data with timestamp and executed command.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [{"timestamp": timestamp, "command": command}] + [vars(result) for result in data]

    @staticmethod
    def _log_txt(file_path: str, data: list):
        """
        Save logs to a plain text file.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            for line in data:
                f.write(str(line) + "\n")

    @staticmethod
    def _log_log(file_path: str, data: list):
        """
        Save logs to a standard .log file format.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"[{data[0]['timestamp']}] Executed Command: {data[0]['command']}\n")
            for row in data[1:]:
                f.write(f"[{row['status_code']}] {row['url']} ({row['elapsed_time']}s)\n")

    @staticmethod
    def _log_json(file_path: str, data: list):
        """
        Save logs in JSON format.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def _log_csv(file_path: str, data: list):
        """
        Save logs in CSV format.
        """
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["status_code", "url", "elapsed_time"])
            writer.writeheader()
            for row in data[1:]:
                writer.writerow({
                    "status_code": row["status_code"],
                    "url": row["url"],
                    "elapsed_time": row["elapsed_time"]
                })

    @staticmethod
    def _log_html(file_path: str, data: list):
        """
        Save logs in HTML format with a styled table.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Log Data</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h2 { color: #333; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
</head>
<body>
""")
            f.write(f"<h2>Log Timestamp</h2><p>{data[0]['timestamp']}</p>")
            f.write(f"<h2>Executed Command</h2><pre>{data[0]['command']}</pre>")
            f.write("<h2>Request Logs</h2>")
            f.write("<table><tr><th>Status Code</th><th>URL</th><th>Request Time (s)</th></tr>")
            for row in data[1:]:
                f.write(f"<tr><td>{row['status_code']}</td><td>{row['url']}</td><td>{row['elapsed_time']}</td></tr>")
            f.write("</table></body></html>")

    @staticmethod
    def _log_md(file_path: str, data: list):
        """
        Save logs in Markdown format.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{data[0]['timestamp']}\n\n")
            f.write(f"```shell\n{data[0]['command']}\n```\n\n")
            f.write("| **Status Code** | **URL** | **Request Time (s)** |\n")
            f.write("| --- | --- | --- |\n")
            for row in data[1:]:
                f.write(f"| {row['status_code']} | {row['url']} | {row['elapsed_time']} |\n")

    @staticmethod
    def _log_xml(file_path: str, data: list):
        """
        Save logs in XML format.
        """
        root = ET.Element("logs")
        for item in data:
            entry = ET.SubElement(root, "entry")
            for key, value in item.items():
                ET.SubElement(entry, key).text = str(value)
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def _log_yaml(file_path: str, data: list):
        """
        Save logs in YAML format.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    @staticmethod
    def _log_xlsx(file_path: str, data: list):
        """
        Save logs in Excel (.xlsx) format.
        """
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)