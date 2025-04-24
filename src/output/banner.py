#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

def get_banner():
    """Return ASCII art banner for the tool."""
    return r"""
     _____          _____ 
    |  ___|_      _|  ___|
    | |_  \ \ /\ / / |_   
    |  _|  \ V  V /|  _|  
    |_|     \_/\_/ |_|                                                                    
                            v1.0.0 by WaiBui                                                  
    """

def display_banner():
    """Print the tool banner."""
    print(get_banner())
    print("-"*60)