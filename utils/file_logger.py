import json
import csv
import yaml
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import sys
from model.result import Result

class FileLogger:
    """
    A class for logging data into files based on their extensions.
    """

    @classmethod
    def log(cls, file_path: str, data: list[Result]):
        """
        Logs data to a file based on its extension, including the executed command.
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
        else:
            cls._log_txt(file_path, formatted_data)

    @staticmethod
    def _get_file_extension(file_path: str) -> str:
        """
        Extracts the file extension from the given file path.
        """
        return file_path.rsplit(".", 1)[-1].lower() if "." in file_path else ""

    @staticmethod
    def _format_data(data: list, command: str) -> list:
        """
        Formats the log data to include a timestamp and the executed command.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = [{"timestamp": timestamp, "command": command}] + [vars(result) for result in data]
        return log_entry

    @staticmethod
    def _log_txt(file_path: str, data: list):
        """
        Logs data to a text file.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            for line in data:
                f.write(str(line) + "\n")

    @staticmethod
    def _log_json(file_path: str, data: list):
        """
        Logs data to a JSON file.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def _log_csv(file_path: str, data: list):
        """
        Logs data to a CSV file, ensuring field consistency.
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
        Logs data to an HTML file with a structured and styled format.
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
        Logs data to a Markdown file in the specified format, including elapsed time for each request.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{data[0]['timestamp']} \n ```{data[0]['command']}```\n\n")
            
            f.write("| **Status Code** | **URL** | **Request Time (s)** |\n")
            f.write("| --- | --- | --- |\n")

            for row in data[1:]:
                f.write(f"| {row['status_code']} | {row['url']} | {row['elapsed_time']} |\n")

    @staticmethod
    def _log_xml(file_path: str, data: list):
        """
        Logs data to an XML file.
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
        Logs data to a YAML file.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    @staticmethod
    def _log_xlsx(file_path: str, data: list):
        """
        Logs data to an Excel file.
        """
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
