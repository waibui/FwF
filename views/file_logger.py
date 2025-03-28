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

import json
import csv
import yaml
import xml.etree.ElementTree as ET
import pandas as pd

class FileLogger:
    """
    A class for logging data into files based on their extensions.
    
    Supported formats:
    - `.txt`: Logs data as plain text.
    - `.json`: Logs data in JSON format.
    - `.csv`: Logs data in CSV format.
    - `.html`: Logs data in an HTML table format.
    - `.md`: Logs data in Markdown table format.
    - `.xml`: Logs data in XML format.
    - `.yaml`: Logs data in YAML format.
    - `.xlsx`: Logs data in Excel format.
    """

    @classmethod
    def log(cls, file_path: str, data: list):
        """
        Logs data to a file based on its extension.
        """
        ext = cls._get_file_extension(file_path)

        if ext == "json":
            cls._log_json(file_path, data)
        elif ext == "csv":
            cls._log_csv(file_path, data)
        elif ext == "html":
            cls._log_html(file_path, data)
        elif ext == "md":
            cls._log_md(file_path, data)
        elif ext == "xml":
            cls._log_xml(file_path, data)
        elif ext in ["yaml", "yml"]:
            cls._log_yaml(file_path, data)
        elif ext == "xlsx":
            cls._log_xlsx(file_path, data)
        else:
            cls._log_txt(file_path, data)

    @staticmethod
    def _get_file_extension(file_path: str) -> str:
        return file_path.rsplit(".", 1)[-1].lower() if "." in file_path else ""

    @staticmethod
    def _log_txt(file_path: str, data: list):
        with open(file_path, "w", encoding="utf-8") as f:
            for status_code, url in data:
                f.write(f"{status_code}, {url}\n")

    @staticmethod
    def _log_json(file_path: str, data: list):
        json_data = [{"status_code": status_code, "url": url} for status_code, url in data]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def _log_csv(file_path: str, data: list):
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["status_code", "url"])  
            writer.writerows(data)

    @staticmethod
    def _log_html(file_path: str, data: list):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("""
            <html>
            <head>
                <title>Log Data</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; padding: 20px; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid black; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                </style>
            </head>
            <body>
            <h2>Log Data</h2>
            <table>
            <tr><th>Status Code</th><th>URL</th></tr>
            """)

            for status_code, url in data:
                f.write(f"<tr><td>{status_code}</td><td>{url}</td></tr>\n")

            f.write("</table></body></html>")

    @staticmethod
    def _log_md(file_path: str, data: list):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# Log Data\n\n")  
            f.write("| Status Code | URL |\n")
            f.write("|------------|-----|\n")
            for status_code, url in data:
                f.write(f"| {status_code} | {url} |\n")

    @staticmethod
    def _log_xml(file_path: str, data: list):
        root = ET.Element("logs")
        
        for status_code, url in data:
            entry = ET.SubElement(root, "entry")
            ET.SubElement(entry, "status_code").text = str(status_code)
            ET.SubElement(entry, "url").text = url

        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def _log_yaml(file_path: str, data: list):
        yaml_data = [{"status_code": status_code, "url": url} for status_code, url in data]
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(yaml_data, f, allow_unicode=True, default_flow_style=False)

    @staticmethod
    def _log_xlsx(file_path: str, data: list):
        df = pd.DataFrame(data, columns=["status_code", "url"])
        df.to_excel(file_path, index=False)
