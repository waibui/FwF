#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

class Logger:
    """
    Singleton logger class for structured logging with optional color support.
    
    Supports logging messages with different severity levels (INFO, WARNING, ERROR, SUCCESS, DEBUG).
    Includes HTTP status logging with colorized output based on the status code.
    
    Methods:
        info(), warn(), error(), success(), debug() - Log messages with different severity.
        http() - Log HTTP status codes with color.
        status() - Log standard HTTP statuses with optional override message.
    """

    _instance = None

    _COLORS = {
        'reset': '\033[0m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'gray': '\033[90m',
        'bright_red': '\033[91;1m',
        'bright_green': '\033[92;1m',
        'bright_yellow': '\033[93;1m',
        'bright_blue': '\033[94;1m',
        'bright_magenta': '\033[95;1m',
        'bright_cyan': '\033[96;1m',
        'orange': '\033[38;5;208m',
        'purple': '\033[38;5;135m',
        'teal': '\033[38;5;6m'
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {
                'enable_color': False,
                'enable_verbose': True
            }
        return cls._instance

    @classmethod
    def get_instance(cls):
        """
        Returns the singleton instance of the logger.
        """
        return cls()

    def set_color_enabled(self, enabled: bool):
        """
        Enable or disable colored output for logs.
        """
        self._config['enable_color'] = enabled
        return self

    def set_verbose_enabled(self, enabled: bool):
        """
        Enable or disable verbose logging mode. In verbose mode, debug logs are shown.
        """
        self._config['enable_verbose'] = enabled
        return self

    def _colorize(self, text: str, color: str) -> str:
        """
        Apply ANSI color to a text if enabled.
        """
        if not self._config['enable_color']:
            return text
        return f"{self._COLORS.get(color, '')}{text}{self._COLORS['reset']}"

    def _format_extra_args(self, args: tuple, color: str = 'white') -> str:
        """
        Format and optionally color extra log arguments.
        """
        if not args:
            return ""
        if self._config['enable_verbose']:
            return ": " + " ".join(self._colorize(str(arg), color) for arg in args)
        return self._colorize(f" (+{len(args)} args)", "gray")

    def _log(self, label: str, message: str, color: str, *args):
        """
        Internal logging handler (label is colored, message is not).
        """
        label_colored = self._colorize(label, color)
        msg = str(message) if message else "" 
        extra = self._format_extra_args(args, color)
        print(f"{label_colored} {msg}{extra}".strip())

    def info(self, message: str, *args):
        """Log informational messages."""
        self._log("::", message, "bright_blue", *args)

    def warn(self, message: str, *args):
        """Log warning messages."""
        self._log("[WARNING]", message, "bright_yellow", *args)

    def error(self, message: str, *args):
        """Log error messages."""
        self._log("[ERROR]", message, "bright_red", *args)

    def success(self, message: str, *args):
        """Log success messages."""
        self._log("[SUCCESS]", message, "bright_green", *args)

    def debug(self, message: str, *args):
        """Log debug messages (shown only in verbose mode)."""
        if self._config['enable_verbose']:
            self._log("[DEBUG]", message, "bright_magenta", *args)

    def http(self, status_code: int, message: str = None, *args):
        """
        Log HTTP status codes with colored [status_code] only.
        """
        category_colors = {
            1: "bright_blue",
            2: "bright_green",
            3: "bright_cyan",
            4: "bright_yellow",
            5: "bright_red",
        }
        color = category_colors.get(status_code // 100, "gray")
        label = self._colorize(f"[{status_code}]", color)
        msg = str(message) if message else "" 
        extra = self._format_extra_args(args, color)
        print(f"{label} {msg}{extra}".strip())

    def status(self, status_code: int, message: str = None, *args):
        """
        Log standard HTTP status with optional override message.
        """
        default_messages = {
            100: "Continue", 101: "Switching Protocols", 102: "Processing", 103: "Early Hints",
            200: "OK", 201: "Created", 202: "Accepted", 204: "No Content", 206: "Partial Content",
            300: "Multiple Choices", 301: "Moved Permanently", 302: "Found", 303: "See Other",
            304: "Not Modified", 307: "Temporary Redirect", 308: "Permanent Redirect",
            400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found",
            405: "Method Not Allowed", 406: "Not Acceptable", 408: "Request Timeout",
            409: "Conflict", 418: "I'm a teapot", 429: "Too Many Requests",
            500: "Internal Server Error", 501: "Not Implemented", 502: "Bad Gateway",
            503: "Service Unavailable", 504: "Gateway Timeout"
        }
        resolved_msg = message if message is not None else default_messages.get(status_code)
        self.http(status_code, resolved_msg, *args)
    