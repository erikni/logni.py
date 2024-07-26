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

	with open('README.md', 'r', encoding='utf-8') as file:
		data = file.read()

	return data


def version():
	""" version """

	ver = None
	with open('setup.cfg', 'r', encoding='utf-8') as file:
		data = file.read().split('\n')

	for line in data:
		if not line:
			continue
		lines = line.split('=')
		if len(lines) != 2:
			continue
		name = lines[0].strip()
		val = lines[1].strip()
		if name == 'version':
			ver = val.strip()

	if not ver:
		raise ValueError('version must be input')

	vers = ver.split('.')
	if len(vers) != 3:
		raise ValueError(f'version must be semver.org format, not version={version}')

	return ver

# setuptools
setuptools.setup(name='logni',\
  version=version(),\
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
