#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

import sys
sys.dont_write_bytecode = True

try:
    import asyncio
except ImportError as e:
    print(f"Error importing required packages: {str(e)}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)
    
try:
    from src.models.config import ScanConfig
    from src.output.logger import Logger
    from src.scanner.scanner import FwFScanner
    from src.input.cli_parser import parse_arguments
    from src.output.banner import print_banner
except ImportError as e:
    print(f"Error importing module: {str(e)}")
    sys.exit(1)

logger = Logger.get_instance()

def main():
    args = parse_arguments()
    
    logger.info(args)
    logger.set_color(args.color).set_verbose(args.verbose)
    
    config = ScanConfig(
        url=args.url,
        method=args.method,
        timeout=args.timeout,
        follow_redirects=args.follow_redirects,
        cookie=args.cookie,
        params=args.params,
        data=args.data,
        user_agent=args.user_agent,
        wordlist=args.wordlist,
        concurrency=args.concurrency,
        retry=args.retry,
        match_codes=args.match_codes,
        output=args.output,
        verbose=args.verbose,
    )
    
    print_banner()
    scanner = FwFScanner(config)
    asyncio.run(scanner.run())
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger = Logger.get_instance()
        logger.info("[KEYBOARD INTERRUPT] Scan terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"Unhandled exception: {str(e)}")
        sys.exit(1)