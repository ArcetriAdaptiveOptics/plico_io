#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='plico_io',
    version='0.1.0',
    description="PLICO controller client for IO device control",
    author="INAF Arcetri Adaptive Optics",
    author_email="",
    url="",
    packages=find_packages(),
    install_requires=[
        'plico',
        'numpy',
        'six',
        'appdirs',
    ],
    entry_points={
        'console_scripts': [
            'plico_io_client=plico_io.client.client:main',
        ],
    },
) 