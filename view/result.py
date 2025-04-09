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

from core.config import Setting

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