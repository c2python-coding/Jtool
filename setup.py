#!/usr/bin/env python 3
from distutils.core import setup
import setuptools

setup(
    name='Jtool',
    version='0.1.0',
    author='c2python-coding',
    author_email='c2python.coding@protonmail.com',
    packages=setuptools.find_packages(),
    url='https://github.com/c2python-coding/Jtool',
    description='Tool for working with json data',
    long_description=open('README.md').read(),
    scripts=["bin/jtool"]
)
