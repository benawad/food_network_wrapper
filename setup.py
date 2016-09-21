from setuptools.command.test import test as TestCommand
from setuptools import setup

import os
import sys

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'food_network_wrapper',
    packages = ['food_network_wrapper'], 
    version = '0.4',
    description = 'Allows you to easily search and scrape recipes from http://foodnetwork.com',
    author = 'Ben Awad',
    author_email = 'benawad97@gmail.com',
    url = 'https://github.com/benawad/food_network_wrapper', 
    download_url = 'https://github.com/benawad/food_network_wrapper/tarball/0.4',
    keywords = ['cooking', 'recipes', 'recipe', 'python', 'harvest', 'foodnetwork', 'scrape', 'scraping'], 
    long_description=README,
    install_requires=[
        "beautifulsoup4",
        "lxml",
        "requests",
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
