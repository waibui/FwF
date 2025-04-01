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

import random

def random_user_agent(user_agent):
    """
    Returns a random User-Agent string based on the input type.
    
    Args:
        user_agent (list | UserAgent): The User-Agent input, which can be a string, a list of strings, or a UserAgent object.
    
    Returns:
        str: A valid User-Agent string.
    """
    if isinstance(user_agent, list):
        return random.choice(user_agent)
    elif hasattr(user_agent, "random"):
        return user_agent.random