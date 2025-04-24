#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

import aiofiles
from typing import Set, List

from src.output.logger import Logger
logger = Logger.get_instance()

async def load_wordlist(wordlist_path: str = 'data/common.txt') -> Set[str]:
    """Load a wordlist from file."""
    return await _load_lines_from_file(wordlist_path, "wordlist")

async def load_user_agent(user_agent_path: str = 'data/user_agent.txt') -> List[str]:
    """Load user-agent strings from file."""
    return await _load_lines_from_file(user_agent_path, "user-agent")

async def _load_lines_from_file(path: str, file_description: str = "file") -> Set[str]:
    """Read all lines from a file asynchronously and return as a set."""
    try:
        async with aiofiles.open(path, 'r') as f:
            lines = await f.read()
            if file_description == "wordlist":
                return set(lines.splitlines()) 
            else:
                return lines.splitlines()
    except Exception as e:
        logger.error(f"Error loading {file_description} from '{path}'", str(e))
        return set() if file_description == "wordlist" else []
