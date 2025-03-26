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

class FileLogging:
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
    - `.pdf`: Logs data in PDF format.
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
        elif ext == "yaml" or ext == "yml":
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
            for line in data:
                f.write(str(line) + "\n")

    @staticmethod
    def _log_json(file_path: str, data: list):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def _log_csv(file_path: str, data: list):
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if data and isinstance(data[0], dict):
                writer.writerow(data[0].keys())  # Write headers
                for row in data:
                    writer.writerow(row.values())
            else:
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
            """)
            f.write("<table>")
            if data and isinstance(data[0], dict):
                f.write("<tr>")
                for header in data[0].keys():
                    f.write(f"<th>{header}</th>")
                f.write("</tr>")
                for row in data:
                    f.write("<tr>")
                    for cell in row.values():
                        f.write(f"<td>{cell}</td>")
                    f.write("</tr>")
            f.write("</table></body></html>")

    @staticmethod
    def _log_md(file_path: str, data: list):
        with open(file_path, "w", encoding="utf-8") as f:
            if data and isinstance(data[0], dict):
                headers = " | ".join(data[0].keys())
                f.write(f"| {headers} |\n")
                f.write(f"| {' | '.join(['---'] * len(data[0]))} |\n")
                for row in data:
                    f.write(f"| {' | '.join(map(str, row.values()))} |\n")

    @staticmethod
    def _log_xml(file_path: str, data: list):
        root = ET.Element("logs")
        for item in data:
            entry = ET.SubElement(root, "entry")
            for key, value in item.items():
                ET.SubElement(entry, key).text = str(value)
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def _log_yaml(file_path: str, data: list):
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    @staticmethod
    def _log_xlsx(file_path: str, data: list):
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
