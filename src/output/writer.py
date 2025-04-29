#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

import os
import sys
import json
import csv
import yaml
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from datetime import datetime
from src.models.result import ScanResult
from src.output.logger import Logger
from src.constants.default import ALLOW_OUTPUT_FORMAT

logger = Logger.get_instance()

class FileWriter:
    """Handles writing scan results to various file formats."""
    
    @staticmethod
    def write_results(results: list[ScanResult], output_file: str, config=None) -> bool:
        """
        Write scan results to the specified output file.
        
        Args:
            results: Set of ScanResult objects
            output_file: Path to the output file
            config: ScanConfig object containing command information
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not output_file:
            return False
            
        try:
            file_ext = output_file.split('.')[-1].lower()
            
            if file_ext not in ALLOW_OUTPUT_FORMAT:
                logger.error("Output", f"Unsupported file format: {file_ext}. "
                            f"Supported formats: {', '.join(ALLOW_OUTPUT_FORMAT)}")
                return False

            command = " ".join(sys.argv) if len(sys.argv) > 0 else "fwf [unknown command]"
                
            sorted_results = sorted(results, key=lambda x: (x.status, x.url))
            
            if file_ext in ["txt", "log"]:
                return FileWriter._write_txt(sorted_results, output_file, command)
            elif file_ext == "json":
                return FileWriter._write_json(sorted_results, output_file, command)
            elif file_ext == "csv":
                return FileWriter._write_csv(sorted_results, output_file, command)
            elif file_ext == "xlsx":
                return FileWriter._write_xlsx(sorted_results, output_file, command)
            elif file_ext in ["yaml", "yml"]:
                return FileWriter._write_yaml(sorted_results, output_file, command)
            elif file_ext == "md":
                return FileWriter._write_markdown(sorted_results, output_file, command)
            elif file_ext == "html":
                return FileWriter._write_html(sorted_results, output_file, command)
            elif file_ext == "xml":
                return FileWriter._write_xml(sorted_results, output_file, command)
            
            return False
        except Exception as e:
            logger.error("Output", f"Failed to write results: {str(e)}")
            return False
    
    @staticmethod
    def _write_txt(results: list[ScanResult], output_file: str, command: str) -> bool:
        """Write results to a plain text file."""
        try:
            with open(output_file, 'w') as f:
                f.write(f"# FwF Scanner Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Command: {command}\n\n")
                
                for result in results:
                    f.write(f"URL: {result.url}\n")
                    f.write(f"Status: {result.status}\n")
                    f.write(f"Content-Length: {result.content_length}\n")
                    f.write(f"Response-Time: {result.response_time:.3f}s\n")
                    f.write(f"Content-Type: {result.content_type or 'N/A'}\n")
                    f.write("-" * 60 + "\n")
            
            logger.info("Output", f"Results written to {output_file}")
            return True
        except Exception as e:
            logger.error("Output", f"Failed to write text file: {str(e)}")
            return False
    
    @staticmethod
    def _write_json(results: list[ScanResult], output_file: str, command: str) -> bool:
        """Write results to a JSON file."""
        try:
            data = {
                "command": command,
                "scan_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "results": [
                    {
                        "url": result.url,
                        "path": result.url,
                        "status": result.status,
                        "content_length": result.content_length,
                        "response_time": round(result.response_time, 3),
                        "content_type": result.content_type or "N/A",
                    } 
                    for result in results
                ]
            }
            
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info("Output", f"Results written to {output_file}")
            return True
        except Exception as e:
            logger.error("Output", f"Failed to write JSON file: {str(e)}")
            return False
    
    @staticmethod
    def _write_csv(results: list[ScanResult], output_file: str, command: str) -> bool:
        """Write results to a CSV file."""
        try:
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                f.write(f"# Command: {command}\n")
                f.write(f"# Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                writer.writerow(['URL', 'Status', 'Content-Length', 'Response-Time', 'Content-Type'])
                
                for result in results:
                    writer.writerow([
                        result.url, 
                        result.status,
                        result.content_length,
                        f"{result.response_time:.3f}",
                        result.content_type or "N/A"
                    ])
                    
            logger.info("Output", f"Results written to {output_file}")
            return True
        except Exception as e:
            logger.error("Output", f"Failed to write CSV file: {str(e)}")
            return False
    
    @staticmethod
    def _write_xlsx(results: list[ScanResult], output_file: str, command: str) -> bool:
        """Write results to an Excel file."""
        try:
            try:
                import pandas as pd
                from openpyxl import Workbook
                from openpyxl.utils.dataframe import dataframe_to_rows
            except ImportError:
                logger.error("Output", "Excel output requires pandas and openpyxl packages. "
                           "Install with: pip install pandas openpyxl")
                return False
            
            data = []
            for result in results:
                data.append({
                    'URL': result.url,
                    'Status': result.status,
                    'Content-Length': result.content_length,
                    'Response-Time': f"{result.response_time:.3f}",
                    'Content-Type': result.content_type or "N/A"
                })
            
            wb = Workbook()
            ws_meta = wb.active
            ws_meta.title = "Metadata"
            ws_meta.append(["FwF Scanner Results"])
            ws_meta.append(["Command", command])
            ws_meta.append(["Scan Date", datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            ws_meta.append(["Total Results", len(results)])
            
            ws_results = wb.create_sheet(title="Results")
            df = pd.DataFrame(data)
            for r in dataframe_to_rows(df, index=False, header=True):
                ws_results.append(r)
                
            wb.save(output_file)
            
            logger.info("Output", f"Results written to {output_file}")
            return True
        except Exception as e:
            logger.error("Output", f"Failed to write Excel file: {str(e)}")
            return False
    
    @staticmethod
    def _write_yaml(results: list[ScanResult], output_file: str, command: str) -> bool:
        """Write results to a YAML file."""
        try:
            data = {
                "command": command,
                "scan_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "results": [
                    {
                        "url": result.url,
                        "status": result.status,
                        "content_length": result.content_length,
                        "response_time": round(result.response_time, 3),
                        "content_type": result.content_type or "N/A"
                    } 
                    for result in results
                ]
            }
            
            with open(output_file, 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
                
            logger.info("Output", f"Results written to {output_file}")
            return True
        except Exception as e:
            logger.error("Output", f"Failed to write YAML file: {str(e)}")
            return False
    
    @staticmethod
    def _write_markdown(results: list[ScanResult], output_file: str, command: str) -> bool:
        """Write results to a Markdown file."""
        try:
            with open(output_file, 'w') as f:
                f.write(f"# FwF Scanner Results\n\n")
                f.write(f"**Command:** `{command}`\n\n")
                f.write(f"*Scan completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                
                f.write("| URL | Status | Content-Length | Response-Time | Content-Type |\n")
                f.write("|-----|--------|---------------|---------------|-------------|\n")
                
                for result in results:
                    f.write(f"| {result.url} | {result.status} | ")
                    f.write(f"{result.content_length} | {result.response_time:.3f}s | ")
                    f.write(f"{result.content_type or 'N/A'} |\n")
                
            logger.info("Output", f"Results written to {output_file}")
            return True
        except Exception as e:
            logger.error("Output", f"Failed to write Markdown file: {str(e)}")
            return False
    
    @staticmethod
    def _write_html(results: list[ScanResult], output_file: str, command: str) -> bool:
        """Write results to an HTML file."""
        try:
            with open(output_file, 'w') as f:
                f.write('<!DOCTYPE html>\n')
                f.write('<html lang="en">\n')
                f.write('<head>\n')
                f.write('  <meta charset="UTF-8">\n')
                f.write('  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
                f.write('  <title>FwF Scanner Results</title>\n')
                f.write('  <style>\n')
                f.write('    body { font-family: Arial, sans-serif; margin: 20px; }\n')
                f.write('    table { border-collapse: collapse; width: 100%; }\n')
                f.write('    th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }\n')
                f.write('    th { background-color: #f2f2f2; }\n')
                f.write('    tr:nth-child(even) { background-color: #f9f9f9; }\n')
                f.write('    .header { margin-bottom: 20px; }\n')
                f.write('    .command { font-family: monospace; background-color: #f8f8f8; padding: 10px; border-radius: 5px; }\n')
                f.write('  </style>\n')
                f.write('</head>\n')
                f.write('<body>\n')
                f.write('  <div class="header">\n')
                f.write('    <h1>FwF Scanner Results</h1>\n')
                f.write(f'    <div class="command"><strong>Command:</strong> {command}</div>\n')
                f.write(f'    <p>Scan completed: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>\n')
                f.write('  </div>\n')
                f.write('  <table>\n')
                f.write('    <tr>\n')
                f.write('      <th>URL</th>\n')
                f.write('      <th>Status</th>\n')
                f.write('      <th>Content-Length</th>\n')
                f.write('      <th>Response-Time</th>\n')
                f.write('      <th>Content-Type</th>\n')
                f.write('    </tr>\n')
                
                for result in results:
                    f.write('    <tr>\n')
                    f.write(f'      <td>{result.url}</td>\n')
                    f.write(f'      <td>{result.status}</td>\n')
                    f.write(f'      <td>{result.content_length}</td>\n')
                    f.write(f'      <td>{result.response_time:.3f}s</td>\n')
                    f.write(f'      <td>{result.content_type or "N/A"}</td>\n')
                    f.write('    </tr>\n')
                
                f.write('  </table>\n')
                f.write('</body>\n')
                f.write('</html>\n')
                
            logger.info("Output", f"Results written to {output_file}")
            return True
        except Exception as e:
            logger.error("Output", f"Failed to write HTML file: {str(e)}")
            return False
    
    @staticmethod
    def _write_xml(results: list[ScanResult], output_file: str, command: str) -> bool:
        """Write results to an XML file."""
        try:
            root = ET.Element("FwFScanResults")
            ET.SubElement(root, "Command").text = command
            ET.SubElement(root, "ScanDate").text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            results_element = ET.SubElement(root, "Results")
            
            for result in results:
                item = ET.SubElement(results_element, "Result")
                ET.SubElement(item, "URL").text = result.url
                ET.SubElement(item, "Status").text = str(result.status)
                ET.SubElement(item, "ContentLength").text = str(result.content_length)
                ET.SubElement(item, "ResponseTime").text = f"{result.response_time:.3f}"
                ET.SubElement(item, "ContentType").text = result.content_type or "N/A"
            
            xml_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            
            with open(output_file, 'w') as f:
                f.write(xml_string)
                
            logger.info("Output", f"Results written to {output_file}")
            return True
        except Exception as e:
            logger.error("Output", f"Failed to write XML file: {str(e)}")
            return False