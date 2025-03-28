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

import sys
import subprocess
import pkg_resources

from core.config import Config

def get_dependencies() -> list[str]:
    """
    Reads and returns the list of dependencies from the requirements.txt file.

    Returns:
        list[str]: A list of package names specified in the requirements file.
    
    Raises:
        SystemExit: If the requirements.txt file is not found.
    """
    try:
        with open(Config.REQUIREMENTS, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print("Can't find requirements.txt")
        sys.exit(1)

def check_dependencies() -> list[str]:
    """
    Checks if all dependencies are installed and returns a list of missing packages.

    Returns:
        list[str]: A list of missing package names that need to be installed.
    """
    dependencies = get_dependencies()
    missing_packages = []
    
    for package in dependencies:
        try:
            pkg_resources.require(package)
        except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
            missing_packages.append(package)
            
    return missing_packages

def install_dependencies() -> None:
    """
    Installs missing dependencies listed in the requirements file.
    
    If all dependencies are already installed, this function does nothing.
    """
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_output(
                [sys.executable, "-m", "pip", "install", *missing_packages],
                stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError:
            print("Failed to install dependencies.")
            sys.exit(1)
