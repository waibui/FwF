#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

from src import __version__
from src.output.logger import Logger

logger = Logger.get_instance()

def get_banner() -> str:
    """Return ASCII art banner for the tool."""
    return rf"""
     _____          _____ 
    |  ___|_      _|  ___|
    | |_  \ \ /\ / / |_   
    |  _|  \ V  V /|  _|  
    |_|     \_/\_/ |_|                                                                    
                            v{__version__} by WaiBui                                                  
    """

def print_banner():
    """Print the tool banner."""
    logger.info(get_banner())