#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

from src.constants.color import RESET, RED, GREEN, YELLOW, MAGENTA, CYAN, BOLD

class Logger:
    """
    Provides methods for printing messages with different
    log levels: info, success, warning, error, debug, bold, plain, and http.
    """
    _instance = None

    def __init__(self, use_color: bool = False, verbose: bool = False):
        self.use_color = use_color
        self.verbose = verbose

    @classmethod
    def get_instance(cls, use_color: bool = False, verbose: bool = False):
        if cls._instance is None:
            cls._instance = cls(use_color=use_color, verbose=verbose)
        return cls._instance

    def set_verbose(self, verbose: bool):
        self.verbose = verbose
        return self

    def set_color(self, use_color: bool):
        self.use_color = use_color
        return self

    def _print(self, *args, color_code: str = "", always: bool = True):
        if not always and not self.verbose:
            return
        message = " ".join(str(arg) for arg in args)
        if self.use_color and color_code:
            print(f"{color_code}{message}{RESET}")
        else:
            print(message)

    def info(self, *args): self._print(*args, color_code=CYAN)
    def success(self, *args): self._print(*args, color_code=GREEN, always=False)
    def warning(self, *args): self._print(*args, color_code=YELLOW, always=False)
    def error(self, *args): self._print(*args, color_code=RED, always=False)
    def debug(self, *args): self._print(*args, color_code=MAGENTA, always=False)
    def bold(self, *args): self._print(*args, color_code=BOLD, always=False)
    def plain(self, *args): self._print(*args, always=False)

    def http(self, status_code: int, match_code: list[int],*args):
        color_map = {
            1: CYAN,
            2: GREEN,
            3: YELLOW,
            4: RED,
            5: MAGENTA
        }
        color_code = color_map.get(status_code // 100, "")
        message = f"[{status_code}] {' '.join(str(arg) for arg in args)}"
        if status_code in match_code or self.verbose:
            self._print(message, color_code=color_code)
