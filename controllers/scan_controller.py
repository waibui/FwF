# -*- coding: utf-8 -*-
#  psdir - Web Path Scanner
#  Copyright (C) 2025 waibui
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  Author: waibui

import requests
from views.logging import Logging

def scan_path(url:str, method:str, user_agent:str, timeout:float, match_code:str):
    headers = {"User-Agent": user_agent}
    try:
        request_func = getattr(requests, method.lower(), requests.get)
        response = request_func(url, headers=headers, timeout=timeout)

        if str(response.status_code) in match_code:
            Logging.result(response.status_code, url)

    except KeyboardInterrupt:
        print("\nUser Interrupted")
    except requests.RequestException:
        pass  

