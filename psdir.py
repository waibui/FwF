#!/usr/bin/env python

"""
Copyright (c) 2025 WaiBui
See the file 'LICENSE' for copying permission
"""

try:
    import sys

    sys.dont_write_bytecode = True
except KeyboardInterrupt:
    pass

from pkg.parse.cmd import parse_arguments

def main():
    opts = parse_arguments()
    print(opts.thread_count)

if __name__ == "__main__":
    main()

