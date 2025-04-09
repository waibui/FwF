# -*- coding: utf-8 -*-
#  psdir - Web Path Scanner
#  Copyright (c) 2025 waibui
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import platform
import sys
from core.config import Setting

def print_banner(
    author: str = 'waibui',
    version: str = Setting.VERSION,
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
        print(Setting.BANNER % (
            f"Author    : {author}",
            f"Version   : {version}",
            f"License   : {license}",
            f"Doccument : {document}",
            f"OS        : {system_info}",
            f"Python    : {python_version}"
        ))
    else:
        print(Setting.BANNER % ('', '', '', '', '', ''))
