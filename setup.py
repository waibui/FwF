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

from setuptools import setup, find_packages
    
setup(
    name="psdir",
    version="1.0.0",
    description="A web directory scanner",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",

    author="waibui",
    author_email="buivanyk4@gmail.com",
    url="https://github.com/waibui/psdir",

    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires=">=3.9",

    packages=find_packages(),

    install_requires=[
        "requests",
    ],

    entry_points={
        "console_scripts": [
            "webscanner=psdir:run"
        ]
    },
)
