#!/usr/bin/python
"""
python setup
"""

import sys
import setuptools


if sys.version_info < (3, 6):
	sys.exit("Python 3.7 or newer is required for logni.py")


def readme():
	""" readme """

	return open('README.md', 'r', encoding='utf-8').read()


def version():
	""" version """

	return open('version.properties', 'r', encoding='utf-8').read()


setuptools.setup(name='logni',\
  version='0.2.2',\
  author='Erik Brozek',\
  author_email='erik@brozek.name',\
  description='python library for event logging and application states',\
  long_description=readme(),\
  long_description_content_type='text/markdown',\
  url='https://github.com/erikni/logni.py',\
  download_url='https://github.com/erik/logni.py/archive/master.zip',\
  packages=['logni'],\
  classifiers=['Development Status :: 4 - Beta',\
    'Programming Language :: Python :: 3',\
    'Programming Language :: Python :: 3.7',\
    'Programming Language :: Python :: 3.8',\
    'Programming Language :: Python :: 3.9',\
    'Programming Language :: Python :: 3.10',\
    'Programming Language :: Python :: 3.11',\
    'License :: OSI Approved :: MIT License',\
    'Topic :: System :: Logging'],\
  python_requires='>=3.7',\
  keywords=['logging', 'logging-library', 'logger'],\
  license='MIT')
