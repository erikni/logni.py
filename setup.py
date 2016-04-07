from distutils.core import setup
import sys

if sys.version_info <= (2, 7):
    sys.exit("Python 2.7 or newer is required for logni.py")

def readme():
    with open('README.md') as f:
        return f.read()

setup(
  name = 'python-logni',
  packages = ['python-logni'], # this must be the same as the name above
  version = '0.0.18',
  description = 'Full-stack error tracking for all apps in python',
  long_description=readme(),
  author = 'Erik Brozek',
  author_email = 'hellocode@logni.net',
  url = 'https://github.com/Logni/logni.py', # use the URL to the github repo
  download_url = 'https://github.com/Logni/logni.py/archive/master.zip', # I'll explain this in a second
  keywords = ['logging', 'testing' ], # arbitrary keywords
  license='MIT',
  classifiers = [
    	# How mature is this project? Common values are
    	#   3 - Alpha
    	#   4 - Beta
    	#   5 - Production/Stable
    	'Development Status :: 4 - Beta',

	# MIT license
	'License :: OSI Approved :: MIT License',

	# List trove classifiers
	'Topic :: System :: Logging',
	
	# Specify the Python versions you support here. In particular, ensure
    	# that you indicate whether you support Python 2, Python 3 or both.
 	'Programming Language :: Python :: 2',
    	'Programming Language :: Python :: 2.6',
    	'Programming Language :: Python :: 2.7'
  ],
)
