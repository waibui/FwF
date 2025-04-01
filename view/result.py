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

from config.settings import Setting

def print_results(total_time, results, status_count):
    """
    Prints a comprehensive summary of the scan results, including:
    - Total scan time.
    - HTTP status code summary.
    - Total URLs scanned.
    - Number of valid URLs found.
    
    Parameters:
    - total_time (float): The total time taken for the scan, in seconds.
    """
    # Print scan results summary
    if not results:
        print("No matching paths found.")

    print(Setting.SEPARATOR)
    print(f"[+] Scan Completed in {total_time:.2f}s")
    for status, count in sorted(status_count.items()):
        print(f"- {status}: {count} occurrences")
    print(Setting.SEPARATOR)