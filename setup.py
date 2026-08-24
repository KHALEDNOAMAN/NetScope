from setuptools import setup, find_packages

setup(
    name="netscope",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "scapy==2.5.0",
        "fastapi==0.109.0",
        "uvicorn==0.27.0",
        "psutil==5.9.7",
        "rich==13.7.0",
        "click==8.1.7"
    ],
    entry_points={
        "console_scripts": [
            "netscope=src.cli:cli",
        ],
    },
)
