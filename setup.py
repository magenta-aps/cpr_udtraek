import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="cpr_udtraek",
    version=read("VERSION").strip(),
    author="Heini Leander Ovason",
    author_email="heini@magenta-aps.dk",
    description=("get and parse files from the danish cpr registry"),
    license="MPL",
    keywords="cpr",
    url="",
    packages=['cpr_udtraek'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MPL License",
    ],
    install_requires=[
        "requests",
        "paramiko",
        "pytz",
    ]
)
