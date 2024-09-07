import os
from setuptools import setup, find_packages

# Ensure __init__.py exists
init_path = os.path.join('port_monitor', '__init__.py')
if not os.path.exists(init_path):
    open(init_path, 'a').close()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="port_monitor",
    version="0.2.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A configurable port monitoring tool with various alert methods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/port_monitor",
    packages=find_packages(),
    install_requires=[
        "psutil>=5.8.0",
        "PyYAML>=5.4.1",
        "Pillow>=8.0.0",
        "pystray>=0.17.0",
    ],
    extras_require={
        "gui": ["pystray>=0.17.0", "Pillow>=8.0.0"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "port_monitor=port_monitor.port_monitor:main",
            "configure_port_monitor=port_monitor.configure_port_monitor:main",
        ],
    },
)
