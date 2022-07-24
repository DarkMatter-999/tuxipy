from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.4'
DESCRIPTION = 'A CLI tool to scrapes Google search'
LONG_DESCRIPTION = 'A CLI tool that scrapes Google search results and SERPs that provides instant and concise answers'

# Setting up
setup(
    name="tuxipy",
    version=VERSION,
    author="DarkMatter-999",
    author_email="<darkmatter999official@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['bs4'],
    keywords=['python', 'google', 'google assistant', 'search results', 'assistant', 'web', 'web scraping', 'result scraping', 'iot', 'amazon', 'amazon alexa', 'google home'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)