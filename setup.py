from setuptools import setup, find_packages

setup(
    name="psdir",  
    version="0.1", 
    packages=find_packages(), 
    install_requires=[
        "requests", 
        "beautifulsoup4"
    ],
    entry_points={
        "console_scripts": [
            "psdir=psdir.cli:main",  
        ]
    },
)
