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
from models.option import Option

def scan_path(path, option: Option, user_agent:str):
    url = f"{option.url}/{path}"
    headers = {"User-Agent": user_agent}
    try:
        request_func = getattr(requests, option.http_method.lower(), requests.get)
        response = request_func(
            url=url, 
            headers=headers, 
            timeout=option.timeout
        )

        if str(response.status_code) in option.match_code:
            Logging.result(response.status_code, url)

    except KeyboardInterrupt:
        print("\nUser Interrupted")
    except requests.RequestException:
        pass  

