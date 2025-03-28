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

import platform
import sys
from core.setting import VERSION
from views.banner import BANNER

def print_banner(
    author: str = 'waibui',
    version: str = VERSION,
    document: str = "https://github.com/waibui/psdir",
    license: str = "LICECSE",
    verbose: bool = True
):
    """
    Prints an ASCII banner with optional information about the project.

    Args:
        author (str, optional): The name of the author. Defaults to 'waibui'.
        version (str, optional): The version of the tool. Defaults to '1.0.0'.
        document (str, optional): The documentation URL. Defaults to "https://github.com/waibui/psdir".
        license (str, optional): The software license type. Defaults to "LICECSE".
        project_name (str, optional): The name of the project. Defaults to "psdir".
        verbose (bool, optional): If True, displays additional details. If False, only the ASCII banner is shown.

    Returns:
        None: This function only prints the banner.
    """
    
    system_info = platform.system() + " " + platform.release()  
    python_version = sys.version.split()[0]  

    if verbose:
        print(BANNER % (
            f"Author    : {author}",
            f"Version   : {version}",
            f"License   : {license}",
            f"Doccument : {document}",
            f"OS        : {system_info}",
            f"Python    : {python_version}"
        ))
    else:
        print(BANNER % ('', '', '', '', '', ''))
