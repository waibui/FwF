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

def print_config(args, wordlist):
    """Prints the scanning configuration based on the provided arguments and wordlist.

    Args:
        args (argparse.Namespace): The object containing configuration parameters.
        wordlist (list): A list of keywords to be scanned.

    Output:
        Prints the scanning configuration details to the console.
    """
    print(Setting.SEPARATOR)
    print(f"- Target URL: {args.url}")
    print(f"- Threads: {args.concurrency}")
    print(f"- Timeout: {args.timeout} seconds")
    print(f"- Allow Redirects: {'Yes' if args.allow_redirect else 'No'}")
    print(f"- Cookie: {args.cookie if args.cookie else 'None'}")
    print(f"- Proxy: {args.proxies if args.proxies else 'None'}")
    print(f"- Wordlist: {args.wordlist} ({len(wordlist)} entries)")
    print(f"- Target Status Codes: {args.match_code}")
    print(Setting.SEPARATOR)
