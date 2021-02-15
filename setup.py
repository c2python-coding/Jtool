from distutils.core import setup

setup(
    name='Jtool',
    version='0.1.0',
    author='c2python-coding',
    author_email='c2python.coding@protonmail.com',
    packages=['jtool'],
    scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Useful towel-related stuff.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.1.1",
        "caldav == 0.1.4",
    ],
)