#!/usr/bin/env python

"""
Copyright (c) 2025 WaiBui
See the file 'LICENSE' for copying permission
"""

from optparse import OptionParser, OptionGroup, Values
from pkg.core.settings import VERSION, USAGE, EPILOG

def parse_arguments() -> Values:
    """
    Parse arguments from the user's CLI input
    """
    parser = OptionParser(usage=USAGE, epilog=EPILOG, version=f"psdir v{VERSION}")

    # 🟢 Mandatory Options: These options must be provided by the user
    mandatory = OptionGroup(parser, "Mandatory Options")
    mandatory.add_option(
        "-u", "--url",
        action="append",
        dest="urls",
        metavar="URL",
        help="Target URL(s), can use multiple flags"
    )
    mandatory.add_option(
        "-w", "--wordlist",
        action="append",
        dest="wordlists",
        metavar="WORDLIST",
        help="Wordlist path, can use multiple flags"
    )

    # 🟡 General Settings: These options control the scanning behavior
    general = OptionGroup(parser, "General Settings")
    general.add_option(
        "-t", "--threads",
        action="store",
        type="int",
        dest="thread_count",
        metavar="THREADS",
        help="Number of threads (default: 10)"
    )
    general.add_option(
        "-p", "--protocol",
        action="store",
        dest="protocol",
        metavar="PROTOCOL",
        help="HTTP protocol (default: https)"
    )
    general.add_option(
        "-m", "--method",
        action="append",
        dest="methods",
        metavar="METHOD",
        help="HTTP methods, can use multiple flags (e.g., GET, POST)"
    )
    general.add_option(
        "-o", "--output",
        action="store",
        dest="output_file",
        metavar="FILE",
        help="Save output results to file"
    )

    # 🔴 Advanced Scanning Options: Additional features for better scanning
    advanced = OptionGroup(parser, "Advanced Scanning Options")
    advanced.add_option(
        "-r", "--recursive",
        action="store_true",
        dest="recursive",
        help="Enable recursive directory scan"
    )
    advanced.add_option(
        "-s", "--status",
        action="append",
        type="int",
        dest="status_codes",
        metavar="STATUS",
        help="Filter by HTTP status codes (e.g., 200, 403, 404)"
    )
    advanced.add_option(
        "-e", "--extensions",
        action="append",
        dest="extensions",
        metavar="EXT",
        help="File extensions to scan (e.g., php, html, txt)"
    )

    # 🟠 HTTP Request Options: Customize HTTP request headers, cookies, etc.
    http = OptionGroup(parser, "HTTP Request Options")
    http.add_option(
        "-H", "--header",
        action="append",
        dest="headers",
        metavar="HEADER",
        help="Add custom HTTP headers (e.g., 'User-Agent: Mozilla/5.0')"
    )
    http.add_option(
        "-c", "--cookie",
        action="store",
        dest="cookie",
        metavar="COOKIE",
        help="Add custom cookies (e.g., 'PHPSESSID=12345')"
    )
    http.add_option(
        "-d", "--delay",
        action="store",
        type="float",
        dest="delay",
        metavar="SECONDS",
        help="Set delay between requests (default: 0.0)"
    )
    http.add_option(
        "--timeout",
        action="store",
        type="float",
        dest="timeout",
        metavar="SECONDS",
        help="Set request timeout (default: 10.0s)"
    )
    http.add_option(
        "--proxy",
        action="store",
        dest="proxy",
        metavar="PROXY",
        help="Use a proxy (e.g., http://127.0.0.1:8080)"
    )
    http.add_option(
        "--user-agent",
        action="store",
        dest="user_agent",
        metavar="USER_AGENT",
        help="Set a custom User-Agent string"
    )

    parser.add_option_group(mandatory)
    parser.add_option_group(general)
    parser.add_option_group(advanced)
    parser.add_option_group(http)

    option, _ = parser.parse_args()
    return option
