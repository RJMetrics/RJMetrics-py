import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

# Don't import rjmetrics module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'rjmetrics'))
from version import VERSION

install_requires = ['requests >= 0.8.8']

# Get simplejson if we don't already have json
if sys.version_info < (3, 0):
    try:
        from util import json
    except ImportError:
        install_requires.append('simplejson')

setup(
    name='rjmetrics',
    cmdclass={'build_py': build_py},
    version=VERSION,
    description='Python client for RJMetrics APIs',
    author='RJMetrics',
    author_email='support@rjmetrics.com',
    url='https://rjmetrics.com/',
    packages=['rjmetrics', 'rjmetrics.test'],
    package_data={'rjmetrics': ['../VERSION']},
    install_requires=install_requires,
    test_suite='rjmetrics.test.all',
    use_2to3=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])
