#!/usr/bin/python
"""
python setup
"""

import sys
import setuptools


if sys.version_info < (2, 7):
	sys.exit("Python 2.7 or newer is required for logni.py")


def readme():
	""" readme """

	return open('README.md', 'r').read()


def version():
	""" version """

	return open('version.properties', 'r').read()


setuptools.setup(name='logni',\
  version='0.1.1',\
  author='Erik Brozek',\
  author_email='erik@brozek.name',\
  description='python library for event logging and application states',\
  long_description=readme(),\
  long_description_content_type='text/markdown',\
  url='https://github.com/erikni/logni.py',\
  download_url='https://github.com/erik/logni.py/archive/master.zip',\
  packages=['logni'],\
  classifiers=['Development Status :: 4 - Beta',\
    'Programming Language :: Python :: 2',\
    'Programming Language :: Python :: 2.7',\
    'Programming Language :: Python :: 3',\
    'Programming Language :: Python :: 3.5',\
    'Programming Language :: Python :: 3.6',\
    'Programming Language :: Python :: 3.7',\
    'Programming Language :: Python :: 3.8',\
    'License :: OSI Approved :: MIT License',\
    'Topic :: System :: Logging'],\
  python_requires='>=2.7',\
  keywords=['logging', 'logging-library', 'logger'],
  license='MIT')
