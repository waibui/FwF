#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

def load_wordlist(wordlist_path: str = 'data/common.txt') -> list[str]:
    """Load a Wordlist from file."""
    return _load_lines_from_file(wordlist_path)

def load_user_agents(user_agent_path: str = 'data/user_agent.txt') -> list[str]:
    """Load a User-Agent from file."""
    return _load_lines_from_file(user_agent_path)

def _load_lines_from_file(path: str):
    """Read all lines from a file asynchronously and return as a list."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.read()
            return lines.splitlines()
    except Exception as e:
        raise RuntimeError(f"Failed to load wordlist from file: {path}") from e