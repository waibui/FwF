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

from optparse import OptionParser, OptionGroup, Values
from core.setting import VERSION

def parse_args() -> Values:
    """Parses command-line arguments and returns the parsed values.

    Returns:
        Values: An object containing the parsed command-line arguments.
    """
    usage = "Usage: %prog [-u|--url] target [options]"
    epilog = "See 'config.ini' for the example configuration file"
    parser = OptionParser(usage=usage, epilog=epilog, version=f"dirsearch v{VERSION}")
    
    # Core Settings
    core = OptionGroup(parser, "CORE SETTINGS")
    core.add_option(
        "-u", "--url",
        action="append",
        dest="urls",
        metavar="URL",
        help="Target URL(s)",
    )
    core.add_option(
        "-w", "--wordlists",
        action="store",
        dest="wordlists",
        help="Wordlist files or directories contain wordlists (comma-separated)",
    )
    core.add_option(
        "-e", "--extensions",
        action="store",
        dest="extensions",
        help="Extension list, separated by commas (e.g., php, asp)",
    )
    core.add_option(
        "--remove-extensions",
        action="store_true",
        dest="remove_extensions",
        help="Remove extensions in all paths (e.g., admin.php -> admin)",
    )
    
    # Performance & Request Settings
    request = OptionGroup(parser, "PERFORMENT & REQUEST SETTINGS")
    request.add_option(
        "-t", "--threads",
        action="store",
        type="int",
        dest="thread_count",
        metavar="THREADS",
        default=40,
        help="Number of threads (default: 40)",
    )
    request.add_option(
        "--timeout",
        action="store",
        type="float",
        dest="timeout",
        help="Connection timeout in seconds",
    )
    request.add_option(
        "-m", "--http-method",
        action="store",
        dest="http_method",
        metavar="METHOD",
        help="HTTP method (default: GET)",
    )
    request.add_option(
        "-p", "--protocol",
        action="store",
        dest="protocol",
        metavar="PROTOCOL",
        help="Protocol (default: HTTPS)",
    )
    request.add_option(
        "--mc", "--match-code",
        action="store",
        dest="match_code",
        metavar="MATCH_CODE",
        help="Match HTTP status code (default: not 404)",
    )
    
    # Output & Logging Settings
    output = OptionGroup(parser, "OUTPUT & LOGGING SETTINGS")
    output.add_option(
        "-o", "--output",
        action="store",
        dest="output_file",
        metavar="FILE",
        help="Save output to a file",
    )
    output.add_option(
        "--quiet",
        action="store_true",
        dest="quiet",
        help="Suppress all non-essential output",
    )

    parser.add_option_group(core)
    parser.add_option_group(request)
    parser.add_option_group(output)

    options, _ = parser.parse_args()

    return options
