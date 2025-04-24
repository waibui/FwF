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
    
    from src.output.logger import Logger    
    from src.models.config import ScanConfig
    from src.scanner.scanner import FwFScanner
    from src.input.cli_parser import parse_arguments
    from src.output.banner import display_banner
except ImportError as e:
    print("Error importing", str(e))

logger = Logger.get_instance()

async def main():
    display_banner()
    
    args = parse_arguments()
    
    logger.set_color_enabled(args.color).set_verbose_enabled(args.verbose)
    
    config = ScanConfig(
        url=args.url,
        method=args.method,
        timeout=args.timeout,
        follow_redirects=args.follow_redirects,
        proxy=args.proxy,
        cookie=args.cookie,
        user_agent=args.user_agent,
        headers={},
        wordlist=args.wordlist,
        crawl=args.crawl,
        crawl_depth=args.crawl_depth,
        concurrency=args.concurrency,
        retry=args.retry,
        match_codes=args.match_codes,
        color=args.color,
        output=args.output,
        verbose=args.verbose,
    )
    
    scanner = FwFScanner(config)
    await scanner.scan()
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.debug("User interupted")
        exit(0)
    except Exception as e:
        logger.error(str(e))