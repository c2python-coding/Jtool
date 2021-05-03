#!/usr/bin/env python 3
from distutils.core import setup

setup(
    name='Jtool',
    version='0.1.0',
    author='c2python-coding',
    author_email='c2python.coding@protonmail.com',
    packages=['jtool'],
    url='https://github.com/c2python-coding/Jtool',
    description='Tool for working with json data',
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['jtool=jtool.main:run'],
    }
)
