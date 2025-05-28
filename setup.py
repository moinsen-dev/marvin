#!/usr/bin/env python
"""Setup script for backward compatibility.

This file is not needed for modern Python packaging, but some tools
still expect it to exist. The actual package configuration is in pyproject.toml.
"""

from setuptools import setup

if __name__ == "__main__":
    setup()