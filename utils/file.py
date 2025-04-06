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
