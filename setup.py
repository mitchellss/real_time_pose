"""Builds the realtimepose python package"""
import os
from setuptools import setup, find_packages

NAME = "realtimepose"
DESCRIPTION = "A library for creating body-interactive guis using computer vision."
URL = ""
EMAIL = "stephen.mitchell2299@gmail.com"
AUTHOR = "Stephen Mitchell"
REQUIRES_PYTHON = ">=3.6.8"
VERSION = "0.0.1"

REQUIRED = [
    "mediapipe>=0.8.7.2",
    "numpy>=1.21.2",
    "opencv_python>=4.3.0.38",
    "typing_extensions>=4.3.0"
]

here = os.path.abspath(os.path.dirname(__file__))
about = {}
about["__version__"] = VERSION

setup(name=NAME, version=about["__version__"],
      description=DESCRIPTION, long_description=DESCRIPTION,
      author=AUTHOR, author_email=EMAIL, REQUIRES_PYTHON=REQUIRES_PYTHON,
      url=URL, packages=find_packages(
          exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
      install_requires=REQUIRED, include_package_data=True)
