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

from config.settings import Setting
from utils.logger import Logger
from model.exception import DependencyError, RequirementsFileNotFoundError

def install_dependencies():
    """
    Installs missing dependencies listed in the requirements file.

    This function first checks for any missing dependencies and then attempts 
    to install them using `pip`. If an installation fails, it raises an exception.

    Raises:
        DependencyError: If installation of any package fails.
    """
    missing_packages = check_dependencies()
    
    if missing_packages:
        Logger.info(f"Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_output(
                [sys.executable, "-m", "pip", "install", *missing_packages],
                stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as e:
            raise DependencyError(f"Failed to install dependencies: {e.output.decode()}") from e

def get_dependencies():
    """
    Reads and returns the list of dependencies from the requirements.txt file.

    Returns:
        list[str]: A list of required package names.

    Raises:
        RequirementsFileNotFoundError: If the requirements.txt file is not found.
        IOError: If there is an error reading the file.
    """
    try: 
        with open(Setting.REQUIREMENTS, 'r', encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError as e:    
        raise RequirementsFileNotFoundError(f"Requirements file not found: {Setting.REQUIREMENTS}") from e
    except IOError as e:
        raise IOError(f"Error reading the requirements file: {Setting.REQUIREMENTS}") from e

def check_dependencies():
    """
    Checks if all required dependencies are installed.

    This function reads the dependencies from the `requirements.txt` file and 
    verifies if they are installed. It returns a list of missing dependencies.

    Returns:
        list[str]: A list of missing package names.
    """
    dependencies = get_dependencies()
    missing_packages = []
    
    for package in dependencies:
        try:
            pkg_resources.require(package)
        except pkg_resources.DistributionNotFound:
            missing_packages.append(package)
        except pkg_resources.VersionConflict as e:
            Logger.warning(f"Version conflict detected for {package}: {e}")
            missing_packages.append(package)
            
    return missing_packages
