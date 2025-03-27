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
from models.option import Option

def scan(session: requests.Session, path: str, option: Option, user_agent: str, cookie: dict = None, proxy: dict = None):
    """
    Sends an HTTP request to a specific path on the server and checks the response.

    This function utilizes `requests.Session()` to optimize scanning speed by reusing TCP connections, 
    reducing latency, and saving system resources.

    Args:
        session (requests.Session): The session object to send HTTP requests, enabling connection reuse.
        path (str): The path to scan (e.g., "/admin").
        option (Option): The configuration options (URL, HTTP method, timeout, etc.).
        user_agent (str): The User-Agent string to include in the request headers.
        cookie (dict, optional): Cookies to include in the HTTP request. Defaults to None.
        proxy (dict, optional): Proxy settings for the request. Defaults to None.
    Returns:
        dict: A dictionary containing the status code and URL if a valid response is found.
    """
    url = f"{option.url.rstrip('/')}/{path.lstrip('/')}"
    headers = {
        "User-Agent": user_agent,
    }
    kwargs = {
        "headers": headers, 
        "timeout": option.timeout,
        "allow_redirects": option.allow_redirect,
    }
    if cookie:
        kwargs["cookies"] = cookie  
    if proxy:
        kwargs["proxies"] = proxy  

    try:
        request_func = getattr(session, option.http_method.lower(), session.get)
        response = request_func(url=url, **kwargs)
        if str(response.status_code) in option.match_code:
            return {"status": response.status_code, "url": url}
    except requests.RequestException:
        return None

