#!/usr/bin/env python3
"""
FwF - Fast Web Fuzzer: A web path discovery tool

Author: WaiBui
License: MIT
"""

# ===== URL & HTTP VALIDATORS =====
URL_PATTERN = r"^(https?://)?((localhost)|(\d{1,3}(\.\d{1,3}){3})|([a-zA-Z0-9.-]+\.[a-zA-Z]{2,}))(:(\d{1,5}))?(/.*)?$"
HTTP_METHOD_PATTERN = r"^(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)$"

# ===== COOKIE, PARAMS, PROXY =====
COOKIE_PATTERN = r"^([\w-]+=[^;]+)(;[\w-]+=[^;]+)*$"
PARAMS_PATTERN = r"^([\w-]+=[\w.-]+)(&[\w-]+=[\w.-]+)*$"
PROXY_PATTERN = r"^(https?://)(?:(\S+):(\S+)@)?((?:[\w.-]+)|(?:\d{1,3}(?:\.\d{1,3}){3})):(\d{2,5})$"
