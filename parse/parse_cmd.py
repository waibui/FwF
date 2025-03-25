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
from core.setting import VERSION, USAGE, WORDLIST_PATH, USER_AGENT_PATH, DEFAULT_METHOD
from views.logging import Logging
from views.banner import print_banner

def parse_args() -> Values:
    """Parses command-line arguments and returns the parsed values.

    Returns:
        Values: An object containing the parsed command-line arguments.
    """
    print_banner(verbose=True)
    epilog = "See 'core/setting.py' for the example configuration file"
    parser = OptionParser(usage=USAGE, epilog=epilog, version=f"psdir v{VERSION}")
    
    # Core Settings
    core = OptionGroup(parser, "CORE SETTINGS")
    core.add_option(
        "-u", "--url",
        action="store",
        dest="url",
        metavar="URL",
        help="Target URL example: https://example.com",
    )
    core.add_option(
        "-w", "--wordlists",
        action="store",
        dest="wordlists",
        default=WORDLIST_PATH,
        help="Wordlist files or directories contain wordlists (comma-separated)",
    )
    core.add_option(
        "--ua", "--user-agent",
        action="store",
        dest="user_agent",
        default=USER_AGENT_PATH,
        help="User-Agent files or directories contain useragent (comma-separated)",
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
        "--to", "--timeout",
        action="store",
        type="float",
        dest="timeout",
        default=10,
        help="Connection timeout in seconds",
    )
    request.add_option(
        "-m", "--http-method",
        action="store",
        dest="http_method",
        metavar="METHOD",
        default="GET",
        help="HTTP method (default: GET)",
    )
    request.add_option(
        "--mc", "--match-code",
        action="store",
        dest="match_code",
        metavar="MATCH_CODE",
        default="200,204,301,302,307,401,403",
        help=f"Match HTTP status code (default: 200,204,301,302,307,401,403)",
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
    
    if not options.url:
        parser.print_usage()
        
    if options.http_method not in DEFAULT_METHOD:
        Logging.error(f"Invalid method {options.http_method}, please use one of the following methods: {DEFAULT_METHOD}")
        exit(1)
        
    return options
