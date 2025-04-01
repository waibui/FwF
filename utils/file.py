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

def get_file_content(path: str):
    """
    Reads a text file and returns a list of non-empty lines.

    Args:
        path (str): The file path to read.

    Returns:
        list[str]: A list of lines from the file (stripped of whitespace and empty lines).

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If an error occurs while opening or reading the file.
    """
    try:
        with open(path, 'r', encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {path}") from e
    except IOError as e:
        raise IOError(f"Error reading file: {path}") from e
