#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

import time

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ScanResult:
    """Represents the result of a path scan."""
    url: str
    path: str
    status: int
    content_length: int
    response_time: float
    content_type: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    
    def __hash__(self):
        """Make ScanResult hashable for use in sets."""
        return hash((self.url, self.path, self.status))
    
    def __eq__(self, other):
        """Define equality for ScanResult objects."""
        if not isinstance(other, ScanResult):
            return False
        return (self.url == other.url and 
                self.path == other.path and 
                self.status == other.status)