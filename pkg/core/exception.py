#!/usr/bin/env python

"""
Copyright (c) 2025 WaiBui
See the file 'LICENSE' for copying permission
"""

class CannotConnect(Exception):
    pass

class FailedDependenciesInstallation(Exception):
    pass

class InvalidURLException(Exception):
    pass

class RequestException(Exception):
    pass

class FileExistsException(Exception):
    pass

class MethodNotFound(Exception):
    pass